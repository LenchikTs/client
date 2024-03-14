# -*- coding: utf-8 -*-

# Заголовок будет потом,
# сейчас это "превью"

# Назначение обменных документов

class CMdplExchangePurpose:

    # iido: Incoming Invoice - Direct Order
    iidoMoveOrderNotification  = 'iido.in.601'
    iidoAccept                 = 'iido.out.701'
    iidoRefusalReceiver        = 'iido.out.252'
    iidoUnitUnpack             = 'iido.out.912'

#    iidoOutPrefix = 'iido.out.'
    iiroReceiveOrder           = 'iiro.out.416'
    iiroWaitAcceptNotification = 'iiro.wait.607'
    iiroAcceptNotification     = 'iiro.in.607'
    iiroUnitUnpack             = 'iiro.out.912'

    iinmPosting                = 'iinm.out.702'
    iinmUnitUnpack             = 'iinm.out.912'
#    iinmWaitPostingNotification= 'iinm.wait.627'



    # intInv: internal invoice
    iimMovePlace               = 'iim.out.431'
    iiwdHealthCare             = 'iiwd.out.531'
#    intInvWithdrawalByDocument =
    iiwrKzkmHealthCare         = 'iiwr.in.10531'
#    intInvWithdrawalByRegisrar = 'iiwr.in.10531'

    mapMdlpActionToName = {
                            '10531': '10531-skzkm_health_care',
                            '252': '252-refusal_receiver',
                            '416': '416-receive_order',
                            '431': '431-move_place',
                            '531': '531-health_care',
                            '601': '601-move_order_notification',
                            '607': '607-accept_notification',
#                            '627': '627-posting_notification',
                            '701': '701-accept',
                            '702': '702-posting',
                            '912': '912-unit_unpack',
                          }

    @classmethod
    def docType(cls, purpose):
        context, direction, mdlpAction = purpose.split('.', 2)
        docTypeName = cls.mapMdlpActionToName.get(mdlpAction, mdlpAction)
        return docTypeName


    @classmethod
    def text(cls, purpose):
        context, direction, mdlpAction = purpose.split('.', 2)
        docTypeName = cls.mapMdlpActionToName.get(mdlpAction, mdlpAction)
        if direction == 'in':
            return u'получение %s' % docTypeName
        elif direction == 'out':
            return u'передача %s' % docTypeName
        elif direction == 'wait':
            return u'ожидание %s' % docTypeName
        else:
            return purpose

    @classmethod
    def isWait(cls, purpose):
        context, direction, mdlpAction = purpose.split('.', 2)
        return direction == 'wait'


