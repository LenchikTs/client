# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class ResourceRef(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.ref = ''  # String Обязательно Uuid строка связывающая результат с определенным ресурсом
        super(ResourceRef, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(ResourceRef, self).elementProperties()
        js.extend([("ref", "ref", str, False, None, True)
                   ])
        return js
