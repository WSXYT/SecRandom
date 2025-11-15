# 抽取设置语言配置
extraction_settings = {
    "ZH_CN": {
        "title": {"name": "抽取设置", "description": "抽取设置"}
    }
}

# 点名设置语言配置
roll_call_settings = {
    "ZH_CN": {
        "title": {"name": "点名设置", "description": "点名设置"},
        "extraction_function": {
            "name": "抽取功能",
            "description": "点名抽取功能相关设置",
        },
        "display_settings": {"name": "显示设置", "description": "点名结果显示相关设置"},
        "basic_animation_settings": {
            "name": "动画设置",
            "description": "点名动画效果相关设置",
        },
        "color_theme_settings": {
            "name": "颜色主题设置",
            "description": "点名结果显示的颜色主题相关设置",
        },
        "student_image_settings": {
            "name": "学生头像设置",
            "description": "点名结果显示的学生头像相关设置",
        },
        "music_settings": {"name": "音乐设置", "description": "点名音乐相关设置"},
        "draw_mode": {
            "name": "抽取模式",
            "description": "设置点名抽取的模式",
            "combo_items": ["重复抽取", "不重复抽取", "半重复抽取"],
        },
        "clear_record": {
            "name": "自动清除点名抽取记录",
            "description": "设置何时自动清除点名抽取记录",
            "combo_items": ["重启后清除", "直到全部抽取完"],
            "combo_items_other": ["重启后清除", "直到全部抽取完", "无需清除"],
        },
        "half_repeat": {
            "name": "半重复抽取次数",
            "description": "设置一个学生在重置抽取记录前最多能被抽取几次",
        },
        "clear_time": {
            "name": "抽取后定时清除时间",
            "description": "设置抽取后定时清除记录的时间(秒)",
        },
        "draw_type": {
            "name": "抽取方式",
            "description": "设置点名抽取的方式",
            "combo_items": ["随机抽取", "公平抽取"],
        },
        "font_size": {"name": "字体大小", "description": "设置点名结果显示的字体大小"},
        "display_format": {
            "name": "结果显示格式",
            "description": "设置点名结果的显示格式",
            "combo_items": ["学号+姓名", "姓名", "学号"],
        },
        "show_random": {
            "name": "显示随机组员格式",
            "description": "设置随机组员的显示格式",
            "combo_items": ["不显示", "组名[换行]姓名", "组名[短横杠]姓名"],
        },
        "animation": {
            "name": "动画模式",
            "description": "设置点名抽取的动画效果",
            "combo_items": ["手动停止动画", "自动播放动画", "直接显示结果"],
        },
        "animation_interval": {
            "name": "动画间隔",
            "description": "设置点名动画的间隔时间(毫秒)",
        },
        "autoplay_count": {
            "name": "自动播放次数",
            "description": "设置点名动画自动播放的次数",
        },
        "animation_color_theme": {
            "name": "动画颜色主题",
            "description": "设置点名动画的颜色主题",
            "combo_items": ["关闭", "随机颜色", "固定颜色"],
        },
        "result_color_theme": {
            "name": "结果颜色主题",
            "description": "设置点名结果显示的颜色主题",
            "combo_items": ["关闭", "随机颜色", "固定颜色"],
        },
        "animation_fixed_color": {
            "name": "动画固定颜色",
            "description": "设置点名动画的固定颜色",
        },
        "result_fixed_color": {
            "name": "结果固定颜色",
            "description": "设置点名结果显示的固定颜色",
        },
        "student_image": {
            "name": "显示学生图片",
            "description": "设置是否显示学生图片",
            "switchbutton_name": {"enable": "显示", "disable": "隐藏"},
        },
        "open_student_image_folder": {
            "name": "学生图片文件夹",
            "description": "管理学生图片文件,图片文件名需与学生姓名一致",
        },
        "animation_music": {
            "name": "动画音乐",
            "description": "设置是否播放动画音乐",
            "switchbutton_name": {"enable": "播放", "disable": "关闭"},
        },
        "result_music": {
            "name": "结果音乐",
            "description": "设置是否播放结果音乐",
            "switchbutton_name": {"enable": "播放", "disable": "关闭"},
        },
        "open_animation_music_folder": {
            "name": "打开动画音乐文件夹",
            "description": "管理动画音乐文件并支持随机播放功能",
        },
        "open_result_music_folder": {
            "name": "打开结果音乐文件夹",
            "description": "管理结果音乐文件并支持随机播放功能",
        },
        "animation_music_volume": {
            "name": "动画音乐音量",
            "description": "设置动画音乐的音量",
        },
        "result_music_volume": {
            "name": "结果音乐音量",
            "description": "设置结果音乐的音量",
        },
        "animation_music_fade_in": {
            "name": "动画音乐淡入时间",
            "description": "设置动画音乐淡入的时间",
        },
        "result_music_fade_in": {
            "name": "结果音乐淡入时间",
            "description": "设置结果音乐淡入的时间",
        },
        "animation_music_fade_out": {
            "name": "动画音乐淡出时间",
            "description": "设置动画音乐淡出的时间",
        },
        "result_music_fade_out": {
            "name": "结果音乐淡出时间",
            "description": "设置结果音乐淡出的时间",
        },
    }
}

