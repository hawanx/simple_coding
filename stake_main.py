import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

# --- Telegram Configuration ---
TOKEN = "8286212832:AAFs3G2lLoxidU_CP6HtGpRKU9d_Vfa0-yg"
CHAT_ID = "-1003905826881"


def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    # Is baar hum 'HTML' parse_mode use kar rahe hain formatting ke liye
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")


def scrape_stake_rates():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    url = "https://stake.ac/sports/cricket/india/indian-premier-league"

    try:
        driver.get(url)
        print("Scraping started... Formatting set to Premium Style.")
        time.sleep(10)

        while True:
            try:
                wait = WebDriverWait(driver, 15)
                # Latest match container
                match = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="fixture-preview"]')))

                # Team buttons
                buttons = match.find_elements(By.CSS_SELECTOR, 'button[data-testid="fixture-outcome"]')

                if len(buttons) >= 2:
                    # Data Extraction
                    t1_name = buttons[0].find_element(By.CSS_SELECTOR,
                                                      'span[data-testid="outcome-button-name"]').text.strip()
                    t1_rate = buttons[0].find_element(By.CSS_SELECTOR, 'span[strong="true"]').text.strip()

                    t2_name = buttons[1].find_element(By.CSS_SELECTOR,
                                                      'span[data-testid="outcome-button-name"]').text.strip()
                    t2_rate = buttons[1].find_element(By.CSS_SELECTOR, 'span[strong="true"]').text.strip()

                    # Premium Formatting (Exactly as per image_82ef0d.png)
                    alert_text = (
                        f"🏏 <b>IPL LIVE ODDS</b>\n"
                        f"━━━━━━━━━━━━━━━\n\n"
                        f"🏆 <b>{t1_name.upper()}</b>\n"
                        f"└─ 💸 <b>ODDS: {t1_rate}</b>\n\n"
                        f"🏆 <b>{t2_name.upper()}</b>\n"
                        f"└─ 💸 <b>ODDS: {t2_rate}</b>\n\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"🕒 <i>Updated at: {time.strftime('%H:%M')}</i>"
                    )

                    print(f"Update Sent: {t1_name} vs {t2_name}")
                    send_telegram_msg(alert_text)
                else:
                    print("Match outcomes not found.")

            except Exception as e:
                print(f"Error: {e}")

            # Har 10 second mein check
            time.sleep(10)

    except KeyboardInterrupt:
        print("Script stopped.")
    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_stake_rates()