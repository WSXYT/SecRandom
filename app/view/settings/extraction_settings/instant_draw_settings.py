# ==================================================
# 导入库
# ==================================================
import os

from loguru import logger
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtNetwork import *
from qfluentwidgets import *

from app.tools.variable import *
from app.tools.path_utils import *
from app.tools.personalised import *
from app.tools.settings_default import *
from app.tools.settings_access import *
from app.Language.obtain_language import *

# ==================================================
# 即抽设置
# ==================================================
class instant_draw_settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 创建垂直布局
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(10)

        # 添加抽取功能设置组件
        self.extraction_function_widget = instant_draw_extraction_function(self)
        self.vBoxLayout.addWidget(self.extraction_function_widget)

        # 添加显示设置组件
        self.display_settings_widget = instant_draw_display_settings(self)
        self.vBoxLayout.addWidget(self.display_settings_widget)

        # 添加动画设置组件
        self.animation_settings_widget = instant_draw_animation_settings(self)
        self.vBoxLayout.addWidget(self.animation_settings_widget)


class instant_draw_extraction_function(GroupHeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(get_content_name_async("instant_draw_settings", "extraction_function"))
        self.setBorderRadius(8)

        # 抽取模式下拉框
        self.draw_mode_combo = ComboBox()
        self.draw_mode_combo.addItems(get_content_combo_name_async("instant_draw_settings", "draw_mode"))
        self.draw_mode_combo.setCurrentIndex(readme_settings_async("instant_draw_settings", "draw_mode"))
        self.draw_mode_combo.currentIndexChanged.connect(self.on_draw_mode_changed)

        # 清除抽取记录方式下拉框
        self.clear_record_combo = ComboBox()
        self.clear_record_combo.addItems(get_content_combo_name_async("instant_draw_settings", "clear_record"))
        self.clear_record_combo.setCurrentIndex(readme_settings_async("instant_draw_settings", "clear_record"))
        self.clear_record_combo.currentIndexChanged.connect(lambda: update_settings("instant_draw_settings", "clear_record", self.clear_record_combo.currentIndex()))

        # 半重复抽取次数输入框
        self.half_repeat_spin = SpinBox()
        self.half_repeat_spin.setFixedWidth(WIDTH_SPINBOX)
        self.half_repeat_spin.setRange(0, 100)
        self.half_repeat_spin.setSuffix("次")
        self.half_repeat_spin.setValue(readme_settings_async("instant_draw_settings", "half_repeat"))
        self.half_repeat_spin.valueChanged.connect(lambda: update_settings("instant_draw_settings", "half_repeat", self.half_repeat_spin.value()))

        # 抽取后定时清除时间输入框
        self.clear_time_spin = SpinBox()
        self.clear_time_spin.setFixedWidth(WIDTH_SPINBOX)
        self.clear_time_spin.setRange(0, 25600)
        self.clear_time_spin.setSuffix("秒")
        self.clear_time_spin.setValue(readme_settings_async("instant_draw_settings", "clear_time"))
        self.clear_time_spin.valueChanged.connect(lambda: update_settings("instant_draw_settings", "clear_time", self.clear_time_spin.value()))

        # 抽取方式下拉框
        self.draw_type_combo = ComboBox()
        self.draw_type_combo.addItems(get_content_combo_name_async("instant_draw_settings", "draw_type"))
        self.draw_type_combo.setCurrentIndex(readme_settings_async("instant_draw_settings", "draw_type"))
        self.draw_type_combo.currentIndexChanged.connect(lambda: update_settings("instant_draw_settings", "draw_type", self.draw_type_combo.currentIndex()))

        # 添加设置项到分组
        self.addGroup(get_theme_icon("ic_fluent_document_bullet_list_cube_20_filled"),
                        get_content_name_async("instant_draw_settings", "draw_mode"), get_content_description_async("instant_draw_settings", "draw_mode"), self.draw_mode_combo)
        self.addGroup(get_theme_icon("ic_fluent_text_clear_formatting_20_filled"),
                        get_content_name_async("instant_draw_settings", "clear_record"), get_content_description_async("instant_draw_settings", "clear_record"), self.clear_record_combo)
        self.addGroup(get_theme_icon("ic_fluent_clipboard_bullet_list_20_filled"),
                        get_content_name_async("instant_draw_settings", "half_repeat"), get_content_description_async("instant_draw_settings", "half_repeat"), self.half_repeat_spin)
        self.addGroup(get_theme_icon("ic_fluent_timer_off_20_filled"),
                        get_content_name_async("instant_draw_settings", "clear_time"), get_content_description_async("instant_draw_settings", "clear_time"), self.clear_time_spin)
        self.addGroup(get_theme_icon("ic_fluent_drawer_add_20_filled"),
                        get_content_name_async("instant_draw_settings", "draw_type"), get_content_description_async("instant_draw_settings", "draw_type"), self.draw_type_combo)

        # 初始化时调用一次，确保界面状态与设置一致
        self.on_draw_mode_changed()

    def on_draw_mode_changed(self):
        """当抽取模式改变时的处理逻辑"""
        # 更新设置值
        update_settings("instant_draw_settings", "draw_mode", self.draw_mode_combo.currentIndex())

        # 获取当前抽取模式索引
        draw_mode_index = self.draw_mode_combo.currentIndex()

        # 根据抽取模式设置不同的控制逻辑
        if draw_mode_index == 0:  # 重复抽取模式
            # 禁用清除抽取记录方式下拉框
            self.clear_record_combo.setEnabled(False)
            # 清空当前选项
            self.clear_record_combo.clear()
            self.clear_record_combo.addItems(get_any_position_value_async("instant_draw_settings", "clear_record", "combo_items_other"))
            # 强制设置为"无需清除"（索引2）
            self.clear_record_combo.setCurrentIndex(2)
            # 更新设置
            update_settings("instant_draw_settings", "clear_record", 2)

            # 设置half_repeat_spin为0并禁用
            self.half_repeat_spin.setEnabled(False)
            self.half_repeat_spin.setRange(0, 0)
            self.half_repeat_spin.setValue(0)
            # 更新设置
            update_settings("instant_draw_settings", "half_repeat", 0)

        else:  # 不重复抽取模式或半重复抽取模式
            # 启用清除抽取记录方式下拉框
            self.clear_record_combo.setEnabled(True)

            # 清空当前选项
            self.clear_record_combo.clear()

            # 添加前两个选项（不包含"无需清除"）
            self.clear_record_combo.addItems(get_content_combo_name_async("instant_draw_settings", "clear_record"))

            # 设置默认选择第一个选项
            self.clear_record_combo.setCurrentIndex(0)
            # 更新设置
            update_settings("instant_draw_settings", "clear_record", 0)

            # 根据具体模式设置half_repeat_spin
            if draw_mode_index == 1:  # 不重复抽取模式
                # 设置half_repeat_spin为1并禁用
                self.half_repeat_spin.setEnabled(False)
                self.half_repeat_spin.setRange(1, 1)
                self.half_repeat_spin.setValue(1)
                # 更新设置
                update_settings("instant_draw_settings", "half_repeat", 1)
            else:  # 半重复抽取模式（索引2）
                # 设置half_repeat_spin为2-100范围并启用
                self.half_repeat_spin.setEnabled(True)
                self.half_repeat_spin.setRange(2, 100)
                # 如果当前值小于2，则设置为2
                if self.half_repeat_spin.value() < 2:
                    self.half_repeat_spin.setValue(2)
                    # 更新设置
                    update_settings("instant_draw_settings", "half_repeat", 2)


class instant_draw_display_settings(GroupHeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(get_content_name_async("instant_draw_settings", "display_settings"))
        self.setBorderRadius(8)

        # 字体大小输入框
        self.font_size_spin = SpinBox()
        self.font_size_spin.setFixedWidth(WIDTH_SPINBOX)
        self.font_size_spin.setRange(10, 1000)
        self.font_size_spin.setSuffix("px")
        self.font_size_spin.setValue(readme_settings_async("instant_draw_settings", "font_size"))
        self.font_size_spin.valueChanged.connect(lambda: update_settings("instant_draw_settings", "font_size", self.font_size_spin.value()))

        # RESULT格式下拉框
        self.display_format_combo = ComboBox()
        self.display_format_combo.addItems(get_content_combo_name_async("instant_draw_settings", "display_format"))
        self.display_format_combo.setCurrentIndex(readme_settings_async("instant_draw_settings", "display_format"))
        self.display_format_combo.currentIndexChanged.connect(lambda: update_settings("instant_draw_settings", "display_format", self.display_format_combo.currentIndex()))

        # 显示随机组员格式下拉框
        self.show_random_format_combo = ComboBox()
        self.show_random_format_combo.addItems(get_content_combo_name_async("instant_draw_settings", "show_random"))
        self.show_random_format_combo.setCurrentIndex(readme_settings_async("instant_draw_settings", "show_random"))
        self.show_random_format_combo.currentIndexChanged.connect(lambda: update_settings("instant_draw_settings", "show_random", self.show_random_format_combo.currentIndex()))

        # 添加设置项到分组
        self.addGroup(get_theme_icon("ic_fluent_text_font_20_filled"),
                        get_content_name_async("instant_draw_settings", "font_size"), get_content_description_async("instant_draw_settings", "font_size"), self.font_size_spin)
        self.addGroup(get_theme_icon("ic_fluent_slide_text_sparkle_20_filled"),
                        get_content_name_async("instant_draw_settings", "display_format"), get_content_description_async("instant_draw_settings", "display_format"), self.display_format_combo)
        self.addGroup(get_theme_icon("ic_fluent_group_list_20_filled"),
                        get_content_name_async("instant_draw_settings", "show_random"), get_content_description_async("instant_draw_settings", "show_random"), self.show_random_format_combo)


class instant_draw_animation_settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 创建垂直布局
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(10)

        # 添加基础动画设置组件
        self.basic_animation_widget = instant_draw_basic_animation_settings(self)
        self.vBoxLayout.addWidget(self.basic_animation_widget)

        # 添加颜色主题设置组件
        self.color_theme_widget = instant_draw_color_theme_settings(self)
        self.vBoxLayout.addWidget(self.color_theme_widget)

        # 添加学生图片设置组件
        self.student_image_widget = instant_draw_student_image_settings(self)
        self.vBoxLayout.addWidget(self.student_image_widget)

        # 添加音乐设置组件
        self.music_settings_widget = instant_draw_music_settings(self)
        self.vBoxLayout.addWidget(self.music_settings_widget)


class instant_draw_basic_animation_settings(GroupHeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(get_content_name_async("instant_draw_settings", "basic_animation_settings"))
        self.setBorderRadius(8)

        # 动画模式下拉框
        self.animation_combo = ComboBox()
        self.animation_combo.addItems(get_content_combo_name_async("instant_draw_settings", "animation"))
        self.animation_combo.setCurrentIndex(readme_settings_async("instant_draw_settings", "animation"))
        self.animation_combo.currentIndexChanged.connect(lambda: update_settings("instant_draw_settings", "animation", self.animation_combo.currentIndex()))

        # 动画间隔输入框
        self.animation_interval_spin = SpinBox()
        self.animation_interval_spin.setFixedWidth(WIDTH_SPINBOX)
        self.animation_interval_spin.setRange(1, 2000)
        self.animation_interval_spin.setSuffix("ms")
        self.animation_interval_spin.setValue(readme_settings_async("instant_draw_settings", "animation_interval"))
        self.animation_interval_spin.valueChanged.connect(lambda: update_settings("instant_draw_settings", "animation_interval", self.animation_interval_spin.value()))

        # 自动播放次数输入框
        self.autoplay_count_spin = SpinBox()
        self.autoplay_count_spin.setFixedWidth(WIDTH_SPINBOX)
        self.autoplay_count_spin.setRange(0, 100)
        self.autoplay_count_spin.setSuffix("次")
        self.autoplay_count_spin.setValue(readme_settings_async("instant_draw_settings", "autoplay_count"))
        self.autoplay_count_spin.valueChanged.connect(lambda: update_settings("instant_draw_settings", "autoplay_count", self.autoplay_count_spin.value()))

        # 添加设置项到分组
        self.addGroup(get_theme_icon("ic_fluent_sanitize_20_filled"),
                        get_content_name_async("instant_draw_settings", "animation"), get_content_description_async("instant_draw_settings", "animation"), self.animation_combo)
        self.addGroup(get_theme_icon("ic_fluent_timeline_20_filled"),
                        get_content_name_async("instant_draw_settings", "animation_interval"), get_content_description_async("instant_draw_settings", "animation_interval"), self.animation_interval_spin)
        self.addGroup(get_theme_icon("ic_fluent_slide_play_20_filled"),
                        get_content_name_async("instant_draw_settings", "autoplay_count"), get_content_description_async("instant_draw_settings", "autoplay_count"), self.autoplay_count_spin)


class instant_draw_color_theme_settings(GroupHeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(get_content_name_async("instant_draw_settings", "color_theme_settings"))
        self.setBorderRadius(8)

        # 动画颜色主题下拉框
        self.animation_color_theme_combo = ComboBox()
        self.animation_color_theme_combo.addItems(get_content_combo_name_async("instant_draw_settings", "animation_color_theme"))
        self.animation_color_theme_combo.setCurrentIndex(readme_settings_async("instant_draw_settings", "animation_color_theme"))
        self.animation_color_theme_combo.currentIndexChanged.connect(lambda: update_settings("instant_draw_settings", "animation_color_theme", self.animation_color_theme_combo.currentIndex()))

        # 结果颜色主题下拉框
        self.result_color_theme_combo = ComboBox()
        self.result_color_theme_combo.addItems(get_content_combo_name_async("instant_draw_settings", "result_color_theme"))
        self.result_color_theme_combo.setCurrentIndex(readme_settings_async("instant_draw_settings", "result_color_theme"))
        self.result_color_theme_combo.currentIndexChanged.connect(lambda: update_settings("instant_draw_settings", "result_color_theme", self.result_color_theme_combo.currentIndex()))

        # 动画固定颜色
        self.animation_fixed_color_button = ColorConfigItem("Theme", "Color", readme_settings_async("instant_draw_settings", "animation_fixed_color"))
        self.animation_fixed_color_button.valueChanged.connect(lambda color: update_settings("instant_draw_settings", "animation_fixed_color", color.name()))

        # 结果固定颜色
        self.result_fixed_color_button = ColorConfigItem("Theme", "Color", readme_settings_async("instant_draw_settings", "result_fixed_color"))
        self.result_fixed_color_button.valueChanged.connect(lambda color: update_settings("instant_draw_settings", "result_fixed_color", color.name()))

        # 添加设置项到分组
        self.addGroup(get_theme_icon("ic_fluent_color_20_filled"),
                        get_content_name_async("instant_draw_settings", "animation_color_theme"), get_content_description_async("instant_draw_settings", "animation_color_theme"), self.animation_color_theme_combo)
        self.addGroup(get_theme_icon("ic_fluent_color_20_filled"),
                        get_content_name_async("instant_draw_settings", "result_color_theme"), get_content_description_async("instant_draw_settings", "result_color_theme"), self.result_color_theme_combo)

        self.animationColorCard = ColorSettingCard(
            self.animation_fixed_color_button,
            get_theme_icon("ic_fluent_text_color_20_filled"),
            self.tr(get_content_name_async("instant_draw_settings", "animation_fixed_color")),
            self.tr(get_content_description_async("instant_draw_settings", "animation_fixed_color")),
            self
        )
        self.resultColorCard = ColorSettingCard(
            self.result_fixed_color_button,
            get_theme_icon("ic_fluent_text_color_20_filled"),
            self.tr(get_content_name_async("instant_draw_settings", "result_fixed_color")),
            self.tr(get_content_description_async("instant_draw_settings", "result_fixed_color")),
            self
        )

        self.vBoxLayout.addWidget(self.animationColorCard)
        self.vBoxLayout.addWidget(self.resultColorCard)

class instant_draw_student_image_settings(GroupHeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(get_content_name_async("instant_draw_settings", "student_image_settings"))
        self.setBorderRadius(8)

        # 学生图片开关
        self.student_image_switch = SwitchButton()
        self.student_image_switch.setOffText(get_content_switchbutton_name_async("instant_draw_settings", "student_image", "disable"))
        self.student_image_switch.setOnText(get_content_switchbutton_name_async("instant_draw_settings", "student_image", "enable"))
        self.student_image_switch.setChecked(readme_settings_async("instant_draw_settings", "student_image"))
        self.student_image_switch.checkedChanged.connect(lambda: update_settings("instant_draw_settings", "student_image", self.student_image_switch.isChecked()))

        # 打开学生图片文件夹按钮
        self.open_student_image_folder_button = PushButton(get_content_name_async("instant_draw_settings", "open_student_image_folder"))
        self.open_student_image_folder_button.clicked.connect(lambda: self.open_student_image_folder())

        # 添加设置项到分组
        self.addGroup(get_theme_icon("ic_fluent_image_circle_20_filled"),
                        get_content_name_async("instant_draw_settings", "student_image"), get_content_description_async("instant_draw_settings", "student_image"), self.student_image_switch)
        self.addGroup(get_theme_icon("ic_fluent_folder_open_20_filled"),
                        get_content_name_async("instant_draw_settings", "open_student_image_folder"), get_content_description_async("instant_draw_settings", "open_student_image_folder"), self.open_student_image_folder_button)

    def open_student_image_folder(self):
        """打开学生图片文件夹"""
        folder_path = get_resources_path(STUDENT_IMAGE_FOLDER)
        if not folder_path.exists():
            os.makedirs(folder_path, exist_ok=True)
        if folder_path:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder_path)))
        else:
            logger.error("无法获取学生图片文件夹路径")

class instant_draw_music_settings(GroupHeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(get_content_name_async("instant_draw_settings", "music_settings"))
        self.setBorderRadius(8)

        # 动画音乐开关
        self.animation_music_switch = SwitchButton()
        self.animation_music_switch.setOffText(get_content_switchbutton_name_async("instant_draw_settings", "animation_music", "disable"))
        self.animation_music_switch.setOnText(get_content_switchbutton_name_async("instant_draw_settings", "animation_music", "enable"))
        self.animation_music_switch.setChecked(readme_settings_async("instant_draw_settings", "animation_music"))
        self.animation_music_switch.checkedChanged.connect(lambda: update_settings("instant_draw_settings", "animation_music", self.animation_music_switch.isChecked()))

        # 结果音乐开关
        self.result_music_switch = SwitchButton()
        self.result_music_switch.setOffText(get_content_switchbutton_name_async("instant_draw_settings", "result_music", "disable"))
        self.result_music_switch.setOnText(get_content_switchbutton_name_async("instant_draw_settings", "result_music", "enable"))
        self.result_music_switch.setChecked(readme_settings_async("instant_draw_settings", "result_music"))
        self.result_music_switch.checkedChanged.connect(lambda: update_settings("instant_draw_settings", "result_music", self.result_music_switch.isChecked()))

        # 动画音乐文件夹按钮
        self.open_animation_music_folder_button = PushButton(get_content_name_async("instant_draw_settings", "open_animation_music_folder"))
        self.open_animation_music_folder_button.clicked.connect(lambda: self.open_animation_music_folder())

        # 结果音乐文件夹按钮
        self.open_result_music_folder_button = PushButton(get_content_name_async("instant_draw_settings", "open_result_music_folder"))
        self.open_result_music_folder_button.clicked.connect(lambda: self.open_result_music_folder())

        # 动画音乐音量
        self.animation_music_volume_spin = SpinBox()
        self.animation_music_volume_spin.setFixedWidth(WIDTH_SPINBOX)
        self.animation_music_volume_spin.setRange(0, 100)
        self.animation_music_volume_spin.setSuffix("%")
        self.animation_music_volume_spin.setValue(readme_settings_async("instant_draw_settings", "animation_music_volume"))
        self.animation_music_volume_spin.valueChanged.connect(lambda: update_settings("instant_draw_settings", "animation_music_volume", self.animation_music_volume_spin.value()))

        # 结果音乐音量
        self.result_music_volume_spin = SpinBox()
        self.result_music_volume_spin.setFixedWidth(WIDTH_SPINBOX)
        self.result_music_volume_spin.setRange(0, 100)
        self.result_music_volume_spin.setSuffix("%")
        self.result_music_volume_spin.setValue(readme_settings_async("instant_draw_settings", "result_music_volume"))
        self.result_music_volume_spin.valueChanged.connect(lambda: update_settings("instant_draw_settings", "result_music_volume", self.result_music_volume_spin.value()))

        # 动画音乐淡入时间
        self.animation_music_fade_in_spin = SpinBox()
        self.animation_music_fade_in_spin.setFixedWidth(WIDTH_SPINBOX)
        self.animation_music_fade_in_spin.setRange(0, 1000)
        self.animation_music_fade_in_spin.setSuffix("ms")
        self.animation_music_fade_in_spin.setValue(readme_settings_async("instant_draw_settings", "animation_music_fade_in"))
        self.animation_music_fade_in_spin.valueChanged.connect(lambda: update_settings("instant_draw_settings", "animation_music_fade_in", self.animation_music_fade_in_spin.value()))

        # 结果音乐淡入时间
        self.result_music_fade_in_spin = SpinBox()
        self.result_music_fade_in_spin.setFixedWidth(WIDTH_SPINBOX)
        self.result_music_fade_in_spin.setRange(0, 1000)
        self.result_music_fade_in_spin.setSuffix("ms")
        self.result_music_fade_in_spin.setValue(readme_settings_async("instant_draw_settings", "result_music_fade_in"))
        self.result_music_fade_in_spin.valueChanged.connect(lambda: update_settings("instant_draw_settings", "result_music_fade_in", self.result_music_fade_in_spin.value()))

        # 动画音乐淡出时间
        self.animation_music_fade_out_spin = SpinBox()
        self.animation_music_fade_out_spin.setFixedWidth(WIDTH_SPINBOX)
        self.animation_music_fade_out_spin.setRange(0, 1000)
        self.animation_music_fade_out_spin.setSuffix("ms")
        self.animation_music_fade_out_spin.setValue(readme_settings_async("instant_draw_settings", "animation_music_fade_out"))
        self.animation_music_fade_out_spin.valueChanged.connect(lambda: update_settings("instant_draw_settings", "animation_music_fade_out", self.animation_music_fade_out_spin.value()))

        # 结果音乐淡出时间
        self.result_music_fade_out_spin = SpinBox()
        self.result_music_fade_out_spin.setFixedWidth(WIDTH_SPINBOX)
        self.result_music_fade_out_spin.setRange(0, 1000)
        self.result_music_fade_out_spin.setSuffix("ms")
        self.result_music_fade_out_spin.setValue(readme_settings_async("instant_draw_settings", "result_music_fade_out"))
        self.result_music_fade_out_spin.valueChanged.connect(lambda: update_settings("instant_draw_settings", "result_music_fade_out", self.result_music_fade_out_spin.value()))

        # 添加设置项到分组
        self.addGroup(get_theme_icon("ic_fluent_music_note_2_20_filled"),
                        get_content_name_async("instant_draw_settings", "animation_music"), get_content_description_async("instant_draw_settings", "animation_music"), self.animation_music_switch)
        self.addGroup(get_theme_icon("ic_fluent_music_note_2_20_filled"),
                        get_content_name_async("instant_draw_settings", "result_music"), get_content_description_async("instant_draw_settings", "result_music"), self.result_music_switch)
        self.addGroup(get_theme_icon("ic_fluent_folder_open_20_filled"),
                        get_content_name_async("instant_draw_settings", "open_animation_music_folder"), get_content_description_async("instant_draw_settings", "open_animation_music_folder"), self.open_animation_music_folder_button)
        self.addGroup(get_theme_icon("ic_fluent_folder_open_20_filled"),
                        get_content_name_async("instant_draw_settings", "open_result_music_folder"), get_content_description_async("instant_draw_settings", "open_result_music_folder"), self.open_result_music_folder_button)
        self.addGroup(get_theme_icon("ic_fluent_speaker_2_20_filled"),
                        get_content_name_async("instant_draw_settings", "animation_music_volume"), get_content_description_async("instant_draw_settings", "animation_music_volume"), self.animation_music_volume_spin)
        self.addGroup(get_theme_icon("ic_fluent_speaker_2_20_filled"),
                        get_content_name_async("instant_draw_settings", "result_music_volume"), get_content_description_async("instant_draw_settings", "result_music_volume"), self.result_music_volume_spin)
        self.addGroup(get_theme_icon("ic_fluent_arrow_up_20_filled"),
                        get_content_name_async("instant_draw_settings", "animation_music_fade_in"), get_content_description_async("instant_draw_settings", "animation_music_fade_in"), self.animation_music_fade_in_spin)
        self.addGroup(get_theme_icon("ic_fluent_arrow_up_20_filled"),
                        get_content_name_async("instant_draw_settings", "result_music_fade_in"), get_content_description_async("instant_draw_settings", "result_music_fade_in"), self.result_music_fade_in_spin)
        self.addGroup(get_theme_icon("ic_fluent_arrow_down_20_filled"),
                        get_content_name_async("instant_draw_settings", "animation_music_fade_out"), get_content_description_async("instant_draw_settings", "animation_music_fade_out"), self.animation_music_fade_out_spin)
        self.addGroup(get_theme_icon("ic_fluent_arrow_down_20_filled"),
                        get_content_name_async("instant_draw_settings", "result_music_fade_out"), get_content_description_async("instant_draw_settings", "result_music_fade_out"), self.result_music_fade_out_spin)

    def open_animation_music_folder(self):
        """打开动画音乐文件夹"""
        folder_path = get_resources_path(ANIMATION_MUSIC_FOLDER)
        if not folder_path.exists():
            os.makedirs(folder_path)
        if folder_path:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder_path)))
        else:
            logger.error("无法获取动画音乐文件夹路径")

    def open_result_music_folder(self):
        """打开结果音乐文件夹"""
        folder_path = get_resources_path(RESULT_MUSIC_FOLDER)
        if not folder_path.exists():
            os.makedirs(folder_path)
        if folder_path:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder_path)))
        else:
            logger.error("无法获取结果音乐文件夹路径")
