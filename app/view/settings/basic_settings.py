# ==================================================
# 导入库
# ==================================================

from loguru import logger
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication
from PySide6.QtGui import QFontDatabase
from qfluentwidgets import (
    GroupHeaderCardWidget,
    SwitchButton,
    ComboBox,
    PushButton,
    ColorConfigItem,
    ColorSettingCard,
    Theme,
    setTheme,
    setThemeColor,
)

from app.tools.personalised import get_theme_icon
from app.tools.settings_access import readme_settings_async, update_settings
from app.Language.obtain_language import (
    get_all_languages_name,
    get_content_combo_name_async,
    get_content_description_async,
    get_content_name_async,
    get_content_pushbutton_name_async,
    get_content_switchbutton_name_async,
)
from app.tools.config import (
    export_diagnostic_data,
    export_settings,
    import_settings,
    export_all_data,
    import_all_data,
    configure_logging,
    set_autostart,
    show_notification,
    NotificationType,
    NotificationConfig,
)
from app.common.IPC_URL import URLIPCHandler


# ==================================================
# 基本设置
# ==================================================
class basic_settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 创建垂直布局
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(10)

        # 添加基本功能设置组件
        self.basic_function_widget = basic_settings_function(self)
        self.vBoxLayout.addWidget(self.basic_function_widget)

        # 添加个性化设置组件
        self.personalised_widget = basic_settings_personalised(self)
        self.vBoxLayout.addWidget(self.personalised_widget)

        # 添加数据管理组件
        self.data_management_widget = basic_settings_data_management(self)
        self.vBoxLayout.addWidget(self.data_management_widget)


