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
        # 创建更新设置区域
        self.setup_update_settings()
        # 添加到主界面
        self.main_layout.addWidget(self.titleLabel)
        self.main_layout.addLayout(self.header_layout)
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

        # 创建状态信息容器
        status_container = QWidget()
        status_container.setMaximumWidth(400)  # 设置最大宽度

        # 创建状态信息布局
        status_layout = QVBoxLayout(status_container)
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
            f"{get_content_name_async('update', 'current_version')}: {VERSION}"
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

        # 检查更新按钮
        self.check_update_button = PushButton(
            get_content_name_async("update", "check_for_updates")
        )
        self.check_update_button.clicked.connect(self.check_for_updates)

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

        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.version_label)
        status_layout.addWidget(self.last_check_label)
        status_layout.addLayout(button_ring_layout)

        self.header_layout.addWidget(status_container)
        self.header_layout.addStretch(1)  # 添加拉伸因子，将内容向左推

    def setup_update_settings(self):
        """设置更新设置区域"""
        self.update_settings_card = GroupHeaderCardWidget()
        self.update_settings_card.setTitle(get_content_name_async("update", "title"))
        self.update_settings_card.setBorderRadius(8)

        # 自动下载更新开关
        self.auto_download_switch = SwitchButton()
        self.auto_download_switch.setOffText(
            get_content_switchbutton_name_async("update", "auto_download", "disable")
        )
        self.auto_download_switch.setOnText(
            get_content_switchbutton_name_async("update", "auto_download", "enable")
        )
        auto_download = readme_settings("update", "auto_download")
        self.auto_download_switch.setChecked(auto_download)
        self.auto_download_switch.checkedChanged.connect(
            lambda: update_settings(
                "update", "auto_download", self.auto_download_switch.isChecked()
            )
        )

        # 自动安装更新开关
        self.auto_update_switch = SwitchButton()
        self.auto_update_switch.setOffText(
            get_content_switchbutton_name_async("update", "auto_update", "disable")
        )
        self.auto_update_switch.setOnText(
            get_content_switchbutton_name_async("update", "auto_update", "enable")
        )
        auto_update = readme_settings("update", "auto_update")
        self.auto_update_switch.setChecked(auto_update)
        self.auto_update_switch.checkedChanged.connect(
            lambda: update_settings(
                "update", "auto_update", self.auto_update_switch.isChecked()
            )
        )

        # 更新通知开关
        self.need_notification_switch = SwitchButton()
        self.need_notification_switch.setOffText(
            get_content_switchbutton_name_async(
                "update", "need_notification", "disable"
            )
        )
        self.need_notification_switch.setOnText(
            get_content_switchbutton_name_async("update", "need_notification", "enable")
        )
        need_notification = readme_settings("update", "need_notification")
        self.need_notification_switch.setChecked(need_notification)
        self.need_notification_switch.checkedChanged.connect(
            lambda: update_settings(
                "update", "need_notification", self.need_notification_switch.isChecked()
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
            get_theme_icon("ic_fluent_database_arrow_down_20_filled"),
            get_content_name_async("update", "auto_download"),
            get_content_description_async("update", "auto_download"),
            self.auto_download_switch,
        )

        self.update_settings_card.addGroup(
            get_theme_icon("ic_fluent_arrow_repeat_all_20_filled"),
            get_content_name_async("update", "auto_update"),
            get_content_description_async("update", "auto_update"),
            self.auto_update_switch,
        )

        self.update_settings_card.addGroup(
            get_theme_icon("ic_fluent_comment_note_20_filled"),
            get_content_name_async("update", "need_notification"),
            get_content_description_async("update", "need_notification"),
            self.need_notification_switch,
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
                        status_text = f"{get_content_name_async('update', 'new_version_available')}: {latest_version}"
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
        # 这里可以添加下载和安装更新的逻辑
        # 暂时显示一个消息框，提示功能正在开发中
        from qfluentwidgets import MessageBox

        msg_box = MessageBox(
            get_content_name_async("update", "download_and_install"),
            get_content_name_async("update", "download_in_progress"),
            self,
        )
        msg_box.exec()

    @Slot(str)
    def _update_check_status(self, status_text):
        """更新UI状态（主线程执行）"""
        self.status_label.setText(status_text)
        self.indeterminate_ring.setVisible(False)  # 隐藏不确定进度环
        self.check_update_button.setEnabled(True)
        # 更新上次检查时间
        self._update_last_check_time()
