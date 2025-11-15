# ==================================================
# 导入库
# ==================================================

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


from app.page_building.settings_window_page import *

# ==================================================
# 主窗口类
# ==================================================
class SettingsWindow(MSFluentWindow):
    """主窗口类
    程序的核心控制中心"""
    showSettingsRequested = pyqtSignal()
    showSettingsRequestedAbout = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.setObjectName("settingWindow")
        self.parent = parent

        # resize_timer的初始化
        self.resize_timer = QTimer(self)
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(lambda: self.save_window_size(self.width(), self.height()))

        # 设置窗口属性
        window_width = 800
        window_height = 600
        self.resize(window_width, window_height)
        self.setMinimumSize(MINIMUM_WINDOW_SIZE[0], MINIMUM_WINDOW_SIZE[1])
        self.setWindowTitle('SecRandom')
        self.setWindowIcon(QIcon(str(get_resources_path('assets/icon', 'secrandom-icon-paper.png'))))

        self._position_window()

        QTimer.singleShot(APP_INIT_DELAY, lambda: (
            self.createSubInterface()
        ))

    def _position_window(self):
        """窗口定位
        根据屏幕尺寸和用户设置自动计算最佳位置"""
        is_maximized = readme_settings_async("settings", "is_maximized")
        if is_maximized:
            pre_maximized_width = readme_settings_async("settings", "pre_maximized_width")
            pre_maximized_height = readme_settings_async("settings", "pre_maximized_height")
            self.resize(pre_maximized_width, pre_maximized_height)
            self._center_window()
            QTimer.singleShot(100, self.showMaximized)
        else:
            setting_window_width = readme_settings_async("settings", "width")
            setting_window_height = readme_settings_async("settings", "height")
            self.resize(setting_window_width, setting_window_height)
            self._center_window()

    def _center_window(self):
        """窗口定位-正常居中显示
        窗口大小设置完成后，将窗口居中显示在屏幕上"""
        screen = QApplication.primaryScreen()
        desktop = screen.availableGeometry()
        w, h = desktop.width(), desktop.height()

        target_x = w // 2 - self.width() // 2
        target_y = h // 2 - self.height() // 2

        self.move(target_x, target_y)

    def _apply_window_visibility_settings(self):
        """应用窗口显示设置
        根据用户保存的设置决定窗口是否显示"""
        try:
            self.show()
        except Exception as e:
            logger.error(f"加载窗口显示设置失败: {e}")

    def createSubInterface(self):
        """创建子界面
        搭建子界面导航系统"""
        self.homeInterface = home_page(self)
        self.homeInterface.setObjectName("homeInterface")

        self.basicSettingsInterface = basic_settings_page(self)
        self.basicSettingsInterface.setObjectName("basicSettingsInterface")

        self.listManagementInterface = list_management_page(self)
        self.listManagementInterface.setObjectName("listManagementInterface")

        self.extractionSettingsInterface = extraction_settings_page(self)
        self.extractionSettingsInterface.setObjectName("extractionSettingsInterface")

        self.notificationSettingsInterface = notification_settings_page(self)
        self.notificationSettingsInterface.setObjectName("notificationSettingsInterface")

        self.safetySettingsInterface = safety_settings_page(self)
        self.safetySettingsInterface.setObjectName("safetySettingsInterface")

        self.customSettingsInterface = custom_settings_page(self)
        self.customSettingsInterface.setObjectName("customSettingsInterface")

        self.voiceSettingsInterface = voice_settings_page(self)
        self.voiceSettingsInterface.setObjectName("voiceSettingsInterface")

        self.historyInterface = history_page(self)
        self.historyInterface.setObjectName("historyInterface")

        self.moreSettingsInterface = more_settings_page(self)
        self.moreSettingsInterface.setObjectName("moreSettingsInterface")

        self.aboutInterface = about_page(self)
        self.aboutInterface.setObjectName("aboutInterface")

        self.initNavigation()

    def initNavigation(self):
        """初始化导航系统
        根据用户设置构建个性化菜单导航"""
        self.addSubInterface(self.homeInterface, get_theme_icon("ic_fluent_home_20_filled"), get_content_name_async("home", "title"), position=NavigationItemPosition.TOP)

        self.addSubInterface(self.basicSettingsInterface, get_theme_icon("ic_fluent_wrench_settings_20_filled"), get_content_name_async("basic_settings", "title"), position=NavigationItemPosition.TOP)

        self.addSubInterface(self.listManagementInterface, get_theme_icon("ic_fluent_list_20_filled"), get_content_name_async("list_management", "title"), position=NavigationItemPosition.TOP)

        self.addSubInterface(self.extractionSettingsInterface, get_theme_icon("ic_fluent_archive_20_filled"), get_content_name_async("extraction_settings", "title"), position=NavigationItemPosition.TOP)

        self.addSubInterface(self.notificationSettingsInterface, get_theme_icon("ic_fluent_comment_note_20_filled"), get_content_name_async("notification_settings", "title"), position=NavigationItemPosition.TOP)

        self.addSubInterface(self.safetySettingsInterface, get_theme_icon("ic_fluent_shield_20_filled"), get_content_name_async("safety_settings", "title"), position=NavigationItemPosition.TOP)

        self.addSubInterface(self.customSettingsInterface, get_theme_icon("ic_fluent_person_edit_20_filled"), get_content_name_async("custom_settings", "title"), position=NavigationItemPosition.TOP)

        self.addSubInterface(self.voiceSettingsInterface, get_theme_icon("ic_fluent_voice_20_filled"), get_content_name_async("voice_settings", "title"), position=NavigationItemPosition.TOP)

        self.addSubInterface(self.historyInterface, get_theme_icon("ic_fluent_history_20_filled"), get_content_name_async("history", "title"), position=NavigationItemPosition.TOP)

        self.addSubInterface(self.moreSettingsInterface, get_theme_icon("ic_fluent_more_horizontal_20_filled"), get_content_name_async("more_settings", "title"), position=NavigationItemPosition.TOP)

        self.addSubInterface(self.aboutInterface, get_theme_icon("ic_fluent_info_20_filled"), get_content_name_async("about", "title"), position=NavigationItemPosition.BOTTOM)

    def closeEvent(self, event):
        """窗口关闭事件处理
        拦截窗口关闭事件，隐藏窗口并保存窗口大小"""
        self.hide()
        event.ignore()
        is_maximized = self.isMaximized()
        update_settings("settings", "is_maximized", is_maximized)
        if is_maximized:
            pass
        else:
            self.save_window_size(self.width(), self.height())

    def resizeEvent(self, event):
        """窗口大小变化事件处理
        检测窗口大小变化，但不启动尺寸记录倒计时，减少IO操作"""
        # 正常的窗口大小变化处理
        self.resize_timer.start(500)
        super().resizeEvent(event)

    def changeEvent(self, event):
        """窗口状态变化事件处理
        检测窗口最大化/恢复状态变化，保存正确的窗口大小"""
        # 检查是否是窗口状态变化
        if event.type() == QEvent.Type.WindowStateChange:
            is_currently_maximized = self.isMaximized()
            was_maximized = readme_settings_async("settings", "is_maximized")
            if is_currently_maximized != was_maximized:
                update_settings("settings", "is_maximized", is_currently_maximized)
                if is_currently_maximized:
                    normal_geometry = self.normalGeometry()
                    update_settings("settings", "pre_maximized_width", normal_geometry.width())
                    update_settings("settings", "pre_maximized_height", normal_geometry.height())
                else:
                    pre_maximized_width = readme_settings_async("settings", "pre_maximized_width")
                    pre_maximized_height = readme_settings_async("settings", "pre_maximized_height")
                    QTimer.singleShot(100, lambda: self.resize(pre_maximized_width, pre_maximized_height))

        super().changeEvent(event)

    def save_window_size(self, setting_window_width, setting_window_height):
        """保存窗口大小
        记录当前窗口尺寸，下次启动时自动恢复"""
        if not self.isMaximized():
            update_settings("settings", "height", setting_window_height)
            update_settings("settings", "width", setting_window_width)

    def show_settings_window(self):
        """显示设置窗口"""
        if self.isMinimized():
            self.showNormal()
            self.activateWindow()
            self.raise_()
        else:
            self.show()
            self.activateWindow()
            self.raise_()

    def show_settings_window_about(self):
        """显示关于窗口"""
        if self.isMinimized():
            self.showNormal()
            self.activateWindow()
            self.raise_()
        else:
            self.show()
            self.activateWindow()
            self.raise_()

        self.switchTo(self.aboutInterface)
