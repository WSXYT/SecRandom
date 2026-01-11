# ==================================================
# 导入库
# ==================================================

from PySide6.QtCore import QTimer, Signal, QObject
from loguru import logger

from app.common.data.list import *
from app.common.display.result_display import *
from app.common.history import *
from app.tools.settings_access import *
from app.common.music.music_player import music_player
from app.common.roll_call.roll_call_utils import RollCallUtils
from app.Language.obtain_language import get_content_combo_name_async


# ==================================================
# 闪抽动画类
# ==================================================
class QuickDrawAnimation(QObject):
    """闪抽动画类，封装闪抽动画逻辑"""

    # 动画完成信号
    animation_finished = Signal()

    def __init__(self, roll_call_widget):
        """初始化闪抽动画类

        Args:
            roll_call_widget: 点名控件实例
        """
        super().__init__()
        self.roll_call_widget = roll_call_widget
        self.is_animating = False
        self.animation_timer = None
        self.final_selected_students = None
        self.final_class_name = None
        self.final_selected_students_dict = None
        self.final_group_filter = None
        self.final_gender_filter = None

    def start_animation(self, quick_draw_settings):
        """开始闪抽动画

        Args:
            quick_draw_settings: 闪抽设置字典
        """
        logger.debug(f"start_animation: 开始闪抽动画，设置: {quick_draw_settings}")

        self.roll_call_widget.is_quick_draw = True

        class_name = readme_settings_async("quick_draw_settings", "default_class")
        group_index = 0
        group_filter = get_content_combo_name_async("roll_call", "range_combobox")[
            group_index
        ]
        gender_index = 0
        gender_filter = get_content_combo_name_async("roll_call", "gender_combobox")[
            gender_index
        ]
        current_count = readme_settings_async("quick_draw_settings", "draw_count")
        half_repeat = readme_settings_async("quick_draw_settings", "half_repeat")

        animation_music = readme_settings_async(
            "quick_draw_settings", "animation_music"
        )
        if animation_music:
            music_player.play_music(
                music_file=animation_music,
                settings_group="quick_draw_settings",
                loop=True,
                fade_in=True,
            )

        animation_mode = quick_draw_settings["animation"]
        animation_interval = quick_draw_settings["animation_interval"]
        autoplay_count = quick_draw_settings["autoplay_count"]

        if animation_mode == 1:
            logger.debug(
                f"start_animation: 自动停止模式，动画间隔: {animation_interval}ms, 运行次数: {autoplay_count}"
            )
            self.is_animating = True
            self.animation_timer = QTimer()
            self.animation_timer.timeout.connect(self._animate_result)
            self.animation_timer.start(animation_interval)
            QTimer.singleShot(
                autoplay_count * animation_interval,
                lambda: [
                    self.stop_animation(),
                    self.animation_timer.stop(),
                ],
            )
        elif animation_mode == 2:
            logger.debug("start_animation: 无动画模式，直接停止动画")
            self.stop_animation()

    def stop_animation(self):
        """停止闪抽动画"""
        logger.debug("stop_animation: 停止闪抽动画")
        self.is_animating = False
        self.roll_call_widget.is_quick_draw = False

        from app.common.behind_scenes.behind_scenes_utils import BehindScenesUtils

        BehindScenesUtils.clear_cache()

        music_player.stop_music(fade_out=True)

        result_music = readme_settings_async("quick_draw_settings", "result_music")
        if result_music:
            music_player.play_music(
                music_file=result_music,
                settings_group="quick_draw_settings",
                loop=False,
                fade_in=True,
            )

        # 动画完成后，更新浮窗通知并启动自动关闭定时器
        if self.final_selected_students and self.final_class_name:
            draw_count = readme_settings_async("quick_draw_settings", "draw_count")
            RollCallUtils.show_notification_if_enabled(
                class_name=self.final_class_name,
                selected_students=self.final_selected_students,
                draw_count=draw_count,
                settings_group="quick_draw_notification_settings",
                display_settings=self.quick_draw_settings,
                is_animating=False,
            )

        self.animation_finished.emit()

    def _animate_result(self):
        """动画过程中更新显示"""
        self.draw_random_students()

        draw_count = readme_settings_async("quick_draw_settings", "draw_count")
        self.display_result_animated(
            self.final_selected_students,
            self.final_class_name,
            self.quick_draw_settings,
            draw_count,
        )

        # 更新浮窗通知
        self._update_floating_notification()

    def is_animation_active(self):
        """检查动画是否正在运行

        Returns:
            bool: 动画是否正在运行
        """
        return self.is_animating

    def draw_random_students(self):
        """独立的随机学生抽取逻辑，不依赖roll_call_widget的状态"""
        class_name = readme_settings_async("quick_draw_settings", "default_class")
        if not class_name:
            logger.exception("draw_random_students: 未设置默认抽取名单")
            return False

        group_index = 0
        group_filter = get_content_combo_name_async("roll_call", "range_combobox")[
            group_index
        ]
        gender_index = 0
        gender_filter = get_content_combo_name_async("roll_call", "gender_combobox")[
            gender_index
        ]
        current_count = readme_settings_async("quick_draw_settings", "draw_count")
        half_repeat = readme_settings_async("quick_draw_settings", "half_repeat")

        result = RollCallUtils.draw_random_students(
            class_name,
            group_index,
            group_filter,
            gender_index,
            gender_filter,
            current_count,
            half_repeat,
        )

        if "reset_required" in result and result["reset_required"]:
            RollCallUtils.reset_drawn_records(
                self.roll_call_widget, class_name, gender_filter, group_filter
            )
            return False

        # 保存抽取结果
        self.final_selected_students = result["selected_students"]
        self.final_class_name = result["class_name"]
        self.final_selected_students_dict = result["selected_students_dict"]
        self.final_group_filter = result["group_filter"]
        self.final_gender_filter = result["gender_filter"]

        # 同时更新roll_call_widget的结果（用于显示）
        self.roll_call_widget.final_selected_students = self.final_selected_students
        self.roll_call_widget.final_class_name = self.final_class_name
        self.roll_call_widget.final_selected_students_dict = (
            self.final_selected_students_dict
        )
        self.roll_call_widget.final_group_filter = self.final_group_filter
        self.roll_call_widget.final_gender_filter = self.final_gender_filter

        return True

    def execute_quick_draw(self, quick_draw_settings):
        """执行完整的闪抽流程

        Args:
            quick_draw_settings: 闪抽设置字典
        """
        logger.debug("execute_quick_draw: 执行完整闪抽流程")

        # 保存闪抽设置，用于动画过程中更新显示和浮窗通知
        self.quick_draw_settings = quick_draw_settings

        try:
            self.animation_finished.connect(
                lambda: self.display_final_result(quick_draw_settings)
            )

            # 根据动画模式执行不同逻辑
            animation_mode = quick_draw_settings["animation"]

            if animation_mode in [0, 1]:
                # 有动画模式，启动动画
                self.start_animation(quick_draw_settings)
            else:
                # 无动画模式，直接抽取
                self.roll_call_widget.is_quick_draw = True
                # 使用独立的抽取逻辑
                success = self.draw_random_students()
                if success:
                    # 使用闪抽设置更新显示结果
                    self.roll_call_widget.display_result(
                        self.final_selected_students,
                        self.final_class_name,
                        quick_draw_settings,
                    )
                self.roll_call_widget.is_quick_draw = False
                self.animation_finished.emit()

        except Exception as e:
            logger.exception(f"execute_quick_draw: 执行闪抽流程失败: {e}")
            self.stop_animation()

    def display_final_result(self, quick_draw_settings):
        """显示最终的闪抽结果

        Args:
            quick_draw_settings: 闪抽设置字典
        """
        try:
            if self.final_selected_students and self.final_class_name:
                draw_count = readme_settings_async("quick_draw_settings", "draw_count")

                RollCallUtils.display_result(
                    result_grid=self.roll_call_widget.result_grid,
                    class_name=self.final_class_name,
                    selected_students=self.final_selected_students,
                    draw_count=draw_count,
                    group_index=0,
                    settings_group="quick_draw_settings",
                    display_settings=quick_draw_settings,
                )

                self._record_drawn_student(quick_draw_settings)

                self.roll_call_widget.update_many_count_label()

                from app.tools.variable import APP_INIT_DELAY
                from PySide6.QtCore import QTimer

                QTimer.singleShot(
                    APP_INIT_DELAY, self.roll_call_widget._update_remaining_list_delayed
                )

                self.roll_call_widget.play_voice_result()

                RollCallUtils.show_notification_if_enabled(
                    class_name=self.final_class_name,
                    selected_students=self.final_selected_students,
                    draw_count=draw_count,
                    settings_group="quick_draw_notification_settings",
                    display_settings=quick_draw_settings,
                )

        except Exception as e:
            logger.exception(f"display_final_result: 显示最终结果失败: {e}")

    def _record_drawn_student(self, quick_draw_settings):
        """记录已抽取的学生

        Args:
            quick_draw_settings: 闪抽设置字典
        """
        try:
            half_repeat = quick_draw_settings.get("half_repeat", 0)

            RollCallUtils.record_drawn_students(
                class_name=self.final_class_name,
                selected_students=self.final_selected_students,
                selected_students_dict=self.final_selected_students_dict,
                gender_filter=self.final_gender_filter,
                group_filter=self.final_group_filter,
                half_repeat=half_repeat,
            )

        except Exception as e:
            logger.exception(f"_record_drawn_student: 记录已抽取学生失败: {e}")

    def _update_floating_notification(self):
        """更新浮窗通知内容

        在动画过程中实时更新浮窗通知的内容
        """
        try:
            if self.final_selected_students and self.final_class_name:
                draw_count = readme_settings_async("quick_draw_settings", "draw_count")

                RollCallUtils.show_notification_if_enabled(
                    class_name=self.final_class_name,
                    selected_students=self.final_selected_students,
                    draw_count=draw_count,
                    settings_group="quick_draw_notification_settings",
                    display_settings=self.quick_draw_settings,
                    is_animating=True,
                )

        except Exception as e:
            logger.exception(f"_update_floating_notification: 更新浮窗通知失败: {e}")

    def display_result_animated(
        self, selected_students, class_name, display_settings, draw_count
    ):
        """动画过程中显示结果

        Args:
            selected_students: 选中的学生列表
            class_name: 班级名称
            display_settings: 显示设置字典
            draw_count: 抽取人数
        """
        student_labels = ResultDisplayUtils.create_student_label(
            class_name=class_name,
            selected_students=selected_students,
            draw_count=draw_count,
            font_size=display_settings["font_size"],
            animation_color=display_settings["animation_color_theme"],
            display_format=display_settings["display_format"],
            show_student_image=display_settings["student_image"],
            group_index=0,
            show_random=display_settings["show_random"],
            settings_group="quick_draw_settings",
        )

        ResultDisplayUtils.display_results_in_grid(
            self.roll_call_widget.result_grid, student_labels
        )
