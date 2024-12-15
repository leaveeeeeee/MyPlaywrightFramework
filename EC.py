import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = os.getenv("DEMO_URL", "http://xn--6frwj470ei1s2kl.com/demo")
driver = None
try:
    driver = webdriver.Chrome()
    driver.get(url)

    # 等待元素出现
    wait = WebDriverWait(driver, 10)
    # 获取 id 元素
    element = wait.until(EC.presence_of_element_located((By.ID, "c6")))
    # 点击后跳转到新页面
    element.click()
    # 获取 class 属性并点击
    try:
        # 使用 CSS 选择器来匹配多个类名
        button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                            ".q-btn.q-btn-item.non-selectable.no-outline.q-btn--standard.q-btn--rectangle.bg-primary.text-white.q-btn--actionable.q-focusable.q-hoverable")))
        button.click()
    except:
        print("未找到元素")
finally:
    driver.quit()
