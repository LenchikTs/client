#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/MedicationStatement) on 2016-03-29.
#  2016, SMART Health IT.


import domainresource

class MedicationStatement(domainresource.DomainResource):
    """ Administration of medication to a patient.
    
    A record of medication being taken by a patient, or that the medication has
    been given to a patient where the record is the result of a report from the
    patient or another clinician.
    """
    
    resource_name = "MedicationStatement"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.dateAsserted = None
        """ When the statement was asserted?.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.dosage = None
        """ Details of how medication was taken.
        List of `MedicationStatementDosage` items (represented as `dict` in JSON). """
        
        self.effectiveDateTime = None
        """ Over what period was medication consumed?.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.effectivePeriod = None
        """ Over what period was medication consumed?.
        Type `Period` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ External Identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.informationSource = None
        """ The person who provided the information about the taking of this
        medication..
        Type `FHIRReference` referencing `Patient, Practitioner, RelatedPerson` (represented as `dict` in JSON). """
        
        self.medication = None
        """ What medication was taken?.
        Type `FHIRReference` referencing `Medication` (represented as `dict` in JSON). """
        
        self.note = None
        """ Further information about the statement.
        Type `str`. """
        
        self.patient = None
        """ Who was/is taking medication.
        Type `FHIRReference` referencing `Patient` (represented as `dict` in JSON). """
        
        self.reasonForUseCodeableConcept = None
        """ A reason for why the medication is being/was taken..
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.reasonForUseReference = None
        """ A reason for why the medication is being/was taken..
        Type `FHIRReference` referencing `Condition` (represented as `dict` in JSON). """
        
        self.reasonNotGiven = None
        """ True if asserting medication was not given.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.status = None
        """ in-progress | completed | entered-in-error.
        Type `str`. """
        
        self.wasNotGiven = None
        """ True if medication is/was not being taken.
        Type `bool`. """
        
        super(MedicationStatement, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(MedicationStatement, self).elementProperties()
        js.extend([
            ("dateAsserted", "dateAsserted", fhirdate.FHIRDate, False, None, False),
            ("dosage", "dosage", MedicationStatementDosage, True, None, False),
            ("effectiveDateTime", "effectiveDateTime", fhirdate.FHIRDate, False, "effective", False),
            ("effectivePeriod", "effectivePeriod", period.Period, False, "effective", False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("informationSource", "informationSource", fhirreference.FHIRReference, False, None, False),
            ("medication", "medication", fhirreference.FHIRReference, False, None, False),
            ("note", "note", str, False, None, False),
            ("patient", "patient", fhirreference.FHIRReference, False, None, False),
            ("reasonForUseCodeableConcept", "reasonForUseCodeableConcept", codeableconcept.CodeableConcept, False, "reasonForUse", False),
            ("reasonForUseReference", "reasonForUseReference", fhirreference.FHIRReference, False, "reasonForUse", False),
            ("reasonNotGiven", "reasonNotGiven", codeableconcept.CodeableConcept, True, None, False),
            ("status", "status", str, False, None, True),
            ("wasNotGiven", "wasNotGiven", bool, False, None, False),
        ])
        return js


import backboneelement

class MedicationStatementDosage(backboneelement.BackboneElement):
    """ Details of how medication was taken.
    
    Indicates how the medication is/was used by the patient.
    """
    
    resource_name = "MedicationStatementDosage"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.asNeededBoolean = None
        """ Take "as needed" f(or x).
        Type `bool`. """
        
        self.asNeededCodeableConcept = None
        """ Take "as needed" f(or x).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.maxDosePerPeriod = None
        """ Maximum dose that was consumed per unit of time.
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.method = None
        """ Technique used to administer medication.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.quantity = None
        """ Amount administered in one dose.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.rate = None
        """ Dose quantity per unit of time.
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.route = None
        """ How did the medication enter the body?.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.schedule = None
        """ When/how often was medication taken?.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.site = None
        """ Where on body was medication administered?.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.text = None
        """ Dosage Instructions.
        Type `str`. """
        
        super(MedicationStatementDosage, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(MedicationStatementDosage, self).elementProperties()
        js.extend([
            ("asNeededBoolean", "asNeededBoolean", bool, False, "asNeeded", False),
            ("asNeededCodeableConcept", "asNeededCodeableConcept", codeableconcept.CodeableConcept, False, "asNeeded", False),
            ("maxDosePerPeriod", "maxDosePerPeriod", ratio.Ratio, False, None, False),
            ("method", "method", codeableconcept.CodeableConcept, False, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("rate", "rate", ratio.Ratio, False, None, False),
            ("route", "route", codeableconcept.CodeableConcept, False, None, False),
            ("schedule", "schedule", timing.Timing, False, None, False),
            ("site", "site", codeableconcept.CodeableConcept, False, None, False),
            ("text", "text", str, False, None, False),
        ])
        return js


import codeableconcept
import fhirdate
import fhirreference
import identifier
import period
import quantity
import ratio
import timing