class basic_settings_function(GroupHeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(get_content_name_async("basic_settings", "basic_function"))
        self.setBorderRadius(8)

        # 开机自启设置
        self.autostart_switch = SwitchButton()
        self.autostart_switch.setOffText(
            get_content_switchbutton_name_async(
                "basic_settings", "autostart", "disable"
            )
        )
        self.autostart_switch.setOnText(
            get_content_switchbutton_name_async("basic_settings", "autostart", "enable")
        )
        self.autostart_switch.setChecked(
            readme_settings_async("basic_settings", "autostart")
        )
        self.autostart_switch.checkedChanged.connect(self.__on_autostart_changed)

        # 启动显示主窗口设置
        self.show_startup_window_switch = SwitchButton()
        self.show_startup_window_switch.setOffText(
            get_content_switchbutton_name_async(
                "basic_settings", "show_startup_window", "disable"
            )
        )
        self.show_startup_window_switch.setOnText(
            get_content_switchbutton_name_async(
                "basic_settings", "show_startup_window", "enable"
            )
        )
        self.show_startup_window_switch.setChecked(
            readme_settings_async("basic_settings", "show_startup_window")
        )
        self.show_startup_window_switch.checkedChanged.connect(
            self.__on_show_startup_window_changed
        )

        # 自动保存窗口大小设置
        self.auto_save_window_size_switch = SwitchButton()
        self.auto_save_window_size_switch.setOffText(
            get_content_switchbutton_name_async(
                "basic_settings", "auto_save_window_size", "disable"
            )
        )
        self.auto_save_window_size_switch.setOnText(
            get_content_switchbutton_name_async(
                "basic_settings", "auto_save_window_size", "enable"
            )
        )
        _auto_save = readme_settings_async("basic_settings", "auto_save_window_size")
        self.auto_save_window_size_switch.setChecked(
            True if _auto_save is None else _auto_save
        )
        self.auto_save_window_size_switch.checkedChanged.connect(
            self.__on_auto_save_window_size_changed
        )

        # 后台驻留设置
        self.resident_switch = SwitchButton()
        self.resident_switch.setOffText(
            get_content_switchbutton_name_async(
                "basic_settings", "background_resident", "disable"
            )
        )
        self.resident_switch.setOnText(
            get_content_switchbutton_name_async(
                "basic_settings", "background_resident", "enable"
            )
        )
        _resident = readme_settings_async("basic_settings", "background_resident")
        self.resident_switch.setChecked(True if _resident is None else _resident)
        self.resident_switch.checkedChanged.connect(self.__on_resident_changed)

        # URL协议注册设置
        self.url_protocol_switch = SwitchButton()
        self.url_protocol_switch.setOffText(
            get_content_switchbutton_name_async(
                "basic_settings", "url_protocol", "disable"
            )
        )
        self.url_protocol_switch.setOnText(
            get_content_switchbutton_name_async(
                "basic_settings", "url_protocol", "enable"
            )
        )

        # 初始化URL IPC处理器
        self.url_ipc_handler = URLIPCHandler("SecRandom", "secrandom")

        # 检查协议是否已注册
        is_protocol_registered = self.url_ipc_handler.is_protocol_registered()
        self.url_protocol_switch.setChecked(is_protocol_registered)
        self.url_protocol_switch.checkedChanged.connect(self.__on_url_protocol_changed)

        # 添加设置项到分组
        self.addGroup(
            get_theme_icon("ic_fluent_arrow_sync_20_filled"),
            get_content_name_async("basic_settings", "autostart"),
            get_content_description_async("basic_settings", "autostart"),
            self.autostart_switch,
        )
        self.addGroup(
            get_theme_icon("ic_fluent_window_20_filled"),
            get_content_name_async("basic_settings", "show_startup_window"),
            get_content_description_async("basic_settings", "show_startup_window"),
            self.show_startup_window_switch,
        )
        self.addGroup(
            get_theme_icon("ic_fluent_save_20_filled"),
            get_content_name_async("basic_settings", "auto_save_window_size"),
            get_content_description_async("basic_settings", "auto_save_window_size"),
            self.auto_save_window_size_switch,
        )
        self.addGroup(
            get_theme_icon("ic_fluent_resize_20_filled"),
            get_content_name_async("basic_settings", "background_resident"),
            get_content_description_async("basic_settings", "background_resident"),
            self.resident_switch,
        )
        self.addGroup(
            get_theme_icon("ic_fluent_link_20_filled"),
            get_content_name_async("basic_settings", "url_protocol"),
            get_content_description_async("basic_settings", "url_protocol"),
            self.url_protocol_switch,
        )

    def __on_autostart_changed(self, checked):
        update_settings("basic_settings", "autostart", checked)
        ok = set_autostart(checked)
        if ok:
            if checked:
                show_notification(
                    NotificationType.SUCCESS,
                    NotificationConfig(
                        title=get_content_name_async("basic_settings", "autostart"),
                        content="已开启开机自启",
                    ),
                    parent=self.window(),
                )
            else:
                show_notification(
                    NotificationType.INFO,
                    NotificationConfig(
                        title=get_content_name_async("basic_settings", "autostart"),
                        content="已关闭开机自启",
                    ),
                    parent=self.window(),
                )
        else:
            show_notification(
                NotificationType.ERROR,
                NotificationConfig(
                    title=get_content_name_async("basic_settings", "autostart"),
                    content="设置开机自启失败",
                ),
                parent=self.window(),
            )

    def __on_show_startup_window_changed(self, checked):
        update_settings("basic_settings", "show_startup_window", checked)
        if checked:
            show_notification(
                NotificationType.SUCCESS,
                NotificationConfig(
                    title=get_content_name_async(
                        "basic_settings", "show_startup_window"
                    ),
                    content=get_content_name_async(
                        "basic_settings", "success_enable_content"
                    ),
                ),
                parent=self.window(),
            )
        else:
            show_notification(
                NotificationType.INFO,
                NotificationConfig(
                    title=get_content_name_async(
                        "basic_settings", "show_startup_window"
                    ),
                    content=get_content_name_async(
                        "basic_settings", "info_disable_content"
                    ),
                ),
                parent=self.window(),
            )

    def __on_resident_changed(self, checked):
        update_settings("basic_settings", "background_resident", checked)
        try:
            app = QApplication.instance()
            if app:
                app.setQuitOnLastWindowClosed(not checked)
        except Exception:
            pass
        if checked:
            show_notification(
                NotificationType.SUCCESS,
                NotificationConfig(
                    title=get_content_name_async(
                        "basic_settings", "background_resident"
                    ),
                    content="已开启后台驻留",
                ),
                parent=self.window(),
            )
        else:
            show_notification(
                NotificationType.INFO,
                NotificationConfig(
                    title=get_content_name_async(
                        "basic_settings", "background_resident"
                    ),
                    content="已关闭后台驻留",
                ),
                parent=self.window(),
            )

    def __on_auto_save_window_size_changed(self, checked):
        update_settings("basic_settings", "auto_save_window_size", checked)
        if checked:
            show_notification(
                NotificationType.SUCCESS,
                NotificationConfig(
                    title=get_content_name_async(
                        "basic_settings", "auto_save_window_size"
                    ),
                    content="已开启自动保存窗口大小",
                ),
                parent=self.window(),
            )
        else:
            show_notification(
                NotificationType.INFO,
                NotificationConfig(
                    title=get_content_name_async(
                        "basic_settings", "auto_save_window_size"
                    ),
                    content="已关闭自动保存窗口大小",
                ),
                parent=self.window(),
            )

    def __on_url_protocol_changed(self, checked):
        """URL协议开关变化处理"""
        # 临时断开信号连接，避免递归
        self.url_protocol_switch.checkedChanged.disconnect(
            self.__on_url_protocol_changed
        )

        try:
            if checked:
                # 注册URL协议
                success = self.url_ipc_handler.register_url_protocol()
                if success:
                    update_settings("basic_settings", "url_protocol", True)
                    show_notification(
                        NotificationType.SUCCESS,
                        NotificationConfig(
                            title=get_content_name_async(
                                "basic_settings", "url_protocol"
                            ),
                            content="已开启URL协议注册",
                        ),
                        parent=self.window(),
                    )
                    # 更新开关状态为成功状态
                    self.url_protocol_switch.setChecked(True)
                else:
                    # 注册失败，保持原状态
                    self.url_protocol_switch.setChecked(False)
                    show_notification(
                        NotificationType.WARNING,
                        NotificationConfig(
                            title=get_content_name_async(
                                "basic_settings", "url_protocol"
                            ),
                            content="URL协议注册失败，需要管理员权限",
                        ),
                        parent=self.window(),
                    )
            else:
                # 注销URL协议
                success = self.url_ipc_handler.unregister_url_protocol()
                if success:
                    update_settings("basic_settings", "url_protocol", False)
                    show_notification(
                        NotificationType.INFO,
                        NotificationConfig(
                            title=get_content_name_async(
                                "basic_settings", "url_protocol"
                            ),
                            content="已关闭URL协议注册",
                        ),
                        parent=self.window(),
                    )
                    # 更新开关状态为成功状态
                    self.url_protocol_switch.setChecked(False)
                else:
                    # 注销失败，保持原状态
                    self.url_protocol_switch.setChecked(True)
                    show_notification(
                        NotificationType.WARNING,
                        NotificationConfig(
                            title=get_content_name_async(
                                "basic_settings", "url_protocol"
                            ),
                            content="URL协议注销失败，可能需要管理员权限",
                        ),
                        parent=self.window(),
                    )
        except Exception as e:
            logger.error(f"URL协议设置错误: {e}")
            # 发生错误时恢复原状态
            self.url_protocol_switch.setChecked(not checked)
            error_msg = str(e)
            if "Access is denied" in error_msg or "WinError 5" in error_msg:
                content = "权限不足，URL协议注册/注销失败"
            else:
                content = f"URL协议设置错误: {error_msg}"

            show_notification(
                NotificationType.ERROR,
                NotificationConfig(
                    title=get_content_name_async("basic_settings", "url_protocol"),
                    content=content,
                ),
                parent=self.window(),
            )
        finally:
            # 重新连接信号
            self.url_protocol_switch.checkedChanged.connect(
                self.__on_url_protocol_changed
            )


class basic_settings_personalised(GroupHeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(get_content_name_async("basic_settings", "personalised"))
        self.setBorderRadius(8)

        # 主题设置卡片
        self.theme = ComboBox()
        self.theme.addItems(get_content_combo_name_async("basic_settings", "theme"))
        theme_to_index = {"LIGHT": 0, "DARK": 1, "AUTO": 2}
        current_theme = readme_settings_async("basic_settings", "theme")
        self.theme.setCurrentIndex(theme_to_index.get(current_theme, 2))
        index_to_theme = {0: Theme.LIGHT, 1: Theme.DARK, 2: Theme.AUTO}
        self.theme.currentIndexChanged.connect(
            lambda index: update_settings(
                "basic_settings", "theme", ["LIGHT", "DARK", "AUTO"][index]
            )
        )
        self.theme.currentIndexChanged.connect(
            lambda index: setTheme(index_to_theme.get(index))
        )

        # 主题色设置卡片
        self.themeColor = ColorConfigItem(
            "basic_settings",
            "theme_color",
            readme_settings_async("basic_settings", "theme_color"),
        )
        self.themeColor.valueChanged.connect(
            lambda color: update_settings("basic_settings", "theme_color", color.name())
        )
        self.themeColor.valueChanged.connect(lambda color: setThemeColor(color))

        # 语言设置卡片
        self.language = ComboBox()
        self.language.addItems(get_all_languages_name())
        self.language.setCurrentText(
            readme_settings_async("basic_settings", "language")
        )
        self.language.currentTextChanged.connect(
            lambda language: update_settings("basic_settings", "language", language)
        )

        # 字体设置卡片
        self.fontComboBox = ComboBox()
        self.fontComboBox.addItems(
            ["HarmonyOS Sans SC"] + sorted(QFontDatabase.families())
        )
        self.fontComboBox.setCurrentText(
            readme_settings_async("basic_settings", "font")
        )
        self.fontComboBox.currentTextChanged.connect(
            lambda font: update_settings("basic_settings", "font", font)
        )

        # 界面缩放设置卡片
        self.dpiScale = ComboBox()
        dpi_scale_items = get_content_combo_name_async("basic_settings", "dpiScale")
        self.dpiScale.addItems(dpi_scale_items)
        # 如果设置值是"Auto"，则显示最后一个选项；否则显示对应的值
        current_dpi_scale = readme_settings_async("basic_settings", "dpiScale")
        if current_dpi_scale == "Auto":
            self.dpiScale.setCurrentText(dpi_scale_items[-1])  # "自动"是最后一个选项
        else:
            self.dpiScale.setCurrentText(current_dpi_scale)
        self.dpiScale.currentTextChanged.connect(
            lambda scale: self.update_dpi_scale_setting(scale, dpi_scale_items)
        )

        # 日志等级设置卡片
        self.logLevel = ComboBox()
        log_level_items = get_content_combo_name_async("basic_settings", "log_level")
        self.logLevel.addItems(log_level_items)
        current_log_level = readme_settings_async("basic_settings", "log_level")
        if current_log_level in log_level_items:
            self.logLevel.setCurrentText(current_log_level)
        self.logLevel.currentTextChanged.connect(
            lambda level: update_settings("basic_settings", "log_level", level)
        )
        self.logLevel.currentTextChanged.connect(lambda: configure_logging())

        # 主题色设置卡片
        self.themeColorCard = ColorSettingCard(
            self.themeColor,
            get_theme_icon("ic_fluent_color_20_filled"),
            self.tr(get_content_name_async("basic_settings", "theme_color")),
            self.tr(get_content_description_async("basic_settings", "theme_color")),
        )

        # 添加设置项到分组
        self.addGroup(
            get_theme_icon("ic_fluent_dark_theme_20_filled"),
            get_content_name_async("basic_settings", "theme"),
            get_content_description_async("basic_settings", "theme"),
            self.theme,
        )
        self.addGroup(
            get_theme_icon("ic_fluent_local_language_20_filled"),
            get_content_name_async("basic_settings", "language"),
            get_content_description_async("basic_settings", "language"),
            self.language,
        )
        self.addGroup(
            get_theme_icon("ic_fluent_text_font_20_filled"),
            get_content_name_async("basic_settings", "font"),
            get_content_description_async("basic_settings", "font"),
            self.fontComboBox,
        )
        self.addGroup(
            get_theme_icon("ic_fluent_zoom_fit_20_filled"),
            get_content_name_async("basic_settings", "dpiScale"),
            get_content_description_async("basic_settings", "dpiScale"),
            self.dpiScale,
        )
        self.addGroup(
            get_theme_icon("ic_fluent_bug_20_filled"),
            get_content_name_async("basic_settings", "log_level"),
            get_content_description_async("basic_settings", "log_level"),
            self.logLevel,
        )
        # 添加卡片到布局
        self.vBoxLayout.addWidget(self.themeColorCard)

    def update_dpi_scale_setting(self, scale, dpi_scale_items):
        """更新DPI缩放设置"""
        # 如果选择的是最后一个选项("自动")，则保存为"Auto"
        if scale == dpi_scale_items[-1]:
            update_settings("basic_settings", "dpiScale", "Auto")
        else:
            update_settings("basic_settings", "dpiScale", scale)


class basic_settings_data_management(GroupHeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setTitle(get_content_name_async("basic_settings", "data_management"))
        self.setBorderRadius(8)

        # 导出诊断数据按钮
        self.export_diagnostic_data_button = PushButton(
            get_content_pushbutton_name_async(
                "basic_settings", "export_diagnostic_data"
            )
        )
        self.export_diagnostic_data_button.clicked.connect(
            lambda: export_diagnostic_data(self.window())
        )

        # 导出设置按钮
        self.export_settings_button = PushButton(
            get_content_pushbutton_name_async("basic_settings", "export_settings")
        )
        self.export_settings_button.clicked.connect(
            lambda: export_settings(self.window())
        )

        # 导入设置按钮
        self.import_settings_button = PushButton(
            get_content_pushbutton_name_async("basic_settings", "import_settings")
        )
        self.import_settings_button.clicked.connect(
            lambda: import_settings(self.window())
        )

        # 导出软件所有数据按钮
        self.export_all_data_button = PushButton(
            get_content_pushbutton_name_async("basic_settings", "export_all_data")
        )
        self.export_all_data_button.clicked.connect(
            lambda: export_all_data(self.window())
        )

        # 导入软件所有数据按钮
        self.import_all_data_button = PushButton(
            get_content_pushbutton_name_async("basic_settings", "import_all_data")
        )
        self.import_all_data_button.clicked.connect(
            lambda: import_all_data(self.window())
        )

        # 添加设置项到分组
        self.addGroup(
            get_theme_icon("ic_fluent_database_arrow_down_20_filled"),
            get_content_name_async("basic_settings", "export_diagnostic_data"),
            get_content_description_async("basic_settings", "export_diagnostic_data"),
            self.export_diagnostic_data_button,
        )
        self.addGroup(
            get_theme_icon("ic_fluent_arrow_clockwise_dashes_settings_20_filled"),
            get_content_name_async("basic_settings", "export_settings"),
            get_content_description_async("basic_settings", "export_settings"),
            self.export_settings_button,
        )
        self.addGroup(
            get_theme_icon("ic_fluent_arrow_clockwise_dashes_settings_20_filled"),
            get_content_name_async("basic_settings", "import_settings"),
            get_content_description_async("basic_settings", "import_settings"),
            self.import_settings_button,
        )
        self.addGroup(
            get_theme_icon("ic_fluent_database_window_20_filled"),
            get_content_name_async("basic_settings", "export_all_data"),
            get_content_description_async("basic_settings", "export_all_data"),
            self.export_all_data_button,
        )
        self.addGroup(
            get_theme_icon("ic_fluent_database_window_20_filled"),
            get_content_name_async("basic_settings", "import_all_data"),
            get_content_description_async("basic_settings", "import_all_data"),
            self.import_all_data_button,
        )