# 闪抽设置
quick_draw_settings = {
    "ZH_CN": {
        "title": {"name": "闪抽设置","description": "闪抽设置"},
        "extraction_function": {
            "name": "抽取功能",
            "description": "闪抽抽取功能相关设置"
        },
        "display_settings": {
            "name": "显示设置",
            "description": "闪抽结果显示相关设置"
        },
        "basic_animation_settings": {
            "name": "动画设置",
            "description": "闪抽动画效果相关设置"
        },
        "color_theme_settings": {
            "name": "颜色主题设置",
            "description": "闪抽结果显示的颜色主题相关设置"
        },
        "student_image_settings": {
            "name": "学生头像设置",
            "description": "闪抽结果显示的学生头像相关设置"
        },
        "music_settings": {
            "name": "音乐设置",
            "description": "闪抽音乐相关设置"
        },
        "draw_mode": {
            "name": "抽取模式",
            "description": "设置闪抽抽取的模式",
            "combo_items": ["重复抽取","不重复抽取","半重复抽取"]
        },
        "clear_record": {
            "name": "清除抽取记录方式",
            "description": "设置清除闪抽抽取记录的方式",
            "combo_items": ["重启后清除","直到全部抽取完"],
            "combo_items_other": ["重启后清除","直到全部抽取完","无需清除"]
        },
        "half_repeat": {
            "name": "半重复抽取次数",
            "description": "设置半重复抽取的次数"
        },
        "clear_time": {
            "name": "抽取后定时清除时间",
            "description": "设置抽取后定时清除记录的时间(秒)"
        },
        "draw_type": {
            "name": "抽取方式",
            "description": "设置闪抽抽取的方式",
            "combo_items": ["随机抽取","公平抽取"]
        },
        "font_size": {
            "name": "字体大小",
            "description": "设置闪抽结果显示的字体大小"
        },
        "display_format": {
            "name": "结果显示格式",
            "description": "设置闪抽结果的显示格式",
            "combo_items": ["学号+姓名","姓名","学号"]
        },
        "show_random": {
            "name": "显示随机组员格式",
            "description": "设置随机组员的显示格式",
            "combo_items": ["不显示","组名[换行]姓名","组名[短横杠]姓名"]
        },
        "animation": {
            "name": "动画模式",
            "description": "设置闪抽抽取的动画效果",
            "combo_items": ["手动停止动画","自动播放动画","直接显示结果"]
        },
        "animation_interval": {
            "name": "动画间隔",
            "description": "设置闪抽动画的间隔时间(毫秒)"
        },
        "autoplay_count": {
            "name": "自动播放次数",
            "description": "设置闪抽动画自动播放的次数"
        },
        "animation_color_theme": {
            "name": "动画颜色主题",
            "description": "设置闪抽动画的颜色主题",
            "combo_items": ["关闭","随机颜色","固定颜色"]
        },
        "result_color_theme": {
            "name": "结果颜色主题",
            "description": "设置闪抽结果显示的颜色主题",
            "combo_items": ["关闭","随机颜色","固定颜色"]
        },
        "animation_fixed_color": {
            "name": "动画固定颜色",
            "description": "设置闪抽动画的固定颜色"
        },
        "result_fixed_color": {
            "name": "结果固定颜色",
            "description": "设置闪抽结果显示的固定颜色"
        },
        "student_image": {
            "name": "显示学生图片",
            "description": "设置是否显示学生图片",
            "switchbutton_name": {"enable": "显示","disable": "隐藏"}
        },
        "open_student_image_folder": {
            "name": "学生图片文件夹",
            "description": "管理学生图片文件,图片文件名需与学生姓名一致"
        },
        "animation_music": {
            "name": "动画音乐",
            "description": "设置是否播放动画音乐",
            "switchbutton_name": {"enable": "播放","disable": "关闭"}
        },
        "result_music": {
            "name": "结果音乐",
            "description": "设置是否播放结果音乐",
            "switchbutton_name": {"enable": "播放","disable": "关闭"}
        },
        "open_animation_music_folder": {
            "name": "打开动画音乐文件夹",
            "description": "管理动画音乐文件并支持随机播放功能"
        },
        "open_result_music_folder": {
            "name": "打开结果音乐文件夹",
            "description": "管理结果音乐文件并支持随机播放功能"
        },
        "animation_music_volume": {
            "name": "动画音乐音量",
            "description": "设置动画音乐的音量"
        },
        "result_music_volume": {
            "name": "结果音乐音量",
            "description": "设置结果音乐的音量"
        },
        "animation_music_fade_in": {
            "name": "动画音乐淡入时间",
            "description": "设置动画音乐淡入的时间"
        },
        "result_music_fade_in": {
            "name": "结果音乐淡入时间",
            "description": "设置结果音乐淡入的时间"
        },
        "animation_music_fade_out": {
            "name": "动画音乐淡出时间",
            "description": "设置动画音乐淡出的时间"
        },
        "result_music_fade_out": {
            "name": "结果音乐淡出时间",
            "description": "设置结果音乐淡出的时间"
        }
    }
}

