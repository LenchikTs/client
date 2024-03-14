# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject
from Exchange.AriadnaModels.SignedDoctor import SignedDoctor


class Semd(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.signedDoctor = None  # Объект Необязательно Данные по подписавшему документ врачу
        self.practitionerSig = None  # String Необязательно Подпись врача в формате Base64
        self.organizationSig = None  # String Необязательно Подпись организации в формате Base64
        self.docData = None  # String Необязательно СЭМД файл в формате Base64
        super(Semd, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Semd, self).elementProperties()
        js.extend([("signedDoctor", "signedDoctor", SignedDoctor, False, None, False),
                   ("practitionerSig", "practitionerSig", str, False, None, False),
                   ("organizationSig", "organizationSig", str, False, None, False),
                   ("docData", "docData", str, False, None, False)
                   ])
        return js
