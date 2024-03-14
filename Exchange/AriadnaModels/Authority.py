# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class Authority(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
                """
        self.id = ''  # String Обязательно Источник ведомости, ID
        self.localName = ''  # String Обязательно Наименование краткое
        self.fullName = ''  # String Обязательно Наименование полное
        super(Authority, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Authority, self).elementProperties()
        js.extend([("id", "id", str, False, None, True),
                   ("localName", "localName", str, False, None, True),
                   ("fullName", "fullName", str, False, None, True), ])
        return js
