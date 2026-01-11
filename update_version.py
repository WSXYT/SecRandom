import os
import re


def get_version_from_env():
    original_version = os.getenv("VERSION", "v0.0.0")
    stripped_version = re.sub(r"^v", "", original_version)
    # 匹配数字版本部分，包括预发布版本标识符之前的部分
    numeric_version = re.search(
        r"^(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:\.(\d+))?", stripped_version
    )
    if numeric_version:
        parts = numeric_version.groups(default="0")
        # 确保至少有三位数字
        if parts[2] is None:
            stripped_version = f"{parts[0]}.{parts[1]}.0"
        elif parts[3] is None:
            stripped_version = f"{parts[0]}.{parts[1]}.{parts[2]}"
        else:
            stripped_version = ".".join(parts)
    else:
        stripped_version = "0.0.0"
        original_version = "v0.0.0"
    return original_version, stripped_version


def update_version_info(version):
    # 处理三位或四位数字的版本号
    version_parts = version.split(".")
    # 确保有四位数字
    while len(version_parts) < 4:
        version_parts.append("0")
    # 只取前四位
    major, minor, patch, build = map(int, version_parts[:4])

    version_tuple = (major, minor, patch, build)
    version_str = f"{major}.{minor}.{patch}.{build}"

    with open("version_info.txt", "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(
        r"filevers=\(\d, \d, \d, \d\)", f"filevers={version_tuple}", content
    )
    content = re.sub(
        r"prodvers=\(\d, \d, \d, \d\)", f"prodvers={version_tuple}", content
    )
    content = re.sub(
        r"StringStruct\(u\'FileVersion\', u\'[^\']+\'\)",
        f"StringStruct(u'FileVersion', u'{version_str}')",
        content,
    )
    content = re.sub(
        r"StringStruct\(u\'ProductVersion\', u\'[^\']+\'\)",
        f"StringStruct(u'ProductVersion', u'{version_str}')",
        content,
    )

    with open("version_info.txt", "w", encoding="utf-8") as f:
        f.write(content)


def update_config_py(version):
    with open("app/tools/variable.py", "r", encoding="utf-8") as f:
        content = f.read()
    # 匹配更广泛的版本号格式，包括三位数字、四位数字和预发布版本
    content = re.sub(r'VERSION = "v?[^\"]+"', f'VERSION = "{version}"', content)
    with open("app/tools/variable.py", "w", encoding="utf-8") as f:
        f.write(content)


def update_iss_version(stripped_version):
    if os.path.exists("SRsetup.iss"):
        with open("SRsetup.iss", "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(
            r'#define MyAppVersion "[^"]+"',
            f'#define MyAppVersion "{stripped_version}"',
            content,
        )
        with open("SRsetup.iss", "w", encoding="utf-8") as f:
            f.write(content)


if __name__ == "__main__":
    original_version, stripped_version = get_version_from_env()
    update_version_info(stripped_version)
    update_config_py(original_version)
    update_iss_version(stripped_version)
