# ==================================================
# 导入模块
# ==================================================
import asyncio
import shutil
import subprocess
import sys
from tempfile import NamedTemporaryFile
import time
from typing import Any, Tuple, Callable, Optional
import zipfile
import aiohttp
from loguru import logger
import yaml
from app.tools.path_utils import *
from app.tools.variable import *
from app.tools.settings_access import *


# ==================================================
# 辅助函数
# ==================================================
def safe_int(s: str) -> int:
    """安全地将字符串转换为整数

    Args:
        s (str): 要转换的字符串

    Returns:
        int: 转换后的整数，如果转换失败则返回 0
    """
    try:
        return int(s) if s else 0
    except ValueError:
        return 0


def _run_async_func(async_func: Any, *args: Any, **kwargs: Any) -> Any:
    """运行异步函数（同步包装器）

    Args:
        async_func: 要运行的异步函数
        *args: 位置参数
        **kwargs: 关键字参数

    Returns:
        Any: 异步函数的返回值
    """
    try:
        return asyncio.run(async_func(*args, **kwargs))
    except Exception as e:
        logger.error(f"运行异步函数失败: {e}")
        return None


def extract_zip(zip_path: str, target_dir: str | Path, overwrite: bool = True) -> bool:
    """解压zip文件到指定目录

    Args:
        zip_path (str): zip文件路径
        target_dir (str | Path): 目标目录
        overwrite (bool, optional): 是否覆盖现有文件. Defaults to True.

    Returns:
        bool: 解压成功返回True，否则返回False
    """
    try:
        logger.debug(f"开始解压文件: {zip_path} 到 {target_dir}")

        # 确保目标目录存在
        ensure_dir(target_dir)

        # 打开zip文件
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            # 获取所有文件列表
            file_list = zip_ref.namelist()
            # 创建已解压文件列表
            extracted_files = set()

            for file in file_list:
                # 构建目标文件路径
                target_file = Path(target_dir) / file

                # 确保父目录存在
                ensure_dir(target_file.parent)

                # 如果文件已存在且不允许覆盖，跳过
                if target_file.exists() and not overwrite:
                    logger.debug(f"文件已存在，跳过: {target_file}")
                    continue

                # 解压文件
                zip_ref.extract(file, target_dir)
                # 添加到已解压文件列表
                extracted_files.add(file)

        logger.debug(f"成功解压以下文件: {extracted_files}")

        logger.debug(f"文件解压完成: {zip_path} 到 {target_dir}")
        return True
    except Exception as e:
        logger.error(f"解压文件失败: {e}")
        return False


def parse_version(version_str: str) -> Tuple[list[int], list[str]]:
    """解析版本号为数字部分和预发布部分

    Args:
        version_str (str): 版本号字符串，如 "1.2.3" 或 "1.2.3-alpha.1"

    Returns:
        Tuple[list[int], list[str]]: 数字部分和预发布部分的元组
    """
    if "-" in version_str:
        main_version, pre_release = version_str.split("-", 1)
        pre_parts = pre_release.split(".")
    else:
        main_version = version_str
        pre_parts = []

    # 分割主版本号为数字部分
    main_parts = list(map(safe_int, main_version.split(".")))
    return main_parts, pre_parts


# ==================================================
# 更新工具函数
# ==================================================
def get_update_source_url() -> str:
    """
    获取更新源 URL

    Returns:
        str: 更新源 URL，如果获取失败则返回默认值
    """
    try:
        # 从设置中读取更新源
        update_source = readme_settings("update", "update_source")
        source_url = SOURCE_MAP.get(update_source, "https://github.com")
        logger.debug(f"获取更新源 URL 成功: {source_url}")
        return source_url
    except Exception as e:
        logger.error(f"获取更新源 URL 失败: {e}")
        return "https://github.com"


