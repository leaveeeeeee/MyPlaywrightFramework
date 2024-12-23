import pytest
import logging
import conftest



class TestUI:
    def test_baidu(self, browser):
        try:
            # 创建新的浏览器上下文
            context = browser.new_context()
            # 创建新页面
            page = context.new_page()
            # 访问百度首页
            page.goto("http://www.baidu.com")
            logging.info("成功访问 http://www.baidu.com.")
        except Exception as e:
            logging.error(f"访问百度时出错: {e}")
        finally:
            # 关闭浏览器上下文
            context.close()

    def test_taobao(self, webkit_browser):
        try:
            # 创建新的浏览器上下文，并设置视口大小
            context = webkit_browser.new_context(viewport={"width": 1280, "height": 720})
            # 创建新页面
            page = context.new_page()
            # 访问淘宝首页
            page.goto("http://www.taobao.com")
            # 截图并保存到指定路径
            screenshot_path = "./taobao.png"
            page.screenshot(path=screenshot_path)
            logging.info(f"截图已保存至 {screenshot_path}")
        except Exception as e:
            logging.error(f"访问淘宝时出错: {e}")
        finally:
            # 关闭浏览器上下文
            context.close()


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
