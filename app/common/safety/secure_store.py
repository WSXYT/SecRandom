import os
import json
import zlib
import hashlib
import platform
import ctypes
import uuid
from loguru import logger
from app.tools.path_utils import get_settings_path, ensure_dir

try:
    from Cryptodome.Cipher import AES
except Exception:
    try:
        from Crypto.Cipher import AES
    except Exception:
        AES = None


def _set_hidden(path: str) -> None:
    try:
        if platform.system() == "Windows":
            # Windows 平台：设置文件属性为隐藏和系统文件
            FILE_ATTRIBUTE_HIDDEN = 0x2
            FILE_ATTRIBUTE_SYSTEM = 0x4
            ctypes.windll.kernel32.SetFileAttributesW(
                path, FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM
            )
        else:  # Linux 平台：使用点前缀隐藏文件
            import os

            dirname = os.path.dirname(path)
            basename = os.path.basename(path)
            # 如果文件名已经以点开头，则不需要处理
            if basename.startswith("."):
                return
            # 将文件重命名为以点开头的文件名
            hidden_path = os.path.join(dirname, f".{basename}")
            # 如果隐藏文件已存在，先删除它
            if os.path.exists(hidden_path):
                os.remove(hidden_path)
            # 重命名原文件为隐藏文件
            os.rename(path, hidden_path)
    except Exception as e:
        logger.warning(f"隐藏文件失败: {e}")
        pass


def _get_machine_guid() -> str:
    if platform.system() == "Windows":
        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography"
            )
            val, _ = winreg.QueryValueEx(key, "MachineGuid")
            winreg.CloseKey(key)
            return str(val)
        except Exception:
            pass
    try:
        return str(uuid.getnode())
    except Exception:
        return "SecRandom"


def _platform_key() -> bytes:
    base = _get_machine_guid() + str(get_settings_path(""))
    return hashlib.sha256(base.encode("utf-8")).digest()[:16]


def _encrypt_payload(data: bytes, key: bytes) -> bytes:
    if AES:
        nonce = os.urandom(16)
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        ct = cipher.encrypt(data)
        return nonce + ct
    stream = hashlib.sha256(key).digest()
    obf = bytes(b ^ stream[i % len(stream)] for i, b in enumerate(data))
    return obf


def _decrypt_payload(payload: bytes, key: bytes) -> bytes:
    if AES:
        nonce = payload[:16]
        ct = payload[16:]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt(ct)
    stream = hashlib.sha256(key).digest()
    data = bytes(b ^ stream[i % len(stream)] for i, b in enumerate(payload))
    return data


def read_secrets() -> dict:
    p = get_settings_path("secrets.json")
    # 不存在则创建空文件
    if not os.path.exists(p):
        ensure_dir(os.path.dirname(p))
        with open(p, "wb") as f:
            f.write(b"")
        _set_hidden(p)
        logger.debug(f"创建空安全配置文件：{p}")
        return {}
    if os.path.exists(p):
        try:
            with open(p, "rb") as f:
                blob = f.read()
            if blob[:4] == b"SRV1":
                payload = blob[4:]
                key = _platform_key()
                data = _decrypt_payload(payload, key)
                dec = zlib.decompress(data)
                out = json.loads(dec.decode("utf-8"))
                logger.debug("读取安全配置成功（SRV1）")
                return out
            with open(p, "r", encoding="utf-8") as f:
                out = json.load(f)
                logger.debug("读取安全配置成功（JSON）")
                return out
        except Exception:
            try:
                with open(p, "r", encoding="utf-8") as f:
                    out = json.load(f)
                    logger.debug("读取安全配置成功（兼容JSON）")
                    return out
            except Exception:
                logger.warning("读取安全配置失败，返回空配置")

    return {}


def write_secrets(d: dict) -> None:
    p = get_settings_path("secrets.json")
    ensure_dir(os.path.dirname(p))
    try:
        raw = json.dumps(d, ensure_ascii=False, indent=4).encode("utf-8")
        comp = zlib.compress(raw, level=6)
        key = _platform_key()
        payload = _encrypt_payload(comp, key)
        with open(p, "wb") as f:
            f.write(b"SRV1" + payload)
        _set_hidden(p)
        logger.debug(f"写入安全配置成功：{p}")
    except Exception:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=4)
        logger.warning(f"写入安全配置降级为明文JSON：{p}")
