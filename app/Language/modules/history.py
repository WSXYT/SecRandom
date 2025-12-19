# 历史记录语言配置
history = {
    "ZH_CN": {
        "title": {"name": "历史记录", "description": "查看和管理点名、抽奖的历史记录"}
    },
    "EN_US": {
        "title": {
            "name": "History",
            "description": "View and manage the pick and lottery history",
        }
    },
}

# 历史记录管理语言配置
history_management = {
    "ZH_CN": {
        "title": {"name": "历史记录管理", "description": "管理点名、抽奖的历史记录"},
        "roll_call": {
            "name": "点名历史记录",
            "description": "查看和管理点名的历史记录",
        },
        "lottery_history": {
            "name": "抽奖历史记录",
            "description": "查看和管理抽奖的历史记录",
        },
        "show_roll_call_history": {
            "name": "启用点名历史记录",
            "description": "控制是否启用点名历史记录功能",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "select_class_name": {
            "name": "选择班级",
            "description": "选择要查看历史记录的班级",
        },
        "clear_roll_call_history": {
            "name": "清除点名历史记录",
            "description": "清除选定班级的点名历史记录",
            "pushbutton_name": "清除",
        },
        "show_lottery_history": {
            "name": "启用抽奖历史记录",
            "description": "控制是否启用抽奖历史记录功能",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "select_pool_name": {
            "name": "选择奖池",
            "description": "选择要查看历史记录的奖池",
        },
        "clear_lottery_history": {
            "name": "清除抽奖历史记录",
            "description": "清除选定奖池的抽奖历史记录",
            "pushbutton_name": "清除",
        },
    },
    "EN_US": {
        "title": {
            "name": "History management",
            "description": "Manage the pick and lottery history",
        },
        "roll_call": {
            "name": "Picking history",
            "description": "View and manage the pick history",
        },
        "lottery_history": {
            "name": "Lottery history",
            "description": "View and manage the lottery history",
        },
        "show_roll_call_history": {
            "name": "Enable picking history",
            "description": "Control whether pick history is enabled",
        },
        "select_class_name": {
            "name": "Select class",
            "description": "Choose a class to view history",
        },
        "clear_roll_call_history": {
            "name": "Clear pick history",
            "description": "Clear the pick history of the selected class",
            "pushbutton_name": "Clear",
        },
        "show_lottery_history": {
            "name": "Enable lottery history",
            "description": "Control whether lottery history is enabled",
        },
        "select_pool_name": {
            "name": "Select pool",
            "description": "Choose a class to view history",
        },
        "clear_lottery_history": {
            "name": "Clear lottery history",
            "description": "Clear the lottery history of the selected pool",
            "pushbutton_name": "Clear",
        },
        "select_weight": {
            "name": "Show weight",
            "description": "Show or hide weight information in table",
        },
    },
}

# 点名历史记录表格语言配置
roll_call_history_table = {
    "ZH_CN": {
        "title": {
            "name": "点名历史记录表格",
            "description": "以表格形式展示点名的历史记录",
        },
        "select_class_name": {
            "name": "选择班级",
            "description": "选择要查看历史记录的班级",
        },
        "select_mode": {
            "name": "查看模式",
            "description": "选择历史记录的查看方式",
            "combo_items": ["全部记录", "按时间查看"],
        },
        "HeaderLabels_all_not_weight": {
            "name": ["学号", "姓名", "性别", "小组", "点名次数"],
            "description": "点名历史记录表格列标题（不包含权重）",
        },
        "HeaderLabels_all_weight": {
            "name": ["学号", "姓名", "性别", "小组", "点名次数", "权重"],
            "description": "点名历史记录表格列标题（包含权重）",
        },
        "HeaderLabels_time_not_weight": {
            "name": ["点名时间", "学号", "姓名", "性别", "小组"],
            "description": "点名历史记录表格列标题（按时间查看，不包含权重）",
        },
        "HeaderLabels_time_weight": {
            "name": ["点名时间", "学号", "姓名", "性别", "小组", "权重"],
            "description": "点名历史记录表格列标题（按时间查看，包含权重）",
        },
        "HeaderLabels_Individual_not_weight": {
            "name": ["点名时间", "点名模式", "点名人数", "性别限制", "小组限制"],
            "description": "点名历史记录表格列标题（个人记录，不包含权重）",
        },
        "HeaderLabels_Individual_weight": {
            "name": [
                "点名时间",
                "点名模式",
                "点名人数",
                "性别限制",
                "小组限制",
                "权重",
            ],
            "description": "点名历史记录表格列标题（个人记录，包含权重）",
        },
    },
    "EN_US": {
        "title": {
            "name": "Picking history table",
            "description": "Display lists of pick history in table form",
        },
        "select_class_name": {
            "name": "Select class",
            "description": "Choose a class to view history",
        },
        "select_mode": {
            "name": "View mode",
            "description": "Choose how history is viewed",
            "combo_items": {"0": "All history", "1": "View by time"},
        },
        "HeaderLabels_all_not_weight": {
            "name": {
                "0": "Student ID",
                "1": "Name",
                "2": "Gender",
                "3": "Group",
                "4": "Picking times",
            },
            "description": "Picking history table title column header (excluding weight)",
        },
        "HeaderLabels_all_weight": {
            "name": {
                "0": "Student ID",
                "1": "Name",
                "2": "Gender",
                "3": "Group",
                "4": "Picking times",
                "5": "Weight",
            },
            "description": "Picking history table title column header (including weight)",
        },
        "HeaderLabels_time_not_weight": {
            "name": {
                "0": "Picking time",
                "1": "Student ID",
                "2": "Name",
                "3": "Gender",
                "4": "Group",
            },
            "description": "Title of the list of picking history tables (viewed by time, excluding weight)",
        },
        "HeaderLabels_time_weight": {
            "name": {
                "0": "Picking time",
                "1": "Student ID",
                "2": "Name",
                "3": "Gender",
                "4": "Group",
                "5": "Weight",
            },
            "description": "Title of the list of picking history tables (viewed by time, including weight)",
        },
        "HeaderLabels_Individual_not_weight": {
            "name": {
                "0": "Picking time",
                "1": "Picking mode",
                "2": "Picking amount",
                "3": "Gender limit",
                "4": "Group limit",
            },
            "description": "Title of the list of picking history tables (personal history, excluding weight)",
        },
        "HeaderLabels_Individual_weight": {
            "name": {
                "0": "Picking time",
                "1": "Picking mode",
                "2": "Picking amount",
                "3": "Gender limit",
                "4": "Group limit",
                "5": "Weight",
            },
            "description": "Title of the list of picking history tables (personal history, including weight)",
        },
        "select_weight": {
            "name": "Show weight",
            "description": "Whether to show weight in table",
            "switchbutton_name": {"enable": "Show", "disable": "Hide"},
        },
    },
}

# 抽奖历史记录表格语言配置
lottery_history_table = {
    "ZH_CN": {
        "title": {
            "name": "抽奖历史记录表格",
            "description": "以表格形式展示抽奖的历史记录",
        },
        "select_pool_name": {
            "name": "选择奖池",
            "description": "选择要查看历史记录的奖池",
        },
        "select_mode": {
            "name": "查看模式",
            "description": "选择历史记录的查看方式",
            "combo_items": ["全部记录", "按时间查看"],
        },
        "HeaderLabels_all_weight": {
            "name": ["序号", "名称", "中奖次数", "权重"],
            "description": "抽奖历史记录表格列标题（全部记录）",
        },
        "HeaderLabels_time_weight": {
            "name": ["抽奖时间", "序号", "名称", "权重"],
            "description": "抽奖历史记录表格列标题（按时间查看）",
        },
        "HeaderLabels_Individual_weight": {
            "name": ["抽奖时间", "抽奖模式", "抽取数量", "权重设置"],
            "description": "抽奖历史记录表格列标题（单次记录）",
        },
    },
    "EN_US": {
        "title": {
            "name": "Lottery history table",
            "description": "Display lists of lottery history in table form",
        },
        "select_pool_name": {
            "name": "Select pool",
            "description": "Choose a lottery pool to view history",
        },
        "select_mode": {
            "name": "View mode",
            "description": "Choose how history is viewed",
            "combo_items": {"0": "All history", "1": "View by time"},
        },
        "HeaderLabels_all_weight": {
            "name": {
                "0": "Serial",
                "1": "Name",
                "2": "Lottery winning times",
                "3": "Weight",
            },
            "description": "Lottery history table title column header weight (all)",
        },
        "HeaderLabels_time_weight": {
            "name": {"0": "Lottery time", "1": "Serial", "2": "Name", "3": "Weight"},
            "description": "Lottery history table title column header weight (sort by time)",
        },
        "HeaderLabels_Individual_weight": {
            "name": {
                "0": "Lottery time",
                "1": "Lottery mode",
                "2": "Picking quantity",
                "3": "Weight settings",
            },
            "description": "Lottery history table title column header (single record)",
        },
    },
}
