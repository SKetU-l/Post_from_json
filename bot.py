import requests
import os
from datetime import datetime

device_codename = os.getenv("DEVICE_CODENAME")
device_changelog = f"https://github.com/RisingOSS-devices/android_vendor_RisingOTA/raw/thirteen/changelog_{device_codename}.txt"
source_changelog ="https://raw.githubusercontent.com/RisingTechOSS/android_vendor_rising/thirteen/build/tools/Changelog.txt"
banner_path = f"banners/{device_codename}.png"
banner_file = {'photo': ('{device_codename}.png', open(banner_path, 'rb').read())}
json_url = f"https://raw.githubusercontent.com/RisingOSS-devices/android_vendor_RisingOTA/thirteen/{device_codename}.json"
response = requests.get(json_url)
data = response.json()
notes_file = open(f"notes/{device_codename}.txt", "r")
notes = notes_file.read()
notes_file.close()

# Extracting the required information from the JSON
maintainer = data['response'][0]['maintainer']
oem = data['response'][0]['oem']
device = data['response'][0]['device']
version = data['response'][0]['version']
download_link = data['response'][0]['download']
support_group = data['response'][0]['forum']
telegram_url = data['response'][0]['telegram']
release_date = datetime.now().strftime('%d/%m/%Y')

message = f"#risingOS #TIRAMISU #ROM #{device}\n" \
          f"risingOS v{version} | Official | Android 13\n" \
          f"<b>Supported Device:</b> {device}\n" \
          f"<b>Released:</b> {release_date}\n" \
          f"<b>Maintainer:</b> <a href=\"{telegram_url}\">{maintainer}</a>\n\n" \
          f"◾<b>Download:</b> <a href=\"https://www.pling.com/p/1935891\">Here</a>\n" \
          f"◾<b>Screenshots:</b> <a href=\"https://t.me/riceDroidNews/719\">Here</a>\n" \
          f"◾<b>Changelogs:</b> <a href=\"{source_changelog}\">Source</a> | <a href=\"{device_changelog}\">Device</a>\n" \
          f"◾<b>Support group:</b> <a href=\"https://t.me/riceDroidsupport\">Source</a> | <a href=\"{support_group}\">Device</a>\n\n" \
          f"<b>Notes:</b>\n{notes}\n" \
          f"<b>Credits:</b>\n- @not_ayan99 for banner"

# Sending the message to Telegram
chat_id = os.getenv('TELEGRAM_CHAT_ID')
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
params = {"chat_id": chat_id, "caption": message, "parse_mode": "HTML"}
response = requests.post(telegram_url, params=params, files=banner_file)

if response.status_code != 200:
    print(f"Error sending message: {response.status_code}, {response.text}")
else:
    print("Message sent successfully!")
