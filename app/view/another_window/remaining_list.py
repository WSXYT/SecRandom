"""
剩余名单页面
用于显示未抽取的学生名单
"""

import json
from typing import Dict, Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import (
    Signal,
    Qt,
    QTimer,
    QThread,
    QRunnable,
    QThreadPool,
    QObject,
)
from qfluentwidgets import SubtitleLabel, BodyLabel, CardWidget
from loguru import logger

from app.tools.variable import (
    STUDENT_CARD_SPACING,
    STUDENT_CARD_FIXED_WIDTH,
    STUDENT_CARD_FIXED_HEIGHT,
    STUDENT_CARD_MARGIN,
)
from app.tools.path_utils import get_data_path
from app.tools.personalised import load_custom_font
from app.Language.obtain_language import (
    get_content_name_async,
    get_any_position_value_async,
)
from app.tools.config import read_drawn_record, read_drawn_record_simple
from app.tools.variable import APP_INIT_DELAY


# 后台加载学生数据的线程
class StudentLoader(QThread):
    """在后台读取并过滤学生数据，避免阻塞 UI 线程"""

    finished = Signal(list)

    def __init__(
        self,
        students_file,
        class_name,
        group_index,
        gender_index,
        group_filter,
        gender_filter,
        half_repeat,
    ):
        super().__init__()
        self.students_file = students_file
        self.class_name = class_name
        self.group_index = group_index
        self.gender_index = gender_index
        self.group_filter = group_filter
        self.gender_filter = gender_filter
        self.half_repeat = half_repeat

    def run(self):
        try:
            # 读取文件
            with open(self.students_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 构建学生列表
            students_dict_list = []
            for name, student_data in data.items():
                student_dict = {
                    "id": student_data.get("id", ""),
                    "name": name,
                    "gender": student_data.get("gender", ""),
                    "group": student_data.get("group", ""),
                    "exist": student_data.get("exist", True),
                }
                students_dict_list.append(student_dict)

            filtered_students = students_dict_list

            # 小组筛选
            if self.group_index > 0:
                groups = set()
                for student in students_dict_list:
                    if "group" in student and student["group"]:
                        groups.add(student["group"])
                sorted_groups = sorted(list(groups))

                if self.group_index == 1:
                    group_data = {}
                    for student in students_dict_list:
                        group_name = student.get("group", "")
                        if group_name:
                            group_data.setdefault(group_name, []).append(student)
                    for group_name in group_data:
                        group_data[group_name] = sorted(
                            group_data[group_name], key=lambda x: x.get("name", "")
                        )
                    filtered_students = []
                    for group_name in sorted(group_data.keys()):
                        group_info = {
                            "id": f"GROUP_{group_name}",
                            "name": f"小组 {group_name}",
                            "gender": "",
                            "group": group_name,
                            "exist": True,
                            "is_group": True,
                            "members": group_data[group_name],
                        }
                        filtered_students.append(group_info)
                elif self.group_index > 1 and sorted_groups:
                    group_index_adjusted = self.group_index - 2
                    if 0 <= group_index_adjusted < len(sorted_groups):
                        selected_group = sorted_groups[group_index_adjusted]
                        filtered_students = [
                            student
                            for student in students_dict_list
                            if "group" in student and student["group"] == selected_group
                        ]

            # 性别筛选
            if self.gender_index > 0:
                genders = set()
                for student in filtered_students:
                    if student["gender"]:
                        genders.add(student["gender"])
                sorted_genders = sorted(list(genders))
                if self.gender_index <= len(sorted_genders):
                    selected_gender = sorted_genders[self.gender_index - 1]
                    filtered_students = [
                        s for s in filtered_students if s["gender"] == selected_gender
                    ]

            # half_repeat 过滤
            if self.half_repeat > 0:
                # 根据数据来源选择读取记录方法
                if "lottery_list" in str(self.students_file):
                    drawn_records = read_drawn_record_simple(self.class_name)
                else:
                    drawn_records = read_drawn_record(
                        self.class_name, self.gender_filter, self.group_filter
                    )
                drawn_counts = {name: count for name, count in drawn_records}
                remaining_students = []
                if self.group_index == 1:
                    for student in filtered_students:
                        if student.get("is_group", False):
                            members = student.get("members", [])
                            all_members_drawn = True
                            for member in members:
                                member_name = member["name"]
                                if (
                                    member_name not in drawn_counts
                                    or drawn_counts[member_name] < self.half_repeat
                                ):
                                    all_members_drawn = False
                                    break
                            if not all_members_drawn:
                                remaining_students.append(student)
                        else:
                            student_name = student["name"]
                            if (
                                student_name not in drawn_counts
                                or drawn_counts[student_name] < self.half_repeat
                            ):
                                remaining_students.append(student)
                else:
                    for student in filtered_students:
                        student_name = student["name"]
                        if (
                            student_name not in drawn_counts
                            or drawn_counts[student_name] < self.half_repeat
                        ):
                            remaining_students.append(student)
                filtered_students = remaining_students

            # 发送结果回主线程
            self.finished.emit(filtered_students)
        except Exception as e:
            from loguru import logger

            logger.exception("在 StudentLoader.run 中加载学生时出错: {}", e)
            # 出错时返回空列表
            try:
                self.finished.emit([])
            except Exception as inner_e:
                logger.exception(
                    "Error emitting finished signal with empty list: {}", inner_e
                )


class RemainingListPage(QWidget):
    """剩余名单页面类"""

    # 定义信号，当剩余人数变化时发出
    count_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.class_name = ""
        self.group_filter = ""
        self.gender_filter = ""
        self.half_repeat = 0
        self.group_index = 0
        self.gender_index = 0
        self.remaining_students = []

        # 布局更新状态跟踪
        self._last_layout_width = 0
        self._last_card_count = 0
        self._layout_update_in_progress = False
        self._resize_timer = None
        self._is_resizing = False

        # 缓存一些在创建大量卡片时会频繁使用的资源
        # 减少每次创建卡片时的重复开销
        try:
            self._font_family = load_custom_font()
        except Exception as e:
            from loguru import logger

            logger.exception("Failed to load custom font: {}", e)
            self._font_family = None
        # 预先设置为空；init_ui 中会尝试异步预取模板文本
        self._student_info_text = None

        # 异步渲染相关状态（使用 QThreadPool）
        self._pending_students = []
        self._batch_size = 20  # 每批创建的卡片数量
        self._rendering = False
        self._thread_pool = QThreadPool.globalInstance()
        self._render_reporter = None

        self.init_ui()

        # 延迟加载学生数据
        QTimer.singleShot(APP_INIT_DELAY, self.load_student_data)

    def stop_loader(self):
        try:
            if hasattr(self, "_loading_thread") and self._loading_thread is not None:
                try:
                    if self._loading_thread.isRunning():
                        try:
                            self._loading_thread.terminate()
                        except Exception:
                            pass
                        try:
                            self._loading_thread.wait(1000)
                        except Exception:
                            pass
                finally:
                    self._loading_thread = None
        except Exception:
            pass

    def closeEvent(self, event):
        """窗口关闭事件"""
        # 停止加载器
        try:
            self.stop_loader()
        except Exception:
            pass
        # 清理定时器
        if hasattr(self, "_resize_timer") and self._resize_timer is not None:
            self._resize_timer.stop()
            self._resize_timer = None
        super().closeEvent(event)

    def init_ui(self):
        """初始化UI"""
        # 主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # 使用异步函数获取标题文本
        title_text = get_content_name_async("remaining_list", "title")
        count_text = get_any_position_value_async(
            "remaining_list", "count_label", "name"
        )

        # 标题
        self.title_label = SubtitleLabel(title_text)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self._font_family:
            self.title_label.setFont(QFont(self._font_family, 18))
        else:
            self.title_label.setFont(QFont("", 18))
        self.main_layout.addWidget(self.title_label)

        # 剩余人数标签
        self.count_label = BodyLabel(count_text.format(count=0))
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self._font_family:
            self.count_label.setFont(QFont(self._font_family, 12))
        else:
            self.count_label.setFont(QFont("", 12))
        self.main_layout.addWidget(self.count_label)

        # 创建网格布局
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(STUDENT_CARD_SPACING)
        self.main_layout.addLayout(self.grid_layout)

        # 初始化卡片列表
        self.cards = []
        # 跟踪已添加到布局的卡片 key，防止重复添加
        self._cards_set = set()
        # 缓存所有创建过的卡片，避免在布局切换时频繁创建/销毁
        self._card_cache = {}

        # 不再使用分页，所有卡片一次性展示

        # 预取学生信息文本，避免在创建每个卡片时重复请求
        try:
            self._student_info_text = get_any_position_value_async(
                "remaining_list", "student_info", "name"
            )
        except Exception:
            self._student_info_text = "{id} {gender} {group}"

    def get_students_file(self):
        """获取学生或奖池数据文件路径"""
        roll_call_list_dir = get_data_path("list", "roll_call_list")
        lottery_list_dir = get_data_path("list/lottery_list")
        roll_file = roll_call_list_dir / f"{self.class_name}.json"
        lottery_file = lottery_list_dir / f"{self.class_name}.json"
        if roll_file.exists():
            return roll_file
        return lottery_file

    def load_student_data(self):
        """开始后台加载学生数据（非阻塞）"""
        # 如果已经有加载线程在运行，则不再重复启动
        try:
            if (
                hasattr(self, "_loading_thread")
                and self._loading_thread is not None
                and self._loading_thread.isRunning()
            ):
                try:
                    self._loading_thread.terminate()
                except Exception:
                    pass
                try:
                    self._loading_thread.wait(500)
                except Exception:
                    pass
        except Exception as e:
            from loguru import logger

            logger.exception("加载剩余名单数据时出错: {}", e)

        students_file = self.get_students_file()
        # 使用 StudentLoader 在后台处理 I/O 和筛选
        loader = StudentLoader(
            str(students_file),
            getattr(self, "class_name", ""),
            getattr(self, "group_index", 0),
            getattr(self, "gender_index", 0),
            getattr(self, "group_filter", ""),
            getattr(self, "gender_filter", ""),
            getattr(self, "half_repeat", 0),
        )

        loader.finished.connect(self._on_students_loaded)
        # 将线程引用保留在实例上，避免过早回收
        self._loading_thread = loader
        loader.start()

    def _on_students_loaded(self, students_list):
        """收到后台加载完成的学生列表并更新 UI（在主线程中执行）"""
        try:
            self.students = students_list
            # 使用QTimer将更新调度到事件循环中，保持与原有逻辑一致
            QTimer.singleShot(0, self.update_ui)
        finally:
            try:
                # 清理线程引用
                if hasattr(self, "_loading_thread"):
                    self._loading_thread = None
            except Exception as e:
                from loguru import logger

                logger.exception("Error handling student group processing: {}", e)

    def update_ui(self):
        """更新UI显示"""
        # 使用异步函数获取文本
        title_text = get_any_position_value_async(
            "remaining_list", "title_with_class", "name"
        )
        count_text = get_any_position_value_async(
            "remaining_list", "count_label", "name"
        )
        group_count_text = get_any_position_value_async(
            "remaining_list", "group_count_label", "name"
        )

        # 更新标题和人数/组数
        self.title_label.setText(title_text.format(class_name=self.class_name))

        # 检查是否显示小组
        is_showing_groups = (
            any(student.get("is_group", False) for student in self.students)
            if self.students
            else False
        )

        if is_showing_groups:
            # 显示组数
            group_count = len(self.students)
            self.count_label.setText(group_count_text.format(count=group_count))
        else:
            # 显示人数
            self.count_label.setText(count_text.format(count=len(self.students)))

        # 清空现有卡片并准备异步渲染
        self.cards = []
        self._clear_grid_layout()

        # 将待渲染学生放入队列，启动增量渲染
        self._pending_students = list(self.students) if self.students else []
        self._start_incremental_render()

    # 已移除分页功能，相关方法已删除

    def update_layout(self):
        """更新布局"""
        if not self.grid_layout or not self.cards:
            return

        # 检查是否需要更新布局
        current_width = self.width()
        current_card_count = len(self.cards)

        # 如果布局正在更新中，或者宽度和卡片数量都没有变化，则跳过更新
        if self._layout_update_in_progress or (
            current_width == self._last_layout_width
            and current_card_count == self._last_card_count
        ):
            logger.debug(
                f"跳过布局更新: 宽度={current_width}, 卡片数={current_card_count}"
            )
            return

        # 设置布局更新标志
        self._layout_update_in_progress = True
        self._last_layout_width = current_width
        self._last_card_count = current_card_count

        try:
            # 在进行大量布局变更时禁用更新，减少中间重绘导致的卡顿
            try:
                top_win = self.window()
                if top_win is not None:
                    top_win.setUpdatesEnabled(False)
            except Exception:
                top_win = None
            self.setUpdatesEnabled(False)

            # 清空现有布局
            self._clear_grid_layout()

            # 计算列数
            window_width = max(self.width(), self.sizeHint().width())
            columns = self._calculate_columns(window_width)

            # 添加卡片到网格布局
            for i, card in enumerate(self.cards):
                row = i // columns
                col = i % columns
                self.grid_layout.addWidget(card, row, col)
                # 仅在控件当前不可见时显示，避免重复触发绘制
                if not card.isVisible():
                    card.show()

            # 设置列的伸缩因子，使卡片均匀分布
            for col in range(columns):
                self.grid_layout.setColumnStretch(col, 1)

            logger.debug(
                f"布局更新完成: 宽度={window_width}, 列数={columns}, 卡片数={len(self.cards)}"
            )
        finally:
            # 清除布局更新标志
            self._layout_update_in_progress = False
            # 恢复更新
            try:
                self.setUpdatesEnabled(True)
            except Exception as e:
                from loguru import logger

                logger.exception("Error processing student in StudentLoader: {}", e)
            try:
                if top_win is not None:
                    top_win.setUpdatesEnabled(True)
            except Exception as e:
                from loguru import logger

                logger.exception(
                    "Error re-enabling updates on top window (ignored): {}", e
                )
            try:
                # 触发一次完整刷新
                self.update()
            except Exception as e:
                from loguru import logger

                logger.exception(
                    "Error calling update() after layout update (ignored): {}", e
                )

    def _calculate_columns(self, width: int) -> int:
        """根据窗口宽度和卡片尺寸动态计算列数"""
        try:
            if width <= 0:
                return 1

            # 计算可用宽度（减去左右边距）
            available_width = width - 40  # 左右各20px边距

            # 所有卡片使用相同的尺寸
            card_actual_width = STUDENT_CARD_FIXED_WIDTH + STUDENT_CARD_SPACING
            max_cols = max(1, available_width // card_actual_width)

            # 至少显示1列，且不超过一个合理上限
            return max(1, min(int(max_cols), 6))
        except Exception as e:
            from loguru import logger

            logger.exception("Error calculating columns (fallback to 1): {}", e)
            return 1

    def _start_incremental_render(self):
        """使用 QThreadPool 启动后台任务，按批准备数据并通过信号通知主线程创建控件"""
        if self._rendering:
            return

        # 准备 reporter（QObject，携带信号）
        class _BatchReporter(QObject):
            batch_ready = Signal(list)
            finished = Signal()

            def __init__(self):
                super().__init__()
                self.cancel_requested = False

        reporter = _BatchReporter()
        # 使用闭包传递 reporter，让主线程槽可以区分不同任务的批次并忽略过期批次
        reporter.batch_ready.connect(
            lambda batch, rep=reporter: self._on_batch_ready(rep, batch)
        )
        reporter.finished.connect(lambda rep=reporter: self._on_render_finished(rep))

        # 启动后台任务
        task_students = list(self._pending_students)

        class StudentRenderTask(QRunnable):
            def __init__(self, students, batch_size, reporter, info_template):
                super().__init__()
                self.students = students
                self.batch_size = batch_size
                self.reporter = reporter
                self.info_template = info_template or "{id} {gender} {group}"
                self.setAutoDelete(True)

            def run(self):
                try:
                    while self.students:
                        # 检查取消请求，若已取消则尽快退出
                        try:
                            if getattr(self.reporter, "cancel_requested", False):
                                break
                        except Exception as e:
                            from loguru import logger

                            logger.exception(
                                "Error checking reporter cancel flag (ignored): {}", e
                            )
                        batch = []
                        for _ in range(self.batch_size):
                            if not self.students:
                                break
                            student = self.students.pop(0)
                            # 在后台预格式化显示文本，减少主线程工作
                            s = dict(student)
                            try:
                                s["info_text_pre"] = self.info_template.format(
                                    id=s.get("id", ""),
                                    gender=s.get("gender", ""),
                                    group=s.get("group", ""),
                                )
                            except Exception:
                                s["info_text_pre"] = (
                                    f"{s.get('id', '')} {s.get('gender', '')} {s.get('group', '')}"
                                )

                            if s.get("is_group", False):
                                members = s.get("members", [])
                                members_names = [m.get("name", "") for m in members[:5]]
                                members_text = "、".join(members_names)
                                if len(members) > 5:
                                    members_text += f" 等{len(members) - 5}名成员"
                                s["members_text_pre"] = members_text

                            batch.append(s)
                        # 发射信号到主线程，主线程负责创建 QWidget
                        # 在发射前再次检查取消标志，避免发送过期批次
                        try:
                            if getattr(self.reporter, "cancel_requested", False):
                                break
                        except Exception as e:
                            from loguru import logger

                            logger.exception(
                                "Error checking reporter cancel flag before emit (ignored): {}",
                                e,
                            )
                        try:
                            self.reporter.batch_ready.emit(batch)
                        except Exception as e:
                            from loguru import logger

                            logger.exception(
                                "Error emitting batch_ready (ignored): {}", e
                            )
                    try:
                        self.reporter.finished.emit()
                    except Exception as e:
                        from loguru import logger

                        logger.exception("Error emitting finished (ignored): {}", e)
                except Exception as e:
                    from loguru import logger

                    logger.exception("Unhandled error in StudentRenderTask.run: {}", e)
                    try:
                        self.reporter.finished.emit()
                    except Exception as inner_e:
                        from loguru import logger

                        logger.exception(
                            "Error emitting finished after exception: {}", inner_e
                        )

        # 请求取消之前正在运行的渲染任务（如果存在）
        try:
            if self._rendering and self._render_reporter is not None:
                try:
                    self._render_reporter.cancel_requested = True
                except Exception as e:
                    from loguru import logger

                    logger.exception(
                        "Error requesting cancel on previous render reporter (ignored): {}",
                        e,
                    )
        except Exception as e:
            from loguru import logger

            logger.exception("Error in RemainingListPage initialization: {}", e)

        self._render_reporter = reporter
        task = StudentRenderTask(
            task_students, self._batch_size, reporter, self._student_info_text
        )
        self._rendering = True
        self._thread_pool.start(task)

    def _render_next_batch(self):
        # 该方法现在由后台任务通过 reporter 信号触发，已废弃
        return

    def _on_batch_ready(self, reporter, batch: list):
        """主线程槽：接收一批学生数据并创建卡片加入布局

        参数:
            reporter: 发出此批次的 reporter 对象，用于判断批次是否过期
            batch: 学生数据列表（可能包含预计算字段）
        """
        # 如果 reporter 已请求取消，则忽略此批次
        try:
            if getattr(reporter, "cancel_requested", False):
                return
        except Exception as e:
            from loguru import logger

            logger.exception(
                "Error checking reporter cancel_requested flag in _on_batch_ready (ignored): {}",
                e,
            )

        if not batch:
            return

        # 创建卡片并直接加入布局缓存（避免重复添加）
        for student in batch:
            key = student.get("name")
            if key in self._cards_set:
                # 已存在，跳过
                continue

            card = self._card_cache.get(key)
            if card is None:
                card = self.create_student_card(student)
                if card is not None:
                    self._card_cache[key] = card

            if card is not None:
                # 确保卡片不在另一个父控件下
                try:
                    if card.parent() is not None and card.parent() is not self:
                        card.setParent(None)
                except Exception as e:
                    from loguru import logger

                    logger.exception("Error resetting card parent (ignored): {}", e)

                self.cards.append(card)
                self._cards_set.add(key)

        # 将新卡片添加到布局（只放置尚未加入布局的卡片）
        try:
            columns = self._calculate_columns(
                max(self.width(), self.sizeHint().width())
            )

            for i, card in enumerate(list(self.cards)):
                # 如果卡片已经在布局中则跳过
                try:
                    if self.grid_layout.indexOf(card) != -1:
                        continue
                except Exception as e:
                    from loguru import logger

                    logger.exception(
                        "Error checking grid_layout.indexOf (ignored): {}", e
                    )

                row = i // columns
                col = i % columns

                # 如果目标格位已有其它控件，先移除避免重叠
                try:
                    existing_item = self.grid_layout.itemAtPosition(row, col)
                    if existing_item is not None:
                        existing_widget = existing_item.widget()
                        if existing_widget is not None and existing_widget is not card:
                            try:
                                self.grid_layout.removeWidget(existing_widget)
                            except Exception as e:
                                from loguru import logger

                                logger.exception(
                                    "Error removing existing widget from grid (ignored): {}",
                                    e,
                                )
                            try:
                                existing_widget.hide()
                            except Exception as e:
                                from loguru import logger

                                logger.exception(
                                    "Error hiding existing widget (ignored): {}", e
                                )
                except Exception as e:
                    from loguru import logger

                    logger.exception(
                        "Error handling existing widget in grid (ignored): {}", e
                    )

                try:
                    self.grid_layout.addWidget(card, row, col)
                    if not card.isVisible():
                        card.show()
                except Exception:
                    logger.exception("向网格添加卡片失败")

            for col in range(columns):
                self.grid_layout.setColumnStretch(col, 1)
        except Exception as e:
            from loguru import logger

            logger.exception("增量渲染时布局更新失败: {}", e)

    def _on_render_finished(self, reporter):
        """后台渲染完成后的槽，接收 reporter 用于忽略过期任务"""
        try:
            if getattr(reporter, "cancel_requested", False):
                return
        except Exception as e:
            from loguru import logger

            logger.exception(
                "Error checking reporter cancel_requested in _on_render_finished (ignored): {}",
                e,
            )

        self._rendering = False
        self._pending_students = []
        # 最后触发完整布局更新以修正位置
        QTimer.singleShot(0, self.update_layout)

    def _finalize_render(self):
        """渲染完成后的收尾工作"""
        # 停止定时器
        try:
            if self._render_timer is not None:
                self._render_timer.stop()
                self._render_timer = None
        except Exception as e:
            from loguru import logger

            logger.exception(
                "Error stopping render timer in _finalize_render (ignored): {}", e
            )

        self._rendering = False

        # 最后触发完整布局更新以修正位置
        QTimer.singleShot(0, self.update_layout)

    def _clear_grid_layout(self):
        """清空网格布局"""
        # 重置列伸缩因子
        for col in range(self.grid_layout.columnCount()):
            self.grid_layout.setColumnStretch(col, 0)

        # 移除布局中的所有项，但不要销毁控件，保留在内存中以便复用
        # 这样可以避免频繁的 setParent()/delete 操作导致的卡顿
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                try:
                    self.grid_layout.removeWidget(widget)
                except Exception as e:
                    from loguru import logger

                    logger.exception(
                        "Error removing widget from grid during clear (ignored): {}", e
                    )
                widget.hide()
        # 清空已记录的已添加卡片集合
        try:
            self._cards_set.clear()
        except Exception as e:
            from loguru import logger

            logger.exception("Error clearing cards set (ignored): {}", e)

    def create_student_card(self, student: Dict[str, Any]) -> CardWidget:
        """创建学生卡片

        Args:
            student: 学生信息字典

        Returns:
            学生卡片
        """
        # 检查是否是小组卡片
        is_group = student.get("is_group", False)

        card = CardWidget()

        # 设置卡片属性，标记是否是小组卡片
        card.setProperty("is_group", is_group)

        if is_group:
            # 小组卡片使用与学生卡片相同的宽度，但高度自适应
            card.setMinimumSize(STUDENT_CARD_FIXED_WIDTH, 0)
            card.setMaximumSize(STUDENT_CARD_FIXED_WIDTH, 500)
            layout = QVBoxLayout(card)
            layout.setContentsMargins(
                STUDENT_CARD_MARGIN,
                STUDENT_CARD_MARGIN,
                STUDENT_CARD_MARGIN,
                STUDENT_CARD_MARGIN,
            )
            layout.setSpacing(8)

            # 小组名称
            name_label = BodyLabel(student["name"])
            custom_font = load_custom_font()
            if custom_font:
                name_label.setFont(QFont(custom_font, 16, QFont.Weight.Bold))
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name_label.setWordWrap(True)  # 启用自动换行
            layout.addWidget(name_label)

            # 小组成员数量
            members = student.get("members", [])
            count_label = BodyLabel(f"成员数量: {len(members)}")
            custom_font = load_custom_font()
            if custom_font:
                count_label.setFont(QFont(custom_font, 10))
            count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(count_label)

            # 小组成员列表
            # 使用后台预计算的 members 文本（若存在）
            members_text = student.get("members_text_pre")
            if members_text is None:
                members_names = [member.get("name", "") for member in members[:5]]
                members_text = "、".join(members_names)
                if len(members) > 5:
                    members_text += f" 等{len(members) - 5}名成员"

            members_label = BodyLabel(members_text)
            custom_font = load_custom_font()
            if custom_font:
                members_label.setFont(QFont(custom_font, 9))
            members_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            members_label.setWordWrap(True)  # 启用自动换行
            layout.addWidget(members_label)
        else:
            # 普通学生卡片
            card.setFixedSize(STUDENT_CARD_FIXED_WIDTH, STUDENT_CARD_FIXED_HEIGHT)

            layout = QVBoxLayout(card)
            layout.setContentsMargins(
                STUDENT_CARD_MARGIN,
                STUDENT_CARD_MARGIN,
                STUDENT_CARD_MARGIN,
                STUDENT_CARD_MARGIN,
            )
            layout.setSpacing(5)

            # 使用后台预计算的 info 文本（若存在），否则从模板生成
            if student.get("info_text_pre") is not None:
                student_info_text = student.get("info_text_pre")
            else:
                if self._student_info_text is None:
                    try:
                        student_info_text = get_any_position_value_async(
                            "remaining_list", "student_info", "name"
                        )
                    except Exception:
                        student_info_text = "{id} {gender} {group}"
                else:
                    student_info_text = self._student_info_text
            # 学生姓名
            name_label = BodyLabel(student["name"])
            if self._font_family:
                name_label.setFont(QFont(self._font_family, 14))
            else:
                name_label.setFont(QFont("", 14))
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(name_label)

            # 学生信息
            if isinstance(student_info_text, str) and "{" in student_info_text:
                info_text = student_info_text.format(
                    id=student.get("id", ""),
                    gender=student.get("gender", ""),
                    group=student.get("group", ""),
                )
            else:
                info_text = student_info_text
            info_label = BodyLabel(info_text)
            if self._font_family:
                info_label.setFont(QFont(self._font_family, 9))
            else:
                info_label.setFont(QFont("", 9))
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(info_label)

        return card

    def _load_and_update_students(self, count=None):
        """加载学生数据并更新UI的通用方法

        Args:
            count: 剩余人数，用于特殊处理当count为0时显示所有学生
        """
        # 设置更新标志，防止递归
        self._updating = True

        try:
            # 获取学生数据
            students_file = self.get_students_file()
            with open(students_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 获取索引
            group_index = getattr(self, "group_index", 0)
            gender_index = getattr(self, "gender_index", 0)

            # 转换为字典格式
            students_dict_list = []
            for name, student_data in data.items():
                student_dict = {
                    "id": student_data.get("id", ""),
                    "name": name,
                    "gender": student_data.get("gender", ""),
                    "group": student_data.get("group", ""),
                    "exist": student_data.get("exist", True),
                }
                students_dict_list.append(student_dict)

            # 根据小组和性别筛选
            filtered_students = students_dict_list

            # 小组筛选
            if group_index > 0:
                # 获取所有可用小组
                groups = set()
                for student in students_dict_list:
                    if "group" in student and student["group"]:
                        groups.add(student["group"])

                # 排序小组列表
                sorted_groups = sorted(list(groups))

                # 处理"抽取全部小组"的情况 (group_index == 1)
                if group_index == 1:
                    # 创建小组数据结构，每个小组包含组名和成员列表
                    group_data = {}
                    for student in students_dict_list:
                        group_name = student.get("group", "")
                        if group_name:  # 只处理有组名的小组
                            if group_name not in group_data:
                                group_data[group_name] = []
                            group_data[group_name].append(student)

                    # 对每个小组内的成员按姓名排序
                    for group_name in group_data:
                        group_data[group_name] = sorted(
                            group_data[group_name], key=lambda x: x.get("name", "")
                        )

                    # 创建一个特殊的学生列表，用于显示小组信息
                    filtered_students = []
                    for group_name in sorted(group_data.keys()):
                        # 添加一个表示小组的特殊条目
                        group_info = {
                            "id": f"GROUP_{group_name}",
                            "name": f"小组 {group_name}",
                            "gender": "",
                            "group": group_name,
                            "exist": True,
                            "is_group": True,  # 标记这是一个小组
                            "members": group_data[group_name],  # 保存小组成员列表
                        }
                        filtered_students.append(group_info)
                elif group_index > 1 and sorted_groups:
                    # 选择特定小组 (索引从2开始，因为0是全部，1是全部小组)
                    group_index_adjusted = group_index - 2
                    if 0 <= group_index_adjusted < len(sorted_groups):
                        selected_group = sorted_groups[group_index_adjusted]
                        filtered_students = [
                            student
                            for student in students_dict_list
                            if "group" in student and student["group"] == selected_group
                        ]

            # 根据性别筛选
            if gender_index > 0:  # 0表示全部性别
                # 获取所有可用的性别
                genders = set()
                for student in filtered_students:
                    if student["gender"]:
                        genders.add(student["gender"])

                # 将性别转换为排序后的列表
                sorted_genders = sorted(list(genders))

                # 根据索引获取选择的性别
                if gender_index <= len(sorted_genders):
                    selected_gender = sorted_genders[gender_index - 1]
                    filtered_students = [
                        student
                        for student in filtered_students
                        if student["gender"] == selected_gender
                    ]

            # 根据half_repeat设置获取未抽取的学生
            if self.half_repeat > 0:
                # 读取已抽取记录（支持奖池）
                students_file = self.get_students_file()
                if "lottery_list" in str(students_file):
                    drawn_records = read_drawn_record_simple(self.class_name)
                else:
                    drawn_records = read_drawn_record(
                        self.class_name, self.gender_filter, self.group_filter
                    )
                drawn_counts = {name: count for name, count in drawn_records}

                # 过滤掉已抽取次数达到或超过设置值的学生
                remaining_students = []

                # 特殊处理小组模式 (group_index == 1)
                if group_index == 1:
                    # 对于小组模式，需要检查每个小组是否还有未被完全抽取的成员
                    for student in filtered_students:
                        # 只处理小组条目
                        if student.get("is_group", False):
                            group_name = student["group"]
                            members = student.get("members", [])

                            # 检查小组成员是否都已被抽取
                            all_members_drawn = True
                            for member in members:
                                member_name = member["name"]
                                # 如果有成员未被抽取或抽取次数小于设置值，则小组保留
                                if (
                                    member_name not in drawn_counts
                                    or drawn_counts[member_name] < self.half_repeat
                                ):
                                    all_members_drawn = False
                                    break

                            # 只有当小组不是所有成员都被抽取时才保留
                            if not all_members_drawn:
                                remaining_students.append(student)
                            # 如果当前剩余人数等于零，则显示所有小组
                            elif count is not None and count == 0:
                                remaining_students.append(student)
                        else:
                            # 非小组条目，按原逻辑处理
                            student_name = student["name"]
                            if (
                                student_name not in drawn_counts
                                or drawn_counts[student_name] < self.half_repeat
                            ):
                                remaining_students.append(student)
                            elif count is not None and count == 0:
                                remaining_students.append(student)
                else:
                    # 非小组模式，按原逻辑处理
                    for student in filtered_students:
                        student_name = student["name"]
                        # 如果学生未被抽取过，或者抽取次数小于设置值，则保留该学生
                        if (
                            student_name not in drawn_counts
                            or drawn_counts[student_name] < self.half_repeat
                        ):
                            remaining_students.append(student)
                        # 如果当前剩余人数等于零，则显示全部学生
                        elif count is not None and count == 0:
                            remaining_students.append(student)
            else:
                # 如果half_repeat为0，则所有学生都显示
                remaining_students = filtered_students

            self.students = remaining_students

            # 使用QTimer延迟更新UI，避免在数据处理过程中直接更新UI
            QTimer.singleShot(10, self.update_ui)
        finally:
            # 清除更新标志
            self._updating = False

    def update_remaining_list(
        self,
        class_name: str,
        group_filter: str,
        gender_filter: str,
        half_repeat: int = 0,
        group_index: int = 0,
        gender_index: int = 0,
        emit_signal: bool = True,
    ):
        """更新剩余名单

        Args:
            class_name: 班级名称
            group_filter: 分组筛选条件
            gender_filter: 性别筛选条件
            half_repeat: 重复抽取次数
            group_index: 分组索引
            gender_index: 性别索引
            emit_signal: 是否发出信号
        """
        # 更新属性
        self.class_name = class_name
        self.group_filter = group_filter
        self.gender_filter = gender_filter
        self.half_repeat = half_repeat
        self.group_index = group_index
        self.gender_index = gender_index

        # 重置布局状态，强制更新
        self._last_layout_width = 0
        self._last_card_count = 0

        # 重新加载学生数据
        self.load_student_data()

        # 如果需要发出信号，则发出count_changed信号
        if emit_signal:
            # 计算剩余人数
            remaining_count = len(self.students) if hasattr(self, "students") else 0
            self.count_changed.emit(remaining_count)

    def refresh(self):
        """刷新页面"""
        if self.class_name:
            # 重置布局状态，强制更新
            self._last_layout_width = 0
            self._last_card_count = 0
            self.load_student_data()

    def on_count_changed(self, count):
        """处理剩余人数变化的槽函数

        Args:
            count: 剩余人数
        """
        # 重新加载学生数据（使用后台加载以避免阻塞）
        # 保持 count 参数以兼容旧逻辑，如需特殊处理可扩展
        self.load_student_data()

    def resizeEvent(self, event):
        """窗口大小变化事件"""
        # 检查窗口大小是否真的改变了
        new_size = event.size()
        old_size = event.oldSize()

        # 如果窗口大小没有改变，不触发布局更新
        if new_size == old_size:
            return

        # 检查宽度是否发生了显著变化（至少变化5像素才触发布局更新）
        width_change = abs(new_size.width() - self._last_layout_width)
        if width_change < 5:
            return

        # 使用QTimer延迟布局更新，避免递归调用
        if self._resize_timer is not None:
            self._resize_timer.stop()
        self._resize_timer = QTimer()
        self._resize_timer.setSingleShot(True)
        self._resize_timer.timeout.connect(self._delayed_update_layout)
        # 增加防抖延迟，避免用户缩放窗口时频繁触发布局重排导致卡顿
        self._is_resizing = True
        self._resize_timer.start(300)
        super().resizeEvent(event)

    def _delayed_update_layout(self):
        """延迟更新布局"""
        try:
            # 调整大小已结束，清除标志
            self._is_resizing = False
            if hasattr(self, "grid_layout") and self.grid_layout is not None:
                if self.isVisible():
                    # 检查是否需要更新布局
                    current_width = self.width()
                    current_card_count = len(self.cards)

                    # 只有当宽度或卡片数量发生变化时才更新布局
                    if (
                        current_width != self._last_layout_width
                        or current_card_count != self._last_card_count
                    ):
                        self.update_layout()
                        logger.debug(
                            f"延迟布局更新完成，当前卡片数量: {len(self.cards)}"
                        )
                    else:
                        logger.debug(
                            f"跳过布局更新: 宽度={current_width}, 卡片数={current_card_count}"
                        )
        except RuntimeError as e:
            logger.error(f"延迟布局更新错误: {e}")
