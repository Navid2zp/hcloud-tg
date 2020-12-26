from typing import List

from hcloud import Client
from hcloud.servers.client import BoundServer
from hcloud.servers.domain import Server

from hcloud_tgbot import config

# All allowed actions for a server
# "update" is used for updating server details message
allowed_actions = ["reset", "reboot", "power-on", "power-off", "shutdown", "password", "update"]


class HetznerCloud(Client):
    """Cloud action handler class"""

    def __init__(self):
        super().__init__(config.HETZNER_API_KEY, poll_interval=3)

    def get_servers_list(self) -> List[BoundServer]:
        """Retrieves all the servers from Hetzner cloud API and returns them"""
        return self.servers.get_all()

    def get_server(self, server_id: int) -> BoundServer:
        """Retrieves a server by id and returns it"""
        return self.servers.get_by_id(server_id)

    def _reset_handler(self, server_id: int):
        """Restarts a server using the given server id"""
        self.servers.reset(server=Server(id=server_id)).wait_until_finished()

    def _reboot_handler(self, server_id: int):
        """Reboots a server using the given server id"""
        self.servers.reboot(server=Server(id=server_id)).wait_until_finished()

    def _shutdown_handler(self, server_id: int):
        """Shutdowns a server using the given server id"""
        self.servers.shutdown(server=Server(id=server_id)).wait_until_finished()

    def _power_on_handler(self, server_id: int):
        """Powers on a server using the given server id"""
        self.servers.power_on(server=Server(id=server_id)).wait_until_finished()

    def _power_off_handler(self, server_id: int):
        """Powers off a server using the given server id"""
        self.servers.power_off(server=Server(id=server_id)).wait_until_finished()

    def _password_handler(self, server_id):
        """Resets server password using the given server id"""
        response = self.servers.reset_password(server=Server(id=server_id))
        return {"root_password": response.root_password}

    def handle_action(self, action: str, server_id: int):
        """
        Validates the given action and maps it to the proper handler if it's valid
        :param action: server action
        :param server_id: server id which the action will be requested for
        :return: True/False if request succeeded/failed and request response payload if available
        """
        if action not in allowed_actions:
            return False, None

        # Check if we have an implemented method for the action
        handler_func = getattr(self, f'_{action.replace("-", "_")}_handler', None)
        if not callable(handler_func):
            return False, None
        try:
            result = handler_func(server_id=server_id)
            return True, result
        except:
            return False, None
