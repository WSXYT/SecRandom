import os
from typing import Optional
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QWidget
from loguru import logger

from app.tools.settings_access import readme_settings_async
from app.tools.variable import FONT_APPLY_DELAY
from app.core.utils import safe_execute
from PySide6.QtGui import QFont, QFontDatabase
from app.tools.path_utils import get_data_path


def get_font_weight_file(weight_value: int) -> str:
    """根据字体粗细数值获取对应的字体文件名

    Args:
        weight_value: 字体粗细数值 (0-8)

    Returns:
        str: 对应的字体文件名
    """
    font_file_map = {
        0: "HarmonyOS_Sans_SC_Light.ttf",
        1: "HarmonyOS_Sans_SC_Light.ttf",
        2: "HarmonyOS_Sans_SC_Light.ttf",
        3: "HarmonyOS_Sans_SC_Medium.ttf",
        4: "HarmonyOS_Sans_SC_Medium.ttf",
        5: "HarmonyOS_Sans_SC_Medium.ttf",
        6: "HarmonyOS_Sans_SC_Bold.ttf",
        7: "HarmonyOS_Sans_SC_Bold.ttf",
        8: "HarmonyOS_Sans_SC_Bold.ttf",
    }
    return font_file_map.get(weight_value, "HarmonyOS_Sans_SC_Medium.ttf")


def load_font_by_weight(font_family: str, font_weight: int) -> str:
    """根据字体家族和粗细加载字体

    Args:
        font_family: 字体家族名称
        font_weight: 字体粗细数值 (0-8)

    Returns:
        str: 加载成功的字体家族名称
    """
    # 如果是默认字体，根据粗细加载对应的字体文件
    if font_family == "HarmonyOS Sans SC SC":
        font_file = get_font_weight_file(font_weight)
        logger.debug(f"根据粗细 {font_weight} 加载字体文件: {font_file}")
        font_path = get_data_path("font/HarmonyOS_Sans_SC", font_file)
        font_id = QFontDatabase.addApplicationFont(str(font_path))

        if font_id < 0:
            logger.exception(f"加载字体文件失败: {font_path}")
            return font_family

        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        logger.debug(f"已加载字体: {font_family} (粗细: {font_weight})")
        return font_family

    # 对于非默认字体，应用字体粗细到应用程序字体
    app_font = QApplication.font()
    app_font.setFamily(font_family)

    # 将数值映射到 QFont.Weight
    weight_map = {
        0: QFont.Weight.Thin,
        1: QFont.Weight.ExtraLight,
        2: QFont.Weight.Light,
        3: QFont.Weight.Normal,
        4: QFont.Weight.Medium,
        5: QFont.Weight.DemiBold,
        6: QFont.Weight.Bold,
        7: QFont.Weight.ExtraBold,
        8: QFont.Weight.Black,
    }
    font_weight_value = weight_map.get(font_weight, QFont.Weight.Normal)
    app_font.setWeight(font_weight_value)

    # 应用到所有控件
    for widget in QApplication.allWidgets():
        if isinstance(widget, QWidget):
            current_font = widget.font()
            if (
                current_font.family() != font_family
                or current_font.weight() != font_weight_value
            ):
                new_font = app_font
                new_font.setBold(current_font.bold())
                new_font.setItalic(current_font.italic())
                widget.setFont(new_font)

    logger.debug(f"已应用字体粗细: {font_family} (粗细值: {font_weight})")
    return font_family


def configure_dpi_scale() -> None:
    """在创建QApplication之前配置DPI缩放模式"""
    try:
        dpi_scale = readme_settings_async("basic_settings", "dpiScale")
        if dpi_scale == "Auto":
            _set_auto_dpi()
        else:
            _set_manual_dpi(dpi_scale)
    except Exception as e:
        logger.warning(f"读取DPI设置失败，使用默认设置: {e}")
        _set_auto_dpi()


def _set_auto_dpi() -> None:
    """设置自动DPI缩放"""
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    logger.debug("DPI缩放已设置为自动模式")


def _set_manual_dpi(scale: str) -> None:
    """设置手动DPI缩放

    Args:
        scale: 缩放倍数
    """
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(scale)
    logger.debug(f"DPI缩放已设置为{scale}倍")


def apply_font_settings() -> None:
    """应用字体设置 - 优化版本，使用字体管理器异步加载"""
    font_family = readme_settings_async("basic_settings", "font")
    font_weight_value = readme_settings_async("basic_settings", "font_weight")

    from qfluentwidgets import setFontFamilies

    # 根据字体粗细加载对应的字体文件
    actual_font_family = load_font_by_weight(
        font_family, int(font_weight_value) if font_weight_value else 3
    )
    setFontFamilies([actual_font_family])
    QTimer.singleShot(
        FONT_APPLY_DELAY,
        lambda: safe_execute(
            apply_font_to_application, actual_font_family, error_message="应用字体失败"
        ),
    )


def apply_font_to_application(font_family: str) -> None:
    """应用字体设置到整个应用程序，优化版本使用字体管理器

    Args:
        font_family: 字体家族名称
    """
    current_font = QApplication.font()
    app_font = current_font
    app_font.setFamily(font_family)

    widgets_updated = 0
    widgets_skipped = 0

    for widget in QApplication.allWidgets():
        if isinstance(widget, QWidget):
            if update_widget_fonts(widget, app_font, font_family):
                widgets_updated += 1
            else:
                widgets_skipped += 1

    logger.debug(
        f"已应用字体: {font_family}, 更新了{widgets_updated}个控件字体, "
        f"跳过了{widgets_skipped}个已有相同字体的控件"
    )


def update_widget_fonts(widget: Optional[QWidget], font, font_family: str) -> bool:
    """更新控件及其子控件的字体，优化版本减少内存占用，特别处理ComboBox等控件

    Args:
        widget: 要更新字体的控件
        font: 要应用的字体
        font_family: 目标字体家族名称

    Returns:
        bool: 是否更新了控件的字体
    """
    if widget is None:
        return False

    if not hasattr(widget, "font") or not hasattr(widget, "setFont"):
        return False

    current_widget_font = widget.font()
    if current_widget_font.family() == font_family:
        return False

    new_font = font
    new_font.setBold(current_widget_font.bold())
    new_font.setItalic(current_widget_font.italic())
    widget.setFont(new_font)

    if isinstance(widget, QWidget):
        children = widget.children()
        for child in children:
            if isinstance(child, QWidget):
                update_widget_fonts(child, font, font_family)

    return True
