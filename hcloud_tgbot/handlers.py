from typing import List

from telegram import Update, ParseMode, ChatAction, TelegramError
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler, Filters, Handler

from hcloud_tgbot.builders import MessageBuilder, MenuBuilder
from hcloud_tgbot import config
from hcloud_tgbot.hetzner.api import HetznerCloud
from hcloud_tgbot.utils import send_typing_action
from hcloud_tgbot.validators import user_validator, action_validator


class BotHandler:
    """
    Main handler class

    Use this class to initiate and run the bot.
    All command/message handlers can be found here
    """
    def __init__(self):
        self.updater = Updater(token=config.BOT_TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.hetzner_client = HetznerCloud()

    def __get_handlers(self) -> List[Handler]:
        """Creates handlers"""
        handlers = [
            # /start and /help
            CommandHandler(['start', 'help'], self.start_handler),
            # /me
            CommandHandler('me', self.me_handler),
            # /servers
            CommandHandler('servers', self.servers_handler),
            # Server details. "/server_1234567"
            MessageHandler(Filters.regex('\/server(_\d*)'), self.server_details_handler),
            # Update server details message. "server_1234567_update"
            CallbackQueryHandler(pattern='server(_\d*)(_update*)', callback=self.update_handler),
            # Server action. "server_1234567_reset", "server_1234567_shutdown", etc
            CallbackQueryHandler(pattern='server(_\d*)(_[a-z]*)', callback=self.action_handler)
        ]

        return handlers

    def __add_handlers(self):
        """Adds all the handlers to the dispatcher"""
        handlers = self.__get_handlers()
        for handler in handlers:
            self.dispatcher.add_handler(handler)

    def init_bot(self):
        """Initiates the bot"""
        self.__add_handlers()
        self.updater.start_polling()
        self.updater.idle()

    @user_validator
    def start_handler(self, update: Update, context: CallbackContext):
        """Handles the /start command by sending the help text and menu"""
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=MessageBuilder.start(),
            reply_markup=MenuBuilder.main()
        )

    @staticmethod
    def me_handler(update: Update, context: CallbackContext):
        """Handles the /me command by sending the user id and username"""
        context.bot.send_message(chat_id=update.effective_chat.id, text=MessageBuilder.me(update))

    @send_typing_action
    @user_validator
    def servers_handler(self, update: Update, context: CallbackContext):
        """
        Handles the /servers command
        Asks for a list of servers from Hetzner api and sends a list of all the returned servers
        """
        servers = self.hetzner_client.get_servers_list()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=MessageBuilder.servers_list(servers),
            parse_mode=ParseMode.HTML
        )

    @send_typing_action
    @user_validator
    def server_details_handler(self, update: Update, context: CallbackContext):
        """
        Handles the server details commands: /server_<SERVER_ID>
        Sends the server details and a menu containing all the available actions to the user
        """
        server_id = int(update.message.text.replace("/server_", ""))
        server = self.hetzner_client.get_server(server_id)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=MessageBuilder.server_details(server),
            parse_mode=ParseMode.HTML,
            reply_markup=MenuBuilder.server_actions(server_id)
        )

    @send_typing_action
    @user_validator
    def update_handler(self, update: Update, context: CallbackContext):
        """Updates the server details message text if there is a change"""
        server_id = int(update.callback_query.data.split("_")[1])
        server = self.hetzner_client.get_server(server_id)

        # An error will be raised if the text hasn't changed
        # Just ignore the error since it has no effect
        try:
            context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=update.callback_query.message.message_id,
                text=MessageBuilder.server_details(server),
                reply_markup=MenuBuilder.server_actions(server_id),
                parse_mode=ParseMode.HTML,
            )
        except TelegramError:
            pass

    @user_validator
    @action_validator
    def action_handler(self, update: Update, context: CallbackContext, action: str, server_id: int):
        """Handles all the server action requests by passing them to the Hetzner API and returns the result"""
        print(update)

        # create a message notifying user that the action is being processed
        msg = context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=MessageBuilder.action_processing(action),
        )
        # 'typing ...'  will stop after first message using the 'send_typing_action' decorator
        # So just add a typing action manually that lasts longer
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)

        ok, result = self.hetzner_client.handle_action(action, server_id)

        # Generate the result text based on the action status
        if not ok:
            text = MessageBuilder.action_failed(action)
        else:
            text = MessageBuilder.action_success(action, result)

        # Update the previous message with action result
        context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=msg.message_id,
            text=text,
            parse_mode=ParseMode.HTML,
        )
