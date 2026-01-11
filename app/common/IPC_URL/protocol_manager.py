"""
协议管理器 - 跨平台URL协议注册管理
支持Windows和Linux系统的自定义协议注册
"""

import os
import sys
import winreg
import subprocess
from pathlib import Path
from loguru import logger


class ProtocolManager:
    """协议管理器 - 处理跨平台的URL协议注册"""

    def __init__(self, app_name: str, protocol_name: str):
        """
        初始化协议管理器

        Args:
            app_name: 应用程序名称
            protocol_name: 自定义协议名称（不含://）
        """
        self.app_name = app_name
        self.protocol_name = protocol_name
        self.is_windows = sys.platform.startswith("win")
        self.is_linux = sys.platform.startswith("linux")

    def register_protocol(self) -> bool:
        """
        注册自定义协议

        Returns:
            注册成功返回True，失败返回False
        """
        if self.is_windows:
            return self._register_windows_protocol()
        elif self.is_linux:
            return self._register_linux_protocol()
        else:
            logger.exception(f"不支持的操作系统: {sys.platform}")
            return False

    def unregister_protocol(self) -> bool:
        """
        注销自定义协议

        Returns:
            注销成功返回True，失败返回False
        """
        if self.is_windows:
            return self._unregister_windows_protocol()
        elif self.is_linux:
            return self._unregister_linux_protocol()
        else:
            logger.exception(f"不支持的操作系统: {sys.platform}")
            return False

    def is_protocol_registered(self) -> bool:
        """
        检查协议是否已注册

        Returns:
            已注册返回True，未注册返回False
        """
        if self.is_windows:
            return self._is_windows_protocol_registered()
        elif self.is_linux:
            return self._is_linux_protocol_registered()
        else:
            return False

    def _register_windows_protocol(self) -> bool:
        """Windows系统注册协议（单用户模式，无需管理员权限）"""
        try:
            # 获取当前可执行文件路径
            exe_path = self._get_executable_path()

            # 直接注册到HKEY_CURRENT_USER（单用户模式，无需管理员权限）
            return self._register_windows_protocol_current_user(exe_path)

        except Exception as e:
            logger.exception(f"Windows协议注册失败: {e}")
            return False

    def _register_windows_protocol_current_user(self, exe_path: str) -> bool:
        """注册到当前用户的Windows协议（无需管理员权限）"""
        try:
            # 注册协议到HKEY_CURRENT_USER\Software\Classes
            key_path = f"Software\\Classes\\{self.protocol_name}"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                winreg.SetValueEx(
                    key, "", 0, winreg.REG_SZ, f"URL:{self.app_name} Protocol"
                )
                winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")

            # 注册命令
            command_key_path = (
                f"Software\\Classes\\{self.protocol_name}\\shell\\open\\command"
            )
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_key_path) as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{exe_path}" --url "%1"')

            return True

        except Exception as e:
            logger.exception(f"Windows当前用户协议注册失败: {e}")
            return False

    def _unregister_windows_protocol(self) -> bool:
        """Windows系统注销协议（单用户模式，无需管理员权限）"""
        try:
            # 直接删除当前用户注册表项（单用户模式，无需管理员权限）
            return self._unregister_windows_protocol_current_user()

        except Exception as e:
            logger.exception(f"Windows协议注销失败: {e}")
            return False

    def _unregister_windows_protocol_current_user(self) -> bool:
        """注销当前用户的Windows协议"""
        try:
            # 删除当前用户注册表项
            key_path = f"Software\\Classes\\{self.protocol_name}\\shell\\open\\command"
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
            winreg.DeleteKey(
                winreg.HKEY_CURRENT_USER,
                f"Software\\Classes\\{self.protocol_name}\\shell\\open",
            )
            winreg.DeleteKey(
                winreg.HKEY_CURRENT_USER,
                f"Software\\Classes\\{self.protocol_name}\\shell",
            )
            winreg.DeleteKey(
                winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{self.protocol_name}"
            )
            return True

        except Exception as e:
            logger.exception(f"Windows当前用户协议注销失败: {e}")
            return False

    def _is_windows_protocol_registered(self) -> bool:
        """检查Windows协议是否已注册（单用户模式）"""
        try:
            # 检查HKEY_CURRENT_USER（用户级）
            key_path = f"Software\\Classes\\{self.protocol_name}"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                return True
        except (OSError, FileNotFoundError):
            return False

    def _register_linux_protocol(self) -> bool:
        """Linux系统注册协议"""
        try:
            # 获取当前可执行文件路径
            exe_path = self._get_executable_path()

            # 创建.desktop文件
            desktop_file_path = self._get_linux_desktop_file_path()
            desktop_content = self._generate_linux_desktop_file(exe_path)

            # 写入.desktop文件
            with open(desktop_file_path, "w", encoding="utf-8") as f:
                f.write(desktop_content)

            # 设置可执行权限
            os.chmod(desktop_file_path, 0o755)

            # 注册协议处理程序
            self._register_linux_mime_handler()

            # 更新桌面数据库
            self._update_linux_desktop_database()

            return True

        except Exception as e:
            logger.exception(f"Linux协议注册失败: {e}")
            return False

    def _unregister_linux_protocol(self) -> bool:
        """Linux系统注销协议"""
        try:
            desktop_file_path = self._get_linux_desktop_file_path()

            if os.path.exists(desktop_file_path):
                os.remove(desktop_file_path)

            # 更新桌面数据库
            self._update_linux_desktop_database()

            return True

        except Exception as e:
            logger.exception(f"Linux协议注销失败: {e}")
            return False

    def _is_linux_protocol_registered(self) -> bool:
        """检查Linux协议是否已注册"""
        desktop_file_path = self._get_linux_desktop_file_path()
        return os.path.exists(desktop_file_path)

    def _get_linux_desktop_file_path(self) -> str:
        """获取Linux桌面文件路径"""
        applications_dir = Path.home() / ".local" / "share" / "applications"
        applications_dir.mkdir(parents=True, exist_ok=True)
        return str(applications_dir / f"{self.app_name.lower()}-url-handler.desktop")

    def _generate_linux_desktop_file(self, exe_path: str) -> str:
        """生成Linux桌面文件内容"""
        return f"""[Desktop Entry]
Name={self.app_name} URL Handler
Comment=Handle {self.protocol_name}:// URLs for {self.app_name}
Exec={exe_path} --url %u
Icon={self.app_name.lower()}
Terminal=false
Type=Application
Categories=Utility;
MimeType=x-scheme-handler/{self.protocol_name};
"""

    def _register_linux_mime_handler(self):
        """注册Linux MIME处理程序"""
        try:
            # 使用xdg-mime注册协议处理程序
            subprocess.run(
                [
                    "xdg-mime",
                    "default",
                    f"{self.app_name.lower()}-url-handler.desktop",
                    f"x-scheme-handler/{self.protocol_name}",
                ],
                check=True,
                capture_output=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            # 如果xdg-mime不可用，尝试直接创建mimeapps.list
            self._create_linux_mimeapps_list()

    def _create_linux_mimeapps_list(self):
        """创建Linux mimeapps.list文件"""
        config_dir = Path.home() / ".config"
        config_dir.mkdir(parents=True, exist_ok=True)

        mimeapps_file = config_dir / "mimeapps.list"
        content = f"""[Default Applications]
x-scheme-handler/{self.protocol_name}={self.app_name.lower()}-url-handler.desktop

[Added Associations]
x-scheme-handler/{self.protocol_name}={self.app_name.lower()}-url-handler.desktop
"""

        with open(mimeapps_file, "a", encoding="utf-8") as f:
            f.write(content)

    def _update_linux_desktop_database(self):
        """更新Linux桌面数据库"""
        try:
            applications_dir = Path.home() / ".local" / "share" / "applications"
            subprocess.run(
                ["update-desktop-database", str(applications_dir)],
                check=True,
                capture_output=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            # 如果update-desktop-database不可用，忽略错误
            pass

    def _get_executable_path(self) -> str:
        """获取当前可执行文件路径"""
        if getattr(sys, "frozen", False):
            # PyInstaller打包后的可执行文件
            exe_path = sys.executable
        else:
            # 普通Python脚本
            exe_path = sys.argv[0]

        return os.path.abspath(exe_path)
