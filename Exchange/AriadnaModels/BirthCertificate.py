# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class BirthCertificate(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.documentType = 'BIRTH_CERTIFICATE'  # String Обязательно Тип документа
        self.series = ''  # String Обязательно Серия
        self.number = ''  # String Обязательно Номер
        self.birthPlace = None  # String Необязательно Место рождения
        self.issueDate = None  # DateTime Необязательно Дата выдачи
        self.issuer = None  # String Необязательно Кем выдан
        super(BirthCertificate, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(BirthCertificate, self).elementProperties()
        js.extend([("documentType", "documentType", str, False, None, True),
                   ("series", "series", str, False, None, True),
                   ("number", "number", str, False, None, True),
                   ("birthPlace", "birthPlace", str, False, None, False),
                   ("issueDate", "issueDate", str, False, None, False),
                   ("issuer", "issuer", str, False, None, False)])
        return js
