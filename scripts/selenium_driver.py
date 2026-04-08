from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def start_selenium_driver(target_url):
    # 使用Selenium启动浏览器并打开购票页面
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(target_url)

    # 示例：定位元素并点击
    login_button = driver.find_element(By.ID, 'login_button')
    login_button.click()
    
    return driver
