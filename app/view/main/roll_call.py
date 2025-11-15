# ==================================================
# 导入库
# ==================================================
import json
import os
import sys
import subprocess

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

from app.tools.list import *
from app.tools.history import *
from app.tools.result_display import *

from random import SystemRandom
system_random = SystemRandom()

# ==================================================
# 班级点名类
# ==================================================
class roll_call(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        """初始化UI"""
        # 主容器
        container = QWidget()
        roll_call_container = QVBoxLayout(container)
        roll_call_container.setContentsMargins(0, 0, 0, 0)
        
        # 结果显示区域
        self.result_widget = QWidget()
        self.result_layout = QVBoxLayout(self.result_widget)
        self.result_grid = QGridLayout()
        self.result_layout.addStretch()
        self.result_layout.addLayout(self.result_grid)
        self.result_layout.addStretch()
        roll_call_container.addWidget(self.result_widget)

        # 减号按钮
        self.minus_button = PushButton('-')
        self.minus_button.clicked.connect(lambda: self.update_count(-1))

        # 人数显示
        self.count_label = BodyLabel('1')
        self.current_count = 1
        
        # 加号按钮
        self.plus_button = PushButton('+')
        self.plus_button.clicked.connect(lambda: self.update_count(1))
        
        # 初始化按钮状态
        self.minus_button.setEnabled(False)  # 初始人数为1，禁用减号按钮
        self.plus_button.setEnabled(True)     # 初始人数为1，启用加号按钮

        # 数量控制区
        count_widget = QWidget()
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.minus_button, 0, Qt.AlignmentFlag.AlignLeft)
        horizontal_layout.addWidget(self.count_label, 0, Qt.AlignmentFlag.AlignLeft)
        horizontal_layout.addWidget(self.plus_button, 0, Qt.AlignmentFlag.AlignLeft)
        count_widget.setLayout(horizontal_layout)

        # 开始按钮
        self.start_button = PrimaryPushButton(get_content_pushbutton_name_async("roll_call", "start_button"))
        self.start_button.clicked.connect(lambda: self.start_draw())

        # 名单选择下拉框
        self.list_combobox = ComboBox()
        self.list_combobox.addItems(get_class_name_list())

        # 范围选择下拉框
        self.range_combobox = ComboBox()
        self.range_combobox.addItems(get_content_combo_name_async("roll_call", "range_combobox") + get_group_list(self.list_combobox.currentText()))

        # 性别选择下拉框
        self.gender_combobox = ComboBox()
        self.gender_combobox.addItems(get_content_combo_name_async("roll_call", "gender_combobox") + get_gender_list(self.list_combobox.currentText()))

        # 右侧控制区
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        control_layout.setContentsMargins(10, 10, 10, 10)
        control_layout.addStretch()
        control_layout.addWidget(count_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        control_layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)
        control_layout.addWidget(self.list_combobox, alignment=Qt.AlignmentFlag.AlignCenter)
        control_layout.addWidget(self.range_combobox, alignment=Qt.AlignmentFlag.AlignCenter)
        control_layout.addWidget(self.gender_combobox, alignment=Qt.AlignmentFlag.AlignCenter)

        # 滚动区
        scroll = SmoothScrollArea()
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)

        # 主布局
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll, 1)
        main_layout.addWidget(control_widget)

    def start_draw(self):
        """开始抽取"""
        self.start_button.setText(get_content_pushbutton_name_async("roll_call", "start_button"))
        self.start_button.setEnabled(True)
        try:
            self.start_button.clicked.disconnect()
        except:
            pass
        self.draw_random()
        animation = readme_settings_async("roll_call_settings", "animation")
        autoplay_count = readme_settings_async("roll_call_settings", "autoplay_count")
        animation_interval = readme_settings_async("roll_call_settings", "animation_interval")
        if animation == 0: # 手动停止动画
            self.start_button.setText(get_content_pushbutton_name_async("roll_call", "stop_button"))
            self.is_animating = True
            self.animation_timer = QTimer()
            self.animation_timer.timeout.connect(self.animate_result)
            self.animation_timer.start(animation_interval)
            self.start_button.clicked.connect(lambda: self.stop_animation())
        elif animation == 1: # 自动停止动画
            self.is_animating = True
            self.animation_timer = QTimer()
            self.animation_timer.timeout.connect(self.animate_result)
            self.animation_timer.start(animation_interval)
            self.start_button.setEnabled(False)
            QTimer.singleShot(autoplay_count * animation_interval, lambda: [
                self.animation_timer.stop(),
                self.stop_animation(),
                self.start_button.setEnabled(True)
            ])
            self.start_button.clicked.connect(lambda: self.start_draw())
        elif animation == 2: # 直接显示结果
            # 直接保存结果到历史记录
            if hasattr(self, 'final_selected_students') and hasattr(self, 'final_class_name'):
                save_roll_call_history(
                    class_name=self.final_class_name,
                    selected_students=self.final_selected_students,
                    students_dict_list=self.final_students_dict_list,
                    group_filter=self.final_group_filter,
                    gender_filter=self.final_gender_filter
                )
            self.start_button.clicked.connect(lambda: self.start_draw())
    
    def stop_animation(self):
        """停止动画"""
        if hasattr(self, 'animation_timer') and self.animation_timer.isActive():
            self.animation_timer.stop()
        self.start_button.setText(get_content_pushbutton_name_async("roll_call", "start_button"))
        self.is_animating = False
        try:
            self.start_button.clicked.disconnect()
        except:
            pass
        self.start_button.clicked.connect(lambda: self.start_draw())
        
        # 保存最终结果到历史记录
        # 保存历史记录
        if hasattr(self, 'final_selected_students') and hasattr(self, 'final_class_name'):
            # 保存历史记录
            save_roll_call_history(
                class_name=self.final_class_name,
                selected_students=self.final_selected_students_dict,
                group_filter=self.final_group_filter,
                gender_filter=self.final_gender_filter
            )
            
        if hasattr(self, 'final_selected_students'):
            self.display_result(self.final_selected_students)
    
    def animate_result(self):
        """动画过程中更新显示"""
        self.draw_random()

    def draw_random(self):
        """抽取随机结果"""
        # 初始化参数
        class_name = self.list_combobox.currentText()
        group_index = self.range_combobox.currentIndex()
        group_filter = self.range_combobox.currentText()
        gender_index = self.gender_combobox.currentIndex()
        gender_filter = self.gender_combobox.currentText()

        # 加载学生数据
        student_file = get_resources_path("list/roll_call_list", f"{class_name}.json")
        with open_file(student_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 过滤学生数据
        students_data = filter_students_data(data, group_index, group_filter, gender_index, gender_filter)
        if group_index == 1:
            students_data = sorted(students_data, key=lambda x: str(x))
        
        # 转换为字典格式
        students_dict_list = []
        for student_tuple in students_data:
            student_dict = {
                "id": student_tuple[0],
                "name": student_tuple[1],
                "gender": student_tuple[2],
                "group": student_tuple[3],
                "exist": student_tuple[4]
            }
            students_dict_list.append(student_dict)
        
        # 计算权重
        students_with_weight = calculate_weight(students_dict_list, class_name)
        weights = []
        for student in students_with_weight:
            weights.append(student.get("weight", 1.0))
        
        # 确定抽取人数
        draw_count = self.current_count
        draw_count = min(draw_count, len(students_with_weight))
        
        # 加权随机抽取
        selected_students = []
        selected_students_dict = []
        for _ in range(draw_count):
            if not students_with_weight:
                break
            total_weight = sum(weights)
            if total_weight <= 0:
                random_index = system_random.randint(0, len(students_with_weight) - 1)
            else:
                rand_value = system_random.uniform(0, total_weight)
                cumulative_weight = 0
                random_index = 0
                for i, weight in enumerate(weights):
                    cumulative_weight += weight
                    if rand_value <= cumulative_weight:
                        random_index = i
                        break
            
            # 保存选中结果
            selected_student = students_with_weight[random_index]
            id = selected_student.get("id", "")
            random_name = selected_student.get("name", "")
            exist = selected_student.get("exist", True)
            selected_students.append((id, random_name, exist))
            selected_students_dict.append(selected_student)
            
            # 移除已选学生，避免重复
            students_with_weight.pop(random_index)
            weights.pop(random_index)
        
        # 存储结果供停止时使用
        self.final_selected_students = selected_students
        self.final_class_name = class_name
        self.final_selected_students_dict = selected_students_dict
        self.final_group_filter = group_filter
        self.final_gender_filter = gender_filter
        
        # 动画过程中显示结果
        self.display_result(selected_students)
    
    def display_result(self, selected_students):
        """显示抽取结果"""
        student_labels = ResultDisplayUtils.create_student_label(
            selected_students=selected_students,
            draw_count=self.current_count,
            font_size=readme_settings_async("roll_call_settings", "font_size"),
            animation_color=readme_settings_async("roll_call_settings", "animation_color_theme"),
            display_format=readme_settings_async("roll_call_settings", "display_format"),
            show_student_image=readme_settings_async("roll_call_settings", "student_image"),
            group_index=0
        )
        ResultDisplayUtils.display_results_in_grid(self.result_grid, student_labels)

    def update_count(self, change):
        """更新人数
        
        Args:
            change (int): 变化量，正数表示增加，负数表示减少
        """
        try:
            self.current_count = max(1, int(self.count_label.text()) + change)
            self.count_label.setText(str(self.current_count))
            self.minus_button.setEnabled(self.current_count > 1)
            self.plus_button.setEnabled(self.current_count < 100)
        except (ValueError, TypeError):
            self.count_label.setText("1")
            self.minus_button.setEnabled(False)
            self.plus_button.setEnabled(True)