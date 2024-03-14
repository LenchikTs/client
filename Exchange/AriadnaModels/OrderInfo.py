# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject
from Exchange.AriadnaModels.Category import Category
from Exchange.AriadnaModels.Service import Service


class OrderInfo(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.service = Service()  # Object Обязательно Услуга
        self.method = ''  # String Обязательно Метод
        self.completed = None  # Boolean Необязательно Услуга выполнена
        self.category = Category()  # Object Обязательно Категория
        self.workplaceID = ''  # String Обязательно Рабочее место
        super(OrderInfo, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(OrderInfo, self).elementProperties()
        js.extend([("service", "service", Service, False, None, True),
                   ("method", "method", str, False, None, True),
                   ("completed", "completed", bool, False, None, False),
                   ("category", "category", Category, False, None, True),
                   ("workplaceID", "workplaceID", str, False, None, True), ])
        return js
