# coding=utf-8
from Exchange.AriadnaModels.ContactPoint import ContactPoint


class Email(ContactPoint):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.contactType = 'EMAIL'  # String Обязательно Тип контактной информации
        self.email = ''  # String Обязательно Адрес электронной почты
        super(Email, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Email, self).elementProperties()
        js.extend([("contactType", "contactType", str, False, None, True),
                   ("email", "email", str, False, None, True)])
        return js
