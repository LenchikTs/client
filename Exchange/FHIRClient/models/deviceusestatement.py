#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/DeviceUseStatement) on 2016-03-29.
#  2016, SMART Health IT.


import domainresource

class DeviceUseStatement(domainresource.DomainResource):
    """ A record of a device being used by a patient where the record is the result
    of a report from the patient or another clinician..
    
    A record of a device being used by a patient where the record is the result
    of a report from the patient or another clinician.
    """
    
    resource_name = "DeviceUseStatement"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.bodySiteCodeableConcept = None
        """ Target body site.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.bodySiteReference = None
        """ Target body site.
        Type `FHIRReference` referencing `BodySite` (represented as `dict` in JSON). """
        
        self.device = None
        """ The details of the device used..
        Type `FHIRReference` referencing `Device` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ An external identifier for this statement such as an IRI..
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.indication = None
        """ Reason or justification for the use of the device..
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.notes = None
        """ Details about the device statement that were not represented at all
        or sufficiently in one of the attributes provided in a class. These
        may include for example a comment, an instruction, or a note
        associated with the statement..
        List of `str` items. """
        
        self.recordedOn = None
        """ The time at which the statement was made/recorded..
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.subject = None
        """ The patient who used the device..
        Type `FHIRReference` referencing `Patient` (represented as `dict` in JSON). """
        
        self.timingDateTime = None
        """ How often the device was used..
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.timingPeriod = None
        """ How often the device was used..
        Type `Period` (represented as `dict` in JSON). """
        
        self.timingTiming = None
        """ How often the device was used..
        Type `Timing` (represented as `dict` in JSON). """
        
        self.whenUsed = None
        """ The time period over which the device was used..
        Type `Period` (represented as `dict` in JSON). """
        
        super(DeviceUseStatement, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(DeviceUseStatement, self).elementProperties()
        js.extend([
            ("bodySiteCodeableConcept", "bodySiteCodeableConcept", codeableconcept.CodeableConcept, False, "bodySite", False),
            ("bodySiteReference", "bodySiteReference", fhirreference.FHIRReference, False, "bodySite", False),
            ("device", "device", fhirreference.FHIRReference, False, None, True),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("indication", "indication", codeableconcept.CodeableConcept, True, None, False),
            ("notes", "notes", str, True, None, False),
            ("recordedOn", "recordedOn", fhirdate.FHIRDate, False, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, True),
            ("timingDateTime", "timingDateTime", fhirdate.FHIRDate, False, "timing", False),
            ("timingPeriod", "timingPeriod", period.Period, False, "timing", False),
            ("timingTiming", "timingTiming", timing.Timing, False, "timing", False),
            ("whenUsed", "whenUsed", period.Period, False, None, False),
        ])
        return js


import codeableconcept
import fhirdate
import fhirreference
import identifier
import period
import timing
