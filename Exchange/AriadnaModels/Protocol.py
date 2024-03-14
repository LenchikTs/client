# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class Protocol(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.resCode = ''  # String Обязательно Код измерения
        self.resultText = ''  # String Обязательно Полный текст значения измерения
        self.resultValue = ''  # String Обязательно Значение измерения
        self.measurName = ''  # String Обязательно Наименование измерения
        super(Protocol, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Protocol, self).elementProperties()
        js.extend([("resCode", "resCode", str, False, None, True),
                   ("resultText", "resultText", str, False, None, True),
                   ("resultValue", "resultValue", str, False, None, True),
                   ("measurName", "measurName", str, False, None, True), ])
        return js
