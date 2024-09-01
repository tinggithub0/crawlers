### 僅作 demo，部分資料以*代替 ###

from selenium import webdriver


def openChrome():
   # 打開chrome瀏覽器
    driver = webdriver.Chrome()
    return driver

def login(driver):
    url = "******"
    driver.get(url)
    # 找到輸入框並輸入内容
    elem_ID = driver.find_element_by_id("edit-name")
    elem_ID.send_keys("*****")
    elem_PASSWORD = driver.find_element_by_id("edit-pass")
    elem_PASSWORD.send_keys("*****")
    elem_enter = driver.find_element_by_id("edit-submit")
    elem_enter.click()

# 自動填表單問題
def send(driver):
    send_work_area = driver.find_element_by_id("*****") # 找到表單問題選項
    send_work_area.click() 
    ### 中間省略 ###
    send_submit = driver.find_element_by_name("**") # 填完送出
    send_submit.click()


if __name__ == '__main__':
    driver = openChrome()
    login(driver)
    send(driver)
