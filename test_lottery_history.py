#!/usr/bin/env python3
"""测试抽奖历史记录功能"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from app.common.history.history import save_lottery_history, lightweight_stats

def test_lottery_history():
    """测试抽奖历史记录保存功能"""
    print("测试抽奖历史记录保存功能...")
    
    # 模拟选中的学生数据
    selected_students = [
        {"name": "张三", "group": "A组", "gender": "男"},
        {"name": "李四", "group": "B组", "gender": "女"},
        {"name": "王五", "group": "A组", "gender": "男"},
    ]
    
    pool_name = "测试奖池"
    group_filter = "A组"
    gender_filter = None
    
    try:
        # 保存历史记录
        result = save_lottery_history(
            pool_name=pool_name,
            selected_students=selected_students,
            group_filter=group_filter,
            gender_filter=gender_filter
        )
        
        if result:
            print("✓ 抽奖历史记录保存成功")
            
            # 检查轻量级统计
            print(f"总统计数: {lightweight_stats.global_stats['total_stats']}")
            print(f"总轮数: {lightweight_stats.global_stats['total_rounds']}")
            print(f"小组统计: {lightweight_stats.global_stats['group_stats']}")
            print(f"性别统计: {lightweight_stats.global_stats['gender_stats']}")
            
            # 检查学生统计
            for student in selected_students:
                name = student["name"]
                stats = lightweight_stats.get_student_stats(name)
                print(f"学生 {name} 统计: {stats}")
                
        else:
            print("✗ 抽奖历史记录保存失败")
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_lottery_history()