# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class Measurement(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.id = ''  # String Обязательно ID измерения в пределах данного отчета
        self.name = ''  # String Обязательно Наименование измеренияя
        self.shortName = ''  # String Обязательно Наименование измерения краткое
        self.code = ''  # String Обязательно Код измерения
        super(Measurement, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Measurement, self).elementProperties()
        js.extend([("id", "id", str, False, None, True),
                   ("name", "name", str, False, None, True),
                   ("shortName", "shortName", str, False, None, True),
                   ("code", "code", str, False, None, True), ])
        return js