# 即抽设置
instant_draw_settings = {
    "ZH_CN": {
        "title": {"name": "即抽设置","description": "即时抽取功能的相关设置"
        },
        "extraction_function": {
            "name": "抽取功能",
            "description": "即抽抽取功能相关设置"
        },
        "display_settings": {
            "name": "显示设置",
            "description": "即抽结果显示相关设置"
        },
        "basic_animation_settings": {
            "name": "动画设置",
            "description": "即抽动画效果相关设置"
        },
        "color_theme_settings": {
            "name": "颜色主题设置",
            "description": "即抽结果显示的颜色主题相关设置"
        },
        "student_image_settings": {
            "name": "学生头像设置",
            "description": "即抽结果显示的学生头像相关设置"
        },
        "music_settings": {
            "name": "音乐设置",
            "description": "即抽音乐相关设置"
        },
        "draw_mode": {
            "name": "抽取模式",
            "description": "设置即抽抽取的模式",
            "combo_items": [
                "重复抽取",
                "不重复抽取",
                "半重复抽取"
            ]
        },
        "clear_record": {
            "name": "清除抽取记录方式",
            "description": "设置清除即抽抽取记录的方式",
            "combo_items": [
                "重启后清除",
                "直到全部抽取完"
            ],
            "combo_items_other": [
                "重启后清除",
                "直到全部抽取完",
                "无需清除"
            ]
        },
        "half_repeat": {
            "name": "半重复抽取次数",
            "description": "设置半重复抽取的次数"
        },
        "clear_time": {
            "name": "抽取后定时清除时间",
            "description": "设置抽取后定时清除记录的时间(秒)"
        },
        "draw_type": {
            "name": "抽取方式",
            "description": "设置即抽抽取的方式",
            "combo_items": [
                "随机抽取",
                "公平抽取"
            ]
        },
        "font_size": {
            "name": "字体大小",
            "description": "设置即抽结果显示的字体大小"
        },
        "display_format": {
            "name": "结果显示格式",
            "description": "设置即抽结果的显示格式",
            "combo_items": [
                "学号+姓名",
                "姓名",
                "学号"
            ]
        },
        "show_random": {
            "name": "显示随机组员格式",
            "description": "设置随机组员的显示格式",
            "combo_items": [
                "不显示",
                "组名[换行]姓名",
                "组名[短横杠]姓名"
            ]
        },
        "animation": {
            "name": "动画模式",
            "description": "设置即抽抽取的动画效果",
            "combo_items": [
                "手动停止动画",
                "自动播放动画",
                "直接显示结果"
            ]
        },
        "animation_interval": {
            "name": "动画间隔",
            "description": "设置即抽动画的间隔时间(毫秒)"
        },
        "autoplay_count": {
            "name": "自动播放次数",
            "description": "设置即抽动画自动播放的次数"
        },
        "animation_color_theme": {
            "name": "动画颜色主题",
            "description": "设置即抽动画的颜色主题",
            "combo_items": [
                "关闭",
                "随机颜色",
                "固定颜色"
            ]
        },
        "result_color_theme": {
            "name": "结果颜色主题",
            "description": "设置即抽结果显示的颜色主题",
            "combo_items": [
                "关闭",
                "随机颜色",
                "固定颜色"
            ]
        },
        "animation_fixed_color": {
            "name": "动画固定颜色",
            "description": "设置即抽动画的固定颜色"
        },
        "result_fixed_color": {
            "name": "结果固定颜色",
            "description": "设置即抽结果显示的固定颜色"
        },
        "student_image": {
            "name": "显示学生图片",
            "description": "设置是否显示学生图片",
            "switchbutton_name": {
                "enable": "显示",
                "disable": "隐藏"
            }
        },
        "open_student_image_folder": {
            "name": "学生图片文件夹",
            "description": "管理学生图片文件,图片文件名需与学生姓名一致"
        },
        "animation_music": {
            "name": "动画音乐",
            "description": "设置是否播放动画音乐",
            "switchbutton_name": {
                "enable": "播放",
                "disable": "关闭"
            }
        },
        "result_music": {
            "name": "结果音乐",
            "description": "设置是否播放结果音乐",
            "switchbutton_name": {
                "enable": "播放",
                "disable": "关闭"
            }
        },
        "open_animation_music_folder": {
            "name": "打开动画音乐文件夹",
            "description": "管理动画音乐文件并支持随机播放功能"
        },
        "open_result_music_folder": {
            "name": "打开结果音乐文件夹",
            "description": "管理结果音乐文件并支持随机播放功能"
        },
        "animation_music_volume": {
            "name": "动画音乐音量",
            "description": "设置动画音乐的音量"
        },
        "result_music_volume": {
            "name": "结果音乐音量",
            "description": "设置结果音乐的音量"
        },
        "animation_music_fade_in": {
            "name": "动画音乐淡入时间",
            "description": "设置动画音乐淡入的时间"
        },
        "result_music_fade_in": {
            "name": "结果音乐淡入时间",
            "description": "设置结果音乐淡入的时间"
        },
        "animation_music_fade_out": {
            "name": "动画音乐淡出时间",
            "description": "设置动画音乐淡出的时间"
        },
        "result_music_fade_out": {
            "name": "结果音乐淡出时间",
            "description": "设置结果音乐淡出的时间"
        }
    }
}

