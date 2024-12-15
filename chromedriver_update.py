import os
import requests
import zipfile
import shutil
from selenium import webdriver
import subprocess
import re
import json

class ChromeDriverUpdater:
    def __init__(self):
        """
        初始化ChromeDriverUpdater类，设置Chrome版本、下载目录和驱动目录。
        """
        self.chrome_version = None
        self.download_dir = "H:\\chromedriverdownload"
        self.driver_dir = "H:\\chromedrivers"

    def get_chrome_version_windows(self):
        """
        获取Windows系统上的Chrome浏览器版本。
        """
        try:
            # Windows系统命令
            result = subprocess.run(
                ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
                capture_output=True, text=True, check=True)
            self.chrome_version = re.search(r'(\d+\.\d+\.\d+\.\d+)', result.stdout).group(1)
        except Exception as e:
            print(f"获取Chrome版本时出错: {e}")
            self.chrome_version = None

    def get_chrome_version_linux(self):
        """
        获取Linux系统上的Chrome浏览器版本。
        """
        try:
            # macOS/Linux系统命令
            result = subprocess.run(['google-chrome-stable', '--version'], capture_output=True, text=True, check=True)
            self.chrome_version = re.search(r'(\d+\.\d+\.\d+\.\d+)', result.stdout).group(1)
        except Exception as e:
            print(f"获取Chrome版本时出错: {e}")
            self.chrome_version = None

    def get_chrome_version(self):
        """
        根据操作系统获取Chrome浏览器版本。
        """
        print("解析系统信息")
        if os.name == 'nt':
            return self.get_chrome_version_windows()
        elif os.name == 'posix':
            return self.get_chrome_version_linux()
        else:
            raise ValueError("未解析到系统信息")

    def get_compatible_chromedriver_version(self):
        """
        获取与Chrome浏览器版本兼容的chromedriver版本。
        """
        url = "https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone.json"
        response = requests.get(url)
        data = response.json()

        chrome_major_version = int(self.chrome_version.split('.')[0])
        compatible_version = None

        for version_info in data['milestones']:
            if version_info['chrome_version'].startswith(str(chrome_major_version)):
                version = version_info['downloads']['chromedriver'][0]['version']
                if self.compare_versions(version, self.chrome_version) <= 0:
                    compatible_version = version
                    break

        if compatible_version is None:
            raise ValueError("未找到兼容的chromedriver版本")

        return compatible_version

    @staticmethod
    def compare_versions(version1, version2):
        """
        比较两个版本号。
        :param version1: 第一个版本号
        :param version2: 第二个版本号
        :return: 如果version1 < version2 返回 -1，如果version1 > version2 返回 1，否则返回 0
        """
        v1_parts = list(map(int, version1.split('.')))
        v2_parts = list(map(int, version2.split('.')))

        for v1, v2 in zip(v1_parts, v2_parts):
            if v1 < v2:
                return -1
            elif v1 > v2:
                return 1

        # If all parts are equal, compare lengths
        if len(v1_parts) < len(v2_parts):
            return -1
        elif len(v1_parts) > len(v2_parts):
            return 1
        else:
            return 0

    def download_chromedriver(self, path, version):
        """
        下载与谷歌浏览器对应的driver文件。
        :param path: 下载路径
        :param version: chromedriver版本号
        """
        url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/win64/chromedriver-win64.zip"
        response = requests.get(url, stream=True)
        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    def extract_chromedriver(self, zip_path, extract_to):
        """
        解压chromedriver压缩包。
        :param zip_path: 压缩包路径
        :param extract_to: 解压目录
        """
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

    @staticmethod
    def replace_chromedriver(new_driver_path, old_driver_path):
        """
        替换旧的chromedriver为新的chromedriver。
        :param new_driver_path: 新的chromedriver路径
        :param old_driver_path: 旧的chromedriver路径
        """
        if os.path.exists(old_driver_path):
            os.remove(old_driver_path)
        shutil.move(new_driver_path, old_driver_path)

    def add_to_system_path(self, directory):
        """
        将指定目录添加到系统环境变量PATH中。
        :param directory: 要添加的目录
        """
        import winreg

        try:
            # 打开系统环境变量
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 0, winreg.KEY_READ)
            current_path, _ = winreg.QueryValueEx(key, 'Path')
            winreg.CloseKey(key)

            # 如果目录不在当前路径中，则添加
            if directory not in current_path.split(';'):
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                     r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 0,
                                     winreg.KEY_WRITE)
                winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, current_path + ';' + directory)
                winreg.CloseKey(key)
                print(f"已将{directory}添加到系统PATH。")
            else:
                print(f"{directory}已在系统PATH中。")
        except Exception as e:
            print(f"添加{directory}到系统PATH时出错: {e}")

    def main(self):
        """
        主函数，执行chromedriver更新流程。
        """
        # 创建下载目录
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            print(f"已创建下载目录: {self.download_dir}")

        # 创建驱动目录
        if not os.path.exists(self.driver_dir):
            os.makedirs(self.driver_dir)
            print(f"已创建驱动目录: {self.driver_dir}")

        driver_zip = os.path.join(self.download_dir, "chromedriver.zip")
        new_driver_path = os.path.join(self.driver_dir, "chromedriver.exe")
        old_driver_path = os.path.join(self.driver_dir, "chromedriver.exe")

        self.get_chrome_version()
        if not self.chrome_version:
            print("未获取到Chrome版本信息")
            return

        compatible_version = self.get_compatible_chromedriver_version()
        print(f"找到兼容的chromedriver版本: {compatible_version}")

        self.download_chromedriver(driver_zip, compatible_version)
        print(f"已下载ChromeDriver到 {driver_zip}")

        self.extract_chromedriver(driver_zip, self.driver_dir)
        print(f"已解压ChromeDriver到 {self.driver_dir}")

        self.replace_chromedriver(new_driver_path, old_driver_path)
        print(f"已将旧的ChromeDriver替换为新的ChromeDriver，路径为 {old_driver_path}")

        # 添加驱动目录到系统环境变量
        self.add_to_system_path(self.driver_dir)


chromedriver_updater = ChromeDriverUpdater()
if __name__ == "__main__":
    chromedriver_updater.main()
