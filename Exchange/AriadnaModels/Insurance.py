# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject
from Exchange.AriadnaModels.Company import Company


class Insurance(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
                """
        self.policyID = ''  # String Обязательно Страховой полис
        self.policyCode = ''  # String Обязательно Серия и номер страхового полиса
        self.statusID = ''  # String Обязательно Страховой статус, ID
        self.statusCode = ''  # String Обязательно Страховой статус, код
        self.status = ''  # String Обязательно Страховой статус
        self.typCode = None  # String Необязательно Шифр в ЛИС включает в себя информацию об источнике финансирования, компании, договоре
        self.company = None  # Object Необязательно Страховая компания
        super(Insurance, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Insurance, self).elementProperties()
        js.extend(
            [("policyID", "policyID", str, False, None, True),
             ("policyCode", "policyCode", str, False, None, True),
             ("statusID", "statusID", str, False, None, True),
             ("statusCode", "statusCode", str, False, None, True),
             ("status", "status", str, False, None, True),
             ("typCode", "typCode", str, False, None, False),
             ("company", "company", Company, False, None, False), ])
        return js
