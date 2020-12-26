from typing import List

from telegram import Update
from telegram.ext import Updater, CallbackContext
from telegram.ext import CommandHandler

from hcloud_tgbot.handlers import BotHandler


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def run():
    # updater = Updater(token=bot_token, use_context=True)
    # dispatcher = updater.dispatcher
    # start_handler = CommandHandler('start', start)
    # dispatcher.add_handler(start_handler)
    # print("pooling ...")
    # updater.start_polling()
    handler = BotHandler()
    handler.init_bot()

