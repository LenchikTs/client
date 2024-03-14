# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject
from Exchange.AriadnaModels.ExternalIdentification import ExternalIdentification
from Exchange.AriadnaModels.Physician import Physician


class OrderingInstitution(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.id = ''  # String Обязательно Организация, ID в МИС
        self.localName = ''  # String Обязательно Наименование краткое
        self.fullName = ''  # String Обязательно Наименование полное
        self.code = ''  # String Обязательно Регистрационный код
        self.phone = ''  # String Обязательно Телефон
        self.cellPhone = ''  # String Обязательно Телефон сотовый
        self.email = ''  # String Обязательно E-mail
        self.department = ''  # String Обязательно Подразделение (отделение)
        self.departmentCode = ''  # String Необязательно Код отделения
        self.icmid = ''  # String Обязательно icmid заказчика
        self.physician = None  # Object Необязательно Направивший врач
        self.externalIdentification = ''  # Array Object Обязательно Внешние идентификаторы
        super(OrderingInstitution, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(OrderingInstitution, self).elementProperties()
        js.extend([("id", "id", str, False, None, True),
                   ("localName", "localName", str, False, None, True),
                   ("fullName", "fullName", str, False, None, True),
                   ("code", "code", str, False, None, True),
                   ("phone", "phone", str, False, None, True),
                   ("cellPhone", "cellPhone", str, False, None, True),
                   ("email", "email", str, False, None, True),
                   ("department", "department", str, False, None, True),
                   ("departmentCode", "departmentCode", str, False, None, True),
                   ("icmid", "icmid", str, False, None, True),
                   ("physician", "physician", Physician, False, None, False),
                   ("externalIdentification", "externalIdentification", ExternalIdentification, True, None, True), ])
        return js
