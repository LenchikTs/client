# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class Certificate(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.documentType = 'CERTIFICATE'  # String Обязательно Тип документа
        self.series = ''  # String Обязательно Серия
        self.number = ''  # String Обязательно Номер
        self.issueDate = None  # DateTime Необязательно Дата выдачи
        self.expirationDate = None  # DateTime Необязательно Дата окончания срока действия
        self.issuer = None  # String Необязательно Кем выдан
        super(Certificate, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Certificate, self).elementProperties()
        js.extend([("documentType", "documentType", str, False, None, True),
                   ("series", "series", str, False, None, True),
                   ("number", "number", str, False, None, True),
                   ("issueDate", "issueDate", str, False, None, False),
                   ("expirationDate", "expirationDate", str, False, None, False),
                   ("issuer", "issuer", str, False, None, False)])
        return js
