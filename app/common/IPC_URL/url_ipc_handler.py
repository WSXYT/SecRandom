"""
URL和IPC混合处理器 - 跨平台通用实现
"""

import json
import socket
import threading
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from loguru import logger
from urllib.parse import urlparse, parse_qs

from .protocol_manager import ProtocolManager
from .url_command_handler import URLCommandHandler
from .security_verifier import SimplePasswordVerifier


class URLIPCHandler:
    """URL和IPC混合处理器"""

    def __init__(self, app_name: str, protocol_name: str, password: str = None):
        """
        初始化URL IPC处理器

        Args:
            app_name: 应用程序名称
            protocol_name: 自定义协议名称（不含://）
            password: 可选的密码验证
        """
        self.app_name = app_name
        self.protocol_name = protocol_name
        self.protocol_manager = ProtocolManager(app_name, protocol_name)
        self.server_thread: Optional[threading.Thread] = None
        self.is_running = False
        self.message_handlers: Dict[str, Callable] = {}

        # 初始化命令处理器
        self.command_handler = URLCommandHandler()

        # 初始化安全验证器
        self.security_verifier = None
        if password:
            self.security_verifier = SimplePasswordVerifier(password)

    def register_url_protocol(self) -> bool:
        """
        注册URL协议

        Returns:
            注册成功返回True，失败返回False
        """
        try:
            return self.protocol_manager.register_protocol()
        except Exception as e:
            logger.exception(f"注册URL协议失败: {e}")
            return False

    def unregister_url_protocol(self) -> bool:
        """
        注销URL协议

        Returns:
            注销成功返回True，失败返回False
        """
        try:
            return self.protocol_manager.unregister_protocol()
        except Exception as e:
            logger.exception(f"注销URL协议失败: {e}")
            return False

    def is_protocol_registered(self) -> bool:
        """
        检查URL协议是否已注册

        Returns:
            已注册返回True，未注册返回False
        """
        return self.protocol_manager.is_protocol_registered()

    def start_ipc_server(self, port: int = 0) -> bool:
        """
        启动IPC服务器

        Args:
            port: 端口号，0表示自动分配

        Returns:
            启动成功返回True，失败返回False
        """
        if self.is_running:
            return True

        try:
            self.server_thread = threading.Thread(target=self._run_server, args=(port,))
            self.server_thread.daemon = True
            self.server_thread.start()
            self.is_running = True
            return True
        except Exception as e:
            logger.exception(f"启动IPC服务器失败: {e}")
            return False

    def stop_ipc_server(self):
        """停止IPC服务器"""
        self.is_running = False
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(timeout=1)

    def _run_server(self, port: int):
        """运行IPC服务器"""
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            if port == 0:
                # 自动分配端口
                server_socket.bind(("localhost", 0))
                port = server_socket.getsockname()[1]
            else:
                server_socket.bind(("localhost", port))

            server_socket.listen(5)

            # 保存端口信息到配置文件
            self._save_port_config(port)

            while self.is_running:
                try:
                    server_socket.settimeout(1.0)  # 1秒超时
                    client_socket, address = server_socket.accept()

                    # 处理客户端连接
                    client_thread = threading.Thread(
                        target=self._handle_client, args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()

                except socket.timeout:
                    continue
                except Exception as e:
                    if self.is_running:
                        logger.exception(f"IPC服务器错误: {e}")
                    break

        except Exception as e:
            logger.exception(f"IPC服务器启动错误: {e}")
        finally:
            if "server_socket" in locals():
                server_socket.close()

    def _handle_client(self, client_socket: socket.socket, address: tuple):
        """处理客户端连接"""
        try:
            data = client_socket.recv(4096).decode("utf-8")
            if data:
                message = json.loads(data)
                response = self._process_message(message)
                client_socket.send(json.dumps(response).encode("utf-8"))
        except Exception as e:
            logger.exception(f"处理IPC消息错误: {e}")
        finally:
            client_socket.close()

    def _process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """处理接收到的消息"""
        message_type = message.get("type", "")
        payload = message.get("payload", {})

        logger.debug(f"收到消息 - 类型: {message_type}, 负载: {payload}")

        # 处理URL消息
        if message_type == "url":
            result = self._handle_url_message(payload)
            logger.debug(f"URL消息处理结果: {result}")
            return result

        # 处理其他消息类型
        if message_type in self.message_handlers:
            try:
                result = self.message_handlers[message_type](payload)
                response = {"success": True, "type": message_type, "result": result}
                logger.debug(f"消息处理成功 - 类型: {message_type}, 结果: {result}")
                return response
            except Exception as e:
                error_response = {
                    "success": False,
                    "type": message_type,
                    "error": str(e),
                }
                logger.exception(f"消息处理失败 - 类型: {message_type}, 错误: {e}")
                return error_response
        else:
            unknown_response = {
                "success": False,
                "type": message_type,
                "error": f"未知的消息类型: {message_type}",
            }
            logger.warning(f"未知消息类型: {message_type}")
            return unknown_response

    def _handle_url_message(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """处理URL消息"""
        url = payload.get("url", "")
        if not url:
            logger.warning("URL消息缺少URL参数")
            return {"success": False, "error": "缺少URL参数"}

        logger.debug(f"处理URL消息: {url}")

        # 验证URL
        verification = payload.get("verification", {})
        if self.security_verifier:
            logger.debug(f"进行安全验证: {verification}")
            if not self.security_verifier.verify(verification):
                logger.warning(f"URL安全验证失败: {url}")
                return {"success": False, "error": "安全验证失败"}
            logger.debug("安全验证通过")

        # 处理URL命令
        try:
            logger.debug(f"执行URL命令: {url}")
            result = self.command_handler.handle_url(url)
            logger.info(f"URL命令执行成功: {url}, 结果: {result}")
            return {"success": True, "result": result}
        except Exception as e:
            logger.exception(f"URL命令执行失败: {url}, 错误: {e}")
            return {"success": False, "error": str(e)}

    def register_message_handler(self, message_type: str, handler: Callable):
        """
        注册消息处理器

        Args:
            message_type: 消息类型
            handler: 处理函数
        """
        self.message_handlers[message_type] = handler

    def send_ipc_message(
        self, port: int, message: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        发送IPC消息

        Args:
            port: 目标端口
            message: 消息内容

        Returns:
            响应内容，失败返回None
        """
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5.0)  # 5秒超时
            client_socket.connect(("localhost", port))

            client_socket.send(json.dumps(message).encode("utf-8"))
            response_data = client_socket.recv(4096).decode("utf-8")

            client_socket.close()
            return json.loads(response_data)

        except Exception as e:
            logger.exception(f"发送IPC消息失败: {e}")
            return None

    def _save_port_config(self, port: int):
        """保存端口配置"""
        config_dir = Path.home() / ".config" / self.app_name
        config_dir.mkdir(parents=True, exist_ok=True)

        config_file = config_dir / "ipc_config.json"
        config = {"port": port}

        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    def load_port_config(self) -> Optional[int]:
        """加载端口配置"""
        config_file = Path.home() / ".config" / self.app_name / "ipc_config.json"

        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    return config.get("port")
            except Exception as e:
                logger.exception(f"加载端口配置失败: {e}")

        return None

    def handle_url_args(self, url: str) -> Dict[str, Any]:
        """
        处理URL参数

        Args:
            url: URL字符串

        Returns:
            解析后的参数
        """
        logger.debug(f"处理URL参数: {url}")

        try:
            parsed = urlparse(url)

            # 检查协议是否匹配
            if parsed.scheme != self.protocol_name:
                logger.warning(
                    f"协议不匹配 - 期望: {self.protocol_name}, 实际: {parsed.scheme}"
                )
                return {"success": False, "error": f"不匹配的协议: {parsed.scheme}"}

            # 解析查询参数
            params = parse_qs(parsed.query)

            # 扁平化参数值（parse_qs返回的是列表）
            flat_params = {k: v[0] if len(v) == 1 else v for k, v in params.items()}

            result = {
                "success": True,
                "path": parsed.path,
                "params": flat_params,
                "action": parsed.path.lstrip("/"),
            }
            logger.debug(f"URL参数解析成功: {result}")
            return result

        except Exception as e:
            logger.exception(f"URL参数解析失败: {url}, 错误: {e}")
            return {"success": False, "error": str(e)}

    def execute_url_command(
        self, url: str, verification: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        执行URL命令（带安全验证）

        Args:
            url: URL命令
            verification: 验证信息

        Returns:
            执行结果
        """
        logger.debug(f"执行URL命令: {url}")

        # 验证URL
        if self.security_verifier:
            verification = verification or {}
            logger.debug(f"进行安全验证: {verification}")
            if not self.security_verifier.verify(verification):
                logger.warning(f"安全验证失败: {url}")
                return {"success": False, "error": "安全验证失败"}
            logger.debug("安全验证通过")

        # 执行命令
        try:
            result = self.command_handler.handle_url(url)
            logger.info(f"URL命令执行成功: {url}, 结果: {result}")
            return {"success": True, "result": result}
        except Exception as e:
            logger.exception(f"URL命令执行失败: {url}, 错误: {e}")
            return {"success": False, "error": str(e)}

    def get_available_commands(self) -> Dict[str, Any]:
        """
        获取可用命令列表

        Returns:
            可用命令列表
        """
        return self.command_handler.get_available_commands()
