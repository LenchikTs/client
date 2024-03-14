# coding=utf-8
from Exchange.AriadnaModels.ContactPoint import ContactPoint


class Phone(ContactPoint):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.contactType = 'PHONE'  # String Обязательно Тип контактной информации
        self.phone = ''  # String Обязательно Номер мобильного телефона
        super(Phone, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Phone, self).elementProperties()
        js.extend([("contactType", "contactType", str, False, None, True),
                   ("phone", "phone", str, False, None, True)])
        return js
