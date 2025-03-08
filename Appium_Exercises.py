from appium import webdriver
from appium.options.android import UiAutomator2Options
import subprocess
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

options = UiAutomator2Options()
options.platform_name = "Android" # 使用的作業系統
options.automation_name = "UiAutomator2"
options.platform_version = "14"  # Android 版本號
options.device_name = "Automation"  # 裝置名稱
options.app_package = "com.android.chrome"  # Chrome 瀏覽器的套件名稱
options.app_activity = "com.google.android.apps.chrome.Main"  # Chrome 瀏覽器的啟動 Activity
options.no_reset = True # 不重置應用程式狀態
options.full_reset = False # 不重置應用程式狀態

# 初始化，關閉 Chrome 瀏覽器
subprocess.run(["adb", "shell", "am", "force-stop", "com.android.chrome"])

# 啟動 Chrome 瀏覽器
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

# 等待 Chrome 瀏覽器啟動
print("等待 Chrome 瀏覽器啟動。")
driver.implicitly_wait(10)
search_box = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((AppiumBy.ID, "com.android.chrome:id/tab_switcher_button"))
)

print("關閉 Chrome 瀏覽器。")
# subprocess.run(["adb", "shell", "am", "force-stop", "com.android.chrome"])
