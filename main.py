import os
import sys
import time
import gc
import subprocess

import sentry_sdk
from sentry_sdk.integrations.loguru import LoguruIntegration, LoggingLevels
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication
from loguru import logger

from app.tools.path_utils import get_app_root
from app.tools.config import configure_logging
from app.tools.settings_access import readme_settings_async
from app.tools.variable import APP_QUIT_ON_LAST_WINDOW_CLOSED, VERSION, EXIT_CODE_RESTART
from app.core.single_instance import (
    check_single_instance,
    setup_local_server,
    send_url_to_existing_instance,
)
from app.core.font_manager import configure_dpi_scale
from app.core.window_manager import WindowManager
from app.core.url_handler_setup import create_url_handler
from app.core.cs_ipc_handler_setup import create_cs_ipc_handler
from app.core.app_init import AppInitializer
from app.tools.update_utils import update_check_thread
import app.core.window_manager as wm


def main():
    """主程序入口"""
    program_dir = str(get_app_root())

    if os.getcwd() != program_dir:
        os.chdir(program_dir)
        logger.debug(f"工作目录已设置为: {program_dir}")

    logger.remove()
    configure_logging()

    # 仅在 非开发 环境（版本号不包含 0.0.0）下初始化 Sentry
    if "0.0.0" not in VERSION:

        def before_send(event, hint):
            # 如果事件中不包含异常信息（即没有堆栈），则不上传
            if "exception" not in event:
                return None
            return event

        sentry_sdk.init(
            dsn="https://f48074b49e319f7b952583c283046259@o4510289605296128.ingest.de.sentry.io/4510681366659152",
            integrations=[
                LoguruIntegration(
                    level=LoggingLevels.INFO.value,
                    event_level=LoggingLevels.ERROR.value,
                ),
            ],
            before_send=before_send,
            release=VERSION,
            send_default_pii=True,
            enable_logs=True,
            # 先1.0（100%上报）试试
            traces_sample_rate=1.0,
        )

    wm.app_start_time = time.perf_counter()

    shared_memory, is_first_instance = check_single_instance()

    # 防止原来的进程没完全结束
    time.sleep(1)

    if not is_first_instance:
        if len(sys.argv) > 1 and any(
            arg.startswith("secrandom://") for arg in sys.argv
        ):
            for arg in sys.argv[1:]:
                if arg.startswith("secrandom://"):
                    send_url_to_existing_instance(arg)
                    break

        logger.info("程序将退出，已有实例已激活")
        sys.exit(0)

    configure_dpi_scale()

    app = QApplication(sys.argv)

    gc.enable()

    try:
        resident = readme_settings_async("basic_settings", "background_resident")
        resident = True if resident is None else resident
        app.setQuitOnLastWindowClosed(not resident)
    except Exception:
        app.setQuitOnLastWindowClosed(APP_QUIT_ON_LAST_WINDOW_CLOSED)

    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

    window_manager = WindowManager()
    url_handler = create_url_handler()
    cs_ipc_handler = create_cs_ipc_handler()
    window_manager.set_url_handler(url_handler)

    local_server = setup_local_server(
        window_manager.get_main_window(), window_manager.get_float_window(), url_handler
    )

    if not local_server:
        logger.exception("无法启动本地服务器，程序将退出")
        shared_memory.detach()
        sys.exit(1)

    app_initializer = AppInitializer(window_manager)
    app_initializer.initialize()

    # 添加开发中提示（仅开发版本）
    if VERSION == "v0.0.0":
        from app.view.components.dev_hint_widget import DevHintWidget

        def add_dev_hint_to_window(window):
            """为窗口添加开发中提示"""
            if not window.isWindow() or hasattr(window, "_dev_hint_added"):
                return

            # 创建开发提示组件并添加到窗口
            dev_hint = DevHintWidget(window)
            dev_hint.setParent(window)
            dev_hint.show()

            # 标记窗口已添加开发提示
            window._dev_hint_added = True

            # 重写窗口的resizeEvent方法以更新提示位置
            original_resize_event = window.resizeEvent

            def new_resize_event(event, orig_event=original_resize_event, dh=dev_hint):
                # 调用原始resize事件
                if orig_event:
                    orig_event(event)

                # 更新开发提示的位置
                dh.update_position()

            window.resizeEvent = new_resize_event

            # 初始定位
            dev_hint.update_position()

        # 为现有窗口添加开发提示
        def add_dev_hints_to_existing_windows():
            for widget in QApplication.topLevelWidgets():
                add_dev_hint_to_window(widget)

        # 使用定时器确保在窗口完全创建后再添加提示
        QTimer.singleShot(100, add_dev_hints_to_existing_windows)

        # 监听新窗口的创建
        original_notify = app.notify

        def new_notify(receiver, event):
            result = original_notify(receiver, event)

            # 当新窗口显示时，添加开发提示
            if (
                hasattr(event, "type")
                and event.type() == event.Type.Show
                and hasattr(receiver, "isWindow")
                and receiver.isWindow()
                and not hasattr(receiver, "_dev_hint_added")
            ):
                add_dev_hint_to_window(receiver)

            return result

        app.notify = new_notify

    try:
        exit_code = app.exec()
        logger.debug("Qt 事件循环已结束")

        # 尝试停止所有后台服务
        if "cs_ipc_handler" in locals() and cs_ipc_handler:
            cs_ipc_handler.stop_ipc_client()

        if "url_handler" in locals() and url_handler:
            if hasattr(url_handler, "url_ipc_handler"):
                url_handler.url_ipc_handler.stop_ipc_server()

        shared_memory.detach()
        logger.debug("共享内存已释放")

        if local_server:
            local_server.close()
            logger.debug("本地服务器已关闭")

        if update_check_thread and update_check_thread.isRunning():
            logger.debug("正在等待更新检查线程完成...")
            update_check_thread.wait(2000)
            if update_check_thread.isRunning():
                logger.warning("更新检查线程超时，强行退出")
            else:
                logger.debug("更新检查线程已安全完成")

        gc.collect()
        logger.debug("垃圾回收已完成")

        logger.info("程序退出流程已完成，正在结束进程")
        if sys.stdout:
            sys.stdout.flush()
        if sys.stderr:
            sys.stderr.flush()

        if exit_code == EXIT_CODE_RESTART:
            logger.info("检测到重启信号，正在重启应用程序...")
            # 过滤掉 --url 等参数
            filtered_args = [arg for arg in sys.argv if not arg.startswith("--")]

            # 获取可执行文件路径
            if getattr(sys, "frozen", False):
                # 打包后的可执行文件
                executable = sys.executable
            else:
                # 开发环境
                executable = sys.executable

            if not os.path.exists(executable):
                logger.critical(f"重启失败：无法找到可执行文件: {executable}")
                os._exit(1)

            try:
                # 跨平台启动新进程
                if sys.platform.startswith("win"):
                    # Windows 特定参数
                    startup_info = subprocess.STARTUPINFO()
                    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    # 使用 CREATE_NO_WINDOW (0x08000000) 来防止创建新的控制台窗口
                    CREATE_NO_WINDOW = 0x08000000
                    subprocess.Popen(
                        [executable] + filtered_args,
                        cwd=program_dir,
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                        | CREATE_NO_WINDOW,
                        startupinfo=startup_info,
                    )
                else:
                    # Linux/macOS
                    subprocess.Popen(
                        [executable] + filtered_args,
                        cwd=program_dir,
                        start_new_session=True,
                    )
                logger.info("新的应用程序实例已启动")
            except Exception as e:
                logger.exception(f"重启应用程序失败: {e}")

        os._exit(0)
    except Exception as e:
        logger.exception(f"程序退出过程中发生异常: {e}")
        if "shared_memory" in locals():
            shared_memory.detach()
        if "local_server" in locals() and local_server:
            local_server.close()
        if sys.stdout:
            sys.stdout.flush()
        if sys.stderr:
            sys.stderr.flush()
        os._exit(1)


if __name__ == "__main__":
    main()
