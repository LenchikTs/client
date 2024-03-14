# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject


class ContactPoint(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
                """
        super(ContactPoint, self).__init__(jsondict)
