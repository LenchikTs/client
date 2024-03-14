# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject
from Exchange.AriadnaModels.Authority import Authority


class Registry(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
                """
        self.id = ''  # String Обязательно Реестр, ID
        self.title = ''  # String Обязательно Наименование
        self.description = ''  # String Обязательно Описание реестра
        self.authority = None  # Object Необязательно Источник ведомости
        super(Registry, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Registry, self).elementProperties()
        js.extend([("id", "id", str, False, None, True),
                   ("title", "title", str, False, None, True),
                   ("description", "description", str, False, None, True),
                   ("authority", "authority", Authority, False, None, False), ])
        return js
