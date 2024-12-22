import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

url = os.getenv("DEMO_URL", "http://xn--6frwj470ei1s2kl.com/demo")
driver = None
try:
    driver = webdriver.Chrome()
    driver.get(url)

    # 等待元素出现
    wait = WebDriverWait(driver, 10)
    # 获取 id 元素
    element = driver.find_element(By.ID, "c6")
    sleep(3)
    # 点击
    element.click()
    sleep(3)
finally:
    driver.quit()
