# ==================================================
# 导入模块
# ==================================================
from qfluentwidgets import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtNetwork import *

from loguru import logger
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import comtypes
from comtypes import POINTER

from app.tools.variable import *
from app.tools.path_utils import *

# ==================================================
# 系统功能相关函数
# ==================================================
def restore_volume(volume_value):
    """跨平台音量恢复函数

    Args:
        volume_value (int): 音量值 (0-100)
    """
    # Windows音频控制
    try:
        # 初始化COM库
        comtypes.CoInitialize()

        # 获取默认音频设备
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
        volume = comtypes.cast(interface, POINTER(IAudioEndpointVolume))

        try:
            # 取消静音
            volume.SetMute(0, None)

            # 设置音量
            volume.SetMasterVolumeLevelScalar(volume_value / 100.0, None)
            logger.info(f"Windows音量设置为: {volume_value}%")
        finally:
            # 确保COM对象在释放COM库前被正确释放
            # 通过将对象设置为None来减少引用计数
            volume = None
            interface = None
            devices = None

            # 释放COM库
            comtypes.CoUninitialize()
    except Exception as e:
        logger.error(f"Windows音量控制失败: {e}")
