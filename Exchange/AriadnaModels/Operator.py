# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class Operator(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.id = None  # Integer Необязательно Исполнитель, ID
        self.name = ''  # String Обязательно Исполнитель (ФИО)
        self.code = ''  # String Обязательно Исполнитель (Рег.Номер)
        super(Operator, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Operator, self).elementProperties()
        js.extend([("id", "id", int, False, None, False),
                   ("name", "name", str, False, None, True),
                   ("code", "code", str, False, None, True), ])
        return js
