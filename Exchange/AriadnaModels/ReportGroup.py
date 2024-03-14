# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject
from Exchange.AriadnaModels.Result import Result


class ReportGroup(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.title = ''  # String Обязательно Заголовки групп результатов
        self.reportSeq = None  # Integer Необязательно Порядок в отчете
        self.finishDate = ''  # String Обязательно Дата завершения исследований
        self.results = []  # Array Object Обязательно Список результатов
        super(ReportGroup, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(ReportGroup, self).elementProperties()
        js.extend([("title", "title", str, False, None, True),
                   ("reportSeq", "reportSeq", int, False, None, False),
                   ("finishDate", "finishDate", str, False, None, True),
                   ("results", "results", Result, True, None, True), ])
        return js
