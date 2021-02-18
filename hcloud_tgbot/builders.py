from typing import List, Union

from hcloud.servers.client import BoundServer
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from hcloud_tgbot.hetzner.api import allowed_actions
from hcloud_tgbot.utils import build_menu, clean_action_name, flag, status_emoji


class MessageBuilder:
    """
        A class containing all the message text generator methods
        All methods are staticmethod
    """

    @staticmethod
    def start() -> str:
        return f'''
Hello there,

You can manage your servers using this bot.
Send /servers to list all the servers you have.
You can then manage each of them from there.

Send /help or /start if you needed some help.

Good luck ;)
'''

    @staticmethod
    def me(update: Update) -> str:
        chat = update.callback_query.message.chat if update.callback_query else update.message.chat
        return f'''
You are {chat.username}
You chat ID is {chat.id}
'''

    @staticmethod
    def servers_list(servers: List[BoundServer]) -> str:
        if len(servers) == 0:
            return f'''
You don't have any servers.
NOTE: Only servers in the same project as the given API key will be listed here.
            '''
        response = f'''
Here is a list of your servers:
        '''

        for server in servers:
            response += f'''
<b>Server name:</b> {server.name}
<b>Server status:</b> {status_emoji(server.status)} {server.status}
<b>Server details:</b> /server_{server.id}

            '''
            return response

    @staticmethod
    def server_details(server: BoundServer):
        return f'''<b>Server name:</b> {server.name}
<b>Server IP:</b> {server.public_net.ipv4.ip}
<b>Server status:</b> {status_emoji(server.status)} {server.status}

<b>Server type:</b> {server.server_type.description}
<b>   - Memory:</b> {server.server_type.memory}GB
<b>   - CPU:</b> {server.server_type.cores} cores
<b>   - Disk:</b> {server.server_type.disk}GB

<b>Datacenter:</b> {server.datacenter.description}
<b>   - Country:</b> {flag(server.datacenter.location.country.lower())} {server.datacenter.location.country}
<b>   - City:</b> {server.datacenter.location.city}'''

    @staticmethod
    def action_processing(action: str):
        if action == "reset":
            return "Restarting the server ..."
        if action == "reboot":
            return "Rebooting the server ..."
        if action == "power-on":
            return "Powering on the server ..."
        if action == "power-off":
            return "Powering off the server ..."
        if action == "shutdown":
            return "Shutting down the server ..."
        if action == "password":
            return "Creating new root password ..."

        return "Unknown action is running ..."

    @staticmethod
    def action_success(action: str, payload: Union[dict, None]) -> str:
        if action == "reset":
            return "Server restarted"
        if action == "reboot":
            return "Server rebooted"
        if action == "power-on":
            return "Server powered on"
        if action == "power-off":
            return "Server powered off"
        if action == "shutdown":
            return "Server shutdown"
        if action == "password":
            return f'''
New password created.

<b>🔑 New root password:</b> <code>{payload.get("root_password") if payload else ""}</code>
            '''

        return "Unknown action finished!"

    @staticmethod
    def action_failed(action: str) -> str:
        if action == "reset":
            return "Failed to restart the server!"
        if action == "reboot":
            return "Failed to reboot the server!"
        if action == "power-on":
            return "Failed to power on the server!"
        if action == "power-off":
            return "Failed to power off the server!"
        if action == "shutdown":
            return "Failed to shutdown the server!"
        if action == "password":
            return "Failed to reset root password!"

        return "Unknown action failed!"


class MenuBuilder:
    """
        A class containing all the message menu generator methods
        All methods are staticmethod
    """

    @staticmethod
    def main() -> ReplyKeyboardMarkup:
        """Generates the main menu"""

        main_keyboard = [['/servers'],
                         ['/help', '/me']]
        reply_markup = ReplyKeyboardMarkup(main_keyboard)
        return reply_markup

    @staticmethod
    def server_actions(server_id: int) -> InlineKeyboardMarkup:
        """Generates the action menu for a server"""

        base_callback_str = f'server_{server_id}_'
        button_list = []

        # Exclude "update" which is the last item in the list action to be used later in footer
        for action in allowed_actions[:-1]:
            button_list.append(
                InlineKeyboardButton(clean_action_name(action), callback_data=base_callback_str + action)
            )

        # Set "update" as the footer button
        footer = InlineKeyboardButton(
            clean_action_name(allowed_actions[-1]), callback_data=base_callback_str + allowed_actions[-1]
        )

        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3, footer_buttons=footer))
        return reply_markup
