# ==================================================
# 导入库
# ==================================================

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtNetwork import *
from qfluentwidgets import *

from app.tools.variable import *
from app.tools.path_utils import *
from app.tools.personalised import *
from app.tools.settings_default import *
from app.tools.settings_access import *
from app.Language.obtain_language import *
from app.tools.settings_visibility_manager import is_setting_visible


# ==================================================
# 浮窗管理 - 主容器
# ==================================================
class floating_window_management(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 创建垂直布局
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(10)

        # 创建基础设置
        self.basic_settings = floating_window_basic_settings(self)
        self.vBoxLayout.addWidget(self.basic_settings)

        # 创建外观设置
        self.appearance_settings = floating_window_appearance_settings(self)
        self.vBoxLayout.addWidget(self.appearance_settings)

        # 创建贴边设置
        self.edge_settings = floating_window_edge_settings(self)
        self.vBoxLayout.addWidget(self.edge_settings)

        # 存储浮窗实例的引用
        self.levitation_window = None

    def set_levitation_window(self, window):
        """设置浮窗实例引用"""
        self.levitation_window = window
        # 连接外观设置变化信号到浮窗重建方法
        self.appearance_settings.appearance_settings_changed.connect(
            self._on_appearance_settings_changed
        )

    def _on_appearance_settings_changed(self):
        """处理外观设置变更"""
        if self.levitation_window:
            self.levitation_window.rebuild_ui()


# ==================================================
# 浮窗管理 - 基础设置
# ==================================================
class floating_window_basic_settings(GroupHeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(
            get_content_name_async("floating_window_management", "basic_settings")
        )
        self.setBorderRadius(8)

        # 软件启动时浮窗显示隐藏开关
        self.startup_display_floating_window_switch = SwitchButton()
        self.startup_display_floating_window_switch.setOffText(
            get_content_switchbutton_name_async(
                "floating_window_management",
                "startup_display_floating_window",
                "disable",
            )
        )
        self.startup_display_floating_window_switch.setOnText(
            get_content_switchbutton_name_async(
                "floating_window_management",
                "startup_display_floating_window",
                "enable",
            )
        )
        self.startup_display_floating_window_switch.setChecked(
            readme_settings_async(
                "floating_window_management", "startup_display_floating_window"
            )
        )
        self.startup_display_floating_window_switch.checkedChanged.connect(
            lambda checked: update_settings(
                "floating_window_management", "startup_display_floating_window", checked
            )
        )

        # 浮窗透明度
        self.floating_window_opacity_spinbox = SpinBox()
        self.floating_window_opacity_spinbox.setFixedWidth(WIDTH_SPINBOX)
        self.floating_window_opacity_spinbox.setRange(0, 100)
        self.floating_window_opacity_spinbox.setSuffix("%")
        self.floating_window_opacity_spinbox.setValue(
            readme_settings_async(
                "floating_window_management", "floating_window_opacity"
            )
            * 100
        )
        self.floating_window_opacity_spinbox.valueChanged.connect(
            lambda value: update_settings(
                "floating_window_management", "floating_window_opacity", value / 100
            )
        )

        # 重置浮窗位置按钮
        self.reset_floating_window_position_button = PushButton(
            get_content_pushbutton_name_async(
                "floating_window_management", "reset_floating_window_position_button"
            )
        )
        self.reset_floating_window_position_button.setText(
            get_content_name_async(
                "floating_window_management", "reset_floating_window_position_button"
            )
        )
        self.reset_floating_window_position_button.clicked.connect(
            self.reset_floating_window_position_button_clicked
        )

        # 浮窗可拖动开关
        self.floating_window_draggable_switch = SwitchButton()
        self.floating_window_draggable_switch.setOffText(
            get_content_switchbutton_name_async(
                "floating_window_management",
                "floating_window_draggable",
                "disable",
            )
        )
        self.floating_window_draggable_switch.setOnText(
            get_content_switchbutton_name_async(
                "floating_window_management",
                "floating_window_draggable",
                "enable",
            )
        )
        self.floating_window_draggable_switch.setChecked(
            readme_settings_async(
                "floating_window_management", "floating_window_draggable"
            )
        )
        self.floating_window_draggable_switch.checkedChanged.connect(
            lambda checked: update_settings(
                "floating_window_management", "floating_window_draggable", checked
            )
        )

        # 浮窗长按拖动时间
        self.floating_window_long_press_duration_spinbox = SpinBox()
        self.floating_window_long_press_duration_spinbox.setFixedWidth(WIDTH_SPINBOX)
        self.floating_window_long_press_duration_spinbox.setRange(50, 3000)
        self.floating_window_long_press_duration_spinbox.setSingleStep(100)
        self.floating_window_long_press_duration_spinbox.setSuffix("ms")
        self.floating_window_long_press_duration_spinbox.setValue(
            readme_settings_async(
                "floating_window_management", "floating_window_long_press_duration"
            )
        )
        self.floating_window_long_press_duration_spinbox.valueChanged.connect(
            lambda value: update_settings(
                "floating_window_management",
                "floating_window_long_press_duration",
                value,
            )
        )

        # 无焦点模式开关
        self.do_not_steal_focus_switch = SwitchButton()
        self.do_not_steal_focus_switch.setOffText(
            get_content_switchbutton_name_async(
                "floating_window_management", "do_not_steal_focus", "disable"
            )
        )
        self.do_not_steal_focus_switch.setOnText(
            get_content_switchbutton_name_async(
                "floating_window_management", "do_not_steal_focus", "enable"
            )
        )
        self.do_not_steal_focus_switch.setChecked(
            readme_settings_async("floating_window_management", "do_not_steal_focus")
        )
        self.do_not_steal_focus_switch.checkedChanged.connect(
            lambda checked: update_settings(
                "floating_window_management", "do_not_steal_focus", checked
            )
        )

        # 添加设置项到分组
        self.addGroup(
            get_theme_icon("ic_fluent_desktop_sync_20_filled"),
            get_content_name_async(
                "floating_window_management", "startup_display_floating_window"
            ),
            get_content_description_async(
                "floating_window_management", "startup_display_floating_window"
            ),
            self.startup_display_floating_window_switch,
        )
        self.addGroup(
            get_theme_icon("ic_fluent_brightness_high_20_filled"),
            get_content_name_async(
                "floating_window_management", "floating_window_opacity"
            ),
            get_content_description_async(
                "floating_window_management", "floating_window_opacity"
            ),
            self.floating_window_opacity_spinbox,
        )
        if is_setting_visible(
            "floating_window_management", "floating_window_draggable"
        ):
            self.addGroup(
                get_theme_icon("ic_fluent_gesture_20_filled"),
                get_content_name_async(
                    "floating_window_management", "floating_window_draggable"
                ),
                get_content_description_async(
                    "floating_window_management", "floating_window_draggable"
                ),
                self.floating_window_draggable_switch,
            )
        if is_setting_visible(
            "floating_window_management", "floating_window_long_press_duration"
        ):
            self.addGroup(
                get_theme_icon("ic_fluent_gesture_20_filled"),
                get_content_name_async(
                    "floating_window_management", "floating_window_long_press_duration"
                ),
                get_content_description_async(
                    "floating_window_management", "floating_window_long_press_duration"
                ),
                self.floating_window_long_press_duration_spinbox,
            )
        if is_setting_visible("floating_window_management", "do_not_steal_focus"):
            self.addGroup(
                get_theme_icon("ic_fluent_lock_open_20_filled"),
                get_content_name_async(
                    "floating_window_management", "do_not_steal_focus"
                ),
                get_content_description_async(
                    "floating_window_management", "do_not_steal_focus"
                ),
                self.do_not_steal_focus_switch,
            )
        self.addGroup(
            get_theme_icon("ic_fluent_arrow_reset_20_filled"),
            get_content_name_async(
                "floating_window_management", "reset_floating_window_position_button"
            ),
            get_content_description_async(
                "floating_window_management", "reset_floating_window_position_button"
            ),
            self.reset_floating_window_position_button,
        )

    def reset_floating_window_position_button_clicked(self):
        """重置浮窗位置按钮点击处理"""
        # 更新设置为默认位置
        update_settings("float_position", "x", 100)
        update_settings("float_position", "y", 100)


# ==================================================
# 浮窗管理 - 外观设置
# ==================================================
class floating_window_appearance_settings(GroupHeaderCardWidget):
    appearance_settings_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(
            get_content_name_async("floating_window_management", "appearance_settings")
        )
        self.setBorderRadius(8)

        # 浮窗按钮控件配置下拉框
        self.floating_window_button_control_combo_box = ComboBox()
        self.floating_window_button_control_combo_box.addItems(
            get_content_combo_name_async(
                "floating_window_management", "floating_window_button_control"
            )
        )
        self.floating_window_button_control_combo_box.setCurrentIndex(
            readme_settings_async(
                "floating_window_management", "floating_window_button_control"
            )
        )
        self.floating_window_button_control_combo_box.currentIndexChanged.connect(
            self.floating_window_button_control_combo_box_changed
        )

        # 浮窗排列方式下拉框
        self.floating_window_placement_combo_box = ComboBox()
        self.floating_window_placement_combo_box.addItems(
            get_content_combo_name_async(
                "floating_window_management", "floating_window_placement"
            )
        )
        self.floating_window_placement_combo_box.setCurrentIndex(
            readme_settings_async(
                "floating_window_management", "floating_window_placement"
            )
        )
        self.floating_window_placement_combo_box.currentIndexChanged.connect(
            self.floating_window_placement_combo_box_changed
        )

        # 浮窗显示样式下拉框
        self.floating_window_display_style_combo_box = ComboBox()
        self.floating_window_display_style_combo_box.addItems(
            get_content_combo_name_async(
                "floating_window_management", "floating_window_display_style"
            )
        )
        self.floating_window_display_style_combo_box.setCurrentIndex(
            readme_settings_async(
                "floating_window_management", "floating_window_display_style"
            )
        )
        self.floating_window_display_style_combo_box.currentIndexChanged.connect(
            self.floating_window_display_style_combo_box_changed
        )

        # 浮窗大小下拉框
        self.floating_window_size_combo_box = ComboBox()
        self.floating_window_size_combo_box.addItems(
            get_content_combo_name_async(
                "floating_window_management", "floating_window_size"
            )
        )
        self.floating_window_size_combo_box.setCurrentIndex(
            readme_settings_async("floating_window_management", "floating_window_size")
        )
        self.floating_window_size_combo_box.currentIndexChanged.connect(
            self.floating_window_size_combo_box_changed
        )

        # 添加设置项到分组
        self.addGroup(
            get_theme_icon("ic_fluent_button_20_filled"),
            get_content_name_async(
                "floating_window_management", "floating_window_button_control"
            ),
            get_content_description_async(
                "floating_window_management", "floating_window_button_control"
            ),
            self.floating_window_button_control_combo_box,
        )
        self.addGroup(
            get_theme_icon("ic_fluent_align_left_20_filled"),
            get_content_name_async(
                "floating_window_management", "floating_window_placement"
            ),
            get_content_description_async(
                "floating_window_management", "floating_window_placement"
            ),
            self.floating_window_placement_combo_box,
        )
        self.addGroup(
            get_theme_icon("ic_fluent_design_ideas_20_filled"),
            get_content_name_async(
                "floating_window_management", "floating_window_display_style"
            ),
            get_content_description_async(
                "floating_window_management", "floating_window_display_style"
            ),
            self.floating_window_display_style_combo_box,
        )
        if is_setting_visible("floating_window_management", "floating_window_size"):
            self.addGroup(
                get_theme_icon("ic_fluent_resize_20_filled"),
                get_content_name_async(
                    "floating_window_management", "floating_window_size"
                ),
                get_content_description_async(
                    "floating_window_management", "floating_window_size"
                ),
                self.floating_window_size_combo_box,
            )

    def floating_window_button_control_combo_box_changed(self, index):
        update_settings(
            "floating_window_management", "floating_window_button_control", index
        )
        self.appearance_settings_changed.emit()

    def floating_window_placement_combo_box_changed(self, index):
        update_settings(
            "floating_window_management", "floating_window_placement", index
        )
        self.appearance_settings_changed.emit()

    def floating_window_display_style_combo_box_changed(self, index):
        update_settings(
            "floating_window_management", "floating_window_display_style", index
        )
        self.appearance_settings_changed.emit()

    def floating_window_size_combo_box_changed(self, index):
        update_settings("floating_window_management", "floating_window_size", index)
        self.appearance_settings_changed.emit()


# ==================================================
# 浮窗管理 - 贴边设置
# ==================================================
class floating_window_edge_settings(GroupHeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(
            get_content_name_async("floating_window_management", "edge_settings")
        )
        self.setBorderRadius(8)

        # 浮窗贴边开关
        self.floating_window_stick_to_edge_switch = SwitchButton()
        self.floating_window_stick_to_edge_switch.setOffText(
            get_content_switchbutton_name_async(
                "floating_window_management", "floating_window_stick_to_edge", "disable"
            )
        )
        self.floating_window_stick_to_edge_switch.setOnText(
            get_content_switchbutton_name_async(
                "floating_window_management", "floating_window_stick_to_edge", "enable"
            )
        )
        self.floating_window_stick_to_edge_switch.setChecked(
            readme_settings_async(
                "floating_window_management", "floating_window_stick_to_edge"
            )
        )
        self.floating_window_stick_to_edge_switch.checkedChanged.connect(
            self.floating_window_stick_to_edge_switch_changed
        )

        # 浮窗贴边回收秒数
        self.floating_window_stick_to_edge_recover_seconds_spinbox = SpinBox()
        self.floating_window_stick_to_edge_recover_seconds_spinbox.setFixedWidth(
            WIDTH_SPINBOX
        )
        self.floating_window_stick_to_edge_recover_seconds_spinbox.setRange(1, 60)
        self.floating_window_stick_to_edge_recover_seconds_spinbox.setSuffix("s")
        self.floating_window_stick_to_edge_recover_seconds_spinbox.setValue(
            readme_settings_async(
                "floating_window_management",
                "floating_window_stick_to_edge_recover_seconds",
            )
        )
        self.floating_window_stick_to_edge_recover_seconds_spinbox.valueChanged.connect(
            self.floating_window_stick_to_edge_recover_seconds_spinbox_changed
        )

        # 浮窗贴边显示样式下拉框
        self.floating_window_stick_to_edge_display_style_combo_box = ComboBox()
        self.floating_window_stick_to_edge_display_style_combo_box.addItems(
            get_content_combo_name_async(
                "floating_window_management",
                "floating_window_stick_to_edge_display_style",
            )
        )
        self.floating_window_stick_to_edge_display_style_combo_box.setCurrentIndex(
            readme_settings_async(
                "floating_window_management",
                "floating_window_stick_to_edge_display_style",
            )
        )
        self.floating_window_stick_to_edge_display_style_combo_box.currentIndexChanged.connect(
            self.floating_window_stick_to_edge_display_style_combo_box_changed
        )

        # 添加设置项到分组
        self.addGroup(
            get_theme_icon("ic_fluent_pin_20_filled"),
            get_content_name_async(
                "floating_window_management", "floating_window_stick_to_edge"
            ),
            get_content_description_async(
                "floating_window_management", "floating_window_stick_to_edge"
            ),
            self.floating_window_stick_to_edge_switch,
        )
        self.addGroup(
            get_theme_icon("ic_fluent_timer_20_filled"),
            get_content_name_async(
                "floating_window_management",
                "floating_window_stick_to_edge_recover_seconds",
            ),
            get_content_description_async(
                "floating_window_management",
                "floating_window_stick_to_edge_recover_seconds",
            ),
            self.floating_window_stick_to_edge_recover_seconds_spinbox,
        )
        if is_setting_visible(
            "floating_window_management", "floating_window_stick_to_edge_display_style"
        ):
            self.addGroup(
                get_theme_icon("ic_fluent_desktop_sync_20_filled"),
                get_content_name_async(
                    "floating_window_management",
                    "floating_window_stick_to_edge_display_style",
                ),
                get_content_description_async(
                    "floating_window_management",
                    "floating_window_stick_to_edge_display_style",
                ),
                self.floating_window_stick_to_edge_display_style_combo_box,
            )

    def floating_window_stick_to_edge_switch_changed(self, checked):
        update_settings(
            "floating_window_management", "floating_window_stick_to_edge", checked
        )

    def floating_window_stick_to_edge_recover_seconds_spinbox_changed(self, value):
        update_settings(
            "floating_window_management",
            "floating_window_stick_to_edge_recover_seconds",
            value,
        )

    def floating_window_stick_to_edge_display_style_combo_box_changed(self, index):
        update_settings(
            "floating_window_management",
            "floating_window_stick_to_edge_display_style",
            index,
        )
