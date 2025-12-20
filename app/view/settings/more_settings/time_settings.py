# ==================================================
# 导入库
# ==================================================
import json
import os

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
from app.page_building.another_window import create_current_config_viewer_window

from app.common.extraction.cses_parser import CSESParser


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
        self.class_break_switch.setChecked(self.class_break_switch.isChecked())

        self.class_break_switch.checkedChanged.connect(
            lambda: update_settings(
                "time_settings",
                "instant_draw_disable",
                self.class_break_switch.isChecked(),
            )
        )

        # 验证流程开关
        self.verification_switch = SwitchButton()
        self.verification_switch.setOffText(
            get_content_name_async("time_settings", "disable")
        )
        self.verification_switch.setOnText(
            get_content_name_async("time_settings", "enable")
        )

        # 从设置中读取当前状态
        self.verification_switch.setChecked(self.verification_switch.isChecked())

        self.verification_switch.checkedChanged.connect(
            lambda: update_settings(
                "time_settings",
                "verification_required",
                self.verification_switch.isChecked(),
            )
        )

        # 添加设置项到分组
        self.addGroup(
            get_theme_icon("ic_fluent_clock_lock_20_filled"),
            get_content_name_async("time_settings", "class_break_function"),
            get_content_description_async("time_settings", "class_break_function"),
            self.class_break_switch,
        )
        self.addGroup(
            get_theme_icon("ic_fluent_shield_lock_20_filled"),
            get_content_name_async("time_settings", "verification_function"),
            get_content_description_async("time_settings", "verification_function"),
            self.verification_switch,
        )


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

        # 查看当前配置按钮
        self.view_current_config_button = PushButton(
            get_content_name_async("time_settings", "view_current_config")
        )
        self.view_current_config_button.setIcon(
            get_theme_icon("ic_fluent_document_20_filled")
        )
        self.view_current_config_button.clicked.connect(
            self.on_view_current_config_clicked
        )

        # 当前课程表信息标签
        self.schedule_info_label = BodyLabel(
            get_content_name_async("time_settings", "no_schedule_imported")
        )
        self._update_schedule_info()

        # 创建按钮布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.import_file_button)
        button_layout.addWidget(self.view_current_config_button)
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
            total_class_periods = 0

            # 检查data/CSES文件夹中是否有课程表文件
            cses_dir = get_data_path("CSES")
            if os.path.exists(cses_dir):
                cses_files = [
                    f for f in os.listdir(cses_dir) if f.endswith((".yaml", ".yml"))
                ]
                if cses_files:
                    # 解析每个课程表文件，计算总上课时间段
                    for file_name in cses_files:
                        file_path = os.path.join(cses_dir, file_name)
                        try:
                            parser = CSESParser()
                            if parser.load_from_file(file_path):
                                class_info = parser.get_class_info()
                                total_class_periods += len(class_info)
                        except Exception as e:
                            logger.error(f"解析文件{file_name}失败: {e}")

            # 从设置文件中获取non_class_times
            settings_path = get_settings_path()
            non_class_times = {}
            if file_exists(settings_path):
                with open_file(settings_path, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                non_class_times = settings.get("non_class_times", {})

            # 判断是否有课程表数据
            if non_class_times or total_class_periods > 0:
                if non_class_times:
                    # 使用non_class_times的数量（非上课时间段）
                    count = len(non_class_times)
                else:
                    # 使用上课时间段数量
                    count = total_class_periods

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

    def on_view_current_config_clicked(self):
        """当点击查看当前配置按钮时的处理"""
        try:
            # 使用独立窗口模板创建当前配置查看器
            create_current_config_viewer_window()

        except Exception as e:
            logger.error(f"显示当前配置失败: {e}")
            InfoBar.error(
                title=get_content_name_async("time_settings", "import_failed"),
                content=f"无法显示当前配置: {str(e)}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
