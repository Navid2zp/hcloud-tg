from telegram import Update
from telegram.ext import CallbackContext

from hcloud_tgbot import config
from hcloud_tgbot.hetzner.api import allowed_actions


def user_validator(func):
    def validation_wrapper(ref, update: Update, context: CallbackContext):
        chat_id = update.callback_query.message.chat.id if update.callback_query else update.message.chat.id
        if chat_id not in config.ALLOWED_USERS:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You're you??\nYour ID: " + str(update.effective_chat.id)
            )
            return
        return func(ref, update, context)

    return validation_wrapper


def action_validator(func):
    def validation_wrapper(ref, update: Update, context: CallbackContext):
        raw_text = update.callback_query.data
        sp = raw_text.split("_")
        if len(sp) != 3:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid action!")
            return
        if sp[-1] not in allowed_actions:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid action!")
            return
        return func(ref, update, context, sp[2], sp[1])

    return validation_wrapper
