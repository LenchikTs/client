# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject
from Exchange.AriadnaModels.SignedDoctor import SignedDoctor


class Binary(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.signedDoctor = None  # Объект Необязательно Данные по подписавшему документ врачу
        self.practitioner = None  # String Необязательно Подпись врача в формате Base64
        self.organization = None  # String Необязательно Подпись организации в формате Base64
        self.pdf = None  # String Необязательно Пдф файл в формате Base64
        super(Binary, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Binary, self).elementProperties()
        js.extend([("signedDoctor", "signedDoctor", SignedDoctor, False, None, False),
                   ("practitioner", "practitioner", str, False, None, False),
                   ("organization", "organization", str, False, None, False),
                   ("pdf", "pdf", str, False, None, False)
                   ])
        return js
