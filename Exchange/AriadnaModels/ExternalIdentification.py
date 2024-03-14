# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject
from Exchange.AriadnaModels.Registry import Registry


class ExternalIdentification(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
                """
        self.value = ''  # String Обязательно Значение внешнего идентификатора
        self.valueText = ''  # String Обязательно Текстовая форма внешнего идентификатора
        self.registry = Registry()  # Object Обязательно Реестр внешних идентификаторов
        super(ExternalIdentification, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(ExternalIdentification, self).elementProperties()
        js.extend([("value", "value", str, False, None, True),
                   ("valueText", "valueText", str, False, None, True),
                   ("registry", "registry", Registry, False, None, True), ])
        return js
