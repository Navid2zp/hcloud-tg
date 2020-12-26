import os

from hcloud_tgbot.handlers import BotHandler
from hcloud_tgbot import config


if __name__ == '__main__':
    bot_token = os.getenv("BOT_TOKEN")
    hetzner_api_key = os.getenv("HETZNER_API_KEY")
    allowed_user_string = os.getenv("ALLOWED_USERS")
    allowed_users = [int(user_id) for user_id in allowed_user_string.split("-")] if allowed_user_string else []
    print("Allowed users:")
    for user in allowed_users:
        print("   - ", user)
    config.set_token(bot_token).set_allowed_users(allowed_users).set_hetzner_api_key(hetzner_api_key)
    print("Bot configured ...")
    print("Running the bot ...")

    handler = BotHandler()
    handler.init_bot()
