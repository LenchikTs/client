#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/Supply) on 2016-03-29.
#  2016, SMART Health IT.


import domainresource

class Supply(domainresource.DomainResource):
    """ A supply -  request and provision.
    
    A supply - a  request for something, and provision of what is supplied.
    """
    
    resource_name = "Supply"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.dispense = None
        """ Supply details.
        List of `SupplyDispense` items (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Unique identifier.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.kind = None
        """ The kind of supply (central, non-stock, etc).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.orderedItem = None
        """ Medication, Substance, or Device requested to be supplied.
        Type `FHIRReference` referencing `Medication, Substance, Device` (represented as `dict` in JSON). """
        
        self.patient = None
        """ Patient for whom the item is supplied.
        Type `FHIRReference` referencing `Patient` (represented as `dict` in JSON). """
        
        self.status = None
        """ requested | dispensed | received | failed | cancelled.
        Type `str`. """
        
        super(Supply, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(Supply, self).elementProperties()
        js.extend([
            ("dispense", "dispense", SupplyDispense, True, None, False),
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("kind", "kind", codeableconcept.CodeableConcept, False, None, False),
            ("orderedItem", "orderedItem", fhirreference.FHIRReference, False, None, False),
            ("patient", "patient", fhirreference.FHIRReference, False, None, False),
            ("status", "status", str, False, None, False),
        ])
        return js


import backboneelement

class SupplyDispense(backboneelement.BackboneElement):
    """ Supply details.
    
    Indicates the details of the dispense event such as the days supply and
    quantity of a supply dispensed.
    """
    
    resource_name = "SupplyDispense"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.destination = None
        """ Where the Supply was sent.
        Type `FHIRReference` referencing `Location` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ External identifier.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.quantity = None
        """ Amount dispensed.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.receiver = None
        """ Who collected the Supply.
        List of `FHIRReference` items referencing `Practitioner` (represented as `dict` in JSON). """
        
        self.status = None
        """ in-progress | dispensed | abandoned.
        Type `str`. """
        
        self.suppliedItem = None
        """ Medication, Substance, or Device supplied.
        Type `FHIRReference` referencing `Medication, Substance, Device` (represented as `dict` in JSON). """
        
        self.supplier = None
        """ Dispenser.
        Type `FHIRReference` referencing `Practitioner` (represented as `dict` in JSON). """
        
        self.type = None
        """ Category of dispense event.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.whenHandedOver = None
        """ Handover time.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.whenPrepared = None
        """ Dispensing time.
        Type `Period` (represented as `dict` in JSON). """
        
        super(SupplyDispense, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(SupplyDispense, self).elementProperties()
        js.extend([
            ("destination", "destination", fhirreference.FHIRReference, False, None, False),
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("receiver", "receiver", fhirreference.FHIRReference, True, None, False),
            ("status", "status", str, False, None, False),
            ("suppliedItem", "suppliedItem", fhirreference.FHIRReference, False, None, False),
            ("supplier", "supplier", fhirreference.FHIRReference, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("whenHandedOver", "whenHandedOver", fhirdate.FHIRDate, False, None, False),
            ("whenPrepared", "whenPrepared", period.Period, False, None, False),
        ])
        return js


import codeableconcept
import fhirdate
import fhirreference
import identifier
import period
import quantity
