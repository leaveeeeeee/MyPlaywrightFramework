import pytest
import logging
import allure
from playwright.sync_api import sync_playwright

# 配置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)




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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get('page')
        if page:
            screenshot_path = f"./screenshots/{item.name}_failed.png"
            page.screenshot(path=screenshot_path)
            allure.attach.file(screenshot_path, name=f"{item.name}_failed", attachment_type=allure.attachment_type.PNG)
            # 添加日志记录失败详情
            logger.error(f"Test {item.name} failed with exception: {rep.longrepr}")
