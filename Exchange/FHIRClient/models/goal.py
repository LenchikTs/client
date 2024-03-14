#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/Goal) on 2016-03-29.
#  2016, SMART Health IT.


import domainresource

class Goal(domainresource.DomainResource):
    """ Describes the intended objective(s) of patient care.
    
    Describes the intended objective(s) of patient care, for example, weight
    loss, restoring an activity of daily living, etc.
    """
    
    resource_name = "Goal"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.author = None
        """ Who's responsible for creating Goal?.
        Type `FHIRReference` referencing `Patient, Practitioner, RelatedPerson` (represented as `dict` in JSON). """
        
        self.concern = None
        """ Health issues this goal addresses.
        List of `FHIRReference` items referencing `Condition, Observation, MedicationStatement, NutritionOrder, ProcedureRequest, RiskAssessment` (represented as `dict` in JSON). """
        
        self.description = None
        """ What's the desired outcome?.
        Type `str`. """
        
        self.identifier = None
        """ External Ids for this goal.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.notes = None
        """ Comments about the goal.
        Type `str`. """
        
        self.outcome = None
        """ What was end result of goal?.
        List of `GoalOutcome` items (represented as `dict` in JSON). """
        
        self.patient = None
        """ The patient for whom this goal is intended for.
        Type `FHIRReference` referencing `Patient` (represented as `dict` in JSON). """
        
        self.priority = None
        """ high | medium |low.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.status = None
        """ proposed | planned | in-progress | achieved | sustaining |
        cancelled | accepted | rejected.
        Type `str`. """
        
        self.statusDate = None
        """ When goal status took effect.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.targetDate = None
        """ Reach goal on or before.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        super(Goal, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(Goal, self).elementProperties()
        js.extend([
            ("author", "author", fhirreference.FHIRReference, False, None, False),
            ("concern", "concern", fhirreference.FHIRReference, True, None, False),
            ("description", "description", str, False, None, True),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("notes", "notes", str, False, None, False),
            ("outcome", "outcome", GoalOutcome, True, None, False),
            ("patient", "patient", fhirreference.FHIRReference, False, None, False),
            ("priority", "priority", codeableconcept.CodeableConcept, False, None, False),
            ("status", "status", str, False, None, True),
            ("statusDate", "statusDate", fhirdate.FHIRDate, False, None, False),
            ("targetDate", "targetDate", fhirdate.FHIRDate, False, None, False),
        ])
        return js


import backboneelement

class GoalOutcome(backboneelement.BackboneElement):
    """ What was end result of goal?.
    
    Identifies the change (or lack of change) at the point where the goal was
    deepmed to be cancelled or achieved.
    """
    
    resource_name = "GoalOutcome"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.resultCodeableConcept = None
        """ Code or observation that resulted from gual.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.resultReference = None
        """ Code or observation that resulted from gual.
        Type `FHIRReference` referencing `Observation` (represented as `dict` in JSON). """
        
        super(GoalOutcome, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(GoalOutcome, self).elementProperties()
        js.extend([
            ("resultCodeableConcept", "resultCodeableConcept", codeableconcept.CodeableConcept, False, "result", False),
            ("resultReference", "resultReference", fhirreference.FHIRReference, False, "result", False),
        ])
        return js


import codeableconcept
import fhirdate
import fhirreference
import identifier