def get_update_check_url() -> str:
    """
    获取更新检查 URL

    Returns:
        str: 更新检查 URL
    """
    source_url = get_update_source_url()
    repo_url = GITHUB_WEB

    # 构建完整的 GitHub URL
    github_raw_url = f"{repo_url}/raw/master/metadata.yaml"

    # 如果是默认源（GitHub），直接返回
    if source_url == "https://github.com":
        update_check_url = github_raw_url
    else:
        # 其他镜像源，在 GitHub URL 前添加镜像源 URL
        update_check_url = f"{source_url}/{github_raw_url}"

    logger.debug(f"生成更新检查 URL 成功: {update_check_url}")
    return update_check_url


async def get_metadata_info_async() -> dict | None:
    """
    异步获取 metadata.yaml 文件信息

    Returns:
        dict: metadata.yaml 文件的内容，如果读取失败则返回 None
    """
    try:
        update_check_url = get_update_check_url()
        logger.debug(f"从网络获取 metadata.yaml: {update_check_url}")

        async with aiohttp.ClientSession() as session:
            async with session.get(update_check_url, timeout=10) as response:
                response.raise_for_status()
                content = await response.text()
                metadata = yaml.safe_load(content)
                logger.debug("成功从网络读取 metadata.yaml 文件")
                return metadata
    except Exception as e:
        logger.error(f"从网络获取 metadata.yaml 文件失败: {e}")
        return None


def get_metadata_info() -> dict | None:
    """
    获取 metadata.yaml 文件信息（同步版本）

    Returns:
        dict: metadata.yaml 文件的内容，如果读取失败则返回 None
    """
    return _run_async_func(get_metadata_info_async)


async def get_latest_version_async(channel: int | None = None) -> dict | None:
    """
    获取最新版本信息（异步版本）

    Args:
        channel (int, optional): 更新通道，默认为 None，此时会从设置中读取
        0: 稳定通道(release), 1: 测试通道(beta), 2: 发布预览通道

    Returns:
        dict: 包含版本号和版本号数字的字典，格式为 {"version": str, "version_no": int}
    """
    try:
        # 如果没有指定通道，从设置中读取
        if channel is None:
            channel = readme_settings("update", "update_channel")

        # 获取 metadata 信息
        metadata = await get_metadata_info_async()
        if not metadata:
            return None

        channel_name = CHANNEL_MAP.get(channel, "release")
        latest = metadata.get("latest", {})
        latest_no = metadata.get("latest_no", {})

        # 获取版本信息，如果通道不存在则使用稳定通道的版本
        version = latest.get(channel_name, latest.get("release", VERSION))
        version_no = latest_no.get(channel_name, latest_no.get("release", 0))

        # 如果版本号是Disable，返回当前版本，禁止该通道更新
        if version == "Disable":
            logger.debug(f"通道 {channel_name} 已禁用，返回当前版本")
            return {"version": VERSION, "version_no": 0}

        logger.debug(
            f"获取最新版本信息成功: 通道={channel_name}, 版本={version}, 版本号={version_no}"
        )
        return {"version": version, "version_no": version_no}
    except Exception as e:
        logger.error(f"获取最新版本信息失败: {e}")
        return None


def get_latest_version(channel: int | None = None) -> dict | None:
    """
    获取最新版本信息（同步版本）

    Args:
        channel (int, optional): 更新通道，默认为 None，此时会从设置中读取
        0: 稳定通道(release), 1: 测试通道(beta), 2: 发布预览通道

    Returns:
        dict: 包含版本号和版本号数字的字典，格式为 {"version": str, "version_no": int}
    """
    return _run_async_func(get_latest_version_async, channel)


