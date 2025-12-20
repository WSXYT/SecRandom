# ==================================================
# 导入模块
# ==================================================
from qfluentwidgets import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtNetwork import *

import json
from typing import Dict
from loguru import logger
import shutil
from pathlib import Path
from PySide6.QtCore import QDateTime

from app.tools.path_utils import *
from app.common.extraction.cses_parser import CSESParser
from app.Language.obtain_language import get_content_name_async


# ==================================================
# 判断当前时间是否在非上课时间段
# ==================================================
def _is_non_class_time() -> bool:
    """检测当前时间是否在非上课时间段

    当'课间禁用'开关启用时，用于判断是否需要安全验证

    Returns:
        bool: 如果当前时间在非上课时间段内返回True，否则返回False
    """
    try:
        # 1. 检查课间禁用开关是否启用
        if not _is_instant_draw_disable_enabled():
            return False

        # 2. 获取非上课时间段配置
        non_class_times = _get_non_class_times_config()
        if not non_class_times:
            return False

        # 3. 获取当前时间并转换为总秒数
        current_total_seconds = _get_current_time_in_seconds()

        # 4. 检查当前时间是否在任何非上课时间段内
        return _is_time_in_ranges(current_total_seconds, non_class_times)

    except Exception as e:
        logger.error(f"检测非上课时间失败: {e}")
        return False


def _is_instant_draw_disable_enabled() -> bool:
    """检查课间禁用开关是否启用

    Returns:
        bool: 如果课间禁用开关启用返回True，否则返回False
    """
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


def _get_non_class_times_config() -> Dict[str, str]:
    """获取非上课时间段配置

    Returns:
        Dict[str, str]: 非上课时间段配置字典，如果获取失败返回空字典
    """
    try:
        time_settings_path = get_settings_path()
        if not file_exists(time_settings_path):
            return {}

        with open_file(time_settings_path, "r", encoding="utf-8") as f:
            time_settings = json.load(f)

        return time_settings.get("non_class_times", {})

    except Exception as e:
        logger.error(f"读取时间设置失败: {e}")
        return {}


def _get_current_time_in_seconds() -> int:
    """获取当前时间并转换为总秒数

    Returns:
        int: 当前时间的总秒数（从午夜开始计算）
    """
    current_time = QDateTime.currentDateTime()
    current_hour = current_time.time().hour()
    current_minute = current_time.time().minute()
    current_second = current_time.time().second()

    return current_hour * 3600 + current_minute * 60 + current_second


def _is_time_in_ranges(current_seconds: int, time_ranges: Dict[str, str]) -> bool:
    """检查当前时间是否在任何一个时间范围内

    Args:
        current_seconds: 当前时间的总秒数
        time_ranges: 时间范围字典，格式为 {"name": "HH:MM:SS-HH:MM:SS"}

    Returns:
        bool: 如果当前时间在任何一个时间范围内返回True，否则返回False
    """
    for range_name, time_range in time_ranges.items():
        try:
            start_end = time_range.split("-")
            if len(start_end) != 2:
                logger.warning(f"时间范围格式错误: {range_name} = {time_range}")
                continue

            start_time_str, end_time_str = start_end

            # 解析开始时间
            start_total_seconds = _parse_time_string_to_seconds(start_time_str)

            # 解析结束时间
            end_total_seconds = _parse_time_string_to_seconds(end_time_str)

            # 检查当前时间是否在该非上课时间段内
            if start_total_seconds <= current_seconds < end_total_seconds:
                return True

        except Exception as e:
            logger.error(
                f"解析非上课时间段失败: {range_name} = {time_range}, 错误: {e}"
            )
            continue

    return False


def _parse_time_string_to_seconds(time_str: str) -> int:
    """将时间字符串转换为总秒数

    Args:
        time_str: 时间字符串，格式为 "HH:MM:SS" 或 "HH:MM"

    Returns:
        int: 时间的总秒数

    Raises:
        ValueError: 如果时间字符串格式不正确
    """
    time_parts = list(map(int, time_str.split(":")))

    if len(time_parts) < 2 or len(time_parts) > 3:
        raise ValueError(f"时间字符串格式不正确: {time_str}")

    hours = time_parts[0]
    minutes = time_parts[1]
    seconds = time_parts[2] if len(time_parts) > 2 else 0

    return hours * 3600 + minutes * 60 + seconds


