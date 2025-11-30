# ==================================================
# 导入库
# ==================================================

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from qfluentwidgets import *

from app.tools.variable import *
from app.tools.path_utils import *
from app.tools.personalised import *
from app.tools.settings_default import *
from app.tools.settings_access import *
from app.tools.update_utils import *
from app.Language.obtain_language import *


# ==================================================
# 辅助类
# ==================================================
class Worker(QObject):
    """用于在后台线程中执行任务的辅助类"""

    finished = Signal()

    def __init__(self, task):
        super().__init__()
        self.task = task

    def run(self):
        """执行任务"""
        self.task()
        self.finished.emit()


# ==================================================
# 更新页面
# ==================================================
class update(QWidget):
    """创建更新页面"""

    def __init__(self, parent=None):
        """初始化更新页面"""
        super().__init__(parent)

        # 创建主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        self.main_layout.setAlignment(Qt.AlignTop)

        # 设置标题
        self.titleLabel = BodyLabel(
            get_content_name_async("update", "secrandom_update_text")
        )
        self.titleLabel.setFont(QFont(load_custom_font(), 20))

        # 创建顶部信息区域
        self.setup_header_info()
        # 创建下载布局
        self.setup_download_layout()
        # 创建更新设置区域
        self.setup_update_settings()

        # 添加到主界面
        self.main_layout.addWidget(self.titleLabel)
        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addLayout(self.download_layout)
        self.main_layout.addWidget(self.update_settings_card)
        # 设置窗口布局
        self.setLayout(self.main_layout)

        # 初始化更新检查
        # self.check_for_updates()

    def setup_header_info(self):
        """设置头部信息区域"""
        # 创建水平布局用于放置状态信息
        self.header_layout = QHBoxLayout()
        self.header_layout.setSpacing(10)  # 减小间距
        self.header_layout.setAlignment(Qt.AlignLeft)

        # 创建状态信息布局（垂直布局）
        status_layout = QVBoxLayout()
        status_layout.setSpacing(5)
        status_layout.setAlignment(Qt.AlignLeft)
        status_layout.setContentsMargins(0, 0, 0, 0)  # 移除边距

        # 当前状态标签
        self.status_label = BodyLabel(
            get_content_name_async("update", "already_latest_version")
        )
        self.status_label.setFont(QFont(load_custom_font(), 16))

        # 版本信息标签
        self.version_label = BodyLabel(
            f"{get_content_name_async('update', 'current_version')}: {SPECIAL_VERSION} | {CODENAME} ({SYSTEM}-{ARCH})"
        )
        self.version_label.setFont(QFont(load_custom_font(), 12))

        # 上次检查更新时间标签
        self.last_check_label = BodyLabel()
        self.last_check_label.setFont(QFont(load_custom_font(), 10))
        # 加载上次检查时间
        self._load_last_check_time()

        # 创建水平布局，包含下载按钮、检查更新按钮和进度环
        button_ring_layout = QHBoxLayout()
        button_ring_layout.setSpacing(10)
        button_ring_layout.setAlignment(Qt.AlignLeft)

        # 下载并安装按钮（默认隐藏，仅在有新版本时显示）
        self.download_install_button = PrimaryPushButton(
            get_content_name_async("update", "download_and_install")
        )
        self.download_install_button.clicked.connect(self.download_and_install)
        self.download_install_button.setVisible(False)  # 默认隐藏

        # 检查更新按钮（带下拉菜单）
        self.check_update_button = DropDownPushButton(
            get_content_name_async("update", "check_for_updates")
        )

        # 创建RoundMenu菜单
        self.check_update_menu = RoundMenu(parent=self.check_update_button)

        # 添加普通检查更新菜单项
        check_update_action = Action(
            get_theme_icon("ic_fluent_arrow_repeat_all_20_filled"),
            get_content_name_async("update", "check_for_updates"),
            triggered=self.check_for_updates,
        )
        self.check_update_menu.addAction(check_update_action)

        # 添加强制检查更新菜单项
        force_check_action = Action(
            get_theme_icon("ic_fluent_arrow_repeat_all_20_filled"),
            get_content_name_async("update", "force_check"),
            triggered=self.force_check_for_updates,
        )
        self.check_update_menu.addAction(force_check_action)

        # 设置菜单
        self.check_update_button.setMenu(self.check_update_menu)

        # 添加不确定进度环（用于检查更新时显示）
        self.indeterminate_ring = IndeterminateProgressRing()
        self.indeterminate_ring.setFixedSize(24, 24)  # 减小进度环大小，适合按钮右侧
        self.indeterminate_ring.setStrokeWidth(3)  # 减小厚度
        self.indeterminate_ring.setVisible(False)  # 默认隐藏

        # 将按钮和进度环添加到水平布局（下载按钮在左侧，检查按钮在中间，进度环在右侧）
        button_ring_layout.addWidget(self.download_install_button)
        button_ring_layout.addWidget(self.check_update_button)
        button_ring_layout.addWidget(self.indeterminate_ring)
        button_ring_layout.addStretch()  # 右侧添加拉伸，确保按钮和进度环靠左

        # 添加控件到状态布局
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.version_label)
        status_layout.addWidget(self.last_check_label)
        status_layout.addLayout(button_ring_layout)

        # 添加状态布局、取消布局和拉伸到头部布局
        self.header_layout.addLayout(status_layout)
        self.header_layout.addStretch(1)  # 添加拉伸因子，将内容向左推

    def setup_download_layout(self):
        """设置下载布局"""
        # 创建下载信息布局（垂直布局，用于进度条和相关信息）
        self.download_layout = QVBoxLayout()
        self.download_layout.setSpacing(5)
        self.download_layout.setAlignment(Qt.AlignLeft)
        self.download_layout.setContentsMargins(0, 0, 0, 0)  # 移除边距

        # 创建下载进度条（单独一个布局，让它可以延伸到窗口最右端）
        self.download_progress = ProgressBar()
        self.download_progress.setRange(0, 100)
        self.download_progress.setValue(0)
        self.download_progress.setVisible(False)  # 默认隐藏

        # 创建下载信息标签（显示速度/总大小）
        self.download_info_label = BodyLabel("")
        self.download_info_label.setFont(QFont(load_custom_font(), 10))
        self.download_info_label.setVisible(False)  # 默认隐藏

        # 创建取消更新按钮
        self.cancel_update_button = PushButton(
            get_content_name_async("update", "cancel_update")
        )
        self.cancel_update_button.clicked.connect(self.cancel_update)
        self.cancel_update_button.setVisible(False)  # 默认隐藏

        # 取消按钮布局（与进度条对齐）
        cancel_layout = QHBoxLayout()
        cancel_layout.setSpacing(10)
        cancel_layout.setAlignment(Qt.AlignLeft)
        cancel_layout.addWidget(self.cancel_update_button)
        cancel_layout.addStretch()  # 右侧添加拉伸

        # 添加控件到下载布局
        self.download_layout.addWidget(self.download_progress)
        self.download_layout.addWidget(self.download_info_label)
        self.download_layout.addLayout(cancel_layout)

    def setup_update_settings(self):
        """设置更新设置区域"""
        self.update_settings_card = GroupHeaderCardWidget()
        self.update_settings_card.setTitle(get_content_name_async("update", "title"))
        self.update_settings_card.setBorderRadius(8)

        # 自动更新模式下拉框
        self.auto_update_combo = ComboBox()
        self.auto_update_combo.addItems(
            get_content_combo_name_async("update", "auto_update_mode")
        )
        self.auto_update_combo.setCurrentIndex(
            readme_settings_async("update", "auto_update_mode")
        )
        self.auto_update_combo.currentIndexChanged.connect(
            lambda: update_settings(
                "update", "auto_update_mode", self.auto_update_combo.currentIndex()
            )
        )

        # 更新通道选择
        self.update_channel_combo = ComboBox()
        self.update_channel_combo.addItems(
            get_content_combo_name_async("update", "update_channel")
        )
        update_channel = readme_settings("update", "update_channel")
        self.update_channel_combo.setCurrentIndex(update_channel)
        self.update_channel_combo.currentIndexChanged.connect(
            lambda: update_settings(
                "update", "update_channel", self.update_channel_combo.currentIndex()
            )
        )

        # 更新源选择
        self.update_source_combo = ComboBox()
        self.update_source_combo.addItems(
            get_content_combo_name_async("update", "update_source")
        )
        update_source = readme_settings("update", "update_source")
        self.update_source_combo.setCurrentIndex(update_source)
        self.update_source_combo.currentIndexChanged.connect(
            lambda: update_settings(
                "update", "update_source", self.update_source_combo.currentIndex()
            )
        )

        # 添加设置项到卡片
        self.update_settings_card.addGroup(
            get_theme_icon("ic_fluent_arrow_repeat_all_20_filled"),
            get_content_name_async("update", "auto_update_mode"),
            get_content_description_async("update", "auto_update_mode"),
            self.auto_update_combo,
        )

        self.update_settings_card.addGroup(
            get_theme_icon("ic_fluent_channel_20_filled"),
            get_content_name_async("update", "update_channel"),
            get_content_description_async("update", "update_channel"),
            self.update_channel_combo,
        )

        self.update_settings_card.addGroup(
            get_theme_icon("ic_fluent_cloud_arrow_down_20_filled"),
            get_content_name_async("update", "update_source"),
            get_content_description_async("update", "update_source"),
            self.update_source_combo,
        )

    def force_check_for_updates(self):
        """强制检查更新"""
        # 直接调用check_for_updates方法执行强制更新检查
        self.check_for_updates()
        logger.debug("用户进行了强制检查更新")

    def check_for_updates(self):
        """触发更新检查"""
        # 更新状态显示
        self.status_label.setText(get_content_name_async("update", "checking_update"))
        self.indeterminate_ring.setVisible(True)  # 显示不确定进度环
        self.check_update_button.setEnabled(False)

        # 使用异步方式检查更新
        def check_update_task():
            status_text = ""
            try:
                # 获取最新版本信息
                latest_version_info = get_latest_version()

                if latest_version_info:
                    latest_version = latest_version_info["version"]
                    latest_version_no = latest_version_info["version_no"]

                    # 比较版本号
                    compare_result = compare_versions(VERSION, latest_version)

                    if compare_result == 1:
                        # 有新版本
                        status_text = f"{get_content_name_async('update', 'new_version_available')}: {latest_version} | {CODENAME} ({SYSTEM}-{ARCH})"
                        # 显示下载并安装按钮
                        self.download_install_button.setVisible(True)
                    elif compare_result == 0:
                        # 当前是最新版本
                        status_text = get_content_name_async(
                            "update", "already_latest_version"
                        )
                        # 隐藏下载并安装按钮
                        self.download_install_button.setVisible(False)
                    else:
                        # 比较失败或版本号异常
                        status_text = get_content_name_async(
                            "update", "check_update_failed"
                        )
                        # 隐藏下载并安装按钮
                        self.download_install_button.setVisible(False)
                else:
                    # 获取版本信息失败
                    status_text = get_content_name_async(
                        "update", "check_update_failed"
                    )
                    # 隐藏下载并安装按钮
                    self.download_install_button.setVisible(False)
            except Exception as e:
                # 处理异常
                status_text = get_content_name_async("update", "check_update_failed")
                # 隐藏下载并安装按钮
                self.download_install_button.setVisible(False)
            finally:
                # 使用QMetaObject.invokeMethod确保UI更新在主线程执行
                QMetaObject.invokeMethod(
                    self,
                    "_update_check_status",
                    Qt.QueuedConnection,
                    Q_ARG(str, status_text),
                )

        # 创建并启动异步任务
        runnable = QRunnable.create(check_update_task)
        QThreadPool.globalInstance().start(runnable)

    def _load_last_check_time(self):
        """加载上次检查更新时间"""
        last_check_time = readme_settings("update", "last_check_time")
        self.last_check_label.setText(
            f"{get_content_name_async('update', 'last_check_time')}: {last_check_time}"
        )

    def _update_last_check_time(self):
        """更新上次检查更新时间为当前时间"""
        from datetime import datetime

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_settings("update", "last_check_time", current_time)
        self._load_last_check_time()

    def download_and_install(self):
        """下载并安装更新"""
        # 获取最新版本信息
        latest_version_info = get_latest_version()
        if not latest_version_info:
            self.status_label.setText(
                get_content_name_async("update", "failed_to_get_version_info")
            )
            return

        latest_version = latest_version_info["version"]
        latest_version_no = latest_version_info["version_no"]

        # 获取下载文件夹路径，与update_utils.py保持一致
        download_dir = get_resources_path("downloads")
        ensure_dir(download_dir)

        # 构建预期的文件名，使用与update_utils.py一致的格式
        expected_filename = DEFAULT_NAME_FORMAT
        expected_filename = expected_filename.replace("[version]", latest_version)
        expected_filename = expected_filename.replace("[system]", SYSTEM)
        expected_filename = expected_filename.replace("[arch]", ARCH)
        expected_filename = expected_filename.replace("[struct]", STRUCT)
        expected_file_path = download_dir / expected_filename

        # 检查文件是否存在且文件名一致（即版本号、系统、架构均匹配）
        file_exists_and_same_version = False
        if expected_file_path.exists():
            # 仅通过文件名判断是否为同一版本
            if expected_file_path.name == expected_filename:
                file_exists_and_same_version = True
                self.status_label.setText(
                    get_content_name_async("update", "already_downloaded_same_version")
                )
                # 直接调用下载完成处理，跳过实际下载
                self.on_download_complete(str(expected_file_path))
                return

        # 更新状态显示
        self.status_label.setText(
            get_content_name_async("update", "downloading_update")
        )
        self.download_progress.setVisible(True)
        self.download_info_label.setVisible(True)
        self.cancel_update_button.setVisible(True)
        self.download_install_button.setEnabled(False)
        self.check_update_button.setEnabled(False)

        # 下载状态变量
        self._download_cancelled = False
        self._start_time = QDateTime.currentDateTime().toMSecsSinceEpoch()
        self._last_speed_update = 0
        self._speed_update_interval = 300  # 每300ms更新一次速度

        # 定义进度回调函数
        def progress_callback(downloaded: int, total: int):
            if self._download_cancelled:
                return

            if total > 0:
                progress = int((downloaded / total) * 100)
                # 使用 QMetaObject.invokeMethod 确保在主线程中更新UI
                QMetaObject.invokeMethod(
                    self.download_progress,
                    "setValue",
                    Qt.QueuedConnection,
                    Q_ARG(int, progress),
                )

                # 格式化速度和总大小
                def format_size(size_bytes):
                    """格式化文件大小"""
                    if size_bytes < 1024:
                        return f"{size_bytes} B"
                    elif size_bytes < 1024 * 1024:
                        return f"{size_bytes / 1024:.1f} KB"
                    else:
                        return f"{size_bytes / (1024 * 1024):.1f} MB"

                current_time = QDateTime.currentDateTime().toMSecsSinceEpoch()
                total_str = format_size(total)
                downloaded_str = format_size(downloaded)

                # 每300ms更新一次速度
                if (
                    current_time - self._last_speed_update
                    >= self._speed_update_interval
                ):
                    elapsed = current_time - self._start_time
                    if elapsed > 0:
                        # 计算累计平均速度（字节/秒）
                        # 从开始下载到当前的总字节数除以总时间
                        speed = downloaded * 1000 / elapsed
                        speed_str = format_size(speed)
                    else:
                        speed_str = "0 B/s"

                    # 更新下载信息标签
                    info_text = f"{speed_str}/s | {downloaded_str} / {total_str}"
                    QMetaObject.invokeMethod(
                        self.download_info_label,
                        "setText",
                        Qt.QueuedConnection,
                        Q_ARG(str, info_text),
                    )

                    # 更新上次速度更新时间
                    self._last_speed_update = current_time

        # 定义下载完成后的处理函数
        def on_download_complete(file_path: Optional[str]):
            if self._download_cancelled:
                # 下载已取消
                QMetaObject.invokeMethod(
                    self.status_label,
                    "setText",
                    Qt.QueuedConnection,
                    Q_ARG(str, get_content_name_async("update", "update_cancelled")),
                )
            elif file_path:
                # 下载成功，询问用户是否现在更新
                QMetaObject.invokeMethod(
                    self,
                    "show_update_confirmation",
                    Qt.QueuedConnection,
                    Q_ARG(str, file_path),
                )
            else:
                # 下载失败
                QMetaObject.invokeMethod(
                    self.status_label,
                    "setText",
                    Qt.QueuedConnection,
                    Q_ARG(
                        str,
                        get_content_name_async("update", "failed_to_download_update"),
                    ),
                )

            # 恢复UI状态
            QMetaObject.invokeMethod(
                self.download_progress,
                "setVisible",
                Qt.QueuedConnection,
                Q_ARG(bool, False),
            )
            QMetaObject.invokeMethod(
                self.download_info_label,
                "setVisible",
                Qt.QueuedConnection,
                Q_ARG(bool, False),
            )
            QMetaObject.invokeMethod(
                self.cancel_update_button,
                "setVisible",
                Qt.QueuedConnection,
                Q_ARG(bool, False),
            )
            QMetaObject.invokeMethod(
                self.download_install_button,
                "setEnabled",
                Qt.QueuedConnection,
                Q_ARG(bool, True),
            )
            QMetaObject.invokeMethod(
                self.check_update_button,
                "setEnabled",
                Qt.QueuedConnection,
                Q_ARG(bool, True),
            )
            QMetaObject.invokeMethod(
                self.download_info_label, "setText", Qt.QueuedConnection, Q_ARG(str, "")
            )

        # 定义下载任务类
        class DownloadTask(QRunnable):
            def __init__(self, version, progress_callback, on_complete):
                super().__init__()
                self.version = version
                self.progress_callback = progress_callback
                self.on_complete = on_complete

            def run(self):
                """执行下载任务"""
                file_path = download_update(
                    self.version, progress_callback=self.progress_callback
                )
                self.on_complete(file_path)

        # 使用 QThreadPool 执行下载任务
        self._download_task = DownloadTask(
            latest_version, progress_callback, on_download_complete
        )
        QThreadPool.globalInstance().start(self._download_task)

    def show_update_confirmation(self, file_path: str):
        """显示更新确认对话框"""
        # 创建消息框
        msg_box = MessageBox(
            title=get_content_name_async("update", "update_confirmation_title"),
            content=get_content_name_async("update", "update_confirmation_content"),
            parent=self,
        )

        # 设置按钮文本
        msg_box.yesButton.setText(get_content_name_async("update", "yes_update_now"))
        msg_box.cancelButton.setText(
            get_content_name_async("update", "no_update_later")
        )

        # 显示消息框并等待用户响应
        result = msg_box.exec()

        if result == MessageBox.Yes:
            # 用户选择现在更新
            self.status_label.setText(
                get_content_name_async("update", "installing_update")
            )

            # 安装更新
            try:
                success = install_update(file_path)
                if success:
                    # 安装成功
                    self.status_label.setText(
                        get_content_name_async(
                            "update", "update_installed_successfully"
                        )
                    )
                else:
                    # 安装失败
                    self.status_label.setText(
                        get_content_name_async("update", "install_failed")
                    )
            except Exception as e:
                # 安装过程中发生错误
                error_text = (
                    f"{get_content_name_async('update', 'install_failed')}: {str(e)}"
                )
                self.status_label.setText(error_text)
        else:
            # 用户选择稍后更新
            self.status_label.setText(
                get_content_name_async("update", "update_cancelled_by_user")
            )

    def cancel_update(self):
        """取消更新"""
        self._download_cancelled = True
        QMetaObject.invokeMethod(
            self.status_label,
            "setText",
            Qt.QueuedConnection,
            Q_ARG(str, get_content_name_async("update", "cancelling_update")),
        )
        QMetaObject.invokeMethod(
            self.cancel_update_button,
            "setEnabled",
            Qt.QueuedConnection,
            Q_ARG(bool, False),
        )

    @Slot(str)
    def _update_check_status(self, status_text):
        """更新UI状态（主线程执行）"""
        self.status_label.setText(status_text)
        self.indeterminate_ring.setVisible(False)  # 隐藏不确定进度环
        self.check_update_button.setEnabled(True)
        # 更新上次检查时间
        self._update_last_check_time()
