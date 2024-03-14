# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class CodeableConcept(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.system = None  # String Обязательно Версия справочника
        self.code = None  # String Обязательно Код справочника
        self.display = None  # String Необязательно Описание справочника
        self.version = None  # String Необязательно Версия справочника
        super(CodeableConcept, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(CodeableConcept, self).elementProperties()
        js.extend([("system", "system", str, False, None, True),
                   ("code", "code", str, False, None, True),
                   ("display", "display", str, False, None, False),
                   ("version", "version", str, False, None, False)
                   ])
        return js
