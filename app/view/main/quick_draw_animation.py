# ==================================================
# 导入库
# ==================================================

from PySide6.QtCore import QTimer, Signal, QObject
from loguru import logger

from app.common.data.list import *
from app.common.display.result_display import *
from app.common.history.history import *
from app.tools.settings_access import *
from app.common.music.music_player import music_player
from app.common.roll_call.roll_call_utils import RollCallUtils


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

        self.is_animating = True

        # 设置闪抽模式标志，避免stop_animation方法覆盖闪抽结果
        self.roll_call_widget.is_quick_draw = True

        # 获取动画音乐设置
        animation_music = readme_settings_async(
            "quick_draw_settings", "animation_music"
        )
        if animation_music:
            # 播放动画音乐
            music_player.play_music(
                music_file=animation_music,
                settings_group="quick_draw_settings",
                loop=True,
                fade_in=True,
            )

        # 根据动画模式选择不同的实现方式
        animation_mode = quick_draw_settings["animation"]
        animation_interval = quick_draw_settings["animation_interval"]
        autoplay_count = quick_draw_settings["autoplay_count"]

        # 创建动画定时器
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._animate_result)
        self.animation_timer.start(animation_interval)

        if animation_mode == 0:  # 手动停止模式（虽然也没有这个了）
            # 这种模式下，动画会一直运行，直到调用stop_animation
            logger.debug(
                f"start_animation: 手动停止模式，动画间隔: {animation_interval}ms"
            )
        elif animation_mode == 1:  # 自动停止模式
            # 这种模式下，动画会运行指定次数后自动停止
            logger.debug(
                f"start_animation: 自动停止模式，动画间隔: {animation_interval}ms, 运行次数: {autoplay_count}"
            )
            QTimer.singleShot(
                autoplay_count * animation_interval, lambda: self.stop_animation()
            )
        elif animation_mode == 2:  # 无动画模式
            # 这种模式下，直接停止动画
            logger.debug("start_animation: 无动画模式，直接停止动画")
            self.stop_animation()

    def stop_animation(self):
        """停止闪抽动画"""
        logger.debug("stop_animation: 停止闪抽动画")

        if (
            self.is_animating
            and self.animation_timer
            and self.animation_timer.isActive()
        ):
            self.animation_timer.stop()
            self.is_animating = False

            # 停止动画音乐
            music_player.stop_music(fade_out=True)

            # 播放结果音乐
            result_music = readme_settings_async("quick_draw_settings", "result_music")
            if result_music:
                music_player.play_music(
                    music_file=result_music,
                    settings_group="quick_draw_settings",
                    loop=False,
                    fade_in=True,
                )

            # 移除闪抽模式标志
            self.roll_call_widget.is_quick_draw = False

            # 发出动画完成信号
            self.animation_finished.emit()

    def _animate_result(self):
        """动画过程中更新显示"""
        if self.is_animating:
            # 使用独立的抽取逻辑更新结果
            self.draw_random_students()

            # 使用闪抽设置更新显示结果
            if self.final_selected_students and self.final_class_name:
                self.roll_call_widget.display_result(
                    self.final_selected_students,
                    self.final_class_name,
                    self.quick_draw_settings,
                )

            # 同时更新浮窗通知内容
            self._update_floating_notification()

    def is_animation_active(self):
        """检查动画是否正在运行

        Returns:
            bool: 动画是否正在运行
        """
        return self.is_animating

    def draw_random_students(self):
        """独立的随机学生抽取逻辑，不依赖roll_call_widget的状态"""
        # 从设置中读取默认抽取名单
        class_name = readme_settings_async("quick_draw_settings", "default_class")
        if not class_name:
            logger.error("draw_random_students: 未设置默认抽取名单")
            return False

        # 设置范围为"抽取全部学生"（索引0）
        group_index = 0
        group_filter = get_content_combo_name_async("roll_call", "range_combobox")[
            group_index
        ]

        # 设置性别为"抽取全部性别"（索引0）
        gender_index = 0
        gender_filter = get_content_combo_name_async("roll_call", "gender_combobox")[
            gender_index
        ]

        # 从闪抽设置中读取抽取人数
        current_count = readme_settings_async("quick_draw_settings", "draw_count")

        # 从闪抽设置中读取半重复设置
        half_repeat = readme_settings_async("quick_draw_settings", "half_repeat")

        logger.debug(
            f"draw_random_students: 班级={class_name}, 范围={group_filter}, 性别={gender_filter}, 数量={current_count}"
        )

        # 使用工具类抽取随机学生
        result = RollCallUtils.draw_random_students(
            class_name,
            group_index,
            group_filter,
            gender_index,
            gender_filter,
            current_count,
            half_repeat,
        )

        # 处理需要重置的情况
        if "reset_required" in result and result["reset_required"]:
            RollCallUtils.reset_drawn_records(
                self.roll_call_widget, class_name, gender_filter, group_filter
            )
            logger.debug("draw_random_students: 已重置抽取记录")
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

        logger.debug(
            f"draw_random_students: 抽取成功，结果: {self.final_selected_students}"
        )
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
            logger.error(f"execute_quick_draw: 执行闪抽流程失败: {e}")
            self.stop_animation()

    def display_final_result(self, quick_draw_settings):
        """显示最终的闪抽结果

        Args:
            quick_draw_settings: 闪抽设置字典
        """
        logger.debug("display_final_result: 显示最终闪抽结果")

        try:
            # 检查是否有抽取结果
            if self.final_selected_students and self.final_class_name:
                # 从闪抽设置中读取抽取人数
                draw_count = readme_settings_async("quick_draw_settings", "draw_count")

                # 使用闪抽设置重新显示结果
                student_labels = ResultDisplayUtils.create_student_label(
                    class_name=self.final_class_name,
                    selected_students=self.final_selected_students,
                    draw_count=draw_count,
                    font_size=quick_draw_settings["font_size"],
                    animation_color=quick_draw_settings["animation_color_theme"],
                    display_format=quick_draw_settings["display_format"],
                    show_student_image=quick_draw_settings["student_image"],
                    group_index=0,
                    show_random=quick_draw_settings["show_random"],
                    settings_group="quick_draw_settings",
                )
                ResultDisplayUtils.display_results_in_grid(
                    self.roll_call_widget.result_grid, student_labels
                )

                # 记录已抽取学生
                self._record_drawn_student(quick_draw_settings)

                # 更新剩余人数显示
                self.roll_call_widget.update_many_count_label()

                # 更新剩余名单窗口
                from app.tools.variable import APP_INIT_DELAY
                from PySide6.QtCore import QTimer

                QTimer.singleShot(
                    APP_INIT_DELAY, self.roll_call_widget._update_remaining_list_delayed
                )

                # 播放语音
                self.roll_call_widget.play_voice_result()

                # 使用闪抽通知设置显示通知
                call_notification_service = readme_settings_async(
                    "quick_draw_notification_settings", "call_notification_service"
                )
                if call_notification_service:
                    # 准备通知设置
                    settings = {
                        "animation": readme_settings_async(
                            "quick_draw_notification_settings", "animation"
                        ),
                        "window_position": readme_settings_async(
                            "quick_draw_notification_settings",
                            "floating_window_position",
                        ),
                        "horizontal_offset": readme_settings_async(
                            "quick_draw_notification_settings",
                            "floating_window_horizontal_offset",
                        ),
                        "vertical_offset": readme_settings_async(
                            "quick_draw_notification_settings",
                            "floating_window_vertical_offset",
                        ),
                        "transparency": readme_settings_async(
                            "quick_draw_notification_settings",
                            "floating_window_transparency",
                        ),
                        "auto_close_time": readme_settings_async(
                            "quick_draw_notification_settings",
                            "floating_window_auto_close_time",
                        ),
                        "enabled_monitor": readme_settings_async(
                            "quick_draw_notification_settings",
                            "floating_window_enabled_monitor",
                        ),
                        "font_size": quick_draw_settings["font_size"],
                        "animation_color_theme": quick_draw_settings[
                            "animation_color_theme"
                        ],
                        "display_format": quick_draw_settings["display_format"],
                        "student_image": quick_draw_settings["student_image"],
                        "show_random": quick_draw_settings["show_random"],
                    }

                    # 使用ResultDisplayUtils显示通知
                    ResultDisplayUtils.show_notification_if_enabled(
                        self.final_class_name,
                        self.final_selected_students,
                        draw_count,
                        settings,
                        settings_group="quick_draw_notification_settings",
                    )

        except Exception as e:
            logger.error(f"display_final_result: 显示最终结果失败: {e}")

    def _record_drawn_student(self, quick_draw_settings):
        """记录已抽取的学生

        Args:
            quick_draw_settings: 闪抽设置字典
        """
        logger.debug("_record_drawn_student: 记录已抽取的学生")

        try:
            # 检查是否需要记录已抽取学生（半重复设置大于0）
            half_repeat = quick_draw_settings.get("half_repeat", 0)
            if half_repeat > 0:
                # 使用原有的记录方法
                from app.tools.config import record_drawn_student

                record_drawn_student(
                    class_name=self.final_class_name,
                    gender=self.final_gender_filter,
                    group=self.final_group_filter,
                    student_name=self.final_selected_students,
                )

            # 使用save_roll_call_history记录历史
            if self.final_selected_students_dict:
                selected_students_dict = self.final_selected_students_dict
                # 保存历史记录
                save_roll_call_history(
                    class_name=self.final_class_name,
                    selected_students=selected_students_dict,
                    group_filter=self.final_group_filter,
                    gender_filter=self.final_gender_filter,
                )

        except Exception as e:
            logger.error(f"_record_drawn_student: 记录已抽取学生失败: {e}")

    def _update_floating_notification(self):
        """更新浮窗通知内容

        在动画过程中实时更新浮窗通知的内容
        """
        try:
            # 检查是否启用了通知服务
            call_notification_service = readme_settings_async(
                "quick_draw_notification_settings", "call_notification_service"
            )

            if call_notification_service:
                # 检查是否有抽取结果
                if self.final_selected_students and self.final_class_name:
                    # 从闪抽设置中读取抽取人数
                    draw_count = readme_settings_async(
                        "quick_draw_settings", "draw_count"
                    )

                    # 准备通知设置
                    settings = {
                        "animation": readme_settings_async(
                            "quick_draw_notification_settings", "animation"
                        ),
                        "window_position": readme_settings_async(
                            "quick_draw_notification_settings",
                            "floating_window_position",
                        ),
                        "horizontal_offset": readme_settings_async(
                            "quick_draw_notification_settings",
                            "floating_window_horizontal_offset",
                        ),
                        "vertical_offset": readme_settings_async(
                            "quick_draw_notification_settings",
                            "floating_window_vertical_offset",
                        ),
                        "transparency": readme_settings_async(
                            "quick_draw_notification_settings",
                            "floating_window_transparency",
                        ),
                        "auto_close_time": readme_settings_async(
                            "quick_draw_notification_settings",
                            "floating_window_auto_close_time",
                        ),
                        "enabled_monitor": readme_settings_async(
                            "quick_draw_notification_settings",
                            "floating_window_enabled_monitor",
                        ),
                        "font_size": self.quick_draw_settings["font_size"],
                        "animation_color_theme": self.quick_draw_settings[
                            "animation_color_theme"
                        ],
                        "display_format": self.quick_draw_settings["display_format"],
                        "student_image": self.quick_draw_settings["student_image"],
                        "show_random": self.quick_draw_settings["show_random"],
                    }

                    # 使用ResultDisplayUtils显示通知
                    from app.common.display.result_display import ResultDisplayUtils

                    ResultDisplayUtils.show_notification_if_enabled(
                        self.final_class_name,
                        self.final_selected_students,
                        draw_count,
                        settings,
                        settings_group="quick_draw_notification_settings",
                    )

        except Exception as e:
            logger.error(f"_update_floating_notification: 更新浮窗通知失败: {e}")
