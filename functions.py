import requests
import logging
import os
import re
import timeit
import subprocess
import datetime
from telegram import *
from telegram.ext import *
from time import *

start_time = datetime.datetime.now()

def start(update, context):
    now = datetime.datetime.now()
    active_duration = now - start_time
    days = active_duration.days
    hours, remainder = divmod(active_duration.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    message = f"Hello, I am ALIVE\n\nDoing SLAVERY Since: <b>{days}d:{hours}h:{minutes}m</b>"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML, reply_to_message_id=update.message.message_id)

def help(update, context):
    message = update.message
    reply_text = """Available commands:
• /ping --> to see response time.
• /start --> to get started.
• /latest --> to see latest roms from me.
• /source --> to see this bot source code.
• /shell --> to run shell commands (limited users only).
• Also yt-dlp function to download video from it's direct link (It will only work on authorised groups or chats)."""
    message.reply_markdown(reply_text, reply_to_message_id=message.message_id)

def supported(update: Update, context: CallbackContext):
    rising = "/latest rising"
    awaken = "/latest awaken"
    message = f"Currently only <b>RisingOS</b> and <b>AwakenOS</b> available\n<b>Run any of these you want:</b>\n<code>{awaken}</code>\n<code>{rising}</code>"
    update.message.reply_html(message, reply_to_message_id=update.message.message_id)

def latest(update: Update, context: CallbackContext):
    msg = update.message.text
    user_id = update.message.chat_id
    msg = msg.split(" ", 1)
    if len(msg) == 1:
        message = f"Use Proper Format.\nFrom: /supported"
        update.message.reply_html(message, reply_to_message_id=update.message.message_id)
    elif len(msg) == 2:
        parameter = msg[1]
        if parameter == "rising":
            try:
                data, source_changelog, device_changelog = f1(parameter)
                message = f2(data, source_changelog, device_changelog)
                update.message.reply_html(message, reply_to_message_id=update.message.message_id, disable_web_page_preview=True)

            except Exception as e:
                message = f"An error occurred while processing the command."
                update.message.reply_html(message, reply_to_message_id=update.message.message_id)
        elif parameter == "awaken":
            try:
                device, source_changelog, download = f3(parameter)
                message = f4(device, source_changelog, download)
                update.message.reply_html(message, reply_to_message_id=update.message.message_id, disable_web_page_preview=True)

            except Exception as e:
                message = f"An error occurred while processing the command."
                update.message.reply_html(message, reply_to_message_id=update.message.message_id)
        else:
            message = f"Use Proper Format.\nFrom: /supported"
            update.message.reply_html(message, reply_to_message_id=update.message.message_id)

def f1(rising):
    device_changelog = f"https://github.com/RisingOSS-devices/android_vendor_RisingOTA/raw/thirteen/changelog_X00TD.txt"
    source_changelog ="https://raw.githubusercontent.com/RisingTechOSS/android_vendor_rising/thirteen/build/tools/Changelog.txt"
    device_json = f"https://raw.githubusercontent.com/RisingOSS-devices/android_vendor_RisingOTA/thirteen/X00TD.json"
    response = requests.get(device_json)
    data = response.json()
    return data, source_changelog , device_changelog


def f2(data, source_changelog, device_changelog):
    device = data['response'][0]['device']
    version = data['response'][0]['version']
    support_group = data['response'][0]['forum']

    message = f"risingOS {version} | Official | Android 13\n" \
              f"<b>Supported Device:</b> {device}\n" \
              f"<b>Maintainer:</b> @SKetUl\n\n" \
              f"<b>Download:</b> <a href=\"https://www.pling.com/p/1935891\">Here</a>\n" \
              f"<b>Changelogs:</b> <a href=\"{source_changelog}\">Source</a> | <a href=\"{device_changelog}\">Device</a>\n" \
              f"<b>Support group:</b> <a href=\"https://t.me/RisingOSG\">Source</a> | <a href=\"{support_group}\">Device</a>\n\n" \
              f"<b>Notes:</b>\n- Non-FBE, LV, enforcing & 4.4 kernel based build\n- Safetynet pass by default\n\n" \

    return message

def f3(awaken):
    device = "X00TD"
    source_changelog = "https://t.me/AwakenOSNews"
    download = "https://www.pling.com/p/1888078/"
    return device, source_changelog, download


