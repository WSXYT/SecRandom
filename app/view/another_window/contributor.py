# ==================================================
# 导入库
# ==================================================

from loguru import logger
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from qfluentwidgets import *

from app.tools.variable import *
from app.tools.path_utils import *
from app.tools.personalised import *
from app.tools.settings_default import *
from app.tools.settings_access import *
from app.Language.obtain_language import *
from app.tools.variable import *


# ==================================================
# 贡献者页面类
# ==================================================
class contributor_page(QWidget):
    """贡献者信息页面 - 显示项目贡献者信息，采用响应式网格布局"""

    def __init__(self, parent=None):
        """初始化贡献者页面"""
        super().__init__(parent)
        self.setObjectName("contributor_page")

        # 初始化UI组件
        self._init_ui()

        # 初始化数据
        self._init_data()

        # 延迟添加贡献者卡片
        QTimer.singleShot(APP_INIT_DELAY, self.create_contributor_cards)

    def _init_ui(self):
        """初始化UI组件"""
        # 创建主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # 创建流式布局
        self.flow_layout = FlowLayout()
        self.flow_layout.setVerticalSpacing(CONTRIBUTOR_CARD_SPACING)
        self.flow_layout.setHorizontalSpacing(CONTRIBUTOR_CARD_SPACING)
        self.main_layout.addLayout(self.flow_layout)

        # 初始化卡片列表
        self.cards = []

        # 布局更新状态跟踪
        self._last_layout_width = 0
        self._last_card_count = 0
        self._layout_update_in_progress = False
        self._resize_timer = None
        self._is_resizing = False

    def _init_data(self):
        """初始化贡献者数据"""
        # 贡献者数据
        contributors = [
            {
                "name": "lzy98276",
                "role": get_any_position_value_async(
                    "about", "contributor", "contributor_role_1"
                ),
                "github": "https://github.com/lzy98276",
                "avatar": str(get_data_path("assets/contribution", "contributor1.png")),
            },
            {
                "name": "chenjintang-shrimp",
                "role": get_any_position_value_async(
                    "about", "contributor", "contributor_role_2"
                ),
                "github": "https://github.com/chenjintang-shrimp",
                "avatar": str(get_data_path("assets/contribution", "contributor2.png")),
            },
            {
                "name": "yuanbenxin",
                "role": get_any_position_value_async(
                    "about", "contributor", "contributor_role_3"
                ),
                "github": "https://github.com/yuanbenxin",
                "avatar": str(get_data_path("assets/contribution", "contributor3.png")),
            },
            {
                "name": "LeafS",
                "role": get_any_position_value_async(
                    "about", "contributor", "contributor_role_4"
                ),
                "github": "https://github.com/LeafS825",
                "avatar": str(get_data_path("assets/contribution", "contributor4.png")),
            },
            {
                "name": "QiKeZhiCao",
                "role": get_any_position_value_async(
                    "about", "contributor", "contributor_role_5"
                ),
                "github": "https://github.com/QiKeZhiCao",
                "avatar": str(get_data_path("assets/contribution", "contributor5.png")),
            },
            {
                "name": "Fox-block-offcial",
                "role": get_any_position_value_async(
                    "about", "contributor", "contributor_role_6"
                ),
                "github": "https://github.com/Fox-block-offcial",
                "avatar": str(get_data_path("assets/contribution", "contributor6.png")),
            },
            {
                "name": "Jursin",
                "role": get_any_position_value_async(
                    "about", "contributor", "contributor_role_7"
                ),
                "github": "https://github.com/jursin",
                "avatar": str(get_data_path("assets/contribution", "contributor7.png")),
            },
            {
                "name": "LHGS-github",
                "role": get_any_position_value_async(
                    "about", "contributor", "contributor_role_8"
                ),
                "github": "https://github.com/LHGS-github",
                "avatar": str(get_data_path("assets/contribution", "contributor8.png")),
            },
            {
                "name": "real01bit",
                "role": get_any_position_value_async(
                    "about", "contributor", "contributor_role_9"
                ),
                "github": "https://github.com/real01bit",
                "avatar": str(get_data_path("assets/contribution", "contributor9.png")),
            },
        ]

        # 标准化职责文本长度
        self._standardize_role_text(contributors)
        self.contributors = contributors

    def _standardize_role_text(self, contributors):
        """标准化职责文本长度，使所有职责文本行数一致"""
        # 计算所有职责文本的行数
        fm = QFontMetrics(self.font())
        max_lines = 0
        role_lines = []

        # 找出最长的职责文本有多少行
        for contributor in contributors:
            role_text = contributor["role"] or ""  # 确保role_text不为None
            contributor["role"] = role_text

            # 计算文本在MAX_ROLE_WIDTH宽度下的行数
            text_rect = fm.boundingRect(
                QRect(0, 0, CONTRIBUTOR_MAX_ROLE_WIDTH, 0),
                Qt.TextFlag.TextWordWrap,
                role_text,
            )
            line_count = text_rect.height() // fm.lineSpacing()
            role_lines.append(line_count)
            max_lines = max(max_lines, line_count)

        # 为每个职责文本添加换行符，确保行数相同
        for i, contributor in enumerate(contributors):
            current_lines = role_lines[i]
            if current_lines < max_lines:
                contributor["role"] += "\n" * (max_lines - current_lines)

    def create_contributor_cards(self):
        """创建贡献者卡片"""
        if not self.grid_layout:
            return

        # 初始化卡片缓存和已添加卡片集合
        if not hasattr(self, "_card_cache"):
            self._card_cache = {}
        if not hasattr(self, "_cards_set"):
            self._cards_set = set()

        # 清空现有卡片列表，但保留在缓存中
        self.cards = []
        self._clear_flow_layout()

        # 添加贡献者卡片
        for contributor in self.contributors:
            key = contributor["name"]
            if key in self._cards_set:
                # 已存在，跳过
                continue

            card = self._card_cache.get(key)
            if card is None:
                card = self.addContributorCard(contributor)
                if card is not None:
                    self._card_cache[key] = card

            if card is not None:
                # 确保卡片不在另一个父控件下
                try:
                    if card.parent() is not None and card.parent() is not self:
                        card.setParent(None)
                except Exception as e:
                    logger.exception("Error resetting card parent (ignored): {}", e)

                self.cards.append(card)
                self._cards_set.add(key)

        # 延迟更新布局
        QTimer.singleShot(50, self.update_layout)

    def _clear_flow_layout(self):
        """清空流式布局"""
        # 使用FlowLayout的removeAllWidgets方法清空布局
        self.flow_layout.removeAllWidgets()
        # 清空已记录的已添加卡片集合
        try:
            self._cards_set.clear()
        except Exception as e:
            logger.exception("Error clearing cards set (ignored): {}", e)

    def update_layout(self):
        """更新布局"""
        if not self.flow_layout or not self.cards:
            return

        # 检查是否需要更新布局
        current_width = self.width()
        current_card_count = len(self.cards)

        # 如果布局正在更新中，或者宽度和卡片数量都没有变化，则跳过更新
        if hasattr(self, "_layout_update_in_progress") and self._layout_update_in_progress or (
            hasattr(self, "_last_layout_width") and current_width == self._last_layout_width
            and hasattr(self, "_last_card_count") and current_card_count == self._last_card_count
        ):
            return

        # 设置布局更新标志
        if not hasattr(self, "_layout_update_in_progress"):
            self._layout_update_in_progress = False
        self._layout_update_in_progress = True
        if not hasattr(self, "_last_layout_width"):
            self._last_layout_width = 0
        if not hasattr(self, "_last_card_count"):
            self._last_card_count = 0
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
            self._clear_flow_layout()

            # 添加卡片到流式布局
            for card in self.cards:
                card.setMinimumWidth(CONTRIBUTOR_CARD_MIN_WIDTH)
                card.setMaximumWidth(CONTRIBUTOR_CARD_MIN_WIDTH * 1.5)
                self.flow_layout.addWidget(card)
                # 仅在控件当前不可见时显示，避免重复触发绘制
                if not card.isVisible():
                    card.show()
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
                    logger.exception("Error removing widget from grid during clear (ignored): {}", e)
                widget.hide()
        # 清空已记录的已添加卡片集合
        try:
            self._cards_set.clear()
        except Exception as e:
            logger.exception("Error clearing cards set (ignored): {}", e)

    def addContributorCard(self, contributor):
        """添加单个贡献者卡片"""
        try:
            card = QWidget()
            card.setObjectName("contributorCard")
            cardLayout = QVBoxLayout(card)
            cardLayout.setContentsMargins(
                CONTRIBUTOR_CARD_MARGIN,
                CONTRIBUTOR_CARD_MARGIN,
                CONTRIBUTOR_CARD_MARGIN,
                CONTRIBUTOR_CARD_MARGIN,
            )
            cardLayout.setSpacing(10)

            # 头像
            avatar = AvatarWidget(contributor["avatar"])
            avatar.setRadius(CONTRIBUTOR_AVATAR_RADIUS)
            avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cardLayout.addWidget(avatar, 0, Qt.AlignmentFlag.AlignCenter)

            # 昵称作为GitHub链接
            name = HyperlinkButton(contributor["github"], contributor["name"], None)
            name.setStyleSheet(
                "text-decoration: underline; color: #0066cc; background: transparent; border: none; padding: 0;"
            )
            cardLayout.addWidget(name, 0, Qt.AlignmentFlag.AlignCenter)

            # 职责
            role_text = contributor["role"] or ""
            role = BodyLabel(role_text)
            role.setAlignment(Qt.AlignmentFlag.AlignCenter)
            role.setWordWrap(True)
            role.setMaximumWidth(CONTRIBUTOR_MAX_ROLE_WIDTH)
            cardLayout.addWidget(role, 0, Qt.AlignmentFlag.AlignCenter)

            return card
        except RuntimeError as e:
            logger.error(f"创建贡献者卡片时出错: {e}")
            return None

    def resizeEvent(self, event):
        """窗口大小变化事件"""
        # 使用QTimer延迟布局更新，避免在窗口调整大小时频繁触发布局更新
        if self._resize_timer is not None:
            self._resize_timer.stop()
        self._resize_timer = QTimer()
        self._resize_timer.setSingleShot(True)
        self._resize_timer.timeout.connect(self._delayed_update_layout)
        self._resize_timer.start(50)
        super().resizeEvent(event)

    def _delayed_update_layout(self):
        """延迟更新布局"""
        try:
            if self.grid_layout is not None and self.isVisible():
                self.update_layout()
        except RuntimeError as e:
            logger.error(f"延迟布局更新错误: {e}")

    def closeEvent(self, event):
        """窗口关闭事件"""
        # 清理定时器
        if hasattr(self, "_resize_timer") and self._resize_timer is not None:
            self._resize_timer.stop()
            self._resize_timer = None

        super().closeEvent(event)
