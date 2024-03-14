# -*- coding: UTF-8 -*-

from v135_generated import ( CreateFromDocument as createFromXml,
                             documents          as _documents,
                             accept             as _accept,
                             health_care        as _health_care,
                             move_destruction   as _move_destruction,
                             move_place         as _move_place,
                             move_return        as _move_return,
                             posting            as _posting,
                             receive_order      as _receive_order,
                             refusal_receiver   as _refusal_receiver,
                             unit_unpack        as _unit_unpack,

#                             query_kiz_info     as QueryKizInfo,
                           )

version = '1.35'

def Documents(**kwargs):
    kwargs.setdefault('version', version)
    return _documents(**kwargs)


class Accept(_accept):
    # 701-accept: Регистрация в ИС МДЛП подтверждения (акцептования) сведений
    def __init__(self, *args, **kwargs):
        _accept.__init__(self, *args, **kwargs)
        self.action_id = self.action_id # обход ошибки b PyXB 1.2.4: объект знает про дефолтное значение, но по своей иницитиве не подставляет. Проявляется при сохранении как xml


class HealthCare(_health_care):
    # 531-health_care: Регистрация в ИС МДЛП сведений о выдаче лекарственного препарата для оказания медицинской помощи
    def __init__(self, *args, **kwargs):
        _health_care.__init__(self, *args, **kwargs)
        self.action_id = self.action_id # обход ошибки b PyXB 1.2.4: объект знает про дефолтное значение, но по своей иницитиве не подставляет. Проявляется при сохранении как xml


class MoveDestruction(_move_destruction):
    # 541-move_destruction: Регистрация в ИС МДЛП сведений о передаче лекарственных препаратов на уничтожение
    def __init__(self, *args, **kwargs):
        _move_destruction.__init__(self, *args, **kwargs)
        self.action_id = self.action_id # обход ошибки b PyXB 1.2.4: объект знает про дефолтное значение, но по своей иницитиве не подставляет. Проявляется при сохранении как xml


class MovePlace(_move_place):
    # 431-move_place: Регистрация в ИС МДЛП сведений о перемещении лекарственных препаратов между различными адресами осуществления деятельности
    def __init__(self, *args, **kwargs):
        _move_place.__init__(self, *args, **kwargs)
        self.action_id = self.action_id # обход ошибки b PyXB 1.2.4: объект знает про дефолтное значение, но по своей иницитиве не подставляет. Проявляется при сохранении как xml


class MoveReturn(_move_return):
    # 417-move_return: Регистрация в ИС МДЛП сведений о возврате приостановленных лекарственных препаратов
    def __init__(self, *args, **kwargs):
        _move_return.__init__(self, *args, **kwargs)
        self.action_id = self.action_id # обход ошибки b PyXB 1.2.4: объект знает про дефолтное значение, но по своей иницитиве не подставляет. Проявляется при сохранении как xml


class Posting(_posting):
    # 702-posting: Регистрация в ИС МДЛП сведений об оприходовании
    def __init__(self, *args, **kwargs):
        _posting.__init__(self, *args, **kwargs)
        self.action_id = self.action_id # обход ошибки b PyXB 1.2.4: объект знает про дефолтное значение, но по своей иницитиве не подставляет. Проявляется при сохранении как xml


class ReceiveOrder(_receive_order):
    # 416-receive_order: Регистрация ИС МДЛП сведений о приемке лекарственных препаратов на склад получателя
    def __init__(self, *args, **kwargs):
        _receive_order.__init__(self, *args, **kwargs)
        self.action_id = self.action_id # обход ошибки b PyXB 1.2.4: объект знает про дефолтное значение, но по своей иницитиве не подставляет. Проявляется при сохранении как xml


class RefusalReceiver(_refusal_receiver):
    # 252-refusal_receiver: Регистрация в ИС МДЛП сведений об отказе получателя от приемки лекарственных препаратов
    def __init__(self, *args, **kwargs):
        _refusal_receiver.__init__(self, *args, **kwargs)
        self.action_id = self.action_id # обход ошибки b PyXB 1.2.4: объект знает про дефолтное значение, но по своей иницитиве не подставляет. Проявляется при сохранении как xml


class UnitUnpack(_unit_unpack):
    # 912-unit_unpack: Регистрация в ИС МДЛП сведений о расформировании третичной (заводской, транспортной) упаковки лекарственных препаратов
    def __init__(self, *args, **kwargs):
        _unit_unpack.__init__(self, *args, **kwargs)
        self.action_id = self.action_id # обход ошибки b PyXB 1.2.4: объект знает про дефолтное значение, но по своей иницитиве не подставляет. Проявляется при сохранении как xml