def compare_versions(current_version: str, latest_version: str) -> int:
    """
    比较版本号，支持语义化版本号格式，包括预发布版本

    Args:
        current_version (str): 当前版本号，格式为 "vX.X.X"、"vX.X.X.X" 或 "vX.X.X-alpha.1" 等
        latest_version (str): 最新版本号，格式为 "vX.X.X"、"vX.X.X.X" 或 "vX.X.X-alpha.1" 等

    Returns:
        int: 1 表示有新版本，0 表示版本相同，-1 表示比较失败
    """
    try:
        # 检查版本号是否为空
        if not current_version or not latest_version:
            logger.error(
                f"比较版本号失败: 版本号为空，current={current_version}, latest={latest_version}"
            )
            return -1

        # 移除版本号前缀 "v"
        current = current_version.lstrip("v")
        latest = latest_version.lstrip("v")

        # 解析两个版本号
        current_main, current_pre = parse_version(current)
        latest_main, latest_pre = parse_version(latest)

        # 比较主版本号部分
        for i in range(max(len(current_main), len(latest_main))):
            current_part = current_main[i] if i < len(current_main) else 0
            latest_part = latest_main[i] if i < len(latest_main) else 0

            if latest_part > current_part:
                return 1
            elif latest_part < current_part:
                return -1

        # 主版本号相同，比较预发布版本
        # 规则：没有预发布标识符的版本 > 有预发布标识符的版本
        if not current_pre and not latest_pre:
            return 0  # 两个都是正式版本，版本号相同
        elif not current_pre:
            return -1  # 当前是正式版本，最新是预发布版本，当前版本更新
        elif not latest_pre:
            return 1  # 当前是预发布版本，最新是正式版本，有新版本

        # 两个都是预发布版本，比较预发布部分
        for i in range(max(len(current_pre), len(latest_pre))):
            if i >= len(current_pre):
                return 1  # 当前预发布部分更短，最新版本更新
            if i >= len(latest_pre):
                return -1  # 最新预发布部分更短，当前版本更新

            current_pre_part = current_pre[i]
            latest_pre_part = latest_pre[i]

            # 尝试转换为整数比较
            try:
                current_pre_int = int(current_pre_part)
                latest_pre_int = int(latest_pre_part)
                if latest_pre_int > current_pre_int:
                    return 1
                elif latest_pre_int < current_pre_int:
                    return -1
            except ValueError:
                # 不是数字，按字典序比较
                if latest_pre_part > current_pre_part:
                    return 1
                elif latest_pre_part < current_pre_part:
                    return -1

        return 0  # 版本号完全相同
    except Exception as e:
        logger.error(f"比较版本号失败: {e}")
        return -1


def get_update_download_url(
    version: str, system: str = SYSTEM, arch: str = ARCH, struct: str = STRUCT
) -> str:
    """
    获取更新下载 URL

    Args:
        version (str): 版本号，格式为 "vX.X.X.X"
        system (str, optional): 系统，默认为当前系统
        arch (str, optional): 架构，默认为当前架构
        struct (str, optional): 结构，默认为当前结构

    Returns:
        str: 更新下载 URL
    """
    try:
        # 获取更新源 URL
        source_url = get_update_source_url()

        # 获取 GitHub 仓库 URL
        repo_url = GITHUB_WEB

        # 从 metadata.yaml 获取文件名格式
        name_format = "SecRandom-[system]-[version]-[arch]-[struct].zip"

        # 替换占位符生成实际文件名
        file_name = name_format.replace("[system]", system)
        file_name = file_name.replace("[version]", version)
        file_name = file_name.replace("[arch]", arch)
        file_name = file_name.replace("[struct]", struct)

        # 构建完整的 GitHub 下载 URL
        github_download_url = f"{repo_url}/releases/download/{version}/{file_name}"

        # 如果是默认源（GitHub），直接返回
        if source_url == "https://github.com":
            download_url = github_download_url
        else:
            # 其他镜像源，在 GitHub URL 前添加镜像源 URL
            download_url = f"{source_url}/{github_download_url}"

        logger.debug(f"生成更新下载 URL 成功: {download_url}")
        return download_url
    except Exception as e:
        logger.error(f"生成更新下载 URL 失败: {e}")
        # 返回默认的 GitHub 下载 URL
        return f"https://github.com/SECTL/SecRandom/releases/download/{version}/SecRandom-{system}-{version}-{arch}-{struct}.zip"


