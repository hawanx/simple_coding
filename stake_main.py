import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

# --- Telegram Configuration ---
TOKEN = "8286212832:AAFs3G2lLoxidU_CP6HtGpRKU9d_Vfa0-yg"
CHAT_ID = "-1003905826881"

# Memory to store the last sent rates
last_sent_data = {"t1_rate": None, "t2_rate": None, "match": None}


def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")


def scrape_stake_rates():
    global last_sent_data
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=148, use_subprocess=True)
    url = "https://stake.ac/sports/cricket/india/indian-premier-league"

    try:
        driver.get(url)
        print("Bot is running... Monitoring for price changes.")
        time.sleep(10)
        # WebDriverWait ko loop ke bahar ek hi baar define karein
        wait = WebDriverWait(driver, 15)

        while True:
            try:
                match_container = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="fixture-preview"]')))
                buttons = match_container.find_elements(By.CSS_SELECTOR, 'button[data-testid="fixture-outcome"]')

                if len(buttons) >= 2:
                    t1_name = buttons[0].find_element(By.CSS_SELECTOR,
                                                      'span[data-testid="outcome-button-name"]').text.strip()
                    t1_rate = buttons[0].find_element(By.CSS_SELECTOR, 'span[strong="true"]').text.strip()

                    t2_name = buttons[1].find_element(By.CSS_SELECTOR,
                                                      'span[data-testid="outcome-button-name"]').text.strip()
                    t2_rate = buttons[1].find_element(By.CSS_SELECTOR, 'span[strong="true"]').text.strip()

                    current_match = f"{t1_name} vs {t2_name}"

                    # --- Check for Change ---
                    # Agar match badal gaya ho (naya match) ya kisi bhi ek team ka rate badal gaya ho
                    if (current_match != last_sent_data["match"] or
                            t1_rate != last_sent_data["t1_rate"] or
                            t2_rate != last_sent_data["t2_rate"]):

                        # Update the Memory
                        last_sent_data = {
                            "match": current_match,
                            "t1_rate": t1_rate,
                            "t2_rate": t2_rate
                        }

                        # Premium Format Message
                        alert_text = (
                            f"🏏 <b>IPL LIVE ODDS</b>\n"
                            f"━━━━━━━━━━━━━━━\n\n"
                            f"🏆 <b>{t1_name.upper()}</b>\n"
                            f"└─ 💸 <b>ODDS: {t1_rate}</b>\n\n"
                            f"🏆 <b>{t2_name.upper()}</b>\n"
                            f"└─ 💸 <b>ODDS: {t2_rate}</b>\n\n"
                            f"━━━━━━━━━━━━━━━\n"
                            f"🕒 <i>Updated at: {time.strftime('%H:%M:%S')}</i>"
                        )

                        send_telegram_msg(alert_text)
                        print(f"Update Sent: {current_match} -> {t1_rate} | {t2_rate}")
                    else:
                        # Agar rate same hai toh sirf console pe print karega, Telegram nahi jayega
                        print(f"Monitoring... No change in rates ({t1_rate} / {t2_rate})", end="\r")

                else:
                    print("Match outcomes not found.")

            except Exception as e:
                print(f"\nError: {e}")

            # Rate check frequency (Stake ke liye 5-10 sec ideal hai)
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nBot Stopped.")
    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_stake_rates()