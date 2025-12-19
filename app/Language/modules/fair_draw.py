# 公平抽取设置语言配置
fair_draw_settings = {
    "ZH_CN": {
        "title": {"name": "公平抽取设置", "description": "公平抽取功能设置"},
        "fair_draw_set": {
            "name": "公平抽取",
            "description": "配置公平抽取算法相关设置",
        },
        "basic_fair_settings": {
            "name": "基础公平设置",
            "description": "配置公平抽取的基础计算方式",
        },
        "weight_range_settings": {
            "name": "权重范围设置",
            "description": "配置权重的基础值和范围",
        },
        "shield_settings": {
            "name": "抽取后屏蔽设置",
            "description": "配置抽取后的屏蔽规则",
        },
        "frequency_settings": {
            "name": "频率函数设置",
            "description": "配置频率惩罚的计算方式",
        },
        "balance_weight_settings": {
            "name": "平衡权重设置",
            "description": "配置各平衡因子的权重占比",
        },
        "cold_start_settings": {
            "name": "冷启动设置",
            "description": "配置新班级初始阶段的冷启动规则",
        },
        "fair_draw": {
            "name": "按总抽取次数公平抽取",
            "description": "启用后根据总抽取次数进行公平抽取",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "fair_draw_group": {
            "name": "按组公平抽取",
            "description": "启用后按组参与公平抽取计算",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "fair_draw_gender": {
            "name": "按性别公平抽取",
            "description": "启用后按性别参与公平抽取计算",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "fair_draw_time": {
            "name": "按时间公平抽取",
            "description": "启用后按时间参与公平抽取计算",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "base_weight": {"name": "基础权重", "description": "设置每个选项的基础权重值"},
        "min_weight": {
            "name": "权重范围最小值",
            "description": "设置每个选项权重最小值",
        },
        "max_weight": {
            "name": "权重范围最大值",
            "description": "设置每个选项权重最大值",
        },
        "frequency_function": {
            "name": "频率惩罚函数",
            "description": "选择频率惩罚的计算函数类型",
            "combo_items": ["线性", "平方根", "指数"],
        },
        "frequency_weight": {
            "name": "频率惩罚权重",
            "description": "调整频率惩罚在总权重中的占比",
        },
        "group_weight": {
            "name": "小组平衡权重",
            "description": "调整小组平衡在总权重中的占比",
        },
        "gender_weight": {
            "name": "性别平衡权重",
            "description": "调整性别平衡在总权重中的占比",
        },
        "time_weight": {
            "name": "时间因子权重",
            "description": "调整时间因子在总权重中的占比",
        },
        "cold_start_enabled": {
            "name": "启用冷启动模式",
            "description": "新班级或初始阶段使用冷启动模式",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "cold_start_rounds": {
            "name": "冷启动轮次",
            "description": "设置冷启动模式的轮次数量",
        },
        "shield_enabled": {
            "name": "启用抽取后屏蔽",
            "description": "启用后，抽取的学生在指定时间内不会被重复抽取",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "shield_time": {
            "name": "屏蔽时间",
            "description": "设置抽取后屏蔽的时间长度",
        },
        "shield_time_unit": {
            "name": "屏蔽时间单位",
            "description": "选择屏蔽时间的时间单位",
            "combo_items": ["秒", "分钟", "小时"],
        },
    },
    "EN_US": {
        "title": {
            "name": "Fair pick settings",
            "description": "Fair pick function settings",
        },
        "fair_draw_set": {
            "name": "Fair pick",
            "description": "Configure fair pick algorithm related settings",
        },
        "basic_fair_settings": {
            "name": "Basic fair settings",
            "description": "Configure base calculation for fair pick",
        },
        "weight_range_settings": {
            "name": "Weight range settings",
            "description": "Configure base value and range of weights",
        },
        "shield_settings": {
            "name": "Block after pick",
            "description": "Configure block rules after picking",
        },
        "frequency_settings": {
            "name": "Frequency function settings",
            "description": "Configure how frequency penalties are to be calculated",
        },
        "balance_weight_settings": {
            "name": "Balanced weight settings",
            "description": "Configure the weight of the balance factors",
        },
        "cold_start_settings": {
            "name": "Cold boot settings",
            "description": "Configure cold start rules for the initial phase of a new class",
        },
        "fair_draw": {
            "name": "Fair pick by total pick times",
            "description": "Enable to make fair pickings based on the total pick times",
        },
        "fair_draw_group": {
            "name": "Fair pick by group",
            "description": "Enable when calculated by group participation",
        },
        "fair_draw_gender": {
            "name": "Fair pick by gender",
            "description": "When enabled and calculated by gender participation",
        },
        "fair_draw_time": {
            "name": "Fair pick by time",
            "description": "Enable to participate in fair pick by time",
        },
        "base_weight": {
            "name": "Base weight",
            "description": "Set the base weight of each option",
        },
        "min_weight": {
            "name": "Minimum weight range",
            "description": "Set minimum weight per option",
        },
        "max_weight": {
            "name": "Maximum weight range",
            "description": "Set maximum weight per option",
        },
        "frequency_function": {
            "name": "Frequency punishment function",
            "description": "Select the type of compute function for frequency punishment",
            "combo_items": {"0": "Linear", "1": "Square root", "2": "Index"},
        },
        "frequency_weight": {
            "name": "Frequency penalties weight",
            "description": "Percentage of frequency penalties in total weight",
        },
        "group_weight": {
            "name": "Group balance weight",
            "description": "Adjustment group balance as a percentage of total weight",
        },
        "gender_weight": {
            "name": "Gender balance weight",
            "description": "Adjust the proportion of gender balance in total weight",
        },
        "time_weight": {
            "name": "Time factor weight",
            "description": "Adjust the percentage of time factor in total weight",
        },
        "cold_start_enabled": {
            "name": "Enable cold launch mode",
            "description": "Use cold boot mode for new class or initial phase",
        },
        "cold_start_rounds": {
            "name": "Cold boot rounds",
            "description": "Sets the number of rounds in cold boot mode",
        },
        "shield_enabled": {
            "name": "Enable block after exam",
            "description": "When enabled, picked students will not be duplicated during the specified time",
        },
        "shield_time": {
            "name": "Blocked time",
            "description": "Set the time to block after picking",
        },
        "shield_time_unit": {
            "name": "Block time units",
            "description": "Select time unit for block time",
            "combo_items": {"0": "Seconds", "1": "Minutes", "2": "Hours"},
        },
    },
}
