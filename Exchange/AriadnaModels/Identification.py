# coding=utf-8
from Exchange.AriadnaModels.AbstractObject import AbstractObject
from Exchange.AriadnaModels.BirthCertificate import BirthCertificate
from Exchange.AriadnaModels.Certificate import Certificate
from Exchange.AriadnaModels.InternationalPassport import InternationalPassport
from Exchange.AriadnaModels.KzIin import KzIin
from Exchange.AriadnaModels.Passport import Passport
from Exchange.AriadnaModels.Snils import Snils


class Identification(AbstractObject):
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
                """
        super(Identification, self).__init__(jsondict)

    @classmethod
    def _with_json_dict(cls, jsondict):
        if not isinstance(jsondict, dict):
            raise Exception("Cannot use this method with anything but a JSON dictionary, got {0}".format(jsondict))
        if jsondict['documentType'] == 'SNILS':
            return Snils(jsondict)
        elif jsondict['documentType'] == 'PASSPORT':
            return Passport(jsondict)
        elif jsondict['documentType'] == 'BIRTH_CERTIFICATE':
            return BirthCertificate(jsondict)
        elif jsondict['documentType'] == 'INTERNATIONAL_PASSPORT':
            return InternationalPassport(jsondict)
        elif jsondict['documentType'] == 'CERTIFICATE':
            return Certificate(jsondict)
        elif jsondict['documentType'] == 'KZ_IIN':
            return KzIin(jsondict)
        else:
            return cls(jsondict)
