#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/Procedure) on 2016-03-29.
#  2016, SMART Health IT.


import domainresource

class Procedure(domainresource.DomainResource):
    """ An action that was or is currently being performed on a patient.
    
    An action that is or was performed on a patient. This can be a physical
    'thing' like an operation, or less invasive like counseling or
    hypnotherapy.
    """
    
    resource_name = "Procedure"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.bodySite = None
        """ Precise location details.
        List of `ProcedureBodySite` items (represented as `dict` in JSON). """
        
        self.category = None
        """ Classification of the procedure.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.complication = None
        """ Complication following the procedure.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.device = None
        """ Device changed in procedure.
        List of `ProcedureDevice` items (represented as `dict` in JSON). """
        
        self.encounter = None
        """ The encounter when procedure performed.
        Type `FHIRReference` referencing `Encounter` (represented as `dict` in JSON). """
        
        self.followUp = None
        """ Instructions for follow up.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.identifier = None
        """ External Ids for this procedure.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.indication = None
        """ Reason procedure performed.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.location = None
        """ Where the procedure happened.
        Type `FHIRReference` referencing `Location` (represented as `dict` in JSON). """
        
        self.notes = None
        """ Additional information about procedure.
        Type `str`. """
        
        self.outcome = None
        """ What was result of procedure?.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.patient = None
        """ Who procedure was performed on.
        Type `FHIRReference` referencing `Patient` (represented as `dict` in JSON). """
        
        self.performedDateTime = None
        """ Date/Period the procedure was performed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.performedPeriod = None
        """ Date/Period the procedure was performed.
        Type `Period` (represented as `dict` in JSON). """
        
        self.performer = None
        """ The people who performed the procedure.
        List of `ProcedurePerformer` items (represented as `dict` in JSON). """
        
        self.relatedItem = None
        """ A procedure that is related to this one.
        List of `ProcedureRelatedItem` items (represented as `dict` in JSON). """
        
        self.report = None
        """ Any report that results from the procedure.
        List of `FHIRReference` items referencing `DiagnosticReport` (represented as `dict` in JSON). """
        
        self.status = None
        """ in-progress | aborted | completed | entered-in-error.
        Type `str`. """
        
        self.type = None
        """ Identification of the procedure.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.used = None
        """ Items used during procedure.
        List of `FHIRReference` items referencing `Device, Medication, Substance` (represented as `dict` in JSON). """
        
        super(Procedure, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(Procedure, self).elementProperties()
        js.extend([
            ("bodySite", "bodySite", ProcedureBodySite, True, None, False),
            ("category", "category", codeableconcept.CodeableConcept, False, None, False),
            ("complication", "complication", codeableconcept.CodeableConcept, True, None, False),
            ("device", "device", ProcedureDevice, True, None, False),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("followUp", "followUp", codeableconcept.CodeableConcept, True, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("indication", "indication", codeableconcept.CodeableConcept, True, None, False),
            ("location", "location", fhirreference.FHIRReference, False, None, False),
            ("notes", "notes", str, False, None, False),
            ("outcome", "outcome", codeableconcept.CodeableConcept, False, None, False),
            ("patient", "patient", fhirreference.FHIRReference, False, None, True),
            ("performedDateTime", "performedDateTime", fhirdate.FHIRDate, False, "performed", False),
            ("performedPeriod", "performedPeriod", period.Period, False, "performed", False),
            ("performer", "performer", ProcedurePerformer, True, None, False),
            ("relatedItem", "relatedItem", ProcedureRelatedItem, True, None, False),
            ("report", "report", fhirreference.FHIRReference, True, None, False),
            ("status", "status", str, False, None, True),
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("used", "used", fhirreference.FHIRReference, True, None, False),
        ])
        return js


import backboneelement

class ProcedureBodySite(backboneelement.BackboneElement):
    """ Precise location details.
    
    Detailed and structured anatomical location information. Multiple locations
    are allowed - e.g. multiple punch biopsies of a lesion.
    """
    
    resource_name = "ProcedureBodySite"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.siteCodeableConcept = None
        """ Precise location details.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.siteReference = None
        """ Precise location details.
        Type `FHIRReference` referencing `BodySite` (represented as `dict` in JSON). """
        
        super(ProcedureBodySite, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ProcedureBodySite, self).elementProperties()
        js.extend([
            ("siteCodeableConcept", "siteCodeableConcept", codeableconcept.CodeableConcept, False, "site", True),
            ("siteReference", "siteReference", fhirreference.FHIRReference, False, "site", True),
        ])
        return js


class ProcedureDevice(backboneelement.BackboneElement):
    """ Device changed in procedure.
    
    A device change during the procedure.
    """
    
    resource_name = "ProcedureDevice"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.action = None
        """ Kind of change to device.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.manipulated = None
        """ Device that was changed.
        Type `FHIRReference` referencing `Device` (represented as `dict` in JSON). """
        
        super(ProcedureDevice, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ProcedureDevice, self).elementProperties()
        js.extend([
            ("action", "action", codeableconcept.CodeableConcept, False, None, False),
            ("manipulated", "manipulated", fhirreference.FHIRReference, False, None, True),
        ])
        return js


class ProcedurePerformer(backboneelement.BackboneElement):
    """ The people who performed the procedure.
    
    Limited to 'real' people rather than equipment.
    """
    
    resource_name = "ProcedurePerformer"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.person = None
        """ The reference to the practitioner.
        Type `FHIRReference` referencing `Practitioner, Patient, RelatedPerson` (represented as `dict` in JSON). """
        
        self.role = None
        """ The role the person was in.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(ProcedurePerformer, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ProcedurePerformer, self).elementProperties()
        js.extend([
            ("person", "person", fhirreference.FHIRReference, False, None, False),
            ("role", "role", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


class ProcedureRelatedItem(backboneelement.BackboneElement):
    """ A procedure that is related to this one.
    
    Procedures may be related to other items such as procedures or medications.
    For example treating wound dehiscence following a previous procedure.
    """
    
    resource_name = "ProcedureRelatedItem"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.target = None
        """ The related item - e.g. a procedure.
        Type `FHIRReference` referencing `AllergyIntolerance, CarePlan, Condition, DiagnosticReport, FamilyMemberHistory, ImagingStudy, Immunization, ImmunizationRecommendation, MedicationAdministration, MedicationDispense, MedicationPrescription, MedicationStatement, Observation, Procedure` (represented as `dict` in JSON). """
        
        self.type = None
        """ caused-by | because-of.
        Type `str`. """
        
        super(ProcedureRelatedItem, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ProcedureRelatedItem, self).elementProperties()
        js.extend([
            ("target", "target", fhirreference.FHIRReference, False, None, False),
            ("type", "type", str, False, None, False),
        ])
        return js


import codeableconcept
import fhirdate
import fhirreference
import identifier
import period
