# -*- coding: utf-8 -*-
from Exchange import AttachService

def sendSanAviacInformation(sanAviacInfo, url = None):
    return AttachService.callService('sendSanAviacInformation', {'sanAviacInfo': sanAviacInfo}, url)
