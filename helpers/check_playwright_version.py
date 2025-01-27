import subprocess
from helpers.helper_functions import *
from packaging import version


def get_latest_version():
    """
    获取 playwright 最新版本号
    """
    try:
        result = subprocess.run(['pip', 'index', 'versions', 'playwright'], capture_output=True, text=True, check=True)
        versions = result.stdout.split('\n')
        for line in versions:
            if line.strip().startswith('playwright'):
                latest_version = line.split()[1].strip('()')
                loginfo(f"获取到的 Playwright 最新版本号为{latest_version}")  # 最新版本在第一行
                return latest_version
        loginfo("无法找到 Playwright 的最新版本号")
        return None
    except subprocess.CalledProcessError as e:
        loginfo(f'获取 Playwright 最新版本失败: {e}')
        return None


# 目标版本，默认为最新
target_version = get_latest_version()  # 请根据需要修改为目标版本


def get_current_version():
    """
    获取当前安装的playwright 版本
    """
    try:
        result = subprocess.run(['pip', 'show', 'playwright'], capture_output=True, text=True, check=True)
        for line in result.stdout.split('\n'):
            if line.startswith('Version:'):
                loginfo(f"获取到的本地 Playwright 版本号为{line.split(': ')[1]}")
                return line.split(': ')[1]
    except subprocess.CalledProcessError as e:
        loginfo(f'获取当前 Playwright 版本失败: {e}')
    return None


def compare_versions(current, target):
    """
    比较版本号
    """
    current_version = version.parse(current)
    target_version = version.parse(target)
    if current_version < target_version:
        return -1  # 当前版本低于目标版本
    elif current_version > target_version:
        return 1  # 当前版本高于目标版本
    else:
        return 0  # 版本相同


def update_or_revert_playwright(current_version):
    """
    更新或回退 Playwright 版本
    """
    comparison = compare_versions(current_version, target_version)
    if comparison == -1:
        loginfo(f'当前版本 {current_version} 低于目标版本 {target_version}。正在更新...')
        subprocess.run(['pip', 'install', f'playwright=={target_version}'], check=True)
        loginfo(f'Playwright 已更新到版本 {target_version}。')
    elif comparison == 1:
        loginfo(f'当前版本 {current_version} 高于目标版本 {target_version}。正在回退...')
        subprocess.run(['pip', 'install', f'playwright=={target_version}'], check=True)
        loginfo(f'Playwright 已回退到版本 {target_version}。')
    else:
        loginfo(f'当前版本 {current_version} 已经是目标版本 {target_version}。无需操作。')


def main():
    current_version = get_current_version()
    if current_version:
        update_or_revert_playwright(current_version)
    else:
        loginfo('无法确定当前 Playwright 版本。')


if __name__ == '__main__':
    main()
