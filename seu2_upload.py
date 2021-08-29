###  不公開資料以*代替  ###

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def webdriver_wait_send_keys(driver, locator, value):
    WebDriverWait(driver, 10, 5).until(EC.presence_of_element_located(locator)).send_keys(value)

def webdriver_click(driver, locator):
    WebDriverWait(driver, 10, 5).until(EC.presence_of_element_located(locator)).click()

def openChrome():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    return driver

def send(driver):
    url = "*****"
    driver.get(url)
    try:
        ###  ###
        work_id_locator = (By.XPATH, '*****')
        webdriver_wait_send_keys(driver, work_id_locator, "*****")
        id_locator = (By.XPATH, '*****')
        webdriver_wait_send_keys(driver, id_locator, "*****")

        locator_1 = (By.XPATH, "*****")
        webdriver_click(driver, locator_1)
        locator_2 = (By.XPATH, "*****")
        webdriver_click(driver, locator_2)
        locator_4 = (By.XPATH, "*****")
        webdriver_click(driver, locator_4)
        locator_5 = (By.XPATH, "*****")
        webdriver_click(driver, locator_5)
        locator_6 = (By.XPATH, "*****")
        webdriver_click(driver, locator_6)
        locator_8 = (By.XPATH, "*****")
        webdriver_click(driver, locator_8)

        send_locator = (By.XPATH, "//button")
        webdriver_click(driver, send_locator)
        driver.quit()
    except:
        driver.quit()
        return False


if __name__ == '__main__':
    driver = openChrome()
    result = send(driver)
    if result is False:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("prefs", {"profile.password_manager_enabled": False, "credentials_enable_service": False})
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

        url = "*****"
        driver.get(url)

