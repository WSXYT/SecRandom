import os
import sys
import time
import gc

import sentry_sdk
from sentry_sdk.integrations.loguru import LoguruIntegration, LoggingLevels
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from loguru import logger

from app.tools.path_utils import get_app_root
from app.tools.config import configure_logging
from app.tools.settings_access import readme_settings_async
from app.tools.variable import APP_QUIT_ON_LAST_WINDOW_CLOSED
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

    def before_send(event, hint):
        # 如果事件中不包含异常信息（即没有堆栈），则不上传
        if "exception" not in event:
            return None
        return event

    sentry_sdk.init(
        dsn="https://f079219d4004591e72e6e4e4155023fe@o4510689230192640.ingest.us.sentry.io/4510689241071616",
        integrations=[
            LoguruIntegration(
                level=LoggingLevels.INFO.value,
                event_level=LoggingLevels.ERROR.value,
            ),
        ],
        before_send=before_send,
        send_default_pii=True,
        enable_logs=True,
    )

    wm.app_start_time = time.perf_counter()

    shared_memory, is_first_instance = check_single_instance()

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

    try:
        app.exec()
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
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(0)
    except Exception as e:
        logger.exception(f"程序退出过程中发生异常: {e}")
        if "shared_memory" in locals():
            shared_memory.detach()
        if "local_server" in locals() and local_server:
            local_server.close()
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(1)


if __name__ == "__main__":
    main()
