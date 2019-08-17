import random

import vk_api.vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

from commander import Commander


class Server:

    def __init__(self, api_token, group_id, server_name: str="Empty"):

        # Даем серверу имя
        self.server_name = server_name

        self.group_id = group_id

        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)

        # Для использоания Long Poll API
        self.long_poll = VkBotLongPoll(self.vk, group_id, wait=30)

        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()

        # Словарь дял каждого отдельного пользователя
        self.users = {}

    def send_msg(self, send_id, message):
        """
        Отправка сообщения через метод messages.send
        :param send_id: vk id пользователя, который получит сообщение
        :param message: содержимое отправляемого письма
        :return: None
        """
        return self.vk_api.messages.send(peer_id=send_id,
                                         message=message,
                                         random_id=random.randint(0, 2048),
                                         keyboard=open("keyboards/default.json", "r", encoding="UTF-8").read())

    def start(self):
        for event in self.long_poll.listen():   # Слушаем сервер
            if event.type == VkBotEventType.MESSAGE_NEW:

                if event.object.from_id not in self.users:
                    self.users[event.object.from_id] = Commander()

                # Пришло новое сообщение
                if event.type == VkBotEventType.MESSAGE_NEW:

                    self.send_msg(event.object.peer_id,
                                  self.users[event.object.from_id].input(event.object.text))
