# 通知设置语言配置
notification_settings = {
    "ZH_CN": {"title": {"name": "通知设置", "description": "通知功能设置"}},
    "EN_US": {
        "title": {
            "name": "Notification settings",
            "description": "Notification settings",
        }
    },
}

# 通用通知文本
notification_common = {
    "ZH_CN": {
        "notification_result": {
            "name": "通知结果",
            "description": "通用通知结果窗口标题",
        }
    },
    "EN_US": {
        "notification_result": {
            "name": "Notice results",
            "description": "Generic notification result window title",
        }
    },
}

# 点名通知设置语言配置
roll_call_notification_settings = {
    "ZH_CN": {
        "title": {"name": "点名通知设置", "description": "点名通知功能设置"},
        "basic_settings": {"name": "基础设置", "description": "配置通知显示基础参数"},
        "window_mode": {
            "name": "窗口模式",
            "description": "配置点名通知窗口显示方式",
        },
        "floating_window_mode": {
            "name": "浮窗模式",
            "description": "配置点名通知浮窗行为",
        },
        "call_notification_service": {
            "name": "调用通知服务",
            "description": "启用后调用系统通知服务发送点名结果",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "animation": {
            "name": "动画效果",
            "description": "控制点名通知窗口动画效果显示",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "floating_window_enabled_monitor": {
            "name": "显示器选择",
            "description": "选择显示点名通知浮窗的显示器",
        },
        "floating_window_position": {
            "name": "浮窗位置",
            "description": "设置点名通知浮窗屏幕显示位置",
            "combo_items": [
                "中心",
                "顶部",
                "底部",
                "左侧",
                "右侧",
                "顶部左侧",
                "顶部右侧",
                "底部左侧",
                "底部右侧",
            ],
        },
        "floating_window_horizontal_offset": {
            "name": "水平偏移",
            "description": "调整点名通知浮窗相对默认位置水平偏移量（像素）",
        },
        "floating_window_vertical_offset": {
            "name": "垂直偏移",
            "description": "调整点名通知浮窗相对默认位置垂直偏移量（像素）",
        },
        "floating_window_transparency": {
            "name": "透明度",
            "description": "调整点名通知浮窗透明度，数值越小越透明（0-100）",
        },
        "floating_window_auto_close_time": {
            "name": "浮窗自动关闭时间",
            "description": "设置浮窗自动关闭时间（秒），设为0表示不自动关闭",
        },
    },
    "EN_US": {
        "title": {
            "name": "Picking notification settings",
            "description": "Picking notification settings",
        },
        "basic_settings": {
            "name": "Basic settings",
            "description": "Configure notification display base parameters",
        },
        "window_mode": {
            "name": "Window mode",
            "description": "Configure generic pick notification window display method",
        },
        "floating_window_mode": {
            "name": "Floating window mode",
            "description": "Configure generic pick notification floating window behavior mode",
        },
        "call_notification_service": {
            "name": "Call notification service",
            "description": "Call the system notification service to send the picking result when enabled",
        },
        "animation": {
            "name": "Animation",
            "description": "Configure Pick notification window display animation effect",
        },
        "floating_window_enabled_monitor": {
            "name": "Monitor select",
            "description": "Select the display monitor for picking notification floating windows",
        },
        "floating_window_position": {
            "name": "Floating window position",
            "description": "Configure picking notification floating window on-screen display position",
            "combo_items": {
                "0": "Center",
                "1": "Top",
                "2": "Bottom",
                "3": "Left",
                "4": "Right",
                "5": "Top left",
                "6": "Top right",
                "7": "Bottom left",
                "8": "Bottom right",
            },
        },
        "floating_window_horizontal_offset": {
            "name": "Horizontal offset",
            "description": "Configure the horizontal offset (in pixels) for the pick notification floating window relative to the default position",
        },
        "floating_window_vertical_offset": {
            "name": "Vertical offset",
            "description": "Configure the vertical offset (in pixels) for the pick notification floating window relative to the default position",
        },
        "floating_window_transparency": {
            "name": "Transparency",
            "description": "Configure pick notification floating window transparency, where a smaller value indicates higher transparency (0-100)",
        },
        "floating_window_auto_close_time": {
            "name": "Floating window auto-close time",
            "description": "Set the time to close the floating window automatically (second), set to 0 to not close automatically",
        },
    },
}

# 闪抽通知设置
quick_draw_notification_settings = {
    "ZH_CN": {
        "title": {
            "name": "闪抽通知设置",
            "description": "配置闪抽结果通知显示方式和参数",
        },
        "basic_settings": {
            "name": "基础设置",
            "description": "配置闪抽通知基础显示参数",
        },
        "window_mode": {
            "name": "窗口模式",
            "description": "设置闪抽通知窗口显示方式",
        },
        "floating_window_mode": {
            "name": "浮窗模式",
            "description": "设置闪抽通知浮窗行为模式",
        },
        "animation": {
            "name": "动画",
            "description": "设置闪抽通知窗口显示动画效果",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "floating_window_enabled_monitor": {
            "name": "选择闪抽通知显示的显示器",
            "description": "选择闪抽通知浮窗显示器",
        },
        "floating_window_position": {
            "name": "浮窗位置",
            "description": "设置闪抽通知浮窗屏幕显示位置",
            "combo_items": [
                "中心",
                "顶部",
                "底部",
                "左侧",
                "右侧",
                "顶部左侧",
                "顶部右侧",
                "底部左侧",
                "底部右侧",
            ],
        },
        "floating_window_horizontal_offset": {
            "name": "水平偏移",
            "description": "设置闪抽通知浮窗相对默认位置水平偏移量（像素）",
        },
        "floating_window_vertical_offset": {
            "name": "垂直偏移",
            "description": "设置闪抽通知浮窗相对默认位置垂直偏移量（像素）",
        },
        "floating_window_transparency": {
            "name": "浮窗透明度",
            "description": "设置闪抽通知浮窗透明度，数值越小越透明（0-100）",
        },
        "floating_window_auto_close_time": {
            "name": "浮窗自动关闭时间",
            "description": "设置浮窗自动关闭时间（秒），设为0表示不自动关闭",
        },
    },
    "EN_US": {
        "title": {
            "name": "Quick Pick notification settings",
            "description": "Configure Quick Pick result notification display method and parameters",
        },
        "basic_settings": {
            "name": "Basic settings",
            "description": "Configure Quick Pick notification basic display parameters",
        },
        "window_mode": {
            "name": "Window mode",
            "description": "Configure Quick Pick notification window display method",
        },
        "floating_window_mode": {
            "name": "Floating window mode",
            "description": "Configure Quick Pick notification floating window behavior mode",
        },
        "animation": {
            "name": "Animation",
            "description": "Configure Quick Pick notification window display animation effect",
        },
        "floating_window_enabled_monitor": {
            "name": "Select the display monitor for Quick Pick notifications",
            "description": "Select the display monitor for Quick Pick notification floating windows",
        },
        "floating_window_position": {
            "name": "Floating window position",
            "description": "Configure Quick Pick notification floating window on-screen display position",
            "combo_items": {
                "0": "Center",
                "1": "Top",
                "2": "Bottom",
                "3": "Left",
                "4": "Right",
                "5": "Top left",
                "6": "Top right",
                "7": "Bottom left",
                "8": "Bottom right",
            },
        },
        "floating_window_horizontal_offset": {
            "name": "Horizontal offset",
            "description": "Configure the horizontal offset (in pixels) for the Quick Pick notification floating window relative to the default position",
        },
        "floating_window_vertical_offset": {
            "name": "Vertical offset",
            "description": "Configure the vertical offset (in pixels) for the Quick Pick notification floating window relative to the default position",
        },
        "floating_window_transparency": {
            "name": "Floating window transparency",
            "description": "Configure Quick Pick notification floating window transparency, where a smaller value indicates higher transparency (0-100)",
        },
        "floating_window_auto_close_time": {
            "name": "Floating window auto-close time",
            "description": "Set the time to close the floating window automatically (seconds), set to 0 to not close automatically",
        },
    },
}

# 即抽通知设置
instant_draw_notification_settings = {
    "ZH_CN": {
        "title": {
            "name": "即抽通知设置",
            "description": "配置即抽结果通知显示方式和参数",
        },
        "basic_settings": {
            "name": "基础设置",
            "description": "配置即抽通知基础显示参数",
        },
        "window_mode": {
            "name": "窗口模式",
            "description": "设置即抽通知窗口显示方式",
        },
        "floating_window_mode": {
            "name": "浮窗模式",
            "description": "设置即抽通知浮窗行为模式",
        },
        "animation": {
            "name": "动画",
            "description": "设置即抽通知窗口显示动画效果",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "floating_window_enabled_monitor": {
            "name": "选择即抽通知显示的显示器",
            "description": "选择即抽通知浮窗显示器",
        },
        "floating_window_position": {
            "name": "浮窗位置",
            "description": "设置即抽通知浮窗屏幕显示位置",
            "combo_items": [
                "中心",
                "顶部",
                "底部",
                "左侧",
                "右侧",
                "顶部左侧",
                "顶部右侧",
                "底部左侧",
                "底部右侧",
            ],
        },
        "floating_window_horizontal_offset": {
            "name": "水平偏移",
            "description": "设置即抽通知浮窗相对默认位置水平偏移量（像素）",
        },
        "floating_window_vertical_offset": {
            "name": "垂直偏移",
            "description": "设置即抽通知浮窗相对默认位置垂直偏移量（像素）",
        },
        "floating_window_transparency": {
            "name": "浮窗透明度",
            "description": "设置即抽通知浮窗透明度，数值越小越透明（0-100）",
        },
        "floating_window_auto_close_time": {
            "name": "浮窗自动关闭时间",
            "description": "设置浮窗自动关闭时间（秒），设为0表示不自动关闭",
        },
    },
    "EN_US": {
        "title": {
            "name": "Instant Pick notification settings",
            "description": "Configure Instant Pick result notification display method and parameters",
        },
        "basic_settings": {
            "name": "Basic settings",
            "description": "Configure Instant Pick notification basic display parameters",
        },
        "window_mode": {
            "name": "Window mode",
            "description": "Configure Instant Pick notification window display method",
        },
        "floating_window_mode": {
            "name": "Floating window mode",
            "description": "Configure Instant Pick notification floating window behavior mode",
        },
        "animation": {
            "name": "Animation",
            "description": "Configure Instant Pick notification window display animation effect",
        },
        "floating_window_enabled_monitor": {
            "name": "Select the display monitor for Instant Pick notification floating windows",
            "description": "Select the display monitor for Instant Pick notification floating windows",
        },
        "floating_window_position": {
            "name": "Floating window position",
            "description": "Configure Instant Pick notification floating window on-screen display position",
            "combo_items": {
                "0": "Center",
                "1": "Top",
                "2": "Bottom",
                "3": "Left",
                "4": "Right",
                "5": "Top left",
                "6": "Top right",
                "7": "Bottom left",
                "8": "Bottom right",
            },
        },
        "floating_window_horizontal_offset": {
            "name": "Horizontal offset",
            "description": "Configure the horizontal offset (in pixels) for the Instant Pick notification floating window relative to the default position",
        },
        "floating_window_vertical_offset": {
            "name": "Vertical offset",
            "description": "Configure the vertical offset (in pixels) for the Instant Pick notification floating window relative to the default position",
        },
        "floating_window_transparency": {
            "name": "Floating window transparency",
            "description": "Configure Instant Pick notification floating window transparency, where a smaller value indicates higher transparency (0-100)",
        },
        "floating_window_auto_close_time": {
            "name": "Floating window auto-close time",
            "description": "Set the time to close the floating window automatically (seconds), set to 0 to not close automatically",
        },
    },
}

# 自定义抽通知设置
custom_draw_notification_settings = {
    "ZH_CN": {
        "title": {"name": "自定义抽通知设置", "description": "自定义抽取通知功能设置"},
        "basic_settings": {"name": "基础设置", "description": "基础功能设置"},
        "window_mode": {
            "name": "窗口模式",
            "description": "设置自定义抽取通知窗口显示方式",
        },
        "floating_window_mode": {
            "name": "浮窗模式",
            "description": "设置自定义抽取通知浮窗行为模式",
        },
        "call_notification_service": {
            "name": "调用通知服务",
            "description": "是否调用系统通知服务发送自定义抽取结果",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "animation": {
            "name": "动画",
            "description": "设置自定义抽取通知窗口显示动画效果",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "floating_window_enabled_monitor": {
            "name": "选择自定义抽取通知显示的显示器",
            "description": "选择自定义抽取通知浮窗显示器",
        },
        "floating_window_position": {
            "name": "浮窗位置",
            "description": "设置自定义抽取通知浮窗屏幕显示位置",
            "combo_items": [
                "中心",
                "顶部",
                "底部",
                "左侧",
                "右侧",
                "顶部左侧",
                "顶部右侧",
                "底部左侧",
                "底部右侧",
            ],
        },
        "floating_window_horizontal_offset": {
            "name": "水平偏移",
            "description": "设置自定义抽取通知浮窗相对默认位置水平偏移量（像素）",
        },
        "floating_window_vertical_offset": {
            "name": "垂直偏移",
            "description": "设置自定义抽取通知浮窗相对默认位置垂直偏移量（像素）",
        },
        "floating_window_transparency": {
            "name": "浮窗透明度",
            "description": "设置自定义抽取通知浮窗透明度，数值越小越透明（0-100）",
        },
        "floating_window_auto_close_time": {
            "name": "浮窗自动关闭时间",
            "description": "设置浮窗自动关闭时间（秒），设为0表示不自动关闭",
        },
    },
    "EN_US": {
        "title": {
            "name": "Custom pick notification settings",
            "description": "Custom pick settings",
        },
        "basic_settings": {"name": "Basic settings", "description": "Basic settings"},
        "window_mode": {
            "name": "Window mode",
            "description": "Configure custom pick notification window display method",
        },
        "floating_window_mode": {
            "name": "Floating window mode",
            "description": "Configure custom pick notification floating window behavior mode",
        },
        "call_notification_service": {
            "name": "Call notification service",
            "description": "Whether to call the system notification service to send custom pick results",
        },
        "animation": {
            "name": "Animation",
            "description": "Configure custom pick notification window display animation effect",
        },
        "floating_window_enabled_monitor": {
            "name": "Select the display monitor for custom pick notifications",
            "description": "Select the display monitor for custom pick notification floating windows",
        },
        "floating_window_position": {
            "name": "Floating window position",
            "description": "Configure custom pick notification floating window on-screen display position",
            "combo_items": {
                "0": "Center",
                "1": "Top",
                "2": "Bottom",
                "3": "Left",
                "4": "Right",
                "5": "Top left",
                "6": "Top right",
                "7": "Bottom left",
                "8": "Bottom right",
            },
        },
        "floating_window_horizontal_offset": {
            "name": "Horizontal offset",
            "description": "Configure the horizontal offset (in pixels) for the custom pick notification floating window relative to the default position",
        },
        "floating_window_vertical_offset": {
            "name": "Vertical offset",
            "description": "Configure the vertical offset (in pixels) for the custom pick notification floating window relative to the default position",
        },
        "floating_window_transparency": {
            "name": "Floating window transparency",
            "description": "Configure custom pick notification floating window transparency, where a smaller value indicates higher transparency (0-100)",
        },
        "floating_window_auto_close_time": {
            "name": "Floating window auto-close time",
            "description": "Set the time to close the floating window automatically (seconds), set to 0 to not close automatically",
        },
    },
}

# 抽奖通知设置
lottery_notification_settings = {
    "ZH_CN": {
        "title": {
            "name": "抽奖通知设置",
            "description": "配置抽奖结果通知显示方式和参数",
        },
        "basic_settings": {
            "name": "基础设置",
            "description": "配置抽奖通知基础显示参数",
        },
        "window_mode": {
            "name": "窗口模式",
            "description": "设置抽奖通知窗口显示方式",
        },
        "floating_window_mode": {
            "name": "浮窗模式",
            "description": "设置抽奖通知浮窗行为模式",
        },
        "call_notification_service": {
            "name": "调用通知服务",
            "description": "是否调用系统通知服务发送抽奖结果",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "animation": {
            "name": "动画",
            "description": "设置抽奖通知窗口显示动画效果",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "floating_window_enabled_monitor": {
            "name": "选择抽奖通知显示的显示器",
            "description": "选择抽奖通知浮窗显示器",
        },
        "floating_window_position": {
            "name": "浮窗位置",
            "description": "设置抽奖通知浮窗屏幕显示位置",
            "combo_items": [
                "中心",
                "顶部",
                "底部",
                "左侧",
                "右侧",
                "顶部左侧",
                "顶部右侧",
                "底部左侧",
                "底部右侧",
            ],
        },
        "floating_window_horizontal_offset": {
            "name": "水平偏移",
            "description": "设置抽奖通知浮窗相对默认位置水平偏移量（像素）",
        },
        "floating_window_vertical_offset": {
            "name": "垂直偏移",
            "description": "设置抽奖通知浮窗相对默认位置垂直偏移量（像素）",
        },
        "floating_window_transparency": {
            "name": "浮窗透明度",
            "description": "设置抽奖通知浮窗透明度，数值越小越透明（0-100）",
        },
        "floating_window_auto_close_time": {
            "name": "浮窗自动关闭时间",
            "description": "设置浮窗自动关闭时间（秒），设为0表示不自动关闭",
        },
    },
    "EN_US": {
        "title": {
            "name": "Lottery notification settings",
            "description": "Configure lottery result notification display method and parameters",
        },
        "basic_settings": {
            "name": "Basic settings",
            "description": "Configure lottery notification basic display parameters",
        },
        "window_mode": {
            "name": "Window mode",
            "description": "Configure lottery notification window display method",
        },
        "floating_window_mode": {
            "name": "Floating window mode",
            "description": "Configure lottery notification floating window behavior mode",
        },
        "call_notification_service": {
            "name": "Call notification service",
            "description": "Whether to call the system notification service to send lottery results",
        },
        "animation": {
            "name": "Animation",
            "description": "Configure lottery notification window display animation effect",
        },
        "floating_window_enabled_monitor": {
            "name": "Select the display monitor for lottery notifications",
            "description": "Select the display monitor for lottery notification floating windows",
        },
        "floating_window_position": {
            "name": "Floating window position",
            "description": "Configure lottery notification floating window on-screen display position",
            "combo_items": {
                "0": "Center",
                "1": "Top",
                "2": "Bottom",
                "3": "Left",
                "4": "Right",
                "5": "Top left",
                "6": "Top right",
                "7": "Bottom left",
                "8": "Bottom right",
            },
        },
        "floating_window_horizontal_offset": {
            "name": "Horizontal offset",
            "description": "Configure the horizontal offset (in pixels) for the lottery notification floating window relative to the default position",
        },
        "floating_window_vertical_offset": {
            "name": "Vertical offset",
            "description": "Configure the vertical offset (in pixels) for the lottery notification floating window relative to the default position",
        },
        "floating_window_transparency": {
            "name": "Floating window transparency",
            "description": "Configure lottery notification floating window transparency, where a smaller value indicates higher transparency (0-100)",
        },
        "floating_window_auto_close_time": {
            "name": "Floating window auto-close time",
            "description": "Set the time to close the floating window automatically (seconds), set to 0 to not close automatically",
        },
    },
}
