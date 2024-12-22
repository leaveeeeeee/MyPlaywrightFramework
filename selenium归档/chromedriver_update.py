import os
import requests
import zipfile
import shutil
from selenium import webdriver
import subprocess
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


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
            print(f"Chrome版本为: {self.chrome_version}")
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
            print(f"Chrome版本为: {self.chrome_version}")
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

    @property
    def get_compatible_chromedriver_version(self):
        """
        获取与Chrome浏览器版本兼容的chromedriver版本。
        """
        url = "https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone.json"

        try:
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            raise ValueError(f"请求失败: {e}")
        except ValueError as e:
            print(f"解析JSON失败: {e}")
            raise ValueError(f"解析JSON失败: {e}")

        chrome_version_parts = self.chrome_version.split('.')
        chrome_major_minor_version = '.'.join(chrome_version_parts[:1])  # 提取主版本号部分，如 131.0.6778
        chrome_minor_version = int(chrome_version_parts[-1])  # 提取小版本号部分，如 140
        compatible_version = None

        print(f"Chrome 主版本号: {chrome_major_minor_version}, 小版本号: {chrome_minor_version}")

        for milestone_number, milestone_info in data.get('milestones', {}).items():
            print(f"检查里程碑: {milestone_number}, {milestone_info}")
            if milestone_number == chrome_major_minor_version:
                compatible_version = milestone_info.get('version')
                print(f"找到的兼容版本: {compatible_version}")
                break

        if compatible_version is None:
            print(f"未找到兼容的chromedriver版本")
            raise ValueError("未找到兼容的chromedriver版本")

        print(f"找到的兼容chromedriver版本: {compatible_version}")
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
        print(f"已成功下载ChromeDriver版本 {version} 到 {path}")

    def extract_chromedriver(self, zip_path, extract_to):
        """
        解压chromedriver压缩包。
        :param zip_path: 压缩包路径
        :param extract_to: 解压目录
        """
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"已成功解压ChromeDriver到 {extract_to}")

    @staticmethod
    def replace_chromedriver(new_driver_path, old_driver_path):
        """
        替换旧的chromedriver为新的chromedriver。
        :param new_driver_path: 新的chromedriver路径
        :param old_driver_path: 旧的chromedriver路径
        """
        if os.path.exists(new_driver_path):
            if os.path.exists(old_driver_path):
                os.remove(old_driver_path)
            shutil.move(new_driver_path, old_driver_path)
            print(f"已成功替换旧的ChromeDriver为新的ChromeDriver，路径为 {old_driver_path}")
        else:
            print(f"新的ChromeDriver文件 {new_driver_path} 不存在，无法替换。")

    def add_to_system_path(self, directory):
        """
        将指定目录添加到系统环境变量PATH中。
        :param directory: 要添加的目录
        """
        # 获取当前的 PATH 环境变量
        current_path = os.environ['PATH']

        # 如果目录不在当前路径中，则添加
        if directory not in current_path.split(';'):
            new_path = current_path + ';' + directory
            os.environ['PATH'] = new_path
            print(f"已将{directory}添加到系统PATH。")
        else:
            print(f"{directory}已在系统PATH中。")

    def test_chromedriver(self):
        """
        启动一次Selenium以确保chromedriver正常工作。
        """
        url = os.getenv("DEMO_URL", "http://xn--6frwj470ei1s2kl.com/demo")
        driver = None
        try:
            driver = webdriver.Chrome()
            driver.get(url)

            # 等待元素出现
            wait = WebDriverWait(driver, 10)
            # 获取 id 元素
            element = wait.until(ec.presence_of_element_located((By.ID, "c6")))
            # 点击后跳转到新页面
            element.click()
            # 获取 class 属性并点击
            try:
                # 使用 CSS 选择器来匹配多个类名
                button = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR,
                                                                    ".q-btn.q-btn-item.non-selectable.no-outline.q-btn--standard.q-btn--rectangle.bg-primary.text-white.q-btn--actionable.q-focusable.q-hoverable")))
                button.click()
                print("点击成功，selenium工作正常")
            except:
                print("未找到元素")
        finally:
            driver.quit()

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

        compatible_version = self.get_compatible_chromedriver_version
        print(f"找到兼容的chromedriver版本: {compatible_version}")

        self.download_chromedriver(driver_zip, compatible_version)
        self.extract_chromedriver(driver_zip, self.driver_dir)
        self.replace_chromedriver(new_driver_path, old_driver_path)
        self.add_to_system_path(self.driver_dir)

        # 测试chromedriver是否正常工作
        self.test_chromedriver()


chromedriver_updater = ChromeDriverUpdater()
if __name__ == "__main__":
    chromedriver_updater.main()
