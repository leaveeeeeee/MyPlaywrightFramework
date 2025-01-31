import subprocess
import pytest
import sys
from playwright.sync_api import sync_playwright
from helpers.helper_functions import *
from helpers import check_playwright_version
from helpers.check_playwright_version import main as check_playwright_version

# 添加当前目录到系统路径，以便导入 check_playwright_version
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 日志目录
LOG_DIR = os.path.join(PROJECT_ROOT, './report/logs')
os.makedirs(LOG_DIR, exist_ok=True)

# 截图目录
SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, './report/screenshots')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Allure 结果目录
ALLURE_RESULTS_DIR = os.path.join(PROJECT_ROOT, './report/allure-results')
os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)


def pytest_sessionstart(session):
    """
    版本检查函数
    """
    loginfo("开始测试前检查 Playwright 版本...")
    check_playwright_version()
    loginfo("Playwright 版本检查完成。")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        test_name = item.name
        if report.failed:
            logerror(f"测试 {test_name} 失败: {report.longreprtext}")
        else:
            loginfo(f"测试 {test_name} 成功")


@pytest.fixture(scope="function", autouse=True)
def setup_test_logging(request):
    test_name = request.node.name
    log_file_path = os.path.join(LOG_DIR, f"{test_name}.log")
    setup_logging(log_file_path)
    yield
    # 清除日志处理器，避免影响其他测试
    logging.getLogger().handlers.clear()


@pytest.fixture(scope="function")
def test_context(request):
    test_name = request.node.name
    screenshot_path = os.path.join(SCREENSHOT_DIR, test_name)
    os.makedirs(screenshot_path, exist_ok=True)
    return {
        "test_name": test_name,
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


def pytest_configure(config):
    """
    动态设置 -alluredir 参数
    """
    if not config.getoption("--alluredir"):
        config.option.alluredir = ALLURE_RESULTS_DIR


def pytest_sessionfinish(session, exitstatus):
    """
    测试会话结束后的操作
    """

    report_dir = os.path.join(PROJECT_ROOT, './report/allure-report')
    results_dir = os.path.join(PROJECT_ROOT, './report/allure-results')
    subprocess.run(['allure', 'generate', results_dir, '-o', report_dir, '--clean'])
