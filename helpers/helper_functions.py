import time
import logging
import allure
import os
from datetime import datetime


# 日志记录
def setup_logging(log_file_path):
    log_dir = os.path.dirname(log_file_path)
    os.makedirs(log_dir, exist_ok=True)
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file_path),
                logging.StreamHandler()
            ]
        )
    else:
        # 如果已经有处理器，确保添加新的处理器
        logger = logging.getLogger()
        file_handler = logging.FileHandler(log_file_path)
        stream_handler = logging.StreamHandler()
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)


def wait(seconds, reason=""):
    print(f"等待{seconds}秒，{reason}/n")
    return time.sleep(seconds)


def loginfo(message=""):
    logging.info(message)


def logdebug(message=""):
    logging.debug(message)


def logerror(message=""):
    logging.error(message)


def take_screenshot(page, screenshot_path, step_name):
    screenshot_name = os.path.join(screenshot_path, f"{step_name}.png")
    page.screenshot(path=screenshot_name)
    loginfo(f"截图已保存至 {screenshot_name}")
    allure.attach.file(screenshot_name, name=f"Screenshot of {step_name}",
                       attachment_type=allure.attachment_type.PNG)


class Step:
    def __init__(self, step_name, page=None, screenshot_path=None):
        self.step_name = step_name
        self.page = page
        self.screenshot_path = screenshot_path
        self.start_time = None
        self.allure_step = None

    def __enter__(self):
        self.start_time = datetime.now()
        loginfo(f"开始步骤 {self.step_name}")
        self.allure_step = allure.step(self.step_name).__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        if exc_type is not None:
            logerror(f"步骤 {self.step_name} 出错: {exc_value}")
            allure.attach(f"步骤 {self.step_name} 出错: {exc_value}", name=f"Error in {self.step_name}",
                          attachment_type=allure.attachment_type.TEXT)
        else:
            loginfo(f"步骤 {self.step_name} 成功，耗时: {duration:.2f} 秒")
            allure.attach(f"步骤 {self.step_name} 成功，耗时: {duration:.2f} 秒", name=f"Success in {self.step_name}",
                          attachment_type=allure.attachment_type.TEXT)

        if self.page and self.screenshot_path:
            screenshot_name = f"{self.screenshot_path}_{self.step_name}.png"
            self.page.screenshot(path=screenshot_name)
            loginfo(f"截图已保存至 {screenshot_name}")
            allure.attach.file(screenshot_name, name=f"Screenshot of {self.step_name}",
                               attachment_type=allure.attachment_type.PNG)

        if self.allure_step:
            self.allure_step.__exit__(exc_type, exc_value, traceback)
