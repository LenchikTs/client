# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject
from Exchange.AriadnaModels.Reagent import Reagent


class ResourceReagent(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.resource = None  # Object Обязательно Передается объект типа реагент
        self.resourceType = 'ReagentType'  # String Обязательно Всегда ReagentType
        self.uri = None  # String Обязательно Uuid ссылка на реагент связывающий реагент и результат
        super(ResourceReagent, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(ResourceReagent, self).elementProperties()
        js.extend([("resource", "resource", Reagent, False, None, True),
                   ("resourceType", "resourceType", str, False, None, True),
                   ("uri", "uri", str, False, None, True)
                   ])
        return js
