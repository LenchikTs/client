# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class GiveResult(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
                """
        self.toOrderingInstitution = None  # Boolean Необязательно Результат выдать направившей организации
        self.toPatient = None  # Boolean Необязательно Результат выдать пациенту
        self.toReceiverInstitution = None  # Boolean Необязательно Результат выдать принявшей организации
        super(GiveResult, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(GiveResult, self).elementProperties()
        js.extend([("toOrderingInstitution", "toOrderingInstitution", bool, False, None, False),
                   ("toPatient", "toPatient", bool, False, None, False),
                   ("toReceiverInstitution", "toReceiverInstitution", bool, False, None, False), ])
        return js
