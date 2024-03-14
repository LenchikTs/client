# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class Snils(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.documentType = 'SNILS'  # String Обязательно Тип документа
        self.number = ''  # String Обязательно Номер
        self.issueDate = None  # DateTime Необязательно Дата регистрации
        super(Snils, self).__init__(jsondict)


    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Snils, self).elementProperties()
        js.extend([("documentType", "documentType", str, False, None, True),
                   ("number", "number", str, False, None, True),
                   ("issueDate", "issueDate", str, False, None, False)])
        return js
