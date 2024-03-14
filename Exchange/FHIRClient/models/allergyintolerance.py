#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/AllergyIntolerance) on 2016-03-29.
#  2016, SMART Health IT.


import domainresource

class AllergyIntolerance(domainresource.DomainResource):
    """ Allergy or Intolerance (generally: Risk Of Adverse reaction to a substance).
    
    Risk of harmful or undesirable, physiological response which is unique to
    an individual and associated with exposure to a substance.
    """
    
    resource_name = "AllergyIntolerance"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.category = None
        """ food | medication | environment - Category of Substance.
        Type `str`. """
        
        self.comment = None
        """ Additional text not captured in other fields.
        Type `str`. """
        
        self.criticality = None
        """ low | high | unassessible - Estimated potential clinical harm.
        Type `str`. """
        
        self.event = None
        """ Adverse Reaction Events linked to exposure to substance.
        List of `AllergyIntoleranceEvent` items (represented as `dict` in JSON). """
        
        self.identifier = None
        """ External Ids for this item.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.lastOccurence = None
        """ Date(/time) of last known occurence of a reaction.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.patient = None
        """ Who the sensitivity is for.
        Type `FHIRReference` referencing `Patient` (represented as `dict` in JSON). """
        
        self.recordedDate = None
        """ When recorded.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.recorder = None
        """ Who recorded the sensitivity.
        Type `FHIRReference` referencing `Practitioner, Patient` (represented as `dict` in JSON). """
        
        self.reporter = None
        """ Source of the information about the allergy.
        Type `FHIRReference` referencing `Patient, RelatedPerson, Practitioner` (represented as `dict` in JSON). """
        
        self.status = None
        """ unconfirmed | confirmed | resolved | refuted | entered-in-error.
        Type `str`. """
        
        self.substance = None
        """ Substance, (or class) considered to be responsible for risk.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.type = None
        """ immune | non-immune - Underlying mechanism (if known).
        Type `str`. """
        
        super(AllergyIntolerance, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(AllergyIntolerance, self).elementProperties()
        js.extend([
            ("category", "category", str, False, None, False),
            ("comment", "comment", str, False, None, False),
            ("criticality", "criticality", str, False, None, False),
            ("event", "event", AllergyIntoleranceEvent, True, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("lastOccurence", "lastOccurence", fhirdate.FHIRDate, False, None, False),
            ("patient", "patient", fhirreference.FHIRReference, False, None, True),
            ("recordedDate", "recordedDate", fhirdate.FHIRDate, False, None, False),
            ("recorder", "recorder", fhirreference.FHIRReference, False, None, False),
            ("reporter", "reporter", fhirreference.FHIRReference, False, None, False),
            ("status", "status", str, False, None, False),
            ("substance", "substance", codeableconcept.CodeableConcept, False, None, True),
            ("type", "type", str, False, None, False),
        ])
        return js


import backboneelement

class  AllergyIntoleranceEvent(backboneelement.BackboneElement):
    """ Adverse Reaction Events linked to exposure to substance.
    
    Details about each Adverse Reaction Event linked to exposure to the
    identified Substance.
    """
    
    resource_name = "AllergyIntoleranceEvent"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.certainty = None
        """ unlikely | likely | confirmed - clinical certainty about the
        specific substance.
        Type `str`. """
        
        self.comment = None
        """ Text about event not captured in other fields.
        Type `str`. """
        
        self.description = None
        """ Description of the event as a whole.
        Type `str`. """
        
        self.duration = None
        """ How long Manifestations persisted.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.exposureRoute = None
        """ How the subject was exposed to the substance.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.manifestation = None
        """ Clinical symptoms/signs associated with the Event.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.onset = None
        """ Date(/time) when manifestations showed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.severity = None
        """ mild | moderate | severe (of event as a whole).
        Type `str`. """
        
        self.substance = None
        """ Specific substance considered to be responsible for event.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(AllergyIntoleranceEvent, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(AllergyIntoleranceEvent, self).elementProperties()
        js.extend([
            ("certainty", "certainty", str, False, None, False),
            ("comment", "comment", str, False, None, False),
            ("description", "description", str, False, None, False),
            ("duration", "duration", duration.Duration, False, None, False),
            ("exposureRoute", "exposureRoute", codeableconcept.CodeableConcept, False, None, False),
            ("manifestation", "manifestation", codeableconcept.CodeableConcept, True, None, True),
            ("onset", "onset", fhirdate.FHIRDate, False, None, False),
            ("severity", "severity", str, False, None, False),
            ("substance", "substance", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


import codeableconcept
import duration
import fhirdate
import fhirreference
import identifier
