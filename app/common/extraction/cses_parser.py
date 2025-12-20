# ==================================================
# CSES (Course Schedule Exchange Schema) 解析器
# ==================================================
import yaml
from datetime import time
from typing import Dict, List
from loguru import logger


class CSESParser:
    """CSES格式课程表解析器"""

    def __init__(self):
        self.schedule_data = None

    def load_from_file(self, file_path: str) -> bool:
        """从文件加载CSES数据

        Args:
            file_path: CSES文件路径

        Returns:
            bool: 加载成功返回True，否则返回False
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.schedule_data = yaml.safe_load(f)
            return self._validate_schedule()
        except Exception as e:
            logger.error(f"加载CSES文件失败: {e}")
            return False

    def load_from_content(self, content: str) -> bool:
        """从字符串内容加载CSES数据

        Args:
            content: YAML格式的CSES内容

        Returns:
            bool: 加载成功返回True，否则返回False
        """
        try:
            self.schedule_data = yaml.safe_load(content)
            return self._validate_schedule()
        except Exception as e:
            logger.error(f"解析CSES内容失败: {e}")
            return False

    def _validate_schedule(self) -> bool:
        """验证课程表数据的有效性

        Returns:
            bool: 数据有效返回True，否则返回False
        """
        if not self.schedule_data:
            logger.error("课程表数据为空")
            return False

        # 基本结构验证
        if "schedule" not in self.schedule_data:
            logger.error("缺少'schedule'字段")
            return False

        schedule = self.schedule_data["schedule"]
        if not isinstance(schedule, dict):
            logger.error("'schedule'字段必须是字典类型")
            return False

        # 验证时间段配置
        if "timeslots" not in schedule:
            logger.error("缺少'timeslots'字段")
            return False

        timeslots = schedule["timeslots"]
        if not isinstance(timeslots, list):
            logger.error("'timeslots'字段必须是列表类型")
            return False

        # 验证每个时间段
        for i, timeslot in enumerate(timeslots):
            if not self._validate_timeslot(timeslot, i):
                return False

        return True

    def _validate_timeslot(self, timeslot: dict, index: int) -> bool:
        """验证单个时间段的配置

        Args:
            timeslot: 时间段配置字典
            index: 时间段索引

        Returns:
            bool: 有效返回True，否则返回False
        """
        required_fields = ["name", "start_time", "end_time"]
        for field in required_fields:
            if field not in timeslot:
                logger.error(f"时间段{index}缺少'{field}'字段")
                return False

        # 验证时间格式
        try:
            start_time = self._parse_time(timeslot["start_time"])
            end_time = self._parse_time(timeslot["end_time"])

            if start_time >= end_time:
                logger.error(f"时间段{index}的开始时间必须早于结束时间")
                return False

        except ValueError as e:
            logger.error(f"时间段{index}时间格式错误: {e}")
            return False

        return True

    def _parse_time(self, time_str: str) -> time:
        """解析时间字符串

        Args:
            time_str: 时间字符串 (HH:MM 或 HH:MM:SS)

        Returns:
            time: 时间对象

        Raises:
            ValueError: 时间格式错误
        """
        try:
            if ":" in time_str:
                parts = time_str.split(":")
                if len(parts) == 2:
                    return time(int(parts[0]), int(parts[1]))
                elif len(parts) == 3:
                    return time(int(parts[0]), int(parts[1]), int(parts[2]))
            raise ValueError(f"无效的时间格式: {time_str}")
        except (ValueError, IndexError):
            raise ValueError(f"无法解析时间: {time_str}") from None

    def get_non_class_times(self) -> Dict[str, str]:
        """获取非上课时间段配置

        将CSES格式的时间段转换为SecRandom使用的非上课时间段格式

        Returns:
            Dict[str, str]: 非上课时间段字典，格式为 {"name": "HH:MM:SS-HH:MM:SS"}
        """
        if not self.schedule_data:
            return {}

        non_class_times = {}
        schedule = self.schedule_data["schedule"]
        timeslots = schedule["timeslots"]

        # 按开始时间排序
        sorted_timeslots = sorted(timeslots, key=lambda x: x["start_time"])

        # 构建上课时间段列表
        class_periods = []
        for timeslot in sorted_timeslots:
            start_time = self._format_time_for_secrandom(timeslot["start_time"])
            end_time = self._format_time_for_secrandom(timeslot["end_time"])
            class_periods.append((start_time, end_time))

        # 生成非上课时间段
        # 1. 第一节课之前的时间
        if class_periods:
            first_start = class_periods[0][0]
            if first_start != "00:00:00":
                non_class_times["before_first_class"] = f"00:00:00-{first_start}"

        # 2. 课间时间（两节课之间）
        for i in range(len(class_periods) - 1):
            current_end = class_periods[i][1]
            next_start = class_periods[i + 1][0]
            if current_end != next_start:
                period_name = f"break_{i + 1}"
                non_class_times[period_name] = f"{current_end}-{next_start}"

        # 3. 最后一节课之后的时间
        if class_periods:
            last_end = class_periods[-1][1]
            if last_end != "23:59:59":
                non_class_times["after_last_class"] = f"{last_end}-23:59:59"

        logger.info(f"成功解析CSES课程表，生成{len(non_class_times)}个非上课时间段")
        return non_class_times

    def _format_time_for_secrandom(self, time_str: str) -> str:
        """将时间字符串格式化为SecRandom需要的格式 (HH:MM:SS)

        Args:
            time_str: 原始时间字符串 (HH:MM 或 HH:MM:SS)

        Returns:
            str: 格式化后的时间字符串 (HH:MM:SS)
        """
        if time_str.count(":") == 1:  # HH:MM 格式
            return f"{time_str}:00"
        return time_str

    def get_class_info(self) -> List[Dict]:
        """获取课程信息列表

        Returns:
            List[Dict]: 课程信息列表
        """
        if not self.schedule_data:
            return []

        schedule = self.schedule_data["schedule"]
        timeslots = schedule.get("timeslots", [])

        class_info = []
        for timeslot in timeslots:
            info = {
                "name": timeslot.get("name", ""),
                "start_time": timeslot.get("start_time", ""),
                "end_time": timeslot.get("end_time", ""),
                "teacher": timeslot.get("teacher", ""),
                "location": timeslot.get("location", ""),
                "day_of_week": timeslot.get("day_of_week", ""),
            }
            class_info.append(info)

        return class_info

    def get_summary(self) -> str:
        """获取课程表摘要信息

        Returns:
            str: 摘要信息
        """
        if not self.schedule_data:
            return "未加载课程表"

        schedule = self.schedule_data["schedule"]
        timeslots = schedule.get("timeslots", [])

        if not timeslots:
            return "课程表为空"

        # 获取最早和最晚时间
        start_times = [slot["start_time"] for slot in timeslots]
        end_times = [slot["end_time"] for slot in timeslots]

        summary = f"课程表包含{len(timeslots)}个时间段，"
        summary += f"最早开始时间：{min(start_times)}，"
        summary += f"最晚结束时间：{max(end_times)}"

        return summary
