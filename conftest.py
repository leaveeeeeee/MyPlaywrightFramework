import pytest
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
from helpers import helper_functions

# 日志目录
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# 截图目录
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        if report.failed:
            log_file_path = os.path.join(LOG_DIR, f"{item.name}_error.log")
            helper_functions.setup_logging(log_file_path)
            helper_functions.logerror(f"测试 {item.name} 失败: {report.longreprtext}")
        else:
            log_file_path = os.path.join(LOG_DIR, f"{item.name}.log")
            helper_functions.setup_logging(log_file_path)
            helper_functions.loginfo(f"测试 {item.name} 成功")


@pytest.fixture(scope="function")
def test_context(request):
    test_name = request.node.name
    log_file_path = os.path.join(LOG_DIR, f"{test_name}.log")
    helper_functions.setup_logging(log_file_path)
    screenshot_path = os.path.join(SCREENSHOT_DIR, test_name)
    os.makedirs(screenshot_path, exist_ok=True)
    return {
        "test_name": test_name,
        "log_file_path": log_file_path,
        "screenshot_path": screenshot_path
    }


@pytest.fixture(scope="module")
def playwright_instance():
    # 启动 Playwright 实例
    playwright = sync_playwright().start()
    yield playwright
    # 停止 Playwright 实例
    playwright.stop()


@pytest.fixture
def browser(playwright_instance):
    # 启动 Chromium 浏览器
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    # 关闭浏览器
    browser.close()


@pytest.fixture
def webkit_browser(playwright_instance):
    # 启动 WebKit 浏览器
    browser = playwright_instance.webkit.launch(headless=False)
    yield browser
    # 关闭浏览器
    browser.close()
