#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/ProcedureRequest) on 2016-03-29.
#  2016, SMART Health IT.


import domainresource

class ProcedureRequest(domainresource.DomainResource):
    """ A request for a procedure to be performed.
    
    A request for a procedure to be performed. May be a proposal or an order.
    """
    
    resource_name = "ProcedureRequest"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.asNeededBoolean = None
        """ PRN.
        Type `bool`. """
        
        self.asNeededCodeableConcept = None
        """ PRN.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.bodySite = None
        """ Target body sites.
        List of `ProcedureRequestBodySite` items (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Encounter.
        Type `FHIRReference` referencing `Encounter` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.indication = None
        """ Indication.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.notes = None
        """ Notes.
        List of `str` items. """
        
        self.orderedOn = None
        """ When Requested.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.orderer = None
        """ Ordering Party.
        Type `FHIRReference` referencing `Practitioner, Patient, RelatedPerson, Device` (represented as `dict` in JSON). """
        
        self.performer = None
        """ Performer.
        Type `FHIRReference` referencing `Practitioner, Organization, Patient, RelatedPerson` (represented as `dict` in JSON). """
        
        self.priority = None
        """ routine | urgent | stat | asap.
        Type `str`. """
        
        self.status = None
        """ proposed | draft | requested | received | accepted | in-progress |
        completed | suspended | rejected | aborted.
        Type `str`. """
        
        self.subject = None
        """ Subject.
        Type `FHIRReference` referencing `Patient` (represented as `dict` in JSON). """
        
        self.timingDateTime = None
        """ Procedure timing schedule.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.timingPeriod = None
        """ Procedure timing schedule.
        Type `Period` (represented as `dict` in JSON). """
        
        self.timingTiming = None
        """ Procedure timing schedule.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.type = None
        """ Procedure Type.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(ProcedureRequest, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ProcedureRequest, self).elementProperties()
        js.extend([
            ("asNeededBoolean", "asNeededBoolean", bool, False, "asNeeded", False),
            ("asNeededCodeableConcept", "asNeededCodeableConcept", codeableconcept.CodeableConcept, False, "asNeeded", False),
            ("bodySite", "bodySite", ProcedureRequestBodySite, True, None, False),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("indication", "indication", codeableconcept.CodeableConcept, True, None, False),
            ("notes", "notes", str, True, None, False),
            ("orderedOn", "orderedOn", fhirdate.FHIRDate, False, None, False),
            ("orderer", "orderer", fhirreference.FHIRReference, False, None, False),
            ("performer", "performer", fhirreference.FHIRReference, False, None, False),
            ("priority", "priority", str, False, None, False),
            ("status", "status", str, False, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, True),
            ("timingDateTime", "timingDateTime", fhirdate.FHIRDate, False, "timing", False),
            ("timingPeriod", "timingPeriod", period.Period, False, "timing", False),
            ("timingTiming", "timingTiming", timing.Timing, False, "timing", False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
        ])
        return js


import backboneelement

class ProcedureRequestBodySite(backboneelement.BackboneElement):
    """ Target body sites.
    
    Indicates the sites on the subject's body where the procedure should be
    performed ( i.e. the target sites).
    """
    
    resource_name = "ProcedureRequestBodySite"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.siteCodeableConcept = None
        """ Target body site.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.siteReference = None
        """ Target body site.
        Type `FHIRReference` referencing `BodySite` (represented as `dict` in JSON). """
        
        super(ProcedureRequestBodySite, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ProcedureRequestBodySite, self).elementProperties()
        js.extend([
            ("siteCodeableConcept", "siteCodeableConcept", codeableconcept.CodeableConcept, False, "site", True),
            ("siteReference", "siteReference", fhirreference.FHIRReference, False, "site", True),
        ])
        return js


import codeableconcept
import fhirdate
import fhirreference
import identifier
import period
import timing
