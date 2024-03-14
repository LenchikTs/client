# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class Reagent(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.code = None  # String Обязательно Код реагента
        self.name = None  # String Необязательно Наименование реагента
        self.lot = None  # String Необязательно Лот реагента
        self.expirationDate = None  # DateTime Необязательно Дата окончания реагента
        super(Reagent, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Reagent, self).elementProperties()
        js.extend([("code", "code", str, False, None, True),
                   ("name", "name", str, False, None, False),
                   ("lot", "lot", str, False, None, False),
                   ("expirationDate", "expirationDate", str, False, None, False)
                   ])
        return js
