import pytest
import logging
from playwright.sync_api import sync_playwright

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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