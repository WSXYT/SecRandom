# 基础设置语言配置
basic_settings = {
    "ZH_CN": {
        "title": {"name": "基础设置", "description": "配置软件的基本功能和外观"},
        "basic_function": {"name": "基础功能", "description": "配置软件的核心功能选项"},
        "data_management": {
            "name": "数据管理",
            "description": "管理软件的数据导入和导出",
        },
        "personalised": {"name": "个性化", "description": "自定义软件外观和用户体验"},
        "autostart": {
            "name": "开机自启",
            "description": "设置软件是否随系统启动自动运行",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "show_startup_window": {
            "name": "启动显示主窗口",
            "description": "设置软件启动时是否自动显示主窗口",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "background_resident": {
            "name": "后台驻留",
            "description": "关闭所有窗口后是否仍在后台常驻",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "url_protocol": {
            "name": "URL协议注册",
            "description": "注册自定义URL协议(secrandom://)，支持通过链接启动应用",
            "switchbutton_name": {"enable": "", "disable": ""},
        },
        "export_diagnostic_data": {
            "name": "导出诊断数据",
            "description": "退出软件时导出诊断信息，用于排查问题",
            "pushbutton_name": "导出诊断数据",
        },
        "export_settings": {
            "name": "导出设置",
            "description": "将当前设置导出为配置文件，用于备份和迁移",
            "pushbutton_name": "导出设置",
        },
        "import_settings": {
            "name": "导入设置",
            "description": "从配置文件导入设置，覆盖当前配置信息",
            "pushbutton_name": "导入设置",
        },
        "export_all_data": {
            "name": "导出所有数据",
            "description": "退出软件时导出全部数据和设置",
            "pushbutton_name": "导出所有数据",
        },
        "import_all_data": {
            "name": "导入所有数据",
            "description": "启动软件时从备份文件恢复全部数据",
            "pushbutton_name": "导入所有数据",
        },
        "log_level": {
            "name": "日志等级",
            "description": "设置日志记录详细程度",
            "combo_items": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        },
        "dpiScale": {
            "name": "DPI缩放",
            "description": "调整软件界面缩放比例（重启软件后生效）",
            "combo_items": ["100%", "125%", "150%", "175%", "200%", "自动"],
        },
        "font": {
            "name": "字体",
            "description": "设置软件界面显示字体（重启软件后生效）",
        },
        "theme": {
            "name": "主题模式",
            "description": "选择软件界面主题样式",
            "combo_items": ["浅色", "深色", "跟随系统"],
        },
        "theme_color": {"name": "主题颜色", "description": "设置软件界面主题色彩"},
        "language": {
            "name": "显示语言",
            "description": "切换软件界面语言（重启软件后生效）",
        },
        "settings_import_export": {
            "export_success_title": {"name": "导出设置"},
            "export_success_content": {"name": "设置已成功导出到:\n{path}"},
            "export_failure_title": {"name": "导出设置"},
            "export_failure_content": {"name": "导出设置失败:\n{error}"},
            "import_confirm_title": {"name": "导入设置"},
            "import_confirm_content": {
                "name": "确定要导入这些设置吗？这将覆盖当前设置"
            },
            "import_confirm_button": {"name": "确认导入"},
            "import_cancel_button": {"name": "取消导入"},
            "import_success_title": {"name": "导入设置"},
            "import_success_content": {
                "name": "设置已成功导入\n重启应用程序以使更改生效"
            },
            "import_success_button": {"name": "我知道了"},
            "export_success_button": {"name": "我知道了"},
            "import_failure_title": {"name": "导入设置"},
            "import_failure_content": {"name": "导入设置失败:\n{error}"},
        },
        "success_enable_content": {"name": "已开启启动显示主窗口"},
        "info_disable_content": {"name": "已关闭启动显示主窗口"},
        "data_import_export": {
            "export_success_title": {"name": "导出所有数据"},
            "export_success_content": {"name": "所有数据已成功导出到:\n{path}"},
            "export_failure_title": {"name": "导出所有数据"},
            "export_failure_content": {"name": "导出所有数据失败:\n{error}"},
            "import_confirm_title": {"name": "导入所有数据"},
            "import_confirm_content": {
                "name": "确定要导入这些数据吗？这将覆盖当前数据"
            },
            "import_confirm_button": {"name": "确认导入"},
            "import_cancel_button": {"name": "取消导入"},
            "import_success_title": {"name": "导入所有数据"},
            "import_success_content": {
                "name": "数据已成功导入\n重启应用程序以使更改生效"
            },
            "import_success_button": {"name": "我知道了"},
            "import_failure_title": {"name": "导入所有数据"},
            "import_failure_content": {"name": "导入所有数据失败:\n{error}"},
            "existing_files_count": {"name": "\n... 还有 {len} 个文件"},
            "existing_files_title": {"name": "文件已存在"},
            "existing_files_content": {
                "name": "以下文件已存在:\n{files}\n\n是否覆盖这些文件？"
            },
            "version_mismatch_title": {"name": "版本不匹配"},
            "version_mismatch_content": {
                "name": "导出数据的软件版本与当前版本不一致:\n\n导出数据的软件: {software_name} {version}\n当前软件: SecRandom {current_version}\n\n是否继续导入？"
            },
            "export_warning_title": {"name": "导出所有数据"},
            "export_warning_content": {
                "name": "即将导出所有数据，包括:\n\n软件版本、设置配置\n点名名单、抽奖名单\n历史记录、日志文件\n\n注意: 导出的数据可能包含敏感信息，请妥善保管。\n\n是否继续导出?"
            },
        },
        "diagnostic_data_export": {
            "export_confirm_button": {"name": "确认导出"},
            "export_cancel_button": {"name": "取消导出"},
            "export_success_title": {"name": "导出诊断数据"},
            "export_success_content": {"name": "诊断数据已成功导出到:\n{path}"},
            "export_failure_title": {"name": "导出诊断数据"},
            "export_failure_content": {"name": "导出诊断数据失败:\n{error}"},
            "export_warning_title": {"name": "导出诊断数据"},
            "export_warning_content": {
                "name": "即将导出诊断数据，包括:\n\n软件信息、设置配置\n点名名单、抽奖名单\n历史记录、日志文件\n\n注意: 导出的数据可能包含敏感信息，请妥善保管。\n\n是否继续导出?"
            },
        },
    },
    "EN_US": {
        "title": {
            "name": "Basic settings",
            "description": "Configure basic features and appearance of software",
        },
        "basic_function": {
            "name": "Basic functions",
            "description": "Configure software's core functions",
        },
        "data_management": {
            "name": "Data management",
            "description": "Import or export the software's data",
        },
        "personalised": {
            "name": "Customization",
            "description": "Customize the look and experience of software",
        },
        "autostart": {
            "name": "Start on boot",
            "description": "Set whether the software is running automatically with the system",
        },
        "check_update": {
            "name": "Check for updates on startup",
            "description": "Set whether to automatically check for new versions when software starts",
        },
        "show_startup_window": {
            "name": "Show splash screen",
            "description": "Set whether to show the splash screen on boot",
        },
        "export_diagnostic_data": {
            "name": "Export diagnostic data",
            "description": "Export Diagnostic Information on Exit",
            "pushbutton_name": "Export diagnostic data",
        },
        "export_settings": {
            "name": "Export settings",
            "description": "Export current settings to profile",
            "pushbutton_name": "Export settings",
        },
        "import_settings": {
            "name": "Import settings",
            "description": "Import settings from profile to overwrite the current profile",
            "pushbutton_name": "Import settings",
        },
        "export_all_data": {
            "name": "Export all data",
            "description": "Export all data and settings when exit",
            "pushbutton_name": "Export all data",
        },
        "import_all_data": {
            "name": "Import all data",
            "description": "Restore all data from backup file when software starts",
            "pushbutton_name": "Import all data",
        },
        "dpiScale": {
            "name": "DPI scale settings",
            "description": "Resize the app interface (restart required)",
            "combo_items": {
                "0": "100%",
                "1": "125%",
                "2": "150%",
                "3": "175%",
                "4": "200%",
                "5": "Auto",
            },
        },
        "font": {
            "name": "Font",
            "description": "Set the font to display (restart required)",
        },
        "theme": {
            "name": "Theme mode",
            "description": "Select the software interface theme style",
            "combo_items": {"0": "Light", "1": "Dark", "2": "Follow system"},
        },
        "theme_color": {
            "name": "Theme color",
            "description": "Set the software interface theme color",
        },
        "language": {
            "name": "Display language",
            "description": "Switch display language (restart required)",
        },
        "background_resident": {
            "name": "Run in background",
            "description": "Whether to remain in the back office after closing all windows",
        },
        "url_protocol": {
            "name": "URL protocol register",
            "description": "Sign up for custom URL protocol (secrandom://), support to launch app via link",
        },
        "log_level": {
            "name": "Log level",
            "description": "Set the level of detail for log entries",
            "combo_items": {
                "0": "DEBUG",
                "1": "INFO",
                "2": "WARNING",
                "3": "ERROR",
                "4": "CRITICAL",
            },
        },
        "settings_import_export": {
            "export_success_title": {"name": "Export settings"},
            "export_success_content": {
                "name": "Settings have been exported to:\n{path}"
            },
            "export_failure_title": {"name": "Export settings"},
            "export_failure_content": {"name": "Failed to export settings: \n{error}"},
            "import_confirm_title": {"name": "Import settings"},
            "import_confirm_content": {
                "name": "Are you sure you want to import these settings? This will overwrite the current settings"
            },
            "import_confirm_button": {"name": "Confirm import"},
            "import_cancel_button": {"name": "Cancel import"},
            "import_success_title": {"name": "Import settings"},
            "import_success_content": {
                "name": "Settings successfully imported\nRestart to take effect"
            },
            "import_success_button": {"name": "Got it"},
            "export_success_button": {"name": "Got it"},
            "import_failure_title": {"name": "Import settings"},
            "import_failure_content": {"name": "Failed to import settings: \n{error}"},
        },
        "data_import_export": {
            "export_success_title": {"name": "Export all data"},
            "export_success_content": {
                "name": "All data has been exported to:\n{path}"
            },
            "export_failure_title": {"name": "Export all data"},
            "export_failure_content": {"name": "Failed to export all data: \n{error}"},
            "import_confirm_title": {"name": "Import all data"},
            "import_confirm_content": {
                "name": "Are you sure you want to import these data? This will overwrite the current data"
            },
            "import_confirm_button": {"name": "Confirm import"},
            "import_cancel_button": {"name": "Cancel import"},
            "import_success_title": {"name": "Import all data"},
            "import_success_content": {
                "name": "Data imported successfully into\nRestart APP to take effect"
            },
            "import_success_button": {"name": "Got it"},
            "import_failure_title": {"name": "Import all data"},
            "import_failure_content": {"name": "Failed to import all data: \n{error}"},
            "existing_files_count": {"name": "\n... still have {len} files"},
            "existing_files_title": {"name": "File already exists"},
            "existing_files_content": {
                "name": "The following files already exist:\n{files}\n\nOverwrite these files?"
            },
            "version_mismatch_title": {"name": "Version mismatch"},
            "version_mismatch_content": {
                "name": "The version from imported data mismatches with current version:\n\nImported data is from: {software_name} {version}\nCurrent software is: SecRandom {current_version}\n\nContinue importing?"
            },
            "export_warning_title": {"name": "Export all data"},
            "export_warning_content": {
                "name": "All data will soon be exported, including:\n\nsoftware version, settings,\nname list, prize list,\nhistory, log file\n\nNOTE: exported data may contain sensitive information, please keep it safe.\n\nContinue exporting?"
            },
        },
        "diagnostic_data_export": {
            "export_confirm_button": {"name": "Confirm Export"},
            "export_cancel_button": {"name": "Cancel export"},
            "export_success_title": {"name": "Export diagnostic data"},
            "export_success_content": {
                "name": "Diagnostic data has been exported to:\n{path}"
            },
            "export_failure_title": {"name": "Export diagnostic data"},
            "export_failure_content": {
                "name": "Failed to export diagnostic data: \n{error}"
            },
            "export_warning_title": {"name": "Export diagnostic data"},
            "export_warning_content": {
                "name": "Diagnostic data will soon be exported, including:\n\nsoftware information, settings,\nname list, prize list,\nhistory, log file\n\nNOTE: exported data may contain sensitive information, please keep it safe.\n\nContinue exporting?"
            },
        },
        "success_enable_content": {
            "name": "Enabled displaying main window when launching"
        },
        "info_disable_content": {
            "name": "Disabled displaying main window when launching"
        },
    },
}
