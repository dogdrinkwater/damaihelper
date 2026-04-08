# coding: utf-8
"""
Appium-based damai ticket buyer.
Requires:
  - Android Studio AVD running (emulator-5554) OR real device connected via USB
  - Appium server running: npx appium
  - Damai app installed on the device and already logged in
  - appium-uiautomator2-driver: appium driver install uiautomator2
"""
import json
import time
from json import loads
from time import sleep, time as now

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


APPIUM_SERVER = "http://127.0.0.1:4723"
DAMAI_PACKAGE = "com.damai"
DAMAI_ACTIVITY = "com.damai.presentation.ui.main.MainActivity"


def _find_by_text(driver, text, timeout=5):
    """Find element by visible text using UiAutomator2."""
    return WebDriverWait(driver, timeout, 0.2).until(
        EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().text("{text}")'
        ))
    )


def _find_by_text_contains(driver, text, timeout=5):
    return WebDriverWait(driver, timeout, 0.2).until(
        EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().textContains("{text}")'
        ))
    )


def _try_find(driver, by, value, timeout=3):
    try:
        return WebDriverWait(driver, timeout, 0.2).until(
            EC.presence_of_element_located((by, value))
        )
    except TimeoutException:
        return None


def build_driver(device_name="emulator-5554"):
    caps = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": device_name,
        "appium:appPackage": DAMAI_PACKAGE,
        "appium:appActivity": DAMAI_ACTIVITY,
        "appium:noReset": True,           # keep login session
        "appium:autoGrantPermissions": True,
        "appium:newCommandTimeout": 120,
    }
    driver = webdriver.Remote(APPIUM_SERVER, caps)
    driver.implicitly_wait(3)
    return driver


def open_item(driver, item_id):
    """Navigate to a ticket item detail page via deep link."""
    print(f"###打开活动页面: itemId={item_id}###")
    driver.get(f"damai://homepage/item_detail?id={item_id}")
    sleep(3)


def wait_for_buy_button(driver, timeout=30):
    """Wait for the 立即购买 / 立即预订 button to appear."""
    print("###等待购买按钮出现###")
    for btn_text in ["立即购买", "立即预订", "即将开抢", "缺货登记"]:
        el = _try_find(
            driver,
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().textContains("{btn_text}")',
            timeout=timeout
        )
        if el:
            return el, el.text
    raise Exception("***Error: 找不到购买按钮***")


def dismiss_popups(driver):
    """Dismiss any modal popups (ad, age verification, etc.)."""
    for dismiss_text in ["我知道了", "关闭", "同意", "确定", "跳过"]:
        el = _try_find(
            driver,
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().text("{dismiss_text}")',
            timeout=1
        )
        if el:
            try:
                el.click()
                sleep(0.5)
            except Exception:
                pass


def choose_date(driver, date_priority):
    """Select preferred date by priority index list."""
    try:
        date_items = driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().resourceIdMatches(".*calendar.*day.*")'
        )
        if not date_items:
            # fallback: find by class in a calendar container
            date_items = driver.find_elements(
                AppiumBy.XPATH,
                '//*[contains(@resource-id,"calendar")]//android.widget.TextView'
            )
        for idx in date_priority:
            if idx <= len(date_items):
                item = date_items[idx - 1]
                if "无票" not in (item.get_attribute("content-desc") or ""):
                    item.click()
                    sleep(0.3)
                    return True
    except Exception as e:
        print(f"日期选择跳过: {e}")
    return False


def choose_session(driver, session_priority):
    """Select preferred session by priority index list."""
    try:
        session_items = driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().resourceIdMatches(".*sku.*times.*item.*")'
        )
        if not session_items:
            session_items = driver.find_elements(
                AppiumBy.XPATH,
                '//*[contains(@resource-id,"session") or contains(@resource-id,"times")]'
                '//android.widget.TextView[@clickable="true"]'
            )
        for idx in session_priority:
            if idx <= len(session_items):
                item = session_items[idx - 1]
                desc = item.get_attribute("content-desc") or item.text or ""
                if "无票" not in desc and "缺货" not in desc:
                    item.click()
                    sleep(0.3)
                    return True
    except Exception as e:
        print(f"场次选择跳过: {e}")
    return False