# ==================================================
# CSES导入功能
# ==================================================
def import_cses_schedule(file_path: str) -> tuple[bool, str]:
    """从CSES文件导入课程表

    Args:
        file_path: CSES文件路径

    Returns:
        tuple[bool, str]: (是否成功, 结果消息)
    """
    try:
        # 创建CSES解析器
        parser = CSESParser()

        # 加载CSES文件
        if not parser.load_from_file(file_path):
            return False, "CSES文件格式错误或文件无法读取"
            return False, get_content_name_async(
                "time_settings", "cses_file_format_error"
            )

        # 获取非上课时间段配置
        non_class_times = parser.get_non_class_times()
        if not non_class_times:
            return False, "未能从课程表中提取有效的时间段信息"
            return False, get_content_name_async(
                "time_settings", "no_valid_time_periods"
            )

        # 保存原始文件到data/CSES文件夹
        original_file_name = Path(file_path).name
        cses_data_path = get_data_path("CSES", original_file_name)
        ensure_dir(get_data_path("CSES"))
        shutil.copy2(file_path, cses_data_path)
        logger.info(f"已将CSES文件保存到: {cses_data_path}")

        # 保存到设置文件
        success = _save_non_class_times_to_settings(non_class_times)
        if not success:
            return False, "保存设置失败"
            return False, get_content_name_async(
                "time_settings", "save_settings_failed"
            )

        # 获取摘要信息
        summary = parser.get_summary()
        return True, f"成功导入课程表: {summary}"
        return True, get_content_name_async("time_settings", "import_success").format(
            summary
        )

    except Exception as e:
        logger.error(f"导入CSES文件失败: {e}")
        return False, f"导入失败: {str(e)}"
        return False, get_content_name_async("time_settings", "import_failed").format(
            str(e)
        )


def import_cses_schedule_from_content(content: str) -> tuple[bool, str]:
    """从CSES内容字符串导入课程表

    Args:
        content: CSES格式的YAML内容

    Returns:
        tuple[bool, str]: (是否成功, 结果消息)
    """
    try:
        # 创建CSES解析器
        parser = CSESParser()

        # 加载CSES内容
        if not parser.load_from_content(content):
            return False, "CSES内容格式错误"
            return False, get_content_name_async(
                "time_settings", "cses_content_format_error"
            )

        # 获取非上课时间段配置
        non_class_times = parser.get_non_class_times()
        if not non_class_times:
            return False, "未能从课程表中提取有效的时间段信息"
            return False, get_content_name_async(
                "time_settings", "no_valid_time_periods"
            )

        # 保存到设置文件
        success = _save_non_class_times_to_settings(non_class_times)
        if not success:
            return False, "保存设置失败"
            return False, get_content_name_async(
                "time_settings", "save_settings_failed"
            )

        # 获取摘要信息
        summary = parser.get_summary()
        return True, f"成功导入课程表: {summary}"
        return True, get_content_name_async("time_settings", "import_success").format(
            summary
        )

    except Exception as e:
        logger.error(f"导入CSES内容失败: {e}")
        return False, f"导入失败: {str(e)}"
        return False, get_content_name_async("time_settings", "import_failed").format(
            str(e)
        )


def _save_non_class_times_to_settings(non_class_times: Dict[str, str]) -> bool:
    """保存非上课时间段到设置文件

    Args:
        non_class_times: 非上课时间段字典

    Returns:
        bool: 保存成功返回True，否则返回False
    """
    try:
        settings_path = get_settings_path()

        # 读取现有设置
        if file_exists(settings_path):
            with open_file(settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
        else:
            settings = {}

        # 更新非上课时间段配置
        settings["non_class_times"] = non_class_times

        # 写入设置文件
        with open_file(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)

        logger.info(f"成功保存{len(non_class_times)}个非上课时间段到设置文件")
        return True

    except Exception as e:
        logger.error(f"保存非上课时间段失败: {e}")
        return False


def get_cses_import_template() -> str:
    """获取CSES导入模板内容

    Returns:
        str: CSES格式的模板内容
    """
    template = """# CSES (Course Schedule Exchange Schema) 课程表模板
# 更多详情请参考: https://github.com/SmartTeachCN/CSES

schedule:
  timeslots:
    - name: "第一节课"
      start_time: "08:00"
      end_time: "08:45"
      teacher: "张老师"
      location: "教室A"
      day_of_week: 1


    - name: "第二节课"
      start_time: "08:55"
      end_time: "09:40"
      teacher: "李老师"
      location: "教室B"
      day_of_week: 1


    - name: "第三节课"
      start_time: "10:00"
      end_time: "10:45"
      teacher: "王老师"
      location: "教室C"
      day_of_week: 1


    - name: "第四节课"
      start_time: "10:55"
      end_time: "11:40"
      teacher: "赵老师"
      location: "教室D"
      day_of_week: 1
"""
    return template


# ==================================================
# 导出函数列表
# ==================================================
__all__ = [
    "import_cses_schedule",
    "import_cses_schedule_from_content",
    "get_cses_import_template",
]
