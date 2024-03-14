##################################################
# file: IdentService_types.py
#
# schema types generated by "ZSI.generate.wsdl2python.WriteServiceModule"
#    /usr/bin/wsdl2py -b -l Ident.wsdl
#
##################################################

import ZSI
import ZSI.TCcompound
from ZSI.schema import LocalElementDeclaration, ElementDeclaration, TypeDefinition, GTD, GED
from ZSI.generate.pyclass import pyclass_type

##############################
# targetNamespace
# http://jaxb.dev.java.net/array
##############################

class ns1:
    targetNamespace = "http://jaxb.dev.java.net/array"

    class stringArray_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://jaxb.dev.java.net/array"
        type = (schema, "stringArray")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns1.stringArray_Def.schema
            TClist = [ZSI.TC.String(pname="item", aname="_item", minOccurs=0, maxOccurs="unbounded", nillable=True, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._item = []
                    return
            Holder.__name__ = "stringArray_Holder"
            self.pyclass = Holder

# end class ns1 (tns: http://jaxb.dev.java.net/array)

##############################
# targetNamespace
# http://identification.ws.eis.spb.ru/
##############################

class ns0:
    targetNamespace = "http://identification.ws.eis.spb.ru/"

    class getIdTArea_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "getIdTArea")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.getIdTArea_Def.schema
            TClist = [ZSI.TC.String(pname="arg0", aname="_arg0", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="arg1", aname="_arg1", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._arg0 = None
                    self._arg1 = None
                    return
            Holder.__name__ = "getIdTArea_Holder"
            self.pyclass = Holder

    class getIdTAreaResponse_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "getIdTAreaResponse")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.getIdTAreaResponse_Def.schema
            TClist = [GTD("http://jaxb.dev.java.net/array","stringArray",lazy=True)(pname="return", aname="_return", minOccurs=0, maxOccurs="unbounded", nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._return = []
                    return
            Holder.__name__ = "getIdTAreaResponse_Holder"
            self.pyclass = Holder

    class Exception_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "Exception")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.Exception_Def.schema
            TClist = [ZSI.TC.String(pname="message", aname="_message", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._message = None
                    return
            Holder.__name__ = "Exception_Holder"
            self.pyclass = Holder

    class getIdGeonimType_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "getIdGeonimType")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.getIdGeonimType_Def.schema
            TClist = [ZSI.TC.String(pname="arg0", aname="_arg0", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="arg1", aname="_arg1", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._arg0 = None
                    self._arg1 = None
                    return
            Holder.__name__ = "getIdGeonimType_Holder"
            self.pyclass = Holder

    class getIdGeonimTypeResponse_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "getIdGeonimTypeResponse")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.getIdGeonimTypeResponse_Def.schema
            TClist = [GTD("http://jaxb.dev.java.net/array","stringArray",lazy=True)(pname="return", aname="_return", minOccurs=0, maxOccurs="unbounded", nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._return = []
                    return
            Holder.__name__ = "getIdGeonimTypeResponse_Holder"
            self.pyclass = Holder

    class getIdMo_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "getIdMo")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.getIdMo_Def.schema
            TClist = [ZSI.TC.String(pname="arg0", aname="_arg0", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="arg1", aname="_arg1", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._arg0 = None
                    self._arg1 = None
                    return
            Holder.__name__ = "getIdMo_Holder"
            self.pyclass = Holder

    class getIdMoResponse_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "getIdMoResponse")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.getIdMoResponse_Def.schema
            TClist = [GTD("http://jaxb.dev.java.net/array","stringArray",lazy=True)(pname="return", aname="_return", minOccurs=0, maxOccurs="unbounded", nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._return = []
                    return
            Holder.__name__ = "getIdMoResponse_Holder"
            self.pyclass = Holder

    class getIdSmo_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "getIdSmo")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.getIdSmo_Def.schema
            TClist = [ZSI.TC.String(pname="arg0", aname="_arg0", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="arg1", aname="_arg1", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._arg0 = None
                    self._arg1 = None
                    return
            Holder.__name__ = "getIdSmo_Holder"
            self.pyclass = Holder

    class getIdSmoResponse_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "getIdSmoResponse")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.getIdSmoResponse_Def.schema
            TClist = [GTD("http://jaxb.dev.java.net/array","stringArray",lazy=True)(pname="return", aname="_return", minOccurs=0, maxOccurs="unbounded", nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._return = []
                    return
            Holder.__name__ = "getIdSmoResponse_Holder"
            self.pyclass = Holder

    class doIdentification_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "doIdentification")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.doIdentification_Def.schema
            TClist = [ZSI.TC.String(pname="arg0", aname="_arg0", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="arg1", aname="_arg1", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), GTD("http://identification.ws.eis.spb.ru/","identTO",lazy=True)(pname="arg2", aname="_arg2", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._arg0 = None
                    self._arg1 = None
                    self._arg2 = None
                    return
            Holder.__name__ = "doIdentification_Holder"
            self.pyclass = Holder

    class identTO_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "identTO")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.identTO_Def.schema
            TClist = [ZSI.TC.String(pname="idCase", aname="_idCase", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="dateBegin", aname="_dateBegin", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="dateEnd", aname="_dateEnd", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="surname", aname="_surname", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="name", aname="_name", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="secondName", aname="_secondName", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="birthday", aname="_birthday", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="docNumber", aname="_docNumber", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="polisS", aname="_polisS", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="polisN", aname="_polisN", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TCnumbers.Ilong(pname="idTArea", aname="_idTArea", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TCnumbers.Ilong(pname="idGeonimName", aname="_idGeonimName", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TCnumbers.Ilong(pname="idGeonimType", aname="_idGeonimType", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="house", aname="_house", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TCnumbers.Ilong(pname="idSmo", aname="_idSmo", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TCnumbers.Ilong(pname="numTest", aname="_numTest", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TCnumbers.Ilong(pname="agrType", aname="_agrType", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), GTD("http://identification.ws.eis.spb.ru/","attachListTO",lazy=True)(pname="attachList", aname="_attachList", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._idCase = None
                    self._dateBegin = None
                    self._dateEnd = None
                    self._surname = None
                    self._name = None
                    self._secondName = None
                    self._birthday = None
                    self._docNumber = None
                    self._polisS = None
                    self._polisN = None
                    self._idTArea = None
                    self._idGeonimName = None
                    self._idGeonimType = None
                    self._house = None
                    self._idSmo = None
                    self._numTest = None
                    self._agrType = None
                    self._attachList = None
                    return
            Holder.__name__ = "identTO_Holder"
            self.pyclass = Holder

    class attachListTO_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "attachListTO")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.attachListTO_Def.schema
            TClist = [GTD("http://identification.ws.eis.spb.ru/","attachTO",lazy=True)(pname="attachItem", aname="_attachItem", minOccurs=0, maxOccurs="unbounded", nillable=True, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._attachItem = []
                    return
            Holder.__name__ = "attachListTO_Holder"
            self.pyclass = Holder

    class attachTO_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "attachTO")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.attachTO_Def.schema
            TClist = [ZSI.TCnumbers.Iint(pname="idNet", aname="_idNet", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TCnumbers.Iint(pname="idMo", aname="_idMo", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._idNet = None
                    self._idMo = None
                    return
            Holder.__name__ = "attachTO_Holder"
            self.pyclass = Holder

    class doIdentificationResponse_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "doIdentificationResponse")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.doIdentificationResponse_Def.schema
            TClist = [GTD("http://identification.ws.eis.spb.ru/","identTO",lazy=True)(pname="return", aname="_return", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._return = None
                    return
            Holder.__name__ = "doIdentificationResponse_Holder"
            self.pyclass = Holder

    class getIdNet_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "getIdNet")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.getIdNet_Def.schema
            TClist = [ZSI.TC.String(pname="arg0", aname="_arg0", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="arg1", aname="_arg1", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._arg0 = None
                    self._arg1 = None
                    return
            Holder.__name__ = "getIdNet_Holder"
            self.pyclass = Holder

    class getIdNetResponse_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "getIdNetResponse")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.getIdNetResponse_Def.schema
            TClist = [GTD("http://jaxb.dev.java.net/array","stringArray",lazy=True)(pname="return", aname="_return", minOccurs=0, maxOccurs="unbounded", nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._return = []
                    return
            Holder.__name__ = "getIdNetResponse_Holder"
            self.pyclass = Holder

    class getIdGeonimName_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "getIdGeonimName")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.getIdGeonimName_Def.schema
            TClist = [ZSI.TC.String(pname="arg0", aname="_arg0", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="arg1", aname="_arg1", minOccurs=0, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._arg0 = None
                    self._arg1 = None
                    return
            Holder.__name__ = "getIdGeonimName_Holder"
            self.pyclass = Holder

    class getIdGeonimNameResponse_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "http://identification.ws.eis.spb.ru/"
        type = (schema, "getIdGeonimNameResponse")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.getIdGeonimNameResponse_Def.schema
            TClist = [GTD("http://jaxb.dev.java.net/array","stringArray",lazy=True)(pname="return", aname="_return", minOccurs=0, maxOccurs="unbounded", nillable=False, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._return = []
                    return
            Holder.__name__ = "getIdGeonimNameResponse_Holder"
            self.pyclass = Holder

    class Exception_Dec(ElementDeclaration):
        literal = "Exception"
        schema = "http://identification.ws.eis.spb.ru/"
        substitutionGroup = None
        def __init__(self, **kw):
            kw["pname"] = ("http://identification.ws.eis.spb.ru/","Exception")
            kw["aname"] = "_Exception"
            if ns0.Exception_Def not in ns0.Exception_Dec.__bases__:
                bases = list(ns0.Exception_Dec.__bases__)
                bases.insert(0, ns0.Exception_Def)
                ns0.Exception_Dec.__bases__ = tuple(bases)

            ns0.Exception_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "Exception_Dec_Holder"

    class doIdentification_Dec(ElementDeclaration):
        literal = "doIdentification"
        schema = "http://identification.ws.eis.spb.ru/"
        substitutionGroup = None
        def __init__(self, **kw):
            kw["pname"] = ("http://identification.ws.eis.spb.ru/","doIdentification")
            kw["aname"] = "_doIdentification"
            if ns0.doIdentification_Def not in ns0.doIdentification_Dec.__bases__:
                bases = list(ns0.doIdentification_Dec.__bases__)
                bases.insert(0, ns0.doIdentification_Def)
                ns0.doIdentification_Dec.__bases__ = tuple(bases)

            ns0.doIdentification_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "doIdentification_Dec_Holder"

    class doIdentificationResponse_Dec(ElementDeclaration):
        literal = "doIdentificationResponse"
        schema = "http://identification.ws.eis.spb.ru/"
        substitutionGroup = None
        def __init__(self, **kw):
            kw["pname"] = ("http://identification.ws.eis.spb.ru/","doIdentificationResponse")
            kw["aname"] = "_doIdentificationResponse"
            if ns0.doIdentificationResponse_Def not in ns0.doIdentificationResponse_Dec.__bases__:
                bases = list(ns0.doIdentificationResponse_Dec.__bases__)
                bases.insert(0, ns0.doIdentificationResponse_Def)
                ns0.doIdentificationResponse_Dec.__bases__ = tuple(bases)

            ns0.doIdentificationResponse_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "doIdentificationResponse_Dec_Holder"

    class getIdGeonimName_Dec(ElementDeclaration):
        literal = "getIdGeonimName"
        schema = "http://identification.ws.eis.spb.ru/"
        substitutionGroup = None
        def __init__(self, **kw):
            kw["pname"] = ("http://identification.ws.eis.spb.ru/","getIdGeonimName")
            kw["aname"] = "_getIdGeonimName"
            if ns0.getIdGeonimName_Def not in ns0.getIdGeonimName_Dec.__bases__:
                bases = list(ns0.getIdGeonimName_Dec.__bases__)
                bases.insert(0, ns0.getIdGeonimName_Def)
                ns0.getIdGeonimName_Dec.__bases__ = tuple(bases)

            ns0.getIdGeonimName_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "getIdGeonimName_Dec_Holder"

    class getIdGeonimNameResponse_Dec(ElementDeclaration):
        literal = "getIdGeonimNameResponse"
        schema = "http://identification.ws.eis.spb.ru/"
        substitutionGroup = None
        def __init__(self, **kw):
            kw["pname"] = ("http://identification.ws.eis.spb.ru/","getIdGeonimNameResponse")
            kw["aname"] = "_getIdGeonimNameResponse"
            if ns0.getIdGeonimNameResponse_Def not in ns0.getIdGeonimNameResponse_Dec.__bases__:
                bases = list(ns0.getIdGeonimNameResponse_Dec.__bases__)
                bases.insert(0, ns0.getIdGeonimNameResponse_Def)
                ns0.getIdGeonimNameResponse_Dec.__bases__ = tuple(bases)

            ns0.getIdGeonimNameResponse_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "getIdGeonimNameResponse_Dec_Holder"

    class getIdGeonimType_Dec(ElementDeclaration):
        literal = "getIdGeonimType"
        schema = "http://identification.ws.eis.spb.ru/"
        substitutionGroup = None
        def __init__(self, **kw):
            kw["pname"] = ("http://identification.ws.eis.spb.ru/","getIdGeonimType")
            kw["aname"] = "_getIdGeonimType"
            if ns0.getIdGeonimType_Def not in ns0.getIdGeonimType_Dec.__bases__:
                bases = list(ns0.getIdGeonimType_Dec.__bases__)
                bases.insert(0, ns0.getIdGeonimType_Def)
                ns0.getIdGeonimType_Dec.__bases__ = tuple(bases)

            ns0.getIdGeonimType_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "getIdGeonimType_Dec_Holder"

    class getIdGeonimTypeResponse_Dec(ElementDeclaration):
        literal = "getIdGeonimTypeResponse"
        schema = "http://identification.ws.eis.spb.ru/"
        substitutionGroup = None
        def __init__(self, **kw):
            kw["pname"] = ("http://identification.ws.eis.spb.ru/","getIdGeonimTypeResponse")
            kw["aname"] = "_getIdGeonimTypeResponse"
            if ns0.getIdGeonimTypeResponse_Def not in ns0.getIdGeonimTypeResponse_Dec.__bases__:
                bases = list(ns0.getIdGeonimTypeResponse_Dec.__bases__)
                bases.insert(0, ns0.getIdGeonimTypeResponse_Def)
                ns0.getIdGeonimTypeResponse_Dec.__bases__ = tuple(bases)

            ns0.getIdGeonimTypeResponse_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "getIdGeonimTypeResponse_Dec_Holder"

    class getIdMo_Dec(ElementDeclaration):
        literal = "getIdMo"
        schema = "http://identification.ws.eis.spb.ru/"
        substitutionGroup = None
        def __init__(self, **kw):
            kw["pname"] = ("http://identification.ws.eis.spb.ru/","getIdMo")
            kw["aname"] = "_getIdMo"
            if ns0.getIdMo_Def not in ns0.getIdMo_Dec.__bases__:
                bases = list(ns0.getIdMo_Dec.__bases__)
                bases.insert(0, ns0.getIdMo_Def)
                ns0.getIdMo_Dec.__bases__ = tuple(bases)

            ns0.getIdMo_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "getIdMo_Dec_Holder"

    class getIdMoResponse_Dec(ElementDeclaration):
        literal = "getIdMoResponse"
        schema = "http://identification.ws.eis.spb.ru/"
        substitutionGroup = None
        def __init__(self, **kw):
            kw["pname"] = ("http://identification.ws.eis.spb.ru/","getIdMoResponse")
            kw["aname"] = "_getIdMoResponse"
            if ns0.getIdMoResponse_Def not in ns0.getIdMoResponse_Dec.__bases__:
                bases = list(ns0.getIdMoResponse_Dec.__bases__)
                bases.insert(0, ns0.getIdMoResponse_Def)
                ns0.getIdMoResponse_Dec.__bases__ = tuple(bases)

            ns0.getIdMoResponse_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "getIdMoResponse_Dec_Holder"

    class getIdNet_Dec(ElementDeclaration):
        literal = "getIdNet"
        schema = "http://identification.ws.eis.spb.ru/"
        substitutionGroup = None
        def __init__(self, **kw):
            kw["pname"] = ("http://identification.ws.eis.spb.ru/","getIdNet")
            kw["aname"] = "_getIdNet"
            if ns0.getIdNet_Def not in ns0.getIdNet_Dec.__bases__:
                bases = list(ns0.getIdNet_Dec.__bases__)
                bases.insert(0, ns0.getIdNet_Def)
                ns0.getIdNet_Dec.__bases__ = tuple(bases)

            ns0.getIdNet_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "getIdNet_Dec_Holder"

    class getIdNetResponse_Dec(ElementDeclaration):
        literal = "getIdNetResponse"
        schema = "http://identification.ws.eis.spb.ru/"
        substitutionGroup = None
        def __init__(self, **kw):
            kw["pname"] = ("http://identification.ws.eis.spb.ru/","getIdNetResponse")
            kw["aname"] = "_getIdNetResponse"
            if ns0.getIdNetResponse_Def not in ns0.getIdNetResponse_Dec.__bases__:
                bases = list(ns0.getIdNetResponse_Dec.__bases__)
                bases.insert(0, ns0.getIdNetResponse_Def)
                ns0.getIdNetResponse_Dec.__bases__ = tuple(bases)

            ns0.getIdNetResponse_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "getIdNetResponse_Dec_Holder"

    class getIdSmo_Dec(ElementDeclaration):
        literal = "getIdSmo"
        schema = "http://identification.ws.eis.spb.ru/"
        substitutionGroup = None
        def __init__(self, **kw):
            kw["pname"] = ("http://identification.ws.eis.spb.ru/","getIdSmo")
            kw["aname"] = "_getIdSmo"
            if ns0.getIdSmo_Def not in ns0.getIdSmo_Dec.__bases__:
                bases = list(ns0.getIdSmo_Dec.__bases__)
                bases.insert(0, ns0.getIdSmo_Def)
                ns0.getIdSmo_Dec.__bases__ = tuple(bases)

            ns0.getIdSmo_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "getIdSmo_Dec_Holder"

    class getIdSmoResponse_Dec(ElementDeclaration):
        literal = "getIdSmoResponse"
        schema = "http://identification.ws.eis.spb.ru/"
        substitutionGroup = None
        def __init__(self, **kw):
            kw["pname"] = ("http://identification.ws.eis.spb.ru/","getIdSmoResponse")
            kw["aname"] = "_getIdSmoResponse"
            if ns0.getIdSmoResponse_Def not in ns0.getIdSmoResponse_Dec.__bases__:
                bases = list(ns0.getIdSmoResponse_Dec.__bases__)
                bases.insert(0, ns0.getIdSmoResponse_Def)
                ns0.getIdSmoResponse_Dec.__bases__ = tuple(bases)

            ns0.getIdSmoResponse_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "getIdSmoResponse_Dec_Holder"

    class getIdTArea_Dec(ElementDeclaration):
        literal = "getIdTArea"
        schema = "http://identification.ws.eis.spb.ru/"
        substitutionGroup = None
        def __init__(self, **kw):
            kw["pname"] = ("http://identification.ws.eis.spb.ru/","getIdTArea")
            kw["aname"] = "_getIdTArea"
            if ns0.getIdTArea_Def not in ns0.getIdTArea_Dec.__bases__:
                bases = list(ns0.getIdTArea_Dec.__bases__)
                bases.insert(0, ns0.getIdTArea_Def)
                ns0.getIdTArea_Dec.__bases__ = tuple(bases)

            ns0.getIdTArea_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "getIdTArea_Dec_Holder"

    class getIdTAreaResponse_Dec(ElementDeclaration):
        literal = "getIdTAreaResponse"
        schema = "http://identification.ws.eis.spb.ru/"
        substitutionGroup = None
        def __init__(self, **kw):
            kw["pname"] = ("http://identification.ws.eis.spb.ru/","getIdTAreaResponse")
            kw["aname"] = "_getIdTAreaResponse"
            if ns0.getIdTAreaResponse_Def not in ns0.getIdTAreaResponse_Dec.__bases__:
                bases = list(ns0.getIdTAreaResponse_Dec.__bases__)
                bases.insert(0, ns0.getIdTAreaResponse_Def)
                ns0.getIdTAreaResponse_Dec.__bases__ = tuple(bases)

            ns0.getIdTAreaResponse_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "getIdTAreaResponse_Dec_Holder"

# end class ns0 (tns: http://identification.ws.eis.spb.ru/)