def f4(device, source_changelog, download):
    message = f"AwakenOS | Unofficial | Android 13\n" \
              f"<b>Supported Device:</b> {device}\n" \
              f"<b>Maintainer:</b> @SKetUl\n\n" \
              f"<b>Download:</b> <a href=\"{download}\">Here</a>\n" \
              f"<b>Changelogs:</b> <a href=\"{source_changelog}\">Source</a>\n" \
              f"<b>Support group:</b> <a href=\"https://t.me/SKetUs_OT\">Device</a>\n\n" \
              f"<b>Notes:</b>\n- Non-FBE, LV, enforcing & 4.4 kernel based build\n- Safetynet pass by default\n\n"

    return message

def ping(update: Update, context: CallbackContext):
    start_time = monotonic()
    message = f"Starting Ping..."
    reply = update.message.reply_text(message, reply_to_message_id=update.message.message_id)
    end_time = monotonic()
    ping_time = int((end_time - start_time) * 1000)
    reply.edit_text(f'{ping_time}ms')

def shell(update, context):
    authorized_users = os.environ.get("SUDO", "").split(",")
    user_id = str(update.effective_user.id)
    if user_id not in authorized_users:
        message = f"You are not sudo user."
        update.message.reply_html(message, reply_to_message_id=update.message.message_id)
        return
    message = update.message
    cmd = message.text.split(maxsplit=1)
    if len(cmd) == 1:
        message = f"No command to execute was given."
        update.message.reply_html(message, reply_to_message_id=update.message.message_id)
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
        message = "An error occurred while processing the command."
        update.message.reply_html(message, reply_to_message_id=update.message.message_id)

def logs(update, context):
    authorized_users = os.environ.get("SUDO", "").split(",")
    user_id = str(update.effective_user.id)
    if user_id not in authorized_users:
        message = f"You are not sudo user."
        update.message.reply_html(message, reply_to_message_id=update.message.message_id)
        return
    command = "tail -n 30 nohup.out"
    output = subprocess.check_output(command, shell=True, text=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=output, reply_to_message_id=update.message.message_id)

def vdl(update, context):
    authorized = os.environ.get("AUTHORISED", "").split(",")
    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)
    message_text = update.message.text
    video_formats = ["https://youtu.be", "https://www.youtube.com", "https://youtube.com/shorts", "http://www.youtube.com", "www.youtube.com", "https://www.instagram.com", "http://www.instagram.com", "https://pin.it", "https://vm.tiktok.com", "https://twitter.com"]
    if chat_id not in authorized and user_id not in authorized:
        return
    for format in video_formats:
        if format in message_text:
            try:
                video_link = extract(message_text, format)
                shared_by = shared(update.message.from_user)
                download(video_link, context, update.message.chat_id, update.message.message_id, update, shared_by)
                break
            except subprocess.CalledProcessError as e:
                context.bot.send_message(chat_id=chat_id, text=f"An error occurred: {e}", reply_to_message_id=update.message.message_id)

def shared(user):
    return user.username

def extract(text, base_url):
    start_index = text.find(base_url)
    end_index = text.find(" ", start_index)
    if end_index == -1:
        end_index = len(text)
    return text[start_index:end_index]

def download(video_link, context, chat_id, reply_to_message_id, update, shared_by):
    message = context.bot.send_message(chat_id=chat_id, text="Processing the video. Please wait...", reply_to_message_id=reply_to_message_id)
    subprocess.run(['yt-dlp', '-f', 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best[ext=mp4]', video_link], check=True)
    video_filename = file()
    file_size = os.path.getsize(video_filename)
    if file_size > 50 * 1024 * 1024:
        file_size_mb = file_size / (1024 * 1024)
        message = f"Video size limit is 50MB, but it's {file_size_mb:.2f}MB"
        context.bot.send_message(chat_id=chat_id, text=message, reply_to_message_id=reply_to_message_id)
        os.remove(video_filename)
        return
    title = ' '.join(word for word in os.path.splitext(os.path.basename(video_filename))[0].split() if not word.startswith('['))
    caption = f"<b>{title}</b>\n\nshared by <b>@{shared_by}</b>"
    with open(video_filename, 'rb') as video_file:
        context.bot.send_video(chat_id=chat_id, video=InputFile(video_file), reply_to_message_id=reply_to_message_id, caption=caption, parse_mode=ParseMode.HTML, timeout=120)
    os.remove(video_filename)
    context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)

def file():
    files = sorted(os.listdir('.'), key=os.path.getctime, reverse=True)
    for file in files:
        if file.endswith('.mp4'):
            return file
    return None

def source(update, context):
    message = f"<b>Intrested in source?</b>\n<a href=\"https://github.com/SKetU-l/mikupeice_robot.git\"><b>Get here</b></a>"
    update.message.reply_html(message, reply_to_message_id=update.message.message_id, disable_web_page_preview=True)
