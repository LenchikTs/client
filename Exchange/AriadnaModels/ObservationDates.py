# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class ObservationDates(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
                """
        self.report = None  # String Необязательно Дата выдачи отчета
        self.finish = None  # String Необязательно Дата завершения исследований
        super(ObservationDates, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(ObservationDates, self).elementProperties()
        js.extend([("report", "report", str, False, None, False),
                   ("finish", "finish", str, False, None, False), ])
        return js
