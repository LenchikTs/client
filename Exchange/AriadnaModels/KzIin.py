# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class KzIin(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.documentType = 'KZ_IIN'  # String Обязательно Тип документа(KZ_IIN)
        self.number = ''  # String Обязательно Номер
        super(KzIin, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(KzIin, self).elementProperties()
        js.extend([("documentType", "documentType", str, False, None, True),
                   ("number", "number", str, False, None, True)
                   ])
        return js
