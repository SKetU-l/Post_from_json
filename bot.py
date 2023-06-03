import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from functions import *

#Enable Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

updater = Updater(token=os.environ['TELEGRAM_BOT_TOKEN'],use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))

dp.add_handler(CommandHandler('latest',latest))

dp.add_handler(CommandHandler('supported', supported))

updater.start_polling()
updater.idle()
