#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/OrderResponse) on 2016-03-29.
#  2016, SMART Health IT.


import domainresource

class OrderResponse(domainresource.DomainResource):
    """ A response to an order.
    """
    
    resource_name = "OrderResponse"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.authorityCodeableConcept = None
        """ If required by policy.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.authorityReference = None
        """ If required by policy.
        Type `FHIRReference` referencing `Resource` (represented as `dict` in JSON). """
        
        self.date = None
        """ When the response was made.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.description = None
        """ Additional description of the response.
        Type `str`. """
        
        self.fulfillment = None
        """ Details of the outcome of performing the order.
        List of `FHIRReference` items referencing `Resource` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Identifiers assigned to this order by the orderer or by the
        receiver.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.orderStatus = None
        """ pending | review | rejected | error | accepted | cancelled |
        replaced | aborted | completed.
        Type `str`. """
        
        self.request = None
        """ The order that this is a response to.
        Type `FHIRReference` referencing `Order` (represented as `dict` in JSON). """
        
        self.who = None
        """ Who made the response.
        Type `FHIRReference` referencing `Practitioner, Organization, Device` (represented as `dict` in JSON). """
        
        super(OrderResponse, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(OrderResponse, self).elementProperties()
        js.extend([
            ("authorityCodeableConcept", "authorityCodeableConcept", codeableconcept.CodeableConcept, False, "authority", False),
            ("authorityReference", "authorityReference", fhirreference.FHIRReference, False, "authority", False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("description", "description", str, False, None, False),
            ("fulfillment", "fulfillment", fhirreference.FHIRReference, True, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("orderStatus", "orderStatus", str, False, None, True),
            ("request", "request", fhirreference.FHIRReference, False, None, True),
            ("who", "who", fhirreference.FHIRReference, False, None, False),
        ])
        return js


import codeableconcept
import fhirdate
import fhirreference
import identifier
