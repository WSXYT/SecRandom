# 更多设置语言配置
more_settings = {
    "ZH_CN": {
        "title": {"name": "更多设置", "description": "更多功能设置"},
    },
    "EN_US": {"title": {"name": "More settings", "description": "More settings"}},
}

settings = {
    "ZH_CN": {
        "title": {"name": "设置", "description": "设置窗口"},
    },
    "EN_US": {"title": {"name": "Settings", "description": "Settings window"}},
}

# 时间设置语言配置
time_settings = {
    "ZH_CN": {
        "title": {"name": "时间设置", "description": "设置课间禁用和课程表导入"},
        "class_break_settings": {
            "name": "课间禁用设置",
            "description": "设置课间禁用功能",
        },
        "cses_import_settings": {
            "name": "CSES课程表导入",
            "description": "从CSES格式文件导入课程表",
        },
        "class_break_function": {
            "name": "课间禁用功能",
            "description": "开启后，在下课时间段内抽取需要安全验证",
        },
        "cses_import": {
            "name": "课程表导入",
            "description": "从CSES格式文件导入上课时间段，用于课间禁用功能",
        },
        "verification_function": {
            "name": "验证流程功能",
            "description": "启用后，在非上课时段触发时将弹出安全验证；若关闭则直接禁用控件",
        },
        "import_from_file": {"name": "从文件导入"},
        "importing": {"name": "导入中..."},
        "view_current_config": {"name": "查看当前配置"},
        "no_schedule_imported": {"name": "未导入课程表"},
        "schedule_imported": {"name": "已导入 {} 个上课时间段"},
        "copy_to_clipboard": {"name": "复制到剪贴板"},
        "save_as_file": {"name": "保存为文件"},
        "close": {"name": "关闭"},
        "copy_success": {"name": "复制成功"},
        "template_copied": {"name": "模板已复制到剪贴板"},
        "save_success": {"name": "保存成功"},
        "template_saved": {"name": "模板已保存到: {}"},
        "import_success": {"name": "成功导入课程表: {}"},
        "import_failed": {"name": "导入失败: {}"},
        "import_error": {"name": "导入过程中发生错误: {}"},
        "template_title": {"name": "CSES课程表模板"},
        "select_cses_file": {"name": "选择CSES课程表文件"},
        "yaml_files": {"name": "YAML文件 (*.yaml *.yml)"},
        "all_files": {"name": "所有文件 (*.*)"},
        "save_template": {"name": "保存CSES模板"},
        "cses_template": {"name": "cses_template.yaml"},
        "save_failed": {"name": "保存失败: {}"},
        "copy_failed": {"name": "复制失败: {}"},
        "cses_file_format_error": {"name": "CSES文件格式错误或文件无法读取"},
        "cses_content_format_error": {"name": "CSES内容格式错误"},
        "no_valid_time_periods": {"name": "未能从课程表中提取有效的时间段信息"},
        "save_settings_failed": {"name": "保存设置失败"},
        "no_cses_folder": {"name": "未找到CSES文件夹"},
        "no_schedule_file": {"name": "未导入课程表文件"},
        "unknown": {"name": "未知"},
        "unknown_course": {"name": "未知课程"},
        "parse_failed": {"name": "解析失败"},
        "load_config_failed": {"name": "加载配置失败: {}"},
        "table_headers": {"name": ["星期", "课程名称", "开始时间", "结束时间", "老师"]},
        "day_map": {
            "1": "周一",
            "2": "周二",
            "3": "周三",
            "4": "周四",
            "5": "周五",
            "6": "周六",
            "7": "周日",
        },
    },
    "EN_US": {
        "title": {
            "name": "Time Settings",
            "description": "Set class break restrictions and schedule import",
        },
        "class_break_settings": {
            "name": "Class Break Settings",
            "description": "Configure class break restrictions",
        },
        "cses_import_settings": {
            "name": "CSES Schedule Import",
            "description": "Import schedule from CSES format files",
        },
        "class_break_function": {
            "name": "Class Break Restriction",
            "description": "When enabled, drawing during break times requires safety verification",
        },
        "cses_import": {
            "name": "Schedule Import",
            "description": "Import class time slots from CSES format files for break time functionality",
        },
        "import_from_file": {"name": "Import from File"},
        "importing": {"name": "Importing..."},
        "view_current_config": {"name": "View Current Config"},
        "no_schedule_imported": {"name": "No schedule imported"},
        "schedule_imported": {"name": "Imported {} non-class time periods"},
        "copy_to_clipboard": {"name": "Copy to Clipboard"},
        "save_as_file": {"name": "Save as File"},
        "close": {"name": "Close"},
        "copy_success": {"name": "Copy Successful"},
        "template_copied": {"name": "Template copied to clipboard"},
        "save_success": {"name": "Save Successful"},
        "template_saved": {"name": "Template saved to: {}"},
        "import_success": {"name": "Import Successful"},
        "import_failed": {"name": "Import Failed"},
        "import_error": {"name": "Error during import: {}"},
        "template_title": {"name": "CSES Schedule Template"},
        "select_cses_file": {"name": "Select CSES Schedule File"},
        "yaml_files": {"name": "YAML files (*.yaml *.yml)"},
        "all_files": {"name": "All files (*.*)"},
        "save_template": {"name": "Save CSES Template"},
        "cses_template": {"name": "cses_template.yaml"},
        "save_failed": {"name": "Save failed: {}"},
        "copy_failed": {"name": "Copy failed: {}"},
        "cses_file_format_error": {
            "name": "CSES file format error or file cannot be read"
        },
        "cses_content_format_error": {"name": "CSES content format error"},
        "no_valid_time_periods": {
            "name": "Failed to extract valid time periods from the schedule"
        },
        "save_settings_failed": {"name": "Failed to save settings"},
        "no_cses_folder": {"name": "CSES folder not found"},
        "no_schedule_file": {"name": "No schedule file imported"},
        "unknown": {"name": "Unknown"},
        "unknown_course": {"name": "Unknown course"},
        "parse_failed": {"name": "Parse failed"},
        "load_config_failed": {"name": "Failed to load config: {}"},
        "table_headers": {
            "name": ["Day", "Course Name", "Start Time", "End Time", "Teacher"]
        },
        "day_map": {
            "1": "Monday",
            "2": "Tuesday",
            "3": "Wednesday",
            "4": "Thursday",
            "5": "Friday",
            "6": "Saturday",
            "7": "Sunday",
        },
    },
}

