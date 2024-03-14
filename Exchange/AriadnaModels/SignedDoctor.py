# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class SignedDoctor(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.birthDate = None  # String Необязательно Дата рождения подписавшего документ врача
        self.name = None  # String Необязательно Имя подписавшего документ врача
        self.middleName = None  # String Необязательно Отчество подписавшего документ врача
        self.surname = None  # String Необязательно Фамилия подписавшего документ врача
        self.role = None  # String Необязательно Роль подписавшего документ врача
        self.speciality = None  # String Необязательно Специальность подписавшего документ врача
        self.position = None  # String Необязательно Должность подписавшего документ врача
        self.snils = None  # String Необязательно Снилс подписавшего документ врача
        super(SignedDoctor, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(SignedDoctor, self).elementProperties()
        js.extend([("birthDate", "birthDate", str, False, None, False),
                   ("name", "name", str, False, None, False),
                   ("middleName", "middleName", str, False, None, False),
                   ("surname", "surname", str, False, None, False),
                   ("role", "role", str, False, None, False),
                   ("speciality", "speciality", str, False, None, False),
                   ("position", "position", str, False, None, False),
                   ("snils", "snils", str, False, None, False)
                   ])
        return js
