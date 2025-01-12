from conftest import test_context
from helpers.helper_functions import *
import pytest
import allure


class TestUI:
    @allure.title("打开百度搜索")
    def test_baidu(self, browser, test_context):
        try:
            with Step("创建浏览器上下文"):
                context = browser.new_context(viewport={"width": 1920, "height": 1080})
            with Step("创建新页面"):
                page = context.new_page()
            with Step("访问百度首页"):
                page.goto("http://www.baidu.com")
                loginfo("成功访问 http://www.baidu.com.")
                take_screenshot(page, test_context["screenshot_path"], " baidu_homepage")

        except Exception as e:
            logging.error(f"访问百度时出错: {e}")
        finally:
            with Step("关闭浏览器上下文"):
                context.close()

    @allure.title("打开淘宝")
    def test_taobao(self, browser, test_context):
        try:
            with Step("创建浏览器上下文"):
                context = browser.new_context(viewport={"width": 1280, "height": 720})
            with Step("创建新页面"):
                page = context.new_page()
            with Step("访问淘宝首页"):
                page.goto("https://www.taobao.com")
                loginfo("成功访问 https://www.taobao.com.")
                take_screenshot(page, test_context["screenshot_path"], "taobao_homepage")

        except Exception as e:
            logging.error(f"访问淘宝时出错: {e}")
        finally:
            with Step("关闭浏览器上下文"):
                context.close()


aw_test = TestUI
if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
