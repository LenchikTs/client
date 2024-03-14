#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/Flag) on 2016-03-29.
#  2016, SMART Health IT.


import domainresource

class Flag(domainresource.DomainResource):
    """ Key information to flag to healthcare providers.
    
    Prospective warnings of potential issues when providing care to the
    patient.
    """
    
    resource_name = "Flag"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.author = None
        """ Flag creator.
        Type `FHIRReference` referencing `Practitioner, Patient, Device` (represented as `dict` in JSON). """
        
        self.category = None
        """ Clinical, administrative, etc..
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.code = None
        """ Partially deaf, Requires easy open caps, No permanent address, etc..
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Business identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.patient = None
        """ Who is flag about?.
        Type `FHIRReference` referencing `Patient` (represented as `dict` in JSON). """
        
        self.period = None
        """ Time period when flag is active.
        Type `Period` (represented as `dict` in JSON). """
        
        self.status = None
        """ active | inactive | entered-in-error.
        Type `str`. """
        
        super(Flag, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(Flag, self).elementProperties()
        js.extend([
            ("author", "author", fhirreference.FHIRReference, False, None, False),
            ("category", "category", codeableconcept.CodeableConcept, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("patient", "patient", fhirreference.FHIRReference, False, None, True),
            ("period", "period", period.Period, False, None, False),
            ("status", "status", str, False, None, True),
        ])
        return js


import codeableconcept
import fhirreference
import identifier
import period
