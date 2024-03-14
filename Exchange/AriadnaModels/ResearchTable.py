# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class ResearchTable(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.id = ''  # String Обязательно Вид исследования, ID
        self.alias = ''  # String Обязательно Кодовое имя вида исследования
        self.name = ''  # String Обязательно Имя вида исследования
        self.description = ''  # String Обязательно Наименование вида исследований
        super(ResearchTable, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(ResearchTable, self).elementProperties()
        js.extend([("id", "id", str, False, None, True),
                   ("alias", "alias", str, False, None, True),
                   ("name", "name", str, False, None, True),
                   ("description", "description", str, False, None, True), ])
        return js
