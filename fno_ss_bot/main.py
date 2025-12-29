# groww_fno_bot.py
import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests

# ===== CONFIG =====
GROWW_POSITIONS_URL = "https://groww.in/futures-and-options/user/investments"
COOKIES_FILE = "groww_cookies.json"     # upload your cookie file here
TELEGRAM_BOT_TOKEN = "8420250453:AAFc1XYole5WhFYJOhiGMYNPHdnyhGOVNqw"
TELEGRAM_CHAT_ID = "-1003467106761"
SCREENSHOT_DIR = "screenshots"
WAIT_TIMEOUT = 15
INTERVAL_SECONDS = 60*4   # 15 minutes
# ==================

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def send_telegram_photo(photo_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    with open(photo_path, "rb") as f:
        files = {"photo": f}
        data = {"chat_id": TELEGRAM_CHAT_ID, "caption": f"Groww Positions: {os.path.basename(photo_path)}"}
        r = requests.post(url, data=data, files=files)
    return r.status_code, r.text

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")   # headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1400,2000")  # tall size for full page
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def load_cookies_and_storage(driver, cookies_path, local_path=None, session_path=None):
    import json
    # load cookies
    with open(cookies_path, "r") as f:
        cookies = json.load(f)

    # go to base domain so cookies/localStorage can be set
    driver.get("https://groww.in/")
    time.sleep(1)

    # add cookies (robust: try minimal cookie if full dict fails)
    for c in cookies:
        cookie = {}
        cookie['name'] = c.get('name')
        cookie['value'] = c.get('value')
        # optional fields
        if 'domain' in c: cookie['domain'] = c['domain']
        if 'path' in c: cookie['path'] = c['path']
        if 'expiry' in c: cookie['expiry'] = int(c['expiry'])
        try:
            driver.add_cookie(cookie)
        except Exception:
            # fallback: minimal cookie
            try:
                driver.add_cookie({'name': c['name'], 'value': c['value']})
            except Exception:
                pass

    # restore localStorage if available
    if local_path and os.path.exists(local_path):
        with open(local_path, "r") as f:
            local = json.load(f)
        # set each key in localStorage via JS
        for k, v in local.items():
            # use JSON stringify to preserve quotes safely
            driver.execute_script(f"window.localStorage.setItem(arguments[0], arguments[1]);", k, v)

    # restore sessionStorage if available
    if session_path and os.path.exists(session_path):
        with open(session_path, "r") as f:
            session = json.load(f)
        for k, v in session.items():
            driver.execute_script(f"window.sessionStorage.setItem(arguments[0], arguments[1]);", k, v)

    # Refresh to make the restored storage & cookies effective
    driver.refresh()
    time.sleep(2)


def take_positions_screenshot(driver):
    driver.get(GROWW_POSITIONS_URL)

    # wait until the page body loads
    try:
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except Exception:
        pass

    # Give initial JS some time to start rendering
    time.sleep(2)
    driver.execute_script("document.body.style.zoom='130%'")
    # Attempt to find & click the "Okay, I understand" (risk disclosure) button.
    # Try multiple XPaths to be robust against small text changes.
    modal_xpaths = [
        "//button[normalize-space(.)='Okay, I understand']",
        "//button[contains(normalize-space(.), 'I understand')]",
        "//button[contains(normalize-space(.), 'Okay')]",
        "//button[contains(., 'understand') or contains(., 'I understand') or contains(., 'Okay')]"
    ]

    clicked = False
    for xp in modal_xpaths:
        try:
            btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xp)))
            btn.click()
            clicked = True
            # small wait after clicking so the positions table can load
            time.sleep(2)
            break
        except Exception:
            # try next xpath
            continue

    if not clicked:
        # No modal found — still wait a bit longer in case the positions table is slow
        time.sleep(2)

    # Additional wait to ensure positions data loaded (increase if your network is slow)
    time.sleep(3)

    filename = f"{SCREENSHOT_DIR}/groww_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    # save full page screenshot
    driver.save_screenshot(filename)
    return filename

from PIL import Image

def upscale_image(img_path):
    img = Image.open(img_path)
    w, h = img.size
    img = img.resize((int(w*2), int(h*2)), Image.LANCZOS)
    img.save(img_path)


def main_loop():
    if not os.path.exists(COOKIES_FILE):
        raise SystemExit(f"{COOKIES_FILE} not found. Upload the cookie file exported locally.")
    while True:
        driver = create_driver()
        load_cookies_and_storage(driver, "groww_cookies.json", "groww_localstorage.json", "groww_sessionstorage.json")
        try:
            screenshot_path = take_positions_screenshot(driver)
            upscale_image(screenshot_path)
            code, text = send_telegram_photo(screenshot_path)
            print(f"{datetime.now()} -> Sent screenshot: {screenshot_path}, telegram_status={code}")
        except Exception as e:
            print("Error during screenshot/send:", e)
        finally:
            driver.quit()
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    main_loop()