# 调试设置语言配置
debug = {
    "ZH_CN": {"title": {"name": "调试设置", "description": "调试功能设置"}},
    "EN_US": {"title": {"name": "Debug settings", "description": "Debug settings"}},
}

# 关于语言配置
about = {
    "ZH_CN": {
        "title": {"name": "关于", "description": "软件关于页面信息"},
        "github": {"name": "Github", "description": "访问项目代码仓库"},
        "bilibili": {
            "name": "Bilibili",
            "description": "访问黎泽懿_Aionflux的Bilibili账号",
        },
        "contributor": {
            "name": "贡献人员",
            "description": "点击查看详细贡献者信息",
            "contributor_role_1": "设计、创意、策划\n维护、文档、测试",
            "contributor_role_2": "维护",
            "contributor_role_3": "响应式前端页面\n设计及维护、文档",
            "contributor_role_4": "创意、文档",
            "contributor_role_5": "创意、维护",
            "contributor_role_6": "应用测试、文档、安装包制作",
            "contributor_role_7": "响应式前端页面\n设计及维护、文档",
        },
        "donation": {"name": "捐赠支持", "description": "支持项目发展，感谢您的捐赠"},
        "website": {"name": "SecRandom 官网", "description": "访问SecRandom软件官网"},
        "copyright": {"name": "版权", "description": "SecRandom遵循GPL-3.0协议"},
        "version": {"name": "版本", "description": "显示当前软件版本号"},
    },
    "EN_US": {
        "title": {"name": "About", "description": "APP about page"},
        "github": {"name": "GitHub", "description": "Visit project repository"},
        "bilibili": {
            "name": "Bilibili",
            "description": "Visit 黎泽懿_Aionflux's Bilibili account",
        },
        "contributor": {
            "name": "Contributors",
            "description": "Click to show full contributor information",
            "contributor_role_1": "Design & Creativity & Test &\nMaintenance & Documentation",
            "contributor_role_2": "Maintenance",
            "contributor_role_3": "Responsive frontend page Design and Maintenance & Documentation",
            "contributor_role_4": "Creativity & Documentation",
            "contributor_role_5": "Creativity & Maintenance",
            "contributor_role_6": "Test & Documentation & Install Package Making",
            "contributor_role_7": "Responsive frontend page Design and Maintenance & Documentation",
        },
        "donation": {"name": "Donate", "description": "Buy me a coffee"},
        "check_update": {
            "name": "Check for updates",
            "description": "Check for updates",
        },
        "website": {
            "name": "SecRandom Website",
            "description": "Visit SecRandom's official website",
        },
        "channel": {
            "name": "Update channel",
            "description": "Select SecRandom software update channel",
            "combo_items": {"0": "Official version", "1": "Beta version"},
        },
        "copyright": {"name": "Copyright", "description": "SecRandom follows GPL-3.0"},
        "version": {"name": "Version", "description": "Show current version"},
    },
}

# 翻译文件信息
translate_JSON_file = {
    "ZH_CN": {
        "name": "简体中文",
        "translated_personnel": "lzy98276",
    },
    "EN_US": {
        "name": "English",
        "translated_personnel": "",
    },
}