# 自定义抽设置
custom_draw_settings = {
    "ZH_CN": {
        "title": {
            "name": "自定义抽设置",
            "description": "自定义抽设置"
        }
    }
}

# 抽奖设置
lottery_settings = {
    "ZH_CN": {
        "title": {
            "name": "抽奖设置",
            "description": "抽奖设置"
        },
        "extraction_function": {
            "name": "抽取功能",
            "description": "抽奖抽取功能相关设置"
        },
        "display_settings": {
            "name": "显示设置",
            "description": "抽奖结果显示相关设置"
        },
        "basic_animation_settings": {
            "name": "动画设置",
            "description": "抽奖动画效果相关设置"
        },
        "color_theme_settings": {
            "name": "颜色主题设置",
            "description": "抽奖结果显示的颜色主题相关设置"
        },
        "student_image_settings": {
            "name": "奖品图片设置",
            "description": "抽奖结果显示的奖品图片相关设置"
        },
        "music_settings": {
            "name": "音乐设置",
            "description": "抽奖音乐相关设置"
        },
        "draw_mode": {
            "name": "抽取模式",
            "description": "设置抽奖抽取的模式",
            "combo_items": [
                "重复抽取",
                "不重复抽取",
                "半重复抽取"
            ]
        },
        "clear_record": {
            "name": "清除抽取记录方式",
            "description": "设置清除抽奖抽取记录的方式",
            "combo_items": [
                "重启后清除",
                "直到全部抽取完"
            ],
            "combo_items_other": [
                "重启后清除",
                "直到全部抽取完",
                "无需清除"
            ]
        },
        "half_repeat": {
            "name": "半重复抽取次数",
            "description": "设置半重复抽取的次数"
        },
        "clear_time": {
            "name": "抽取后定时清除时间",
            "description": "设置抽取后定时清除记录的时间(秒)"
        },
        "draw_type": {
            "name": "抽取方式",
            "description": "设置抽奖抽取的方式",
            "combo_items": [
                "随机抽取",
                "公平抽取"
            ]
        },
        "font_size": {
            "name": "字体大小",
            "description": "设置抽奖结果显示的字体大小"
        },
        "display_format": {
            "name": "结果显示格式",
            "description": "设置抽奖结果的显示格式",
            "combo_items": [
                "序号+名称",
                "名称",
                "序号"
            ]
        },
        "animation": {
            "name": "动画模式",
            "description": "设置抽奖抽取的动画效果",
            "combo_items": [
                "手动停止动画",
                "自动播放动画",
                "直接显示结果"
            ]
        },
        "animation_interval": {
            "name": "动画间隔",
            "description": "设置抽奖动画的间隔时间(毫秒)"
        },
        "autoplay_count": {
            "name": "自动播放次数",
            "description": "设置抽奖动画自动播放的次数"
        },
        "animation_color_theme": {
            "name": "动画颜色主题",
            "description": "设置抽奖动画的颜色主题",
            "combo_items": [
                "关闭",
                "随机颜色",
                "固定颜色"
            ]
        },
        "result_color_theme": {
            "name": "结果颜色主题",
            "description": "设置抽奖结果显示的颜色主题",
            "combo_items": [
                "关闭",
                "随机颜色",
                "固定颜色"
            ]
        },
        "animation_fixed_color": {
            "name": "动画固定颜色",
            "description": "设置抽奖动画的固定颜色"
        },
        "result_fixed_color": {
            "name": "结果固定颜色",
            "description": "设置抽奖结果显示的固定颜色"
        },
        "lottery_image": {
            "name": "显示学生图片",
            "description": "设置是否显示学生图片",
            "switchbutton_name": {
                "enable": "显示",
                "disable": "隐藏"
            }
        },
        "open_lottery_image_folder": {
            "name": "奖品图片文件夹",
            "description": "管理奖品图片文件,图片文件名需与奖品名称一致"
        },
        "animation_music": {
            "name": "动画音乐",
            "description": "设置是否播放动画音乐",
            "switchbutton_name": {
                "enable": "播放",
                "disable": "关闭"
            }
        },
        "result_music": {
            "name": "结果音乐",
            "description": "设置是否播放结果音乐",
            "switchbutton_name": {
                "enable": "播放",
                "disable": "关闭"
            }
        },
        "open_animation_music_folder": {
            "name": "打开动画音乐文件夹",
            "description": "管理动画音乐文件并支持随机播放功能"
        },
        "open_result_music_folder": {
            "name": "打开结果音乐文件夹",
            "description": "管理结果音乐文件并支持随机播放功能"
        },
        "animation_music_volume": {
            "name": "动画音乐音量",
            "description": "设置动画音乐的音量"
        },
        "result_music_volume": {
            "name": "结果音乐音量",
            "description": "设置结果音乐的音量"
        },
        "animation_music_fade_in": {
            "name": "动画音乐淡入时间",
            "description": "设置动画音乐淡入的时间"
        },
        "result_music_fade_in": {
            "name": "结果音乐淡入时间",
            "description": "设置结果音乐淡入的时间"
        },
        "animation_music_fade_out": {
            "name": "动画音乐淡出时间",
            "description": "设置动画音乐淡出的时间"
        },
        "result_music_fade_out": {
            "name": "结果音乐淡出时间",
            "description": "设置结果音乐淡出的时间"
        }
    }
}
