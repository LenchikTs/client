# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class Condition(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.id = ''  # String Обязательно Id по справочнику
        self.text = ''  # String Обязательно Наименование
        self.code = ''  # String Обязательно Код
        self.lcode = ''  # String Обязательно Строковый код
        self.groupCode = ''  # String Обязательно Код группы состояния
        super(Condition, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Condition, self).elementProperties()
        js.extend([("id", "id", str, False, None, True),
                   ("text", "text", str, False, None, True),
                   ("code", "code", str, False, None, True),
                   ("lcode", "lcode", str, False, None, True),
                   ("groupCode", "groupCode", str, False, None, True), ])
        return js
