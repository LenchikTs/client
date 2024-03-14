# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class Equipment(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.serialNumber = ''  # String Необязательно серийный номер лабораторного оборудования
        self.inventoryNumber = ''  # String Необязательно инвентарный номер лабораторного оборудования
        self.workplaceId = 0  # Long Необязательно Идентификатор рабочего места
        super(Equipment, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Equipment, self).elementProperties()
        js.extend([("serialNumber", "serialNumber", str, False, None, False),
                   ("inventoryNumber", "inventoryNumber", str, False, None, False),
                   ("workplaceId", "workplaceId", int, False, None, False)
                   ])
        return js
