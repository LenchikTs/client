# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class Norm(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.min = None  # Double Необязательно Минимальное значение референтного интервала
        self.max = None  # Double Необязательно Максимальное значение референтного интервала
        self.text = ''  # String Обязательно Текстовая форма референтного интервала
        super(Norm, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Norm, self).elementProperties()
        js.extend([("min", "min", float, False, None, False),
                   ("max", "max", float, False, None, False),
                   ("text", "text", str, False, None, True), ])
        return js
