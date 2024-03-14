# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class Antibiotic(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties."""
        self.code = ''  # String Обязательно Код антибиотика
        self.name = ''  # String Обязательно Название антибиотика
        self.sir = 0  # Integer Обязательно SIR (чувствительность)
        # 1 - S — бактерия восприимчива к данному антибиотику, его можно использовать для лечения;
        # 2 - I — промежуточный вариант, микроб умеренно чувствителен, препарат можно использовать для лечения, если другого лекарства нет или у человека имеется его непереносимость;
        # 3 - R — микроб абсолютно устойчив к антибиотику, препарат для лечения не подходит.

        self.dia = 0  # Integer Обязательно DIA (диаметр зон задержки роста)
        self.mic = ''  # String Обязательно MIC (Минимальная ингибирующая концентрация)
        self.sortCode = 0  # Integer Обязательно Поле для сортировки
        super(Antibiotic, self).__init__(jsondict)

    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        js = super(Antibiotic, self).elementProperties()
        js.extend([("code", "code", str, False, None, True),
                   ("name", "name", str, False, None, True),
                   ("sir", "sir", int, False, None, True),
                   ("dia", "dia", int, False, None, True),
                   ("mic", "mic", str, False, None, True),
                   ("sortCode", "sortCode", int, False, None, True), ])
        return js
