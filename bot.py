import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from functions import *
from dotenv import load_dotenv

load_dotenv('config.env')

# Enable Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

updater = Updater(token=os.environ['BOT_TOKEN'], use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('ping', ping))
dp.add_handler(CommandHandler('latest', latest))
dp.add_handler(CommandHandler('supported', supported))
dp.add_handler(CommandHandler('shell', shell))
dp.add_handler(MessageHandler(Filters.text & (~Filters.command), ytdl))

updater.start_polling()
updater.idle()
