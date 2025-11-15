# 历史记录语言配置
history = {"ZH_CN": {"title": {"name": "历史记录", "description": "历史记录设置"}}}

# 历史记录管理语言配置
history_management = {
    "ZH_CN": {
        "title": {"name": "历史记录管理", "description": "历史记录管理"},
        "roll_call": {
            "name": "点名历史记录",
            "description": "配置点名历史记录相关设置",
        },
        "lottery_history": {
            "name": "抽奖历史记录",
            "description": "配置抽奖历史记录相关设置",
        },
        "show_roll_call_history": {
            "name": "启用点名历史记录",
            "description": "启用点名历史记录",
            "switchbutton_name": {"enable": "启用", "disable": "禁用"},
        },
        "select_class_name": {
            "name": "选择班级",
            "description": "选择要显示历史记录的班级",
        },
        "clear_roll_call_history": {
            "name": "清除点名历史记录",
            "description": "清除点名历史记录",
            "pushbutton_name": "清除",
        },
        "show_lottery_history": {
            "name": "启用抽奖历史记录",
            "description": "启用抽奖历史记录",
            "switchbutton_name": {"enable": "启用", "disable": "禁用"},
        },
        "select_pool_name": {
            "name": "选择奖池",
            "description": "选择要显示历史记录的奖池",
        },
        "clear_lottery_history": {
            "name": "清除抽奖历史记录",
            "description": "清除抽奖历史记录",
            "pushbutton_name": "清除",
        },
    }
}

# 点名历史记录表格语言配置
roll_call_history_table = {
    "ZH_CN": {
        "title": {
            "name": "点名历史记录表格",
            "description": "用于展示和管理点名历史记录的表格",
        },
        "select_class_name": {
            "name": "选择班级",
            "description": "选择要显示历史记录的班级",
        },
        "select_mode": {
            "name": "选择查看模式",
            "description": "选择要查看的历史记录模式",
            "combo_items": ["全部", "时间"],
        },
        "HeaderLabels_all_not_weight": {
            "name": ["学号", "姓名", "性别", "小组", "总次数"],
            "description": "点名历史记录表格的列标题",
        },
        "HeaderLabels_all_weight": {
            "name": ["学号", "姓名", "性别", "小组", "总次数", "权重"],
            "description": "点名历史记录表格的列标题",
        },
        "HeaderLabels_time_not_weight": {
            "name": ["时间", "学号", "姓名", "性别", "小组"],
            "description": "点名历史记录表格的列标题",
        },
        "HeaderLabels_time_weight": {
            "name": ["时间", "学号", "姓名", "性别", "小组", "权重"],
            "description": "点名历史记录表格的列标题",
        },
        "HeaderLabels_Individual_not_weight": {
            "name": ["时间", "模式", "人数", "性别", "小组"],
            "description": "点名历史记录表格的列标题",
        },
        "HeaderLabels_Individual_weight": {
            "name": ["时间", "模式", "人数", "性别", "小组", "权重"],
            "description": "点名历史记录表格的列标题",
        },
        "select_weight": {
            "name": "是否显示权重",
            "description": "选择是否显示权重在表格中",
            "switchbutton_name": {
                "enable": "显示",
                "disable": "隐藏"
            }
        },
    }
}

# 抽奖历史记录表格语言配置
lottery_history_table = {
    "ZH_CN": {
        "title": {
            "name": "抽奖历史记录表格",
            "description": "用于展示和管理抽奖历史记录的表格",
        },
        "select_pool_name": {
            "name": "选择奖池",
            "description": "选择要显示历史记录的奖池",
        },
        "select_mode": {
            "name": "选择查看模式",
            "description": "选择要查看的历史记录模式",
            "combo_items": ["全部", "时间"],
        },
        "HeaderLabels_all_weight": {
            "name": ["序号", "名称", "总次数", "权重"],
            "description": "抽奖历史记录表格的列标题",
        },
        "HeaderLabels_time_weight": {
            "name": ["时间", "序号", "名称", "权重"],
            "description": "抽奖历史记录表格的列标题",
        },
        "HeaderLabels_Individual_weight": {
            "name": ["时间", "模式", "数量", "权重"],
            "description": "抽奖历史记录表格的列标题",
        },
    }
}
