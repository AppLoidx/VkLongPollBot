from enum import Enum


class Mode(Enum):
    default = ["Обычный режим", "default"]
    translate = ["Режим переводчика", "translate"]
    get_ans = ["Режим ввода ответа"]
