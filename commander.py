# Перечисления команд, режимов
from command_enum import Command
from mode_enum import Mode

# Рабочие модули
from translate.yandex_translate import Translator
from weather import Weather
from myanimelist import Myanimelist

# Config
from config import yandex_translate_api


class Commander:

    def __init__(self):

        # Текущий, предыдущий режимы
        self.now_mode = Mode.default
        self.last_mode = Mode.default

        self.last_command = None

        # Для запомминания ответов пользователя
        self.last_ans = None

        # Работа с переводом
        self.translator = Translator(yandex_translate_api)

    def change_mode(self, to_mode):
        """
        Меняет режим приема команд
        :param to_mode: Измененный мод
        """
        self.last_mode = self.now_mode
        self.now_mode = to_mode

        self.last_ans = None

    def input(self, msg):
        """
        Функция принимающая сообщения пользователя
        :param msg: Сообщение
        :return: Ответ пользователю, отправившему сообщение
        """

        # Проверка на команду смены мода

        if msg.startswith("/"):
            for mode in Mode:
                if msg[1::] in mode.value:
                    self.change_mode(mode)
                    return "Режим изменен на " + self.now_mode.value[0]
            return "Неизвестный мод " + msg[1::]

        # Режим получения ответа
        if self.now_mode == Mode.get_ans:
            self.last_ans = msg
            self.now_mode = self.last_mode
            return "Ok!"

        if self.now_mode == Mode.default:

            # Погода
            if msg in Command.weather.value:
                return Weather.get_weather_today()

            # Топ аниме
            if msg in Command.anime_top.value:
                res = ""
                top = Myanimelist.get_top()
                for anime in top:
                    res += anime + " : " + top[anime] + "\n"

                return res

        if self.now_mode == Mode.translate:
            if self.last_ans is None:

                # Если язык не выбран, просим пользователя ввести
                self.change_mode(Mode.get_ans)
                self.last_command = msg
                return "Выберите язык на который следует перевести"

            elif self.last_ans == "change":

                # Меняем переводимый язык
                self.last_ans = None
                self.change_mode(Mode.default)

            else:
                # Переводим
                return self.translator.translate_to(msg, self.last_ans)

        return "Команда не распознана!"
