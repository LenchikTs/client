# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class Service(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.id = ''  # String Обязательно ID по справочнику
        self.name = ''  # String Обязательно Наименование услуги
        self.code = ''  # String Обязательно Код услуги
        super(Service, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Service, self).elementProperties()
        js.extend([("id", "id", str, False, None, True),
                   ("name", "name", str, False, None, True),
                   ("code", "code", str, False, None, True), ])
        return js
