from typing import List


global BOT_TOKEN
global ALLOWED_USERS


class Config:
    BOT_TOKEN: str = ""
    ALLOWED_USERS: List[int] = []
    HETZNER_API_KEY: str = ""

    def set_token(self, token: str):
        self.BOT_TOKEN = token
        return self

    def set_hetzner_api_key(self, key: str):
        self.HETZNER_API_KEY = key
        return self

    def set_allowed_users(self, allowed_users: List[int]):
        self.ALLOWED_USERS = allowed_users
        return self


config = Config()



