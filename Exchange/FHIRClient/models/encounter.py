#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/Encounter) on 2016-03-29.
#  2016, SMART Health IT.


import domainresource

class Encounter(domainresource.DomainResource):
    """ An interaction during which services are provided to the patient.
    
    An interaction between a patient and healthcare provider(s) for the purpose
    of providing healthcare service(s) or assessing the health status of a
    patient.
    """
    
    resource_name = "Encounter"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.class_fhir = None
        """ inpatient | outpatient | ambulatory | emergency +.
        Type `str`. """
        
        self.episodeOfCare = None
        """ An episode of care that this encounter should be recorded against.
        Type `FHIRReference` referencing `EpisodeOfCare` (represented as `dict` in JSON). """
        
        self.fulfills = None
        """ The appointment that scheduled this encounter.
        Type `FHIRReference` referencing `Appointment` (represented as `dict` in JSON). """
        
        self.hospitalization = None
        """ Details about an admission to a clinic.
        Type `EncounterHospitalization` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Identifier(s) by which this encounter is known.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.incomingReferralRequest = None
        """ Incoming Referral Request.
        List of `FHIRReference` items referencing `ReferralRequest` (represented as `dict` in JSON). """
        
        self.indication = None
        """ Reason the encounter takes place (resource).
        List of `FHIRReference` items referencing `Resource` (represented as `dict` in JSON). """
        
        self.length = None
        """ Quantity of time the encounter lasted (less time absent).
        Type `Duration` (represented as `dict` in JSON). """
        
        self.location = None
        """ List of locations the patient has been at.
        List of `EncounterLocation` items (represented as `dict` in JSON). """
        
        self.partOf = None
        """ Another Encounter this encounter is part of.
        Type `FHIRReference` referencing `Encounter` (represented as `dict` in JSON). """
        
        self.participant = None
        """ List of participants involved in the encounter.
        List of `EncounterParticipant` items (represented as `dict` in JSON). """
        
        self.patient = None
        """ The patient present at the encounter.
        Type `FHIRReference` referencing `Patient` (represented as `dict` in JSON). """
        
        self.period = None
        """ The start and end time of the encounter.
        Type `Period` (represented as `dict` in JSON). """
        
        self.priority = None
        """ Indicates the urgency of the encounter.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.reason = None
        """ Reason the encounter takes place (code).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.serviceProvider = None
        """ The custodian organization of this Encounter record.
        Type `FHIRReference` referencing `Organization` (represented as `dict` in JSON). """
        
        self.status = None
        """ planned | arrived | in-progress | onleave | finished | cancelled.
        Type `str`. """
        
        self.statusHistory = None
        """ List of Encounter statuses.
        List of `EncounterStatusHistory` items (represented as `dict` in JSON). """
        
        self.type = None
        """ Specific type of encounter.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        super(Encounter, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(Encounter, self).elementProperties()
        js.extend([
            ("class_fhir", "class", str, False, None, False),
            ("episodeOfCare", "episodeOfCare", fhirreference.FHIRReference, False, None, False),
            ("fulfills", "fulfills", fhirreference.FHIRReference, False, None, False),
            ("hospitalization", "hospitalization", EncounterHospitalization, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("incomingReferralRequest", "incomingReferralRequest", fhirreference.FHIRReference, True, None, False),
            ("indication", "indication", fhirreference.FHIRReference, True, None, False),
            ("length", "length", duration.Duration, False, None, False),
            ("location", "location", EncounterLocation, True, None, False),
            ("partOf", "partOf", fhirreference.FHIRReference, False, None, False),
            ("participant", "participant", EncounterParticipant, True, None, False),
            ("patient", "patient", fhirreference.FHIRReference, False, None, False),
            ("period", "period", period.Period, False, None, False),
            ("priority", "priority", codeableconcept.CodeableConcept, False, None, False),
            ("reason", "reason", codeableconcept.CodeableConcept, True, None, False),
            ("serviceProvider", "serviceProvider", fhirreference.FHIRReference, False, None, False),
            ("status", "status", str, False, None, True),
            ("statusHistory", "statusHistory", EncounterStatusHistory, True, None, False),
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
        ])
        return js


import backboneelement

class EncounterHospitalization(backboneelement.BackboneElement):
    """ Details about an admission to a clinic.
    """
    
    resource_name = "EncounterHospitalization"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.admitSource = None
        """ From where patient was admitted (physician referral, transfer).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.destination = None
        """ Location to which the patient is discharged.
        Type `FHIRReference` referencing `Location` (represented as `dict` in JSON). """
        
        self.dietPreference = None
        """ Diet preferences reported by the patient.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.dischargeDiagnosis = None
        """ The final diagnosis given a patient before release from the
        hospital after all testing, surgery, and workup are complete.
        Type `FHIRReference` referencing `Resource` (represented as `dict` in JSON). """
        
        self.dischargeDisposition = None
        """ Category or kind of location after discharge.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.origin = None
        """ The location from which the patient came before admission.
        Type `FHIRReference` referencing `Location` (represented as `dict` in JSON). """
        
        self.preAdmissionIdentifier = None
        """ Pre-admission identifier.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.reAdmission = None
        """ Is this hospitalization a readmission?.
        Type `bool`. """
        
        self.specialArrangement = None
        """ Wheelchair, translator, stretcher, etc.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.specialCourtesy = None
        """ Special courtesies (VIP, board member).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        super(EncounterHospitalization, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(EncounterHospitalization, self).elementProperties()
        js.extend([
            ("admitSource", "admitSource", codeableconcept.CodeableConcept, False, None, False),
            ("destination", "destination", fhirreference.FHIRReference, False, None, False),
            ("dietPreference", "dietPreference", codeableconcept.CodeableConcept, False, None, False),
            ("dischargeDiagnosis", "dischargeDiagnosis", fhirreference.FHIRReference, False, None, False),
            ("dischargeDisposition", "dischargeDisposition", codeableconcept.CodeableConcept, False, None, False),
            ("origin", "origin", fhirreference.FHIRReference, False, None, False),
            ("preAdmissionIdentifier", "preAdmissionIdentifier", identifier.Identifier, False, None, False),
            ("reAdmission", "reAdmission", bool, False, None, False),
            ("specialArrangement", "specialArrangement", codeableconcept.CodeableConcept, True, None, False),
            ("specialCourtesy", "specialCourtesy", codeableconcept.CodeableConcept, True, None, False),
        ])
        return js


class EncounterLocation(backboneelement.BackboneElement):
    """ List of locations the patient has been at.
    
    List of locations at which the patient has been.
    """
    
    resource_name = "EncounterLocation"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.location = None
        """ Location the encounter takes place.
        Type `FHIRReference` referencing `Location` (represented as `dict` in JSON). """
        
        self.period = None
        """ Time period during which the patient was present at the location.
        Type `Period` (represented as `dict` in JSON). """
        
        self.status = None
        """ planned | present | reserved.
        Type `str`. """
        
        super(EncounterLocation, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(EncounterLocation, self).elementProperties()
        js.extend([
            ("location", "location", fhirreference.FHIRReference, False, None, True),
            ("period", "period", period.Period, False, None, False),
            ("status", "status", str, False, None, False),
        ])
        return js


class EncounterParticipant(backboneelement.BackboneElement):
    """ List of participants involved in the encounter.
    
    The main practitioner responsible for providing the service.
    """
    
    resource_name = "EncounterParticipant"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.individual = None
        """ Persons involved in the encounter other than the patient.
        Type `FHIRReference` referencing `Practitioner, RelatedPerson` (represented as `dict` in JSON). """
        
        self.period = None
        """ Period of time during the encounter participant was present.
        Type `Period` (represented as `dict` in JSON). """
        
        self.type = None
        """ Role of participant in encounter.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        super(EncounterParticipant, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(EncounterParticipant, self).elementProperties()
        js.extend([
            ("individual", "individual", fhirreference.FHIRReference, False, None, False),
            ("period", "period", period.Period, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
        ])
        return js


class EncounterStatusHistory(backboneelement.BackboneElement):
    """ List of Encounter statuses.
    
    The current status is always found in the current version of the resource.
    This status history permits the encounter resource to contain the status
    history without the needing to read through the historical versions of the
    resource, or even have the server store them.
    """
    
    resource_name = "EncounterStatusHistory"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.period = None
        """ The time that the episode was in the specified status.
        Type `Period` (represented as `dict` in JSON). """
        
        self.status = None
        """ planned | arrived | in-progress | onleave | finished | cancelled.
        Type `str`. """
        
        super(EncounterStatusHistory, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(EncounterStatusHistory, self).elementProperties()
        js.extend([
            ("period", "period", period.Period, False, None, True),
            ("status", "status", str, False, None, True),
        ])
        return js


import codeableconcept
import duration
import fhirreference
import identifier
import period
