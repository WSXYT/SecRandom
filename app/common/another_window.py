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
# 贡献者对话框类
# ==================================================
class ContributorDialog(QDialog):
    """ 贡献者信息对话框 """
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置无边框窗口样式并解决屏幕设置冲突
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setWindowTitle('贡献人员')
        self.setMinimumSize(900, 600)
        self.setSizeGripEnabled(True) #启用右下角拖动柄
        self.update_theme_style()

        self.saved = False
        self.dragging = False
        self.drag_position = None

        # 确保不设置子窗口的屏幕属性
        if parent is not None:
            self.setParent(parent)

        # 创建自定义标题栏
        self.title_bar = QWidget()
        self.title_bar.setObjectName("CustomTitleBar")
        self.title_bar.setFixedHeight(35)

        # 标题栏布局
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)

        # 窗口标题
        self.title_label = BodyLabel(get_content_name_async("about", "contributor"))
        self.title_label.setObjectName("TitleLabel")

        # 窗口控制按钮
        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("CloseButton")
        self.close_btn.setFixedSize(25, 25)
        self.close_btn.clicked.connect(self.reject)

        # 添加组件到标题栏
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.close_btn)

        # 创建滚动区域
        scroll = SingleDirectionScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        self.grid_layout = QGridLayout(content)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollArea QWidget {
                border: none;
                background-color: transparent;
            }
        """)
        scroll.setWidget(content)

        # 主布局
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # 添加自定义标题栏
        self.layout.addWidget(self.title_bar)
        # 添加内容区域
        content_layout = QVBoxLayout()
        content_layout.addWidget(scroll)
        content_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(content_layout)

        self.update_theme_style()
        qconfig.themeChanged.connect(self.update_theme_style)

        # 贡献者数据
        contributors = [
            {
                'name': 'lzy98276',
                'role': get_any_position_value_async("about", "contributor", "contributor_role_1"),
                'github': 'https://github.com/lzy98276',
                'avatar': str(get_resources_path('assets/contribution', 'contributor1.png'))

            },
            {
                'name': 'QiKeZhiCao',
                'role': get_any_position_value_async("about", "contributor", "contributor_role_2"),
                'github': 'https://github.com/QiKeZhiCao',
                'avatar': str(get_resources_path('assets/contribution', 'contributor2.png'))
            },
            {
                'name': 'Fox-block-offcial',
                'role': get_any_position_value_async("about", "contributor", "contributor_role_3"),
                'github': 'https://github.com/Fox-block-offcial',
                'avatar': str(get_resources_path('assets/contribution', 'contributor3.png'))
            },
            {
                'name': 'yuanbenxin',
                'role': get_any_position_value_async("about", "contributor", "contributor_role_4"),
                'github': 'https://github.com/yuanbenxin',
                'avatar': str(get_resources_path('assets/contribution', 'contributor4.png'))
            },
            {
                'name': 'LeafS',
                'role': get_any_position_value_async("about", "contributor", "contributor_role_5"),
                'github': 'https://github.com/LeafS825',
                'avatar': str(get_resources_path('assets/contribution', 'contributor5.png'))
            },
            {
                'name': 'Jursin',
                'role': get_any_position_value_async("about", "contributor", "contributor_role_6"),
                'github': 'https://github.com/jursin',
                'avatar': str(get_resources_path('assets/contribution', 'contributor6.png'))
            },
            {
                'name': 'LHGS-github',
                'role': get_any_position_value_async("about", "contributor", "contributor_role_7"),
                'github': 'https://github.com/LHGS-github',
                'avatar': str(get_resources_path('assets/contribution', 'contributor7.png'))
            },
            {
                'name': 'real01bit',
                'role': get_any_position_value_async("about", "contributor", "contributor_role_8"),
                'github': 'https://github.com/real01bit',
                'avatar': str(get_resources_path('assets/contribution', 'contributor8.png'))
            }
        ]

        # 计算所有职责文本的行数，让它们变得整齐划一
        fm = QFontMetrics(self.font())
        max_lines = 0
        role_lines = []

        # 第一步：找出最长的职责文本有多少行
        for contributor in contributors:
            role_text = contributor['role']
            # 确保role_text不为None
            if role_text is None:
                role_text = ''
                contributor['role'] = role_text
            # 计算文本在500像素宽度下的行数（和UI显示保持一致）
            text_rect = fm.boundingRect(QRect(0, 0, 500, 0), Qt.TextFlag.TextWordWrap, role_text)
            line_count = text_rect.height() // fm.lineSpacing()
            role_lines.append(line_count)
            if line_count > max_lines:
                max_lines = line_count

        # 第二步：为每个职责文本添加换行符，确保行数相同
        for i, contributor in enumerate(contributors):
            current_lines = role_lines[i]
            if current_lines < max_lines:
                # 确保role不为None
                if contributor['role'] is None:
                    contributor['role'] = ''
                # 添加缺少的换行符
                contributor['role'] += '\n' * (max_lines - current_lines)

        self.cards = []
        # 添加贡献者卡片
        for contributor in contributors:
            card = self.addContributorCard(contributor)
            self.cards.append(card)

        self.update_layout()

    def update_layout(self):
        # 清空网格布局
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.hide()

        # 响应式布局配置
        CARD_MIN_WIDTH = 250  # 卡片最小宽度
        MAX_COLUMNS = 12       # 最大列数限制

        def calculate_columns(width):
            """根据窗口宽度和卡片尺寸动态计算列数"""
            if width <= 0:
                return 1
            # 计算最大可能列数（不超过MAX_COLUMNS）
            cols = min(width // CARD_MIN_WIDTH, MAX_COLUMNS)
            # 至少显示1列
            return max(cols, 1)

        # 根据窗口宽度计算列数
        cols = calculate_columns(self.width())

        # 添加卡片到网格
        for i, card in enumerate(self.cards):
            row = i // cols
            col = i % cols
            self.grid_layout.addWidget(card, row, col, Qt.AlignmentFlag.AlignCenter)
            card.show()

    def resizeEvent(self, event):
        self.update_layout()
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        # 窗口拖动功能
        if event.button() == Qt.MouseButton.LeftButton and self.title_bar.underMouse():
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def update_theme_style(self):
        """根据当前主题更新样式"""
        if qconfig.theme == Theme.AUTO:
            # 获取系统当前主题
            lightness = QApplication.palette().color(QPalette.Window).lightness()
            is_dark = lightness <= 127
        else:
            is_dark = qconfig.theme == Theme.DARK

        # 主题样式更新
        colors = {'text': '#F5F5F5', 'bg': '#111116', 'title_bg': '#2D2D2D'} if  is_dark else {'text': '#111116', 'bg': '#F5F5F5', 'title_bg': '#E0E0E0'}
        self.setStyleSheet(f"""
            QDialog {{ background-color: {colors['bg']}; border-radius: 5px; }}
            #CustomTitleBar {{ background-color: {colors['title_bg']}; }}
            #TitleLabel {{ color: {colors['text']}; font-weight: bold; padding: 5px; }}
            #CloseButton {{
                background-color: transparent;
                color: {colors['text']};
                border-radius: 4px;
                font-weight: bold;
                border: none;
            }}
            #CloseButton:hover {{
                background-color: #ff4d4d;
                color: white;
                border: none;
            }}
            QLabel, QPushButton, QTextEdit {{ color: {colors['text']}; }}
            QLineEdit {{
                background-color: {colors['bg']};
                color: {colors['text']};
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px;
            }}
            QPushButton {{
                background-color: {colors['bg']};
                color: {colors['text']};
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px;
            }}
            QPushButton:hover {{ background-color: #606060; }}
            QComboBox {{
                background-color: {colors['bg']};
                color: {colors['text']};
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px;
            }}
        """)

        # 设置标题栏颜色以匹配背景色（仅Windows系统）
        if os.name == 'nt':
            try:
                import ctypes
                # 修复参数类型错误
                hwnd = int(self.winId())  # 转换为整数句柄

                # 颜色格式要改成ARGB格式
                bg_color = colors['bg'].lstrip('#')
                # 转换为ARGB格式（添加不透明通道）
                rgb_color = int(f'FF{bg_color}', 16) if len(bg_color) == 6 else int(bg_color, 16)

                # 设置窗口标题栏颜色
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    ctypes.c_int(hwnd),  # 窗口句柄（整数类型）
                    35,  # DWMWA_CAPTION_COLOR
                    ctypes.byref(ctypes.c_uint(rgb_color)),  # 颜色值指针
                    ctypes.sizeof(ctypes.c_uint)  # 数据大小
                )
            except Exception as e:
                logger.error(f"设置标题栏颜色失败: {str(e)}")

    def closeEvent(self, event):
        if not self.saved:
            w = Dialog('未保存内容', '确定要关闭吗？', self)
            w.yesButton.setText("确定")
            w.cancelButton.setText("取消")
            w.yesButton = PrimaryPushButton('确定')
            w.cancelButton = PushButton('取消')

            if w.exec():
                self.reject()
                return
            else:
                event.ignore()
                return
        event.accept()

    def update_card_theme_style(self, card):
        """根据当前主题更新样式"""
        if qconfig.theme == Theme.AUTO:
            # 获取系统当前主题
            lightness = QApplication.palette().color(QPalette.Window).lightness()
            is_dark = lightness <= 127
        else:
            is_dark = qconfig.theme == Theme.DARK
        # 主题样式更新
        colors = {'bg': '#111116'} if is_dark else {'bg': '#F5F5F5'}
        card.setStyleSheet(f'''
            QWidget#contributorCard {{
                background: {colors['bg']};
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 10px;
            }}
        ''')

    def addContributorCard(self, contributor):
        """ 添加贡献者卡片 """
        card = QWidget()
        card.setObjectName('contributorCard')
        self.update_card_theme_style(card)
        cardLayout = QVBoxLayout(card)  # 垂直布局
        cardLayout.setContentsMargins(15, 15, 15, 15)
        cardLayout.setSpacing(10)

        # 头像
        avatar = AvatarWidget(contributor['avatar'])
        avatar.setRadius(64)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cardLayout.addWidget(avatar, 0, Qt.AlignmentFlag.AlignCenter)

        # 昵称作为GitHub链接
        name = HyperlinkButton(contributor['github'], contributor['name'], self)
        name.setStyleSheet('text-decoration: underline; color: #0066cc; background: transparent; border: none; padding: 0;')
        cardLayout.addWidget(name, 0, Qt.AlignmentFlag.AlignCenter)

        # 职责
        role_text = contributor['role']
        if role_text is None:
            role_text = ''
        role = BodyLabel(role_text)
        role.setAlignment(Qt.AlignmentFlag.AlignCenter)
        role.setWordWrap(True)
        role.setMaximumWidth(500)
        cardLayout.addWidget(role, 0, Qt.AlignmentFlag.AlignCenter)

        return card
