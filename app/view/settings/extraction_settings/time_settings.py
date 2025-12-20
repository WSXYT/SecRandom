# ==================================================
# 导入库
# ==================================================
import json

from loguru import logger
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
from app.common.extraction.extract import import_cses_schedule
from app.page_building.another_window import create_cses_template_viewer_window


# ==================================================
# 时间设置
# ==================================================
class time_settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 创建垂直布局
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(10)

        # 添加课间禁用设置组件
        self.class_break_widget = class_break_settings(self)
        self.vBoxLayout.addWidget(self.class_break_widget)

        # 添加CSES导入组件
        self.cses_import_widget = cses_import_settings(self)
        self.vBoxLayout.addWidget(self.cses_import_widget)


class class_break_settings(GroupHeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(
            get_content_name_async("time_settings", "class_break_settings", "name")
        )
        self.setBorderRadius(8)

        # 课间禁用开关
        self.class_break_switch = SwitchButton()
        self.class_break_switch.setOffText(
            get_content_name_async("time_settings", "disable")
        )
        self.class_break_switch.setOnText(
            get_content_name_async("time_settings", "enable")
        )

        # 从设置中读取当前状态
        current_enabled = self._get_class_break_enabled()
        self.class_break_switch.setChecked(current_enabled)

        self.class_break_switch.checkedChanged.connect(self.on_class_break_changed)

        # 添加设置项到分组
        self.addGroup(
            get_theme_icon("ic_fluent_clock_lock_20_filled"),
            get_content_name_async("time_settings", "class_break_function", "name"),
            get_content_name_async(
                "time_settings", "class_break_function", "description"
            ),
            self.class_break_switch,
        )

    def _get_class_break_enabled(self) -> bool:
        """获取课间禁用功能是否启用"""
        try:
            settings_path = get_settings_path()
            if not file_exists(settings_path):
                return False

            with open_file(settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)

            program_functionality = settings.get("program_functionality", {})
            return program_functionality.get("instant_draw_disable", False)
        except Exception as e:
            logger.error(f"读取课间禁用设置失败: {e}")
            return False

    def on_class_break_changed(self, is_checked: bool):
        """当课间禁用开关状态改变时的处理"""
        try:
            settings_path = get_settings_path()

            # 读取现有设置
            if file_exists(settings_path):
                with open_file(settings_path, "r", encoding="utf-8") as f:
                    settings = json.load(f)
            else:
                settings = {}

            # 更新程序功能设置
            if "program_functionality" not in settings:
                settings["program_functionality"] = {}

            settings["program_functionality"]["instant_draw_disable"] = is_checked

            # 写入设置文件
            with open_file(settings_path, "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)

            logger.info(f"课间禁用功能已{'开启' if is_checked else '关闭'}")

        except Exception as e:
            logger.error(f"保存课间禁用设置失败: {e}")
            # 恢复开关状态
            self.class_break_switch.setChecked(not is_checked)


class cses_import_settings(GroupHeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(
            get_content_name_async("time_settings", "cses_import_settings", "name")
        )
        self.setBorderRadius(8)

        # 导入文件按钮
        self.import_file_button = PushButton(
            get_content_name_async("time_settings", "import_from_file")
        )
        self.import_file_button.setIcon(
            get_theme_icon("ic_fluent_folder_open_20_filled")
        )
        self.import_file_button.clicked.connect(self.on_import_file_clicked)

        # 查看模板按钮
        self.view_template_button = PushButton(
            get_content_name_async("time_settings", "view_template")
        )
        self.view_template_button.setIcon(
            get_theme_icon("ic_fluent_document_20_filled")
        )
        self.view_template_button.clicked.connect(self.on_view_template_clicked)

        # 当前课程表信息标签
        self.schedule_info_label = QLabel(
            get_content_name_async("time_settings", "no_schedule_imported")
        )
        self._update_schedule_info()

        # 创建按钮布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.import_file_button)
        button_layout.addWidget(self.view_template_button)
        button_layout.addStretch()

        # 创建信息布局
        info_layout = QVBoxLayout()
        info_layout.addLayout(button_layout)
        info_layout.addWidget(self.schedule_info_label)

        # 创建容器控件来包含布局
        info_widget = QWidget()
        info_widget.setLayout(info_layout)

        # 添加设置项到分组
        self.addGroup(
            get_theme_icon("ic_fluent_calendar_ltr_20_filled"),
            get_content_name_async("time_settings", "cses_import", "name"),
            get_content_name_async("time_settings", "cses_import", "description"),
            info_widget,
        )

    def _update_schedule_info(self):
        """更新课程表信息显示"""
        try:
            settings_path = get_settings_path()
            if not file_exists(settings_path):
                self.schedule_info_label.setText(
                    get_content_name_async("time_settings", "no_schedule_imported")
                )
                return

            with open_file(settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)

            non_class_times = settings.get("non_class_times", {})
            if non_class_times:
                count = len(non_class_times)
                self.schedule_info_label.setText(
                    get_content_name_async("time_settings", "schedule_imported").format(
                        count
                    )
                )
            else:
                self.schedule_info_label.setText(
                    get_content_name_async("time_settings", "no_schedule_imported")
                )

        except Exception as e:
            logger.error(f"更新课程表信息失败: {e}")
            self.schedule_info_label.setText("获取课程表信息失败")

    def on_import_file_clicked(self):
        """当点击导入文件按钮时的处理"""
        # 打开文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            get_content_name_async("time_settings", "select_cses_file"),
            "",
            f"{get_content_name_async('time_settings', 'yaml_files')};;{get_content_name_async('time_settings', 'all_files')}",
        )

        if file_path:
            self._import_cses_file(file_path)

    def _import_cses_file(self, file_path: str):
        """导入CSES文件"""
        try:
            # 显示等待对话框
            self.import_file_button.setEnabled(False)
            self.import_file_button.setText(
                get_content_name_async("time_settings", "importing")
            )

            # 调用导入函数
            success, message = import_cses_schedule(file_path)

            if success:
                # 显示成功信息
                InfoBar.success(
                    title=get_content_name_async("time_settings", "import_success"),
                    content=message,
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self,
                )

                # 更新课程表信息
                self._update_schedule_info()

            else:
                # 显示错误信息
                InfoBar.error(
                    title=get_content_name_async("time_settings", "import_failed"),
                    content=message,
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=5000,
                    parent=self,
                )

        except Exception as e:
            logger.error(f"导入CSES文件失败: {e}")
            InfoBar.error(
                title=get_content_name_async("time_settings", "import_failed"),
                content=get_content_name_async("time_settings", "import_error").format(
                    str(e)
                ),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=5000,
                parent=self,
            )

        finally:
            # 恢复按钮状态
            self.import_file_button.setEnabled(True)
            self.import_file_button.setText(
                get_content_name_async("time_settings", "import_from_file")
            )

    def on_view_template_clicked(self):
        """当点击查看模板按钮时的处理"""
        try:
            # 使用独立窗口模板创建CSES模板查看器
            create_cses_template_viewer_window()

        except Exception as e:
            logger.error(f"显示模板失败: {e}")
            InfoBar.error(
                title=get_content_name_async("time_settings", "import_failed"),
                content=f"无法显示模板: {str(e)}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
