# export_groww_storage.py
import time, json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--window-size=1400,900")  # visible
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://groww.in/futures-and-options/user/investments")

input("Log in manually in the opened browser, then press ENTER here when you see your positions...")

time.sleep(5)

# cookies
cookies = driver.get_cookies()

# localStorage
local_storage = driver.execute_script(
    "var ls = {}; for (var i=0;i<localStorage.length;i++){var k=localStorage.key(i); ls[k]=localStorage.getItem(k);} return ls;"
)

# sessionStorage (if used)
session_storage = driver.execute_script(
    "var ss = {}; for (var i=0;i<sessionStorage.length;i++){var k=sessionStorage.key(i); ss[k]=sessionStorage.getItem(k);} return ss;"
)

with open("groww_cookies.json", "w") as f:
    json.dump(cookies, f)

with open("groww_localstorage.json", "w") as f:
    json.dump(local_storage, f)

with open("groww_sessionstorage.json", "w") as f:
    json.dump(session_storage, f)

print("Saved groww_cookies.json, groww_localstorage.json, groww_sessionstorage.json")
driver.quit()
