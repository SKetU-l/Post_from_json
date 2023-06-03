import requests
import os
from datetime import datetime
from dotenv.main import load_dotenv
load_dotenv()
from telegram import Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello am active")

def supported(update: Update, context: CallbackContext):
    rising = "/latest awaken"
    awaken = "/latest rising"
    message = f"Currently only <b>RisingOS</b> and <b>AwakenOS</b> available\n<b>run any of these you want:</b>\n <code>{rising}</code>\n <code>{awaken}</code>"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")

def latest(update: Update, context: CallbackContext):
    msg = update.message.text
    user_id = update.message.chat_id
    msg = msg.split(" ", 1)
    if len(msg) == 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Use Proper Format. Example: /supported", parse_mode='HTML')
    elif len(msg) == 2:
        parameter = msg[1]
        if parameter == "rising":
            try:
                data, source_changelog, device_changelog = function1(parameter)
                message = function2(data, source_changelog, device_changelog)

                context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='HTML', disable_web_page_preview=True)

            except Exception as e:
                print(f"An error occurred: {str(e)}")
                context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred while processing the command.")
        elif parameter == "awaken":
            try:
                device, source_changelog, download = function3(parameter)
                message = function4(device, source_changelog, download)

                context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='HTML', disable_web_page_preview=True)

            except Exception as e:
                print(f"An error occurred: {str(e)}")
                context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred while processing the command.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid parameter.")

def function1(rising):
    device_changelog = f"https://github.com/RisingOSS-devices/android_vendor_RisingOTA/raw/thirteen/changelog_X00TD.txt"
    source_changelog ="https://raw.githubusercontent.com/RisingTechOSS/android_vendor_rising/thirteen/build/tools/Changelog.txt"
    device_json = f"https://raw.githubusercontent.com/RisingOSS-devices/android_vendor_RisingOTA/thirteen/X00TD.json"
    response = requests.get(device_json)
    data = response.json()
    return data, source_changelog , device_changelog


def function2(data, source_changelog, device_changelog):
    device = data['response'][0]['device']
    version = data['response'][0]['version']
    support_group = data['response'][0]['forum']

    message = f"rising v{version} | Official | Android 13\n" \
              f"<b>Supported Device:</b> {device}\n" \
              f"<b>Maintainer:</b> @SKetUl\n\n" \
              f"<b>Download:</b> <a href=\"https://www.pling.com/p/1935891\">Here</a>\n" \
              f"<b>Screenshots:</b> <a href=\"https://t.me/riceDroidNews/719\">Here</a>\n" \
              f"<b>Changelogs:</b> <a href=\"{source_changelog}\">Source</a> | <a href=\"{device_changelog}\">Device</a>\n" \
              f"<b>Support group:</b> <a href=\"https://t.me/RisingOSG\">Source</a> | <a href=\"{support_group}\">Device</a>\n\n" \
              f"<b>Notes:</b>\n- Non-FBE, LV, enforcing & 4.4 kernel based build\n- Safetynet pass by default\n\n" \

    return message

def function3(awaken):
    device ="X00TD"
    source_changelog ="https://t.me/AwakenOSNews"
    download ="https://www.pling.com/p/1888078/"
    return device, source_changelog, download

def function4(device, source_changelog, download):
    message = f"AwakenOS | Unofficial | Android 13\n" \
              f"<b>Supported Device:</b> {device}\n" \
              f"<b>Maintainer:</b> @SKetUl\n\n" \
              f"<b>Download:</b> <a href=\"{download}\">Here</a>\n" \
              f"<b>Changelogs:</b> <a href=\"{source_changelog}\">Source</a>\n" \
              f"<b>Support group:</b> <a href=\"https://t.me/X00TDDISC\">Device</a>\n\n" \
              f"<b>Notes:</b>\n- Non-FBE, LV, enforcing & 4.4 kernel based build\n- Safetynet pass by default\n\n" \

    return message

# Sending the message to Telegram
def send_msg(message,chat_id):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    params = {"chat_id": chat_id, "caption": message, "parse_mode": "HTML"}
    response = requests.post(telegram_url, params=params)
