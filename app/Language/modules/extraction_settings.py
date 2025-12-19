# 抽取设置语言配置
extraction_settings = {
    "ZH_CN": {"title": {"name": "抽取设置", "description": "抽取功能设置"}}
}

# 点名设置语言配置
roll_call_settings = {
    "ZH_CN": {
        "title": {"name": "点名设置", "description": "点名功能设置"},
        "extraction_function": {
            "name": "抽取功能",
            "description": "设置点名抽取功能",
        },
        "display_settings": {
            "name": "显示设置",
            "description": "设置点名结果显示方式",
        },
        "basic_animation_settings": {
            "name": "动画设置",
            "description": "设置点名动画效果",
        },
        "color_theme_settings": {
            "name": "颜色主题设置",
            "description": "设置点名结果颜色主题",
        },
        "student_image_settings": {
            "name": "学生头像设置",
            "description": "设置点名结果中学生头像显示",
        },
        "music_settings": {"name": "音乐设置", "description": "设置点名时播放的音乐"},
        "draw_mode": {
            "name": "抽取模式",
            "description": "设置点名抽取模式",
            "combo_items": ["重复抽取", "不重复抽取", "半重复抽取"],
        },
        "clear_record": {
            "name": "清除抽取记录方式",
            "description": "设置清除抽取记录的时机",
            "combo_items": ["重启后清除", "直到全部抽取完"],
            "combo_items_other": ["重启后清除", "直到全部抽取完", "无需清除"],
        },
        "half_repeat": {
            "name": "半重复抽取次数",
            "description": "设置每人被抽中多少次后清除抽取记录",
        },
        "draw_type": {
            "name": "抽取方式",
            "description": "设置点名抽取方式",
            "combo_items": ["随机抽取", "公平抽取"],
        },
        "font_size": {"name": "字体大小", "description": "设置点名结果字体大小"},
        "display_format": {
            "name": "结果显示格式",
            "description": "设置点名结果显示格式",
            "combo_items": ["学号+姓名", "姓名", "学号"],
        },
        "show_random": {
            "name": "显示随机组员格式",
            "description": "设置随机组员显示格式",
            "combo_items": ["不显示", "组名[换行]姓名", "组名[短横杠]姓名"],
        },
        "animation": {
            "name": "动画模式",
            "description": "设置点名抽取动画效果",
            "combo_items": ["手动停止动画", "自动播放动画", "直接显示结果"],
        },
        "animation_interval": {
            "name": "动画间隔",
            "description": "设置点名动画间隔时间（毫秒）",
        },
        "autoplay_count": {
            "name": "自动播放次数",
            "description": "设置点名动画自动播放次数",
        },
        "animation_color_theme": {
            "name": "动画/结果颜色主题",
            "description": "设置点名动画/结果颜色主题",
            "combo_items": ["关闭", "随机颜色", "固定颜色"],
        },
        "animation_fixed_color": {
            "name": "动画/结果固定颜色",
            "description": "设置点名动画/结果固定颜色",
        },
        "student_image": {
            "name": "显示学生图片",
            "description": "设置是否显示学生图片",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "open_student_image_folder": {
            "name": "学生图片文件夹",
            "description": "管理学生图片文件，图片文件名需与学生姓名一致",
        },
    }
}

# 闪抽设置
quick_draw_settings = {
    "ZH_CN": {
        "title": {"name": "闪抽设置", "description": "闪抽功能设置"},
        "extraction_function": {
            "name": "抽取功能",
            "description": "设置闪抽抽取功能",
        },
        "display_settings": {
            "name": "显示设置",
            "description": "设置闪抽结果显示方式",
        },
        "basic_animation_settings": {
            "name": "动画设置",
            "description": "设置闪抽动画效果",
        },
        "color_theme_settings": {
            "name": "颜色主题设置",
            "description": "设置闪抽结果颜色主题",
        },
        "student_image_settings": {
            "name": "学生头像设置",
            "description": "设置闪抽结果中学生头像显示",
        },
        "music_settings": {"name": "音乐设置", "description": "设置闪抽时播放的音乐"},
        "draw_mode": {
            "name": "抽取模式",
            "description": "设置闪抽抽取模式",
            "combo_items": ["重复抽取", "不重复抽取", "半重复抽取"],
        },
        "clear_record": {
            "name": "清除抽取记录方式",
            "description": "设置清除闪抽抽取记录方式",
            "combo_items": ["重启后清除", "直到全部抽取完"],
            "combo_items_other": ["重启后清除", "直到全部抽取完", "无需清除"],
        },
        "half_repeat": {
            "name": "半重复抽取次数",
            "description": "设置每人被抽中多少次后清除抽取记录",
        },
        "draw_type": {
            "name": "抽取方式",
            "description": "设置闪抽抽取方式",
            "combo_items": ["随机抽取", "公平抽取"],
        },
        "font_size": {"name": "字体大小", "description": "设置闪抽结果字体大小"},
        "display_format": {
            "name": "结果显示格式",
            "description": "设置闪抽结果显示格式",
            "combo_items": ["学号+姓名", "姓名", "学号"],
        },
        "show_random": {
            "name": "显示随机组员格式",
            "description": "设置随机组员显示格式",
            "combo_items": ["不显示", "组名[换行]姓名", "组名[短横杠]姓名"],
        },
        "animation": {
            "name": "动画模式",
            "description": "设置闪抽抽取动画效果",
            "combo_items": ["自动播放动画", "直接显示结果"],
        },
        "animation_interval": {
            "name": "动画间隔",
            "description": "设置闪抽动画间隔时间(毫秒)",
        },
        "autoplay_count": {
            "name": "自动播放次数",
            "description": "设置闪抽动画自动播放次数",
        },
        "animation_color_theme": {
            "name": "动画/结果颜色主题",
            "description": "设置闪抽动画/结果颜色主题",
            "combo_items": ["关闭", "随机颜色", "固定颜色"],
        },
        "animation_fixed_color": {
            "name": "动画/结果固定颜色",
            "description": "设置闪抽动画/结果固定颜色",
        },
        "student_image": {
            "name": "显示学生图片",
            "description": "设置是否显示学生图片",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "open_student_image_folder": {
            "name": "学生图片文件夹",
            "description": "管理学生图片文件，图片文件名需与学生姓名一致",
        },
    }
}

# 即抽设置
instant_draw_settings = {
    "ZH_CN": {
        "title": {"name": "即抽设置", "description": "即抽功能设置"},
        "extraction_function": {
            "name": "抽取功能",
            "description": "设置即抽抽取功能",
        },
        "display_settings": {
            "name": "显示设置",
            "description": "设置即抽结果显示方式",
        },
        "basic_animation_settings": {
            "name": "动画设置",
            "description": "设置即抽动画效果",
        },
        "color_theme_settings": {
            "name": "颜色主题设置",
            "description": "设置即抽结果颜色主题",
        },
        "student_image_settings": {
            "name": "学生头像设置",
            "description": "设置即抽结果中学生头像显示",
        },
        "music_settings": {"name": "音乐设置", "description": "设置即抽时播放的音乐"},
        "draw_mode": {
            "name": "抽取模式",
            "description": "设置即抽抽取模式",
            "combo_items": ["重复抽取", "不重复抽取", "半重复抽取"],
        },
        "clear_record": {
            "name": "清除抽取记录方式",
            "description": "设置清除即抽抽取记录方式",
            "combo_items": ["重启后清除", "直到全部抽取完"],
            "combo_items_other": ["重启后清除", "直到全部抽取完", "无需清除"],
        },
        "half_repeat": {
            "name": "半重复抽取次数",
            "description": "设置每人被抽中多少次后清除抽取记录",
        },
        "draw_type": {
            "name": "抽取方式",
            "description": "设置即抽抽取方式",
            "combo_items": ["随机抽取", "公平抽取"],
        },
        "font_size": {"name": "字体大小", "description": "设置即抽结果字体大小"},
        "display_format": {
            "name": "结果显示格式",
            "description": "设置即抽结果显示格式",
            "combo_items": ["学号+姓名", "姓名", "学号"],
        },
        "show_random": {
            "name": "显示随机组员格式",
            "description": "设置随机组员显示格式",
            "combo_items": ["不显示", "组名[换行]姓名", "组名[短横杠]姓名"],
        },
        "animation": {
            "name": "动画模式",
            "description": "设置即抽抽取动画效果",
            "combo_items": ["自动播放动画", "直接显示结果"],
        },
        "animation_interval": {
            "name": "动画间隔",
            "description": "设置即抽动画间隔时间(毫秒)",
        },
        "autoplay_count": {
            "name": "自动播放次数",
            "description": "设置即抽动画自动播放次数",
        },
        "animation_color_theme": {
            "name": "动画/结果颜色主题",
            "description": "设置即抽动画/结果颜色主题",
            "combo_items": ["关闭", "随机颜色", "固定颜色"],
        },
        "animation_fixed_color": {
            "name": "动画/结果固定颜色",
            "description": "设置即抽动画/结果固定颜色",
        },
        "student_image": {
            "name": "显示学生图片",
            "description": "设置是否显示学生图片",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "open_student_image_folder": {
            "name": "学生图片文件夹",
            "description": "管理学生图片文件，图片文件名需与学生姓名一致",
        },
    }
}

# 自定义抽设置
custom_draw_settings = {
    "ZH_CN": {"title": {"name": "自定义抽设置", "description": "自定义抽取功能设置"}},
    "EN_US": {
        "title": {
            "name": "Custom pick settings",
            "description": "Custom pick settings",
        },
    },
}

# 抽奖设置
lottery_settings = {
    "ZH_CN": {
        "title": {"name": "抽奖设置", "description": "抽奖功能设置"},
        "extraction_function": {
            "name": "抽取功能",
            "description": "设置抽奖抽取功能",
        },
        "display_settings": {
            "name": "显示设置",
            "description": "设置抽奖结果显示方式",
        },
        "basic_animation_settings": {
            "name": "动画设置",
            "description": "设置抽奖动画效果",
        },
        "color_theme_settings": {
            "name": "颜色主题设置",
            "description": "设置抽奖结果颜色主题",
        },
        "lottery_image_settings": {
            "name": "奖品图片设置",
            "description": "设置抽奖结果中奖品图片显示",
        },
        "music_settings": {"name": "音乐设置", "description": "设置抽奖时播放的音乐"},
        "draw_mode": {
            "name": "抽取模式",
            "description": "设置抽奖抽取模式",
            "combo_items": ["重复抽取", "不重复抽取", "半重复抽取"],
        },
        "clear_record": {
            "name": "清除抽取记录方式",
            "description": "设置清除抽奖抽取记录方式",
            "combo_items": ["重启后清除", "直到全部抽取完"],
            "combo_items_other": ["重启后清除", "直到全部抽取完", "无需清除"],
        },
        "half_repeat": {
            "name": "半重复抽取次数",
            "description": "设置每人被抽中多少次后清除抽取记录",
        },
        "draw_type": {
            "name": "抽取方式",
            "description": "设置抽奖抽取方式",
            "combo_items": ["随机抽取", "公平抽取"],
        },
        "font_size": {"name": "字体大小", "description": "设置抽奖结果字体大小"},
        "display_format": {
            "name": "结果显示格式",
            "description": "设置抽奖结果显示格式",
            "combo_items": ["序号+名称", "名称", "序号"],
        },
        "animation": {
            "name": "动画模式",
            "description": "设置抽奖抽取动画效果",
            "combo_items": ["手动停止动画", "自动播放动画", "直接显示结果"],
        },
        "animation_interval": {
            "name": "动画间隔",
            "description": "设置抽奖动画间隔时间(毫秒)",
        },
        "autoplay_count": {
            "name": "自动播放次数",
            "description": "设置抽奖动画自动播放次数",
        },
        "animation_color_theme": {
            "name": "动画/结果颜色主题",
            "description": "设置抽奖动画/结果颜色主题",
            "combo_items": ["关闭", "随机颜色", "固定颜色"],
        },
        "animation_fixed_color": {
            "name": "动画/结果固定颜色",
            "description": "设置抽奖动画/结果固定颜色",
        },
        "lottery_image": {
            "name": "显示奖品图片",
            "description": "设置是否显示奖品图片",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "open_lottery_image_folder": {
            "name": "奖品图片文件夹",
            "description": "管理奖品图片文件，图片文件名需与奖品名称一致",
        },
    }
}
