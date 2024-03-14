# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject
from Exchange.AriadnaModels.CodeableConcept import CodeableConcept
from Exchange.AriadnaModels.Identification import Identification


class Physician(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.id = ''  # String Обязательно Врач, ID по справочнику
        self.regCode = ''  # String Обязательно Регистрационный код
        self.givenName = ''  # String Обязательно Имя
        self.familyName = ''  # String Обязательно Фамилия
        self.middleName = ''  # String Необязательно Отчество
        self.adress = ''  # String Обязательно Адрес
        self.email = ''  # String Обязательно E-mail
        self.phone = ''  # String Обязательно Телефон
        self.cellPhone = ''  # String Обязательно Телефон сотовый
        self.identifications = []  # Array Object Обязательно Массив содержащий в себе данные удостоверяющие
        # личность врача(объекты SNILS,PASSPORT, INTERNATIONAL_PASSPORT, BIRTH_CERTIFICATE, CERTIFICATE)
        self.role = None  # Object Необязательно Объект содержащий в себе информацию о роли врача
        self.speciality = []  # Array Object Обязательно Массив содержащий в себе информацию о специальности врача
        super(Physician, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Physician, self).elementProperties()
        js.extend([("id", "id", str, False, None, True),
                   ("regCode", "regCode", str, False, None, True),
                   ("givenName", "givenName", str, False, None, True),
                   ("familyName", "familyName", str, False, None, True),
                   ("middleName", "middleName", str, False, None, False),
                   ("adress", "adress", str, False, None, True),
                   ("email", "email", str, False, None, True),
                   ("phone", "phone", str, False, None, True),
                   ("cellPhone", "cellPhone", str, False, None, True),
                   ("identifications", "identifications", Identification, True, None, False),
                   ("role", "role", CodeableConcept, False, None, False),
                   ("speciality", "speciality", CodeableConcept, True, None, True)
                   ])
        return js
