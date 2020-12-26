from functools import wraps

from telegram import ChatAction


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(ref, update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(ref, update, context,  *args, **kwargs)

    return command_func


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    """Builds a menu with the given style using the provided buttons

    :return:
        list of buttons
    """
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def clean_action_name(action: str) -> str:
    """Cleans the given action to be used in the texts"""
    return action.replace("-", " ").capitalize()


def flag(code):
    """Returns the emoji flag for the given ISO code"""
    OFFSET = 127462 - ord('A')
    code = code.upper()
    return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)


# Emoji map
status_emoji_map = {
    "running": "🟢",
    "off": "🔴",
    "migrating": "🔵",
    "initializing": "🟤",
}


def status_emoji(status: str):
    """Returns an emoji based on the given status"""
    return status_emoji_map.get(status, "⚪️")


