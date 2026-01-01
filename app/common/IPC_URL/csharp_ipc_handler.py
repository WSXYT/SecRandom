import asyncio
import threading
from typing import Optional
from loguru import logger

from app.tools.path_utils import get_data_path

# 导入 Python.NET
from pythonnet import load
load("coreclr", runtime_config=get_data_path("dlls", "dotnet.runtimeconfig.json"))

# 加载 .NET CoreCLR 程序集
import clr
clr.AddReference("ClassIsland.Shared.IPC")
clr.AddReference("SecRandom4CiTest.Interface")

# 导入程序集
from System import Action
from ClassIsland.Shared.IPC import IpcClient, IpcRoutedNotifyIds
from ClassIsland.Shared.IPC.Abstractions.Services import IPublicLessonsService, IFooService
from dotnetCampus.Ipc.CompilerServices.GeneratedProxies import GeneratedIpcFactory
from SecRandom4CiTest.Interface.Services import ISecRandomService
from SecRandom4CiTest.Interface.Models import CallResult, Student


class CSharpIPCHandler:
    """C# dotnetCampus.Ipc 处理器，用于连接 ClassIsland 实例"""
    _instance: Optional["CSharpIPCHandler"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @classmethod
    def instance(cls):
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """
        初始化 C# IPC 处理器
        """
        self.ipc_client: Optional[IpcClient] = None
        self.client_thread: Optional[threading.Thread] = None
        self.is_running = False
    
    def start_ipc_client(self) -> bool:
        """
        启动 C# IPC 客户端

        Returns:
            启动成功返回True，失败返回False
        """
        if self.is_running:
            return True

        try:
            self.client_thread = threading.Thread(target=self._run_client, daemon=False)
            self.client_thread.start()
            self.is_running = True
            return True
        except Exception as e:
            logger.error(f"启动 C# IPC 客户端失败: {e}")
            return False

    def stop_ipc_client(self):
        """停止 C# IPC 客户端"""
        self.is_running = False
        if self.client_thread and self.client_thread.is_alive():
            self.client_thread.join(timeout=1)
    
    def send_notification(
            self,
            class_name,
            selected_students,
            draw_count=1,
            settings=None,
            settings_group=None
        ):
        logger.debug(settings)
        if settings:
            display_duration = settings.get("notification_display_duration", 5)
        else:
            display_duration = 5
        
        randomService = GeneratedIpcFactory.CreateIpcProxy[ISecRandomService](
            self.ipc_client.Provider, self.ipc_client.PeerProxy)
        result = self.convert_to_call_result(class_name, selected_students, draw_count, display_duration)
        randomService.NotifyResult(result)

    @staticmethod
    def convert_to_call_result(class_name: str, selected_students, draw_count: int, display_duration=5.0) -> CallResult:
        result = CallResult()
        result.ClassName = class_name
        result.DrawCount = draw_count
        result.DisplayDuration = display_duration
        for student in selected_students:
            cs_student = Student()
            cs_student.StudentId = student[0]
            cs_student.StudentName = student[1]
            cs_student.Exists = student[2]
            result.SelectedStudents.Add(cs_student)
        return result

    def _on_class_test(self):
        lessonSc = GeneratedIpcFactory.CreateIpcProxy[IPublicLessonsService](
            self.ipc_client.Provider, self.ipc_client.PeerProxy)
        logger.debug(f"上课 {lessonSc.CurrentSubject.Name} 时间: {lessonSc.CurrentTimeLayoutItem}")

    def _run_client(self):
        """运行 C# IPC 客户端"""

        async def client():
            """异步客户端"""

            self.ipc_client = IpcClient()
            self.ipc_client.JsonIpcProvider.AddNotifyHandler(IpcRoutedNotifyIds.OnClassNotifyId, Action(lambda: self._on_class_test()))

            task = self.ipc_client.Connect()
            await loop.run_in_executor(None, lambda: task.Wait())
            
            while self.is_running:
                await asyncio.sleep(1)
            
            self.ipc_client = None
        
        # 启动新的 asyncio 事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(client())
        loop.close()    