async def download_update_async(
    version: str,
    system: str = SYSTEM,
    arch: str = ARCH,
    struct: str = STRUCT,
    progress_callback: Optional[Callable] = None,
    timeout: int = 300,  # 增加超时参数，默认300秒
) -> Optional[str]:
    """
    异步下载更新文件

    Args:
        version (str): 版本号，格式为 "vX.X.X.X"
        system (str, optional): 系统，默认为当前系统
        arch (str, optional): 架构，默认为当前架构
        struct (str, optional): 结构，默认为当前结构
        progress_callback (Optional[Callable]): 进度回调函数，接收已下载字节数和总字节数
        timeout (int, optional): 下载超时时间（秒），默认300秒

    Returns:
        Optional[str]: 下载完成的文件路径，如果下载失败则返回 None
    """
    try:
        # 获取下载 URL
        download_url = get_update_download_url(version, system, arch, struct)
        logger.debug(f"开始下载更新文件: {download_url}")

        # 从 metadata.yaml 获取文件名格式
        name_format = "SecRandom-[system]-[version]-[arch]-[struct].zip"

        # 替换占位符生成实际文件名
        file_name = name_format.replace("[system]", system)
        file_name = file_name.replace("[version]", version)
        file_name = file_name.replace("[arch]", arch)
        file_name = file_name.replace("[struct]", struct)

        # 确定下载保存路径
        download_dir = get_data_path("downloads")
        ensure_dir(download_dir)
        file_path = download_dir / file_name

        # 配置客户端超时设置
        client_timeout = aiohttp.ClientTimeout(
            total=timeout,  # 总超时时间
            connect=30,  # 连接超时时间
            sock_read=60,  # 读取超时时间
            sock_connect=30,  # Socket连接超时时间
        )

        # 发送异步请求
        async with aiohttp.ClientSession(timeout=client_timeout) as session:
            async with session.get(
                download_url,
                allow_redirects=True,
                headers={"User-Agent": "SecRandom Update Client"},
            ) as response:
                response.raise_for_status()

                # 获取文件总大小
                total_size = int(response.headers.get("Content-Length", 0))
                downloaded_size = 0
                last_progress_time = time.time()

                # 开始下载文件
                with open(file_path, "wb") as f:
                    # 使用更大的块大小提高下载速度
                    async for chunk in response.content.iter_chunked(32768):
                        if not chunk:
                            break

                        # 写入文件
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        last_progress_time = time.time()

                        # 调用进度回调函数
                        if progress_callback:
                            progress_callback(downloaded_size, total_size)

        logger.debug(f"更新文件下载成功: {file_path}")
        return file_path
    except aiohttp.ClientTimeout as e:
        logger.error(f"下载超时: {e}")
        return None
    except aiohttp.ClientError as e:
        logger.error(f"HTTP请求失败: {e}")
        # 尝试使用不同的超时策略重试一次
        logger.info("尝试使用更长超时时间重试下载...")
        return await download_update_async(
            version, system, arch, struct, progress_callback, timeout=timeout * 2
        )
    except Exception as e:
        logger.error(f"下载更新文件失败: {e}")
        return None


def download_update(
    version: str,
    system: str = SYSTEM,
    arch: str = ARCH,
    struct: str = STRUCT,
    progress_callback: Optional[Callable] = None,
    timeout: int = 300,  # 增加超时参数，默认300秒
) -> Optional[str]:
    """
    下载更新文件（同步版本）

    Args:
        version (str): 版本号，格式为 "vX.X.X.X"
        system (str, optional): 系统，默认为当前系统
        arch (str, optional): 架构，默认为当前架构
        struct (str, optional): 结构，默认为当前结构
        progress_callback (Optional[Callable]): 进度回调函数，接收已下载字节数和总字节数
        timeout (int, optional): 下载超时时间（秒），默认300秒

    Returns:
        Optional[str]: 下载完成的文件路径，如果下载失败则返回 None
    """
    return _run_async_func(
        download_update_async, version, system, arch, struct, progress_callback, timeout
    )


