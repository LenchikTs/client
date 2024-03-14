# coding=utf-8
from Exchange.AriadnaModels.ContactPoint import ContactPoint


class Cellular(ContactPoint):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.contactType = 'CELLULAR'  # String Обязательно Тип контактной информации
        self.cellular = ''  # String Обязательно Номер мобильного телефона
        super(Cellular, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Cellular, self).elementProperties()
        js.extend([("contactType", "contactType", str, False, None, True),
                   ("cellular", "cellular", str, False, None, True)])
        return js
