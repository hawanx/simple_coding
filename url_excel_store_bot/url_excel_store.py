import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import instaloader
from urllib.parse import urlparse
import requests

# 1. Setup Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Insta Promotions Urls").sheet1  # Make sure sheet name matches exactly

# 2. Setup Telegram Bot
TOKEN = "8514662555:AAEZt43BbIiH46TFQ1wYdfc_ohuacBCIhVo"
bot = telebot.TeleBot(TOKEN)

print("Bot is running...")


L = instaloader.Instaloader()

def find_item_index(data_list, target):
    if target in data_list:
        return data_list.index(target)
    return -1  # Or None, if you prefer

def get_page_name_and_post_type(raw_url):
    try:
        split_list = raw_url.split('/')

        index = find_item_index(split_list, 'stories')
        if index == -1:
            index = find_item_index(split_list, 'reel')
            promotion_type = "Reel" if index != -1 else "Post"
            if index == -1:
                index = find_item_index(split_list, 'p')
            post = instaloader.Post.from_shortcode(L.context, split_list[index+1])
            username = post.owner_username
            post_date = post.date_local.strftime("%#d %b")
        else:
            username = split_list[index+1]
            promotion_type = "Story"
            post_date = datetime.now().strftime("%#d %b")

        return username, promotion_type, post_date
    except Exception as e:
        print(f"Error: {e}")
        return "Unknown Page", raw_url


def get_followers(username):
    # This internal URL sometimes provides JSON data
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
        "x-ig-app-id": "936619743392459"  # This ID changes periodically
    }

    response = requests.get(url, headers=headers)
    try:
        if response.status_code == 200:
            data = response.json()
            return data['data']['user']['edge_followed_by']['count']
    except Exception as ex:
        print(f"BLOCKED OR PRIVATE :: {ex}")
    return ""

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    print(f"Received a message: {message.text}")  # Debug
    url = message.text

    if "instagram.com" in url:
        page_name, promotion_type, post_date = get_page_name_and_post_type(url)
        follower_count = get_followers(page_name)

        try:
            # Append row to Google Sheet
            sheet.append_row([post_date, page_name, "", promotion_type, url, follower_count])
            bot.reply_to(message, f"✅ Added to Excel!\nPage Name: {page_name}\nDate: {post_date}")
        except Exception as e:
            bot.reply_to(message, f"❌ Error: {str(e)}")
    else:
        bot.reply_to(message, "Please send a valid Instagram URL.")

bot.infinity_polling()
