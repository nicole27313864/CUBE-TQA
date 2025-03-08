import os
import subprocess
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By

# 
# --------------------------- init global variables -------------------------- #
step_counter = 0   # 記錄步驟 (Step) 編號
check_counter = 0  # 記錄當前步驟內的檢查 (Check) 編號
# --------------------------------- function --------------------------------- #

def AddStep(stepDesc):
    """新增一個步驟，並重置子步驟計數"""
    if "[" in stepDesc:  # 如果步驟描述以 [ 開頭，則直接顯示
        print(stepDesc)
        return

    global step_counter, check_counter
    step_counter += 1
    check_counter = 0  # 每次新增步驟時，子步驟計數從 0 開始
    print(f"Step {step_counter}. {stepDesc}")

def AddCheckPass(desc):
    """新增一個通過的檢查，格式為 [Passed] Step X-Y desc"""
    global step_counter, check_counter
    check_counter += 1
    print(f"[Passed] 檢核 {step_counter}-{check_counter}. {desc}")

def AddCheckFail(desc, exception=None):
    """新增一個失敗的檢查，格式為 [Failed] Step X-Y desc (錯誤訊息)"""
    global step_counter, check_counter
    check_counter += 1
    error_msg = f"[Failed] 檢核 {step_counter}-{check_counter}. {desc}"
    # 如果有錯誤訊息，則加入到 error_msg 中
    if exception:
        error_msg += f" | 錯誤訊息: {str(exception)}"

    print(error_msg)

# 關閉 Chrome 瀏覽器內的所有分頁
def close_all_chrome_tabs(driver):
    try:
        # 點擊分頁切換按鈕
        tab_switcher = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (AppiumBy.ID, "com.android.chrome:id/tab_switcher_button")))
        tab_switcher.click()
        driver.implicitly_wait(0.5)  # 等待 0.5 秒

        # 循環點擊關閉按鈕
        while True:
            try:
                close_button = driver.find_element(AppiumBy.ID,"com.android.chrome:id/action_button")
                close_button.click()
            except: 
                break
    except Exception as e:
        AddCheckFail(f"關閉頁籤時發生錯誤：{e}")

def take_screenshot(driver, folder="screenshot"):
    """
    截圖並保存到當前工作目錄下指定的資料夾中，檔案名稱預設為 1.png、2.png、3.png ... 
    每次呼叫時會自動增加。
    :return: 截圖檔案的完整路徑
    """
    # 使用函數屬性來儲存計數器，如果不存在則初始化為 1
    if not hasattr(take_screenshot, "counter"):
        take_screenshot.counter = 1

    # 取得當前工作目錄
    current_dir = os.getcwd()
    # 拼接指定資料夾的路徑
    folder_path = os.path.join(current_dir, folder)
    # 如果資料夾不存在則建立
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # 使用計數器作為檔案名稱
    filename = f"{take_screenshot.counter}.png"
    screenshot_path = os.path.join(folder_path, filename)
    
    # 截圖並保存
    driver.save_screenshot(screenshot_path)
    print("截圖已保存到:", screenshot_path)
    
    # 計數器增加
    take_screenshot.counter += 1
    
    return screenshot_path



# --------------------------------- function --------------------------------- #
# 設定 Appium 連線選項
options = UiAutomator2Options()
options.platform_name = "Android"  # 使用的作業系統
options.automation_name = "UiAutomator2"
options.platform_version = "9"  # Android 版本號
options.device_name = "Nox"  # 裝置名稱
options.app_package = "com.android.chrome"  # Chrome 瀏覽器的套件名稱
options.app_activity = "com.google.android.apps.chrome.Main"  # Chrome 瀏覽器的啟動 Activity
options.no_reset = True  # 不重置應用程式狀態
options.full_reset = False  # 不重置應用程式狀態
# options.chromedriver_executable = "D:/APP/chrome-win64/chromedriver.exe"  # 指定 ChromeDriver 路徑
options.chromedriver_executable = "D:\\APP\\chrome-win64\\chromedriver.exe"  # 指定 ChromeDriver 路徑

# 初始化，關閉 Chrome 瀏覽器
# AddStep("[初始化]關閉 Chrome 瀏覽器")
result = subprocess.run(["adb", "shell", "am", "force-stop", "com.android.chrome"], check=False)

# 啟動 Chrome 瀏覽器
AddStep("[初始化]啟動 Chrome 瀏覽器")
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
# driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)


# 關閉 Chrome 瀏覽器內的所有分頁
# AddStep("[初始化]關閉 Chrome 瀏覽器內的所有分頁")
# close_all_chrome_tabs(driver)

# ---------------------------------------------------------------------------- #
# Step 1: 使用Chrome App到國泰世華銀行官網(https://www.cathaybk.com.tw/cathaybk/)並將畫面截圖。
# 預期結果: 開啟網頁(並截圖)
# ---------------------------------------------------------------------------- #
AddStep("開啟國泰世華銀行網站，並將畫面截圖")
# driver.get("https://www.cathaybk.com.tw/cathaybk/")
try:
    # 等待網站 logo 出現
    WebElement = WebDriverWait(driver, 20).until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "cathaybk")))

    AddCheckPass("成功進入首頁")
    take_screenshot(driver) # 截圖
except Exception as e:
    AddCheckFail(f"應成功進入首頁{e}")


# ---------------------------------------------------------------------------- #
# Step 2: 點選左上角選單，進入 個人金融 > 產品介紹 > 信用卡列表，需計算有幾個項目並將畫面截圖。
# 預期結果: 1. 進入信用卡列表選單後截圖
#          2. 計算有幾項目在信用卡選單下面
# ---------------------------------------------------------------------------- #
AddStep("點選左上角選單，進入 個人金融 > 產品介紹 > 信用卡列表，需計算有幾個項目並將畫面截圖")
try:
    # 點選左上角選單
    menu_burger = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.view.View\").instance(5)")
    menu_burger.click()
    time.sleep(1)

    # 點選【個人金融】
    WebElement  = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"產品介紹\")")
    WebElement.click()
    time.sleep(1)

    # 點選【信用卡】
    WebElement = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"信用卡\")")
    WebElement.click()
    time.sleep(1)

    # 計算【信用卡】選擔下項目數量 (class = "lnk_Link")
    item_count = len(driver.find_elements(by=AppiumBy.XPATH, value="//*[@resource-id='lnk_Link']"))
    if item_count:
        take_screenshot(driver)
        AddCheckPass(f"成功進入信用卡列表，共有 {item_count} 個項目")
    else:
        AddCheckFail("沒有找到信用卡列表項目")

except Exception as e:
    AddCheckFail(f"網站載入超時或發生錯誤：{e}")


# ---------------------------------------------------------------------------- #
# Step 3: 個人金融 > 產品介紹 > 信用卡 > 卡片介紹 > 計算頁面上所有(停發)信用卡數量並截圖。
# 預期結果: 1. 進入信用卡列表選單後計算(停發)信用卡數量並截圖
#          2. 比對計算(停發)信用卡數量與截圖數量相同
# ---------------------------------------------------------------------------- #
AddStep("進入信用卡【卡片介紹】計算頁面上所有(停發)信用卡數量並截圖")
try:
    # 點選【卡片介紹】
    WebElement = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"卡片介紹\")")
    WebElement.click()
    time.sleep(1)

    # 計算【(停發)信用卡】數量
    time.sleep(1)
except Exception as e:
    AddCheckFail(f"網站載入超時或發生錯誤：{e}")