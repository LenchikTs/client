# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject
from Exchange.AriadnaModels.Physician import Physician


class ResourcePhysician(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.resource = None  # Object Обязательно Передается объект типа врача
        self.resourceType = 'PhysicianType'  # String Обязательно Всегда PhysicianType
        self.uri = None  # String Обязательно Uuid ссылка на врача заверившего результат
        super(ResourcePhysician, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(ResourcePhysician, self).elementProperties()
        js.extend([("resource", "resource", Physician, False, None, True),
                   ("resourceType", "resourceType", str, False, None, True),
                   ("uri", "uri", str, False, None, True)
                   ])
        return js
