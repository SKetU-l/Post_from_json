import requests
import logging
import os
import timeit
import subprocess
from datetime import datetime
from telegram import *
from telegram.ext import *
from time import *

def start(update: Update, context: CallbackContext):
    reply_text = "Hello, I am alive."
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text, reply_to_message_id=update.message.message_id)

def supported(update: Update, context: CallbackContext):
    rising = "/latest awaken"
    awaken = "/latest rising"
    reply_text = f"Currently only <b>RisingOS</b> and <b>AwakenOS</b> available\n<b>Run any of these you want:</b>\n<code>{rising}</code>\n<code>{awaken}</code>"
    update.message.reply_html(reply_text, reply_to_message_id=update.message.message_id)

def latest(update: Update, context: CallbackContext):
    msg = update.message.text
    user_id = update.message.chat_id
    msg = msg.split(" ", 1)
    if len(msg) == 1:
        reply_text = "Use Proper Format. From: /supported"
        update.message.reply_html(reply_text, reply_to_message_id=update.message.message_id)
    elif len(msg) == 2:
        parameter = msg[1]
        if parameter == "rising":
            try:
                data, source_changelog, device_changelog = function1(parameter)
                reply_text = function2(data, source_changelog, device_changelog)
                update.message.reply_html(reply_text, reply_to_message_id=update.message.message_id, disable_web_page_preview=True)

            except Exception as e:
                reply_text = "An error occurred while processing the command."
                update.message.reply_html(reply_text, reply_to_message_id=update.message.message_id)
        elif parameter == "awaken":
            try:
                device, source_changelog, download = function3(parameter)
                reply_text = function4(device, source_changelog, download)
                update.message.reply_html(reply_text, reply_to_message_id=update.message.message_id, disable_web_page_preview=True)

            except Exception as e:
                reply_text = "An error occurred while processing the command."
                update.message.reply_html(reply_text, reply_to_message_id=update.message.message_id)
        else:
            reply_text ="Use Proper Format. From: /supported"
            update.message.reply_html(reply_text, reply_to_message_id=update.message.message_id)

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
    device = "X00TD"
    source_changelog = "https://t.me/AwakenOSNews"
    download = "https://www.pling.com/p/1888078/"
    return device, source_changelog, download


def function4(device, source_changelog, download):
    message = f"AwakenOS | Unofficial | Android 13\n" \
              f"<b>Supported Device:</b> {device}\n" \
              f"<b>Maintainer:</b> @SKetUl\n\n" \
              f"<b>Download:</b> <a href=\"{download}\">Here</a>\n" \
              f"<b>Changelogs:</b> <a href=\"{source_changelog}\">Source</a>\n" \
              f"<b>Support group:</b> <a href=\"https://t.me/X00TDDISC\">Device</a>\n\n" \
              f"<b>Notes:</b>\n- Non-FBE, LV, enforcing & 4.4 kernel based build\n- Safetynet pass by default\n\n"

    return message

def ping(update: Update, context: CallbackContext):
    start_time = monotonic()
    reply_text = "Starting Ping..."
    reply = update.message.reply_text(reply_text, reply_to_message_id=update.message.message_id)
    end_time = monotonic()
    ping_time = int((end_time - start_time) * 1000)
    reply.edit_text(f'{ping_time}ms')

LOGGER = logging.getLogger(__name__)

def shell(update, context):
    authorized_users = os.environ.get("SUDO", "").split(",")
    user_id = str(update.effective_user.id)

    if user_id not in authorized_users:
        reply_text = "You are not authorized to use this command."
        update.message.reply_html(reply_text, reply_to_message_id=update.message.message_id)
        return

    message = update.message
    cmd = message.text.split(maxsplit=1)
    if len(cmd) == 1:
        reply_text = "No command to execute was given."
        update.message.reply_html(reply_text, reply_to_message_id=update.message.message_id)
        return
    cmd = cmd[1]
    start_time = timeit.default_timer()
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        end_time = timeit.default_timer()
        ping_time = int((end_time - start_time) * 1000)
        reply = f"<b>Command Output:</b>\n\n{result.stdout}"
        if result.stderr:
            reply += f"\n\n<b>Error Output:</b>\n\n{result.stderr}"
        reply += f"\n\n<b>Execution Time:</b> {ping_time}ms"
        update.message.reply_html(reply, reply_to_message_id=update.message.message_id, disable_web_page_preview=True)
    except Exception as e:
        reply_text = "An error occurred while processing the command."
        update.message.reply_html(reply_text, reply_to_message_id=update.message.message_id)

def ytdl(update, context):
    authorized = os.environ.get("AUTHORISED", "").split(",")
    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)
    message_text = update.message.text
    video_formats = ["https://youtu.be", "https://www.youtube.com", "http://www.youtube.com", "www.youtube.com", "https://www.instagram.com", "http://www.instagram.com", "www.instagram.com", "https://pin.it"]

    if chat_id not in authorized and user_id not in authorized:
        return

    for format in video_formats:
        if format in message_text:
            try:
                video_link = extract(message_text, format)
                download_video(video_link, context, update.message.chat_id, update.message.message_id)
                break
            except subprocess.CalledProcessError as e:
                update.message.reply_text(f"An error occurred: {e}", reply_to_message_id=update.message.message_id)

def extract(text, base_url):
    start_index = text.find(base_url)
    end_index = text.find(" ", start_index)
    if end_index == -1:
        end_index = len(text)
    return text[start_index:end_index]

def download_video(video_link, context, chat_id, reply_to_message_id):
    subprocess.run(['yt-dlp', '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', video_link], check=True)
    video_filename = get_file()
    with open(video_filename, 'rb') as video_file:
        context.bot.send_video(chat_id=chat_id, video=InputFile(video_file), reply_to_message_id=reply_to_message_id, timeout=120)
    os.remove(video_filename)

def get_file():
    files = sorted(os.listdir('.'), key=os.path.getctime, reverse=True)
    for file in files:
        if file.endswith('.mp4'):
            return file
    return None