async def install_update_async(file_path: str) -> bool:
    """
    异步安装更新文件

    Args:
        file_path (str): 更新文件的路径

    Returns:
        bool: 安装成功返回 True，否则返回 False
    """
    temp_script_path = (
        get_path("TEMP") / "installer_temp_script.py"
    )  # 初始化为临时脚本路径，便于后续清理
    try:
        logger.debug(f"开始安装更新文件: {file_path}")

        # 验证更新文件存在
        if not Path(file_path).exists():
            logger.error(f"更新文件不存在: {file_path}")
            return False

        # 判断是否是开发环境
        is_dev_env = False
        try:
            # 检查是否存在 .git 目录
            git_dir = get_path(".git")
            is_dev_env = git_dir.exists()
        except Exception as e:
            logger.debug(f"检查开发环境失败: {e}")

        if is_dev_env:
            # 开发环境：安装到 TEMP 文件夹
            logger.info("开发环境，安装到 TEMP 文件夹")
            temp_dir = get_path("TEMP")
            ensure_dir(temp_dir)

            # 解压更新文件到 TEMP 目录
            success = extract_zip(file_path, temp_dir, overwrite=True)
            if success:
                # 开发环境：删除旧版本文件
                old_version_dir = get_path("SecRandom")
                if old_version_dir.exists():
                    shutil.rmtree(old_version_dir)
                    logger.info(f"删除旧版本目录: {old_version_dir}")

                logger.info(f"开发环境更新文件安装成功: {file_path}")
                return True
            else:
                logger.error(f"开发环境更新文件安装失败: {file_path}")
                return False
        else:
            # 生产环境：新开进程安装，主进程关闭
            logger.info("生产环境，准备启动独立更新进程")

            # 获取根目录
            root_dir = get_app_root()
            if not Path(root_dir).exists():
                logger.error(f"应用根目录不存在: {root_dir}")
                return False

            # 创建临时安装脚本
            installer_script = """
import zipfile
import os
import sys
import shutil
import time
from pathlib import Path

# 配置日志
from loguru import logger

# 确保日志目录存在
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

# 配置日志格式 - 文件输出
logger.add(
    log_dir / 'update_install_{time:YYYY-MM-DD}.log',
    rotation='1 MB',
    retention='30 days',
    compression='tar.gz',
    backtrace=True,
    diagnose=True,
    level='INFO',
    format='<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>'
)

# 配置日志格式 - 终端输出
if sys.stdout is not None:
    logger.add(
        sys.stdout,
        format='<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>',
        level='INFO',
        colorize=True
    )


def ensure_dir(path):
    # 确保目录存在
    Path(path).mkdir(parents=True, exist_ok=True)


def extract_zip(zip_path, target_dir, overwrite=True):
    # 解压zip文件
    try:
        logger.info(f"开始解压文件: {zip_path} 到 {target_dir}")
        ensure_dir(target_dir)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                target_file = Path(target_dir) / file
                ensure_dir(target_file.parent)

                if target_file.exists() and not overwrite:
                    logger.info(f"文件已存在，跳过: {target_file}")
                    continue

                # 解压文件
                try:
                    zip_ref.extract(file, target_dir)
                    logger.info(f"解压文件成功: {target_file}")
                except PermissionError:
                    # Windows 上可能需要删除旧文件
                    if target_file.exists():
                        try:
                            target_file.unlink()
                            zip_ref.extract(file, target_dir)
                            logger.info(f"重新解压文件成功: {target_file}")
                        except Exception as e:
                            logger.warning(f"覆盖文件失败，跳过: {target_file}, 错误: {e}")
                            continue
                    else:
                        raise

                # Linux系统下设置可执行权限
                if os.name != 'nt' and file.endswith(('.py', '.sh')):
                    try:
                        # 获取文件的当前权限
                        current_mode = os.stat(target_file).st_mode
                        # 添加执行权限
                        os.chmod(target_file, current_mode | 0o111)
                        logger.info(f"已设置文件执行权限: {target_file}")
                    except Exception as e:
                        logger.warning(f"设置文件执行权限失败: {e}")

        logger.info(f"文件解压完成: {zip_path} 到 {target_dir}")
        return True
    except Exception as e:
        logger.error(f"解压文件失败: {e}")
        return False


def restart_application(root_dir):
    try:
        logger.info("准备重启应用程序")

        # 确定主程序文件
        main_program = None
        possible_main_files = ['main.py', 'SecRandom', 'SecRandom.exe']

        for main_file in possible_main_files:
            main_path = Path(root_dir) / main_file
            if main_path.exists():
                main_program = main_path
                break

        if not main_program:
            logger.error("未找到主程序文件")
            return False

        logger.info(f"找到主程序文件: {main_program}")

        # 根据系统类型选择重启方式
        if os.name == 'nt':
            # Windows系统 - 使用引号保护路径中的空格
            logger.info("Windows系统，使用start命令重启")
            import subprocess
            subprocess.Popen(
                ['start', '""', f'"{main_program}"'],
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            # Linux系统
            logger.info("Linux系统，使用nohup命令后台重启")
            import subprocess
            subprocess.Popen(
                [sys.executable, str(main_program)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )

        logger.info("应用程序重启成功")
        return True
    except Exception as e:
        logger.error(f"重启应用程序失败: {e}")
        return False


if __name__ == '__main__':
    try:
        # 获取参数
        update_file = sys.argv[1]
        root_dir = sys.argv[2]

        logger.info(f"更新安装脚本启动")
        logger.info(f"更新文件: {update_file}")
        logger.info(f"根目录: {root_dir}")

        # 验证参数
        if not Path(update_file).exists():
            logger.error(f"更新文件不存在: {update_file}")
            sys.exit(1)

        if not Path(root_dir).exists():
            logger.error(f"根目录不存在: {root_dir}")
            sys.exit(1)

        # 等待一段时间，确保主进程已关闭（可配置）
        wait_time = 2
        logger.info(f"等待主进程关闭... ({wait_time}秒)")
        time.sleep(wait_time)

        # 解压更新文件到根目录
        success = extract_zip(update_file, root_dir, overwrite=True)
        if success:
            logger.info("更新安装成功")

            # 重启应用程序
            restart_application(root_dir)

            # 删除下载的更新文件
            logger.info(f"准备删除更新文件: {update_file}")
            try:
                time.sleep(1)  # 给文件系统一点时间
                Path(update_file).unlink()
                logger.info(f"更新文件已删除: {update_file}")
            except Exception as e:
                logger.error(f"删除更新文件失败: {e}")
        else:
            logger.error("更新安装失败")
            sys.exit(1)

    except Exception as e:
        logger.error(f"更新安装脚本执行失败: {e}")
        sys.exit(1)
"""

            # 写入临时脚本文件
            try:
                with NamedTemporaryFile(
                    mode="w", encoding="utf-8", delete=False, suffix=".py"
                ) as temp_script:
                    temp_script.write(installer_script)
                    temp_script_path = temp_script.name
                    logger.debug(f"临时脚本已创建: {temp_script_path}")
            except Exception as e:
                logger.error(f"创建临时脚本失败: {e}")
                return False

            try:
                # 启动独立更新进程
                logger.info("启动独立更新进程")
                subprocess.Popen(
                    [sys.executable, temp_script_path, file_path, str(root_dir)],
                    close_fds=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                    if sys.platform == "win32"
                    else 0,
                )

                # 给子进程足够的时间启动
                time.sleep(1)

                # 关闭主进程
                logger.info("生产环境更新进程已启动，主进程将关闭")
                sys.exit(0)
            except Exception as e:
                logger.error(f"启动更新进程失败: {e}")
                return False

            return True
    except Exception as e:
        logger.error(f"安装更新文件失败: {e}")
        return False
    finally:
        # 说明：
        # - 生产环境中，临时安装脚本会在子进程内部自删除；
        # - 开发环境中，不会创建临时安装脚本（temp_script_path 为空）。
        # 因此，此处不再尝试在主进程中清理临时脚本文件，以避免无效的清理逻辑。
        pass


def install_update(file_path: str) -> bool:
    """
    安装更新文件（同步版本）

    Args:
        file_path (str): 更新文件的路径

    Returns:
        bool: 安装成功返回 True，否则返回 False
    """
    return _run_async_func(install_update_async, file_path)
