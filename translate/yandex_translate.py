import requests
from config import yandex_translate_api


class Translator:
    """
    Класс-переводчик использующий API Yandex Translate

    Параметры:

    _key -- ключ от API Yandex.Translate
    _yandex_comment -- согласовано с правилами офомления и использования API Yandex.Translate
    """
    def __init__(self, key, comment=None):
        """
        :param key: ключ от API Yandex.Translate
        :param comment: Комментарий к каждому переводу
        """
        self._key = key
        if comment is None:
            self._yandex_comment = "\nПереведено сервисом «Яндекс.Переводчик» http://translate.yandex.ru/"
        else:
            self._yandex_comment = comment

    def translate(self, text, lang, to_lang=None):
        """
        Переводит текст с указанного языка в другой указанный

        :param text: Текст, который нужно перевести
        :param lang: исходный язык
        :param to_lang: конечный язык
        :return: Переведенный текст
        """
        if to_lang is not None:
            lang = f"{lang}-{to_lang}"
        main_url = "https://translate.yandex.net/api/v1.5/tr.json/translate"
        response = requests.get(f"{main_url}?"
                                f"key={self._key}&"
                                f"lang={lang}&"
                                f"text={text}")

        return response.json()['text'][0] + self._yandex_comment

    def lang_identify(self, text, hint="ru,en"):
        """
        Идентифицирует язык

        :param text: Текст
        :param hint: Подсказки для определения языка
        :return: код языка
        """
        main_url = "https://translate.yandex.net/api/v1.5/tr.json/detect"
        response = requests.get(f"{main_url}?"
                                f"key={self._key}&"
                                f"hint={hint}&"
                                f"text={text}")

        return response.json()['lang']

    def translate_ru_en(self, text):
        """
        Переводит текст с русского на английский
        :param text: Текст, который нужно перевести
        :return: Текст переведенный на английский язык
        """
        if self.lang_identify(text) == "ru":
            to_lang = "en"
            from_lang = "ru"
        else:
            to_lang = "ru"
            from_lang = "en"

        return self.translate(text, from_lang, to_lang)

    def translate_to_ru(self, text, hint=None):
        """
        Переводит текст на русский

        :param text: Текст, который нужно перевести
        :param hint: Подсказки к определению языка
        :return: Текст переведенный на русский язык
        """
        if hint is None:
            hint = "ru,en"
        from_lang = self.lang_identify(text, hint)

        return self.translate(text, from_lang, "ru")

    def translate_to(self, text, to_lang, hint=None):
        """
        Переводит текст в нужный язык

        :param text: Текст, который нужно перевести
        :param to_lang: Код результирующего языка
        :param hint: Подсказки к определению языка
        :return: Переведенный текст
        """
        if hint is None:
            hint = "ru,en"
        from_lang = self.lang_identify(text, hint)

        return self.translate(text, from_lang, to_lang)