def choose_price(driver, price_priority):
    """Select preferred price tier by priority index list."""
    try:
        price_items = driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().resourceIdMatches(".*sku.*ticket.*item.*")'
        )
        if not price_items:
            price_items = driver.find_elements(
                AppiumBy.XPATH,
                '//*[contains(@resource-id,"price") or contains(@resource-id,"ticket")]'
                '//android.widget.TextView[@clickable="true"]'
            )
        for idx in price_priority:
            if idx <= len(price_items):
                item = price_items[idx - 1]
                desc = item.get_attribute("content-desc") or item.text or ""
                if "缺货" not in desc and "无票" not in desc:
                    item.click()
                    sleep(0.3)
                    return True
    except Exception as e:
        print(f"票价选择跳过: {e}")
    return False


def set_ticket_count(driver, ticket_num):
    """Increase ticket count to desired amount."""
    for _ in range(ticket_num - 1):
        plus_btn = _try_find(
            driver,
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().resourceIdMatches(".*counter.*plus.*|.*plus.*enable.*")',
            timeout=2
        )
        if plus_btn:
            plus_btn.click()
            sleep(0.2)


def submit_order(driver):
    """Click the final confirm button in the SKU sheet."""
    for btn_text in ["立即购买", "立即预订", "确定"]:
        btn = _try_find(
            driver,
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().textContains("{btn_text}")',
            timeout=3
        )
        if btn:
            btn.click()
            print(f"###点击了: {btn_text}###")
            sleep(2)
            return True
    return False


def choose_viewer(driver, viewer_priority):
    """Select viewer/attendee persons on the order confirmation page."""
    try:
        viewer_items = driver.find_elements(
            AppiumBy.XPATH,
            '//*[contains(@resource-id,"viewer") or contains(@resource-id,"attendee")]'
            '//android.widget.TextView'
        )
        for idx in viewer_priority:
            if idx <= len(viewer_items):
                viewer_items[idx - 1].click()
                sleep(0.2)
    except Exception as e:
        print(f"观影人选择跳过: {e}")


def confirm_order(driver):
    """Press the final submit order button."""
    for btn_text in ["提交订单", "确认下单", "立即支付"]:
        btn = _try_find(
            driver,
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().text("{btn_text}")',
            timeout=5
        )
        if btn:
            btn.click()
            print(f"###提交订单: {btn_text}###")
            return True
    return False


def run(config):
    item_id = config["target_url"].split("itemId=")[-1]
    device_name = config.get("appium_device", "emulator-5554")
    date_priority = config.get("date", [1])
    session_priority = config.get("sess", [1])
    price_priority = config.get("price", [1])
    ticket_num = config.get("ticket_num", 1)
    viewer_priority = config.get("viewer_person", [1])

    print("###启动 Appium 驱动###")
    driver = build_driver(device_name)

    try:
        open_item(driver, item_id)
        dismiss_popups(driver)

        attempt = 0
        while True:
            attempt += 1
            print(f"###第 {attempt} 次尝试抢票###")
            try:
                buy_btn, btn_text = wait_for_buy_button(driver, timeout=10)

                if "即将开抢" in btn_text:
                    print("---尚未开售，刷新等待---")
                    driver.get(f"damai://homepage/item_detail?id={item_id}")
                    sleep(1)
                    continue

                if "缺货" in btn_text:
                    print("---已缺货，继续轮询---")
                    driver.get(f"damai://homepage/item_detail?id={item_id}")
                    sleep(config.get("retry_interval", 2))
                    continue

                buy_btn.click()
                sleep(1.5)
                dismiss_popups(driver)

                # SKU selection sheet
                choose_date(driver, date_priority)
                choose_session(driver, session_priority)
                choose_price(driver, price_priority)
                set_ticket_count(driver, ticket_num)
                submit_order(driver)

                # Order confirmation page
                sleep(2)
                choose_viewer(driver, viewer_priority)
                if confirm_order(driver):
                    print("###成功提交订单，请手动完成支付###")
                    break
                else:
                    raise Exception("找不到提交订单按钮")

            except Exception as e:
                print(f"本轮失败: {e}，重试中...")
                driver.get(f"damai://homepage/item_detail?id={item_id}")
                sleep(1)

    finally:
        input("按回车键关闭浏览器...")
        driver.quit()


if __name__ == "__main__":
    with open("./config/config.json", "r", encoding="utf-8") as f:
        config = loads(f.read())
    run(config)

