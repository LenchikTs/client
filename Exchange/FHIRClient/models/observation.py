#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/Observation) on 2016-03-29.
#  2016, SMART Health IT.


import domainresource

class Observation(domainresource.DomainResource):
    """ Measurements and simple assertions.
    
    Measurements and simple assertions made about a patient, device or other
    subject.
    """
    
    resource_name = "Observation"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.appliesDateTime = None
        """ Physiologically Relevant time/time-period for observation.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.appliesPeriod = None
        """ Physiologically Relevant time/time-period for observation.
        Type `Period` (represented as `dict` in JSON). """
        
        self.bodySiteCodeableConcept = None
        """ Observed body part.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.bodySiteReference = None
        """ Observed body part.
        Type `FHIRReference` referencing `BodySite` (represented as `dict` in JSON). """
        
        self.code = None
        """ Type of observation (code / type).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.comments = None
        """ Comments about result.
        Type `str`. """
        
        self.dataAbsentReason = None
        """ Why the result is missing.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.device = None
        """ (Measurement) Device.
        Type `FHIRReference` referencing `Device, DeviceMetric` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Healthcare event during which this observation is made.
        Type `FHIRReference` referencing `Encounter` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Unique Id for this particular observation.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.interpretation = None
        """ High, low, normal, etc..
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.issued = None
        """ Date/Time this was made available.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.method = None
        """ How it was done.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.performer = None
        """ Who did the observation.
        List of `FHIRReference` items referencing `Practitioner, Organization, Patient, RelatedPerson` (represented as `dict` in JSON). """
        
        self.referenceRange = None
        """ Provides guide for interpretation.
        List of `ObservationReferenceRange` items (represented as `dict` in JSON). """
        
        self.related = None
        """ Observations related to this observation.
        List of `ObservationRelated` items (represented as `dict` in JSON). """
        
        self.reliability = None
        """ ok | ongoing | early | questionable | calibrating | error +.
        Type `str`. """
        
        self.specimen = None
        """ Specimen used for this observation.
        Type `FHIRReference` referencing `Specimen` (represented as `dict` in JSON). """
        
        self.status = None
        """ registered | preliminary | final | amended +.
        Type `str`. """
        
        self.subject = None
        """ Who and/or what this is about.
        Type `FHIRReference` referencing `Patient, Group, Device, Location` (represented as `dict` in JSON). """
        
        self.valueAttachment = None
        """ Actual result.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.valueCodeableConcept = None
        """ Actual result.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.valueDateTime = None
        """ Actual result.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valuePeriod = None
        """ Actual result.
        Type `Period` (represented as `dict` in JSON). """
        
        self.valueQuantity = None
        """ Actual result.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.valueRange = None
        """ Actual result.
        Type `Range` (represented as `dict` in JSON). """
        
        self.valueRatio = None
        """ Actual result.
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.valueSampledData = None
        """ Actual result.
        Type `SampledData` (represented as `dict` in JSON). """
        
        self.valueString = None
        """ Actual result.
        Type `str`. """
        
        self.valueTime = None
        """ Actual result.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        super(Observation, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(Observation, self).elementProperties()
        js.extend([
            ("appliesDateTime", "appliesDateTime", fhirdate.FHIRDate, False, "applies", False),
            ("appliesPeriod", "appliesPeriod", period.Period, False, "applies", False),
            ("bodySiteCodeableConcept", "bodySiteCodeableConcept", codeableconcept.CodeableConcept, False, "bodySite", False),
            ("bodySiteReference", "bodySiteReference", fhirreference.FHIRReference, False, "bodySite", False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
            ("comments", "comments", str, False, None, False),
            ("dataAbsentReason", "dataAbsentReason", codeableconcept.CodeableConcept, False, None, False),
            ("device", "device", fhirreference.FHIRReference, False, None, False),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("interpretation", "interpretation", codeableconcept.CodeableConcept, False, None, False),
            ("issued", "issued", fhirdate.FHIRDate, False, None, False),
            ("method", "method", codeableconcept.CodeableConcept, False, None, False),
            ("performer", "performer", fhirreference.FHIRReference, False, None, False),
            ("referenceRange", "referenceRange", ObservationReferenceRange, False, None, False),
            ("related", "related", ObservationRelated, True, None, False),
            ("reliability", "reliability", str, False, None, False),
            ("specimen", "specimen", fhirreference.FHIRReference, False, None, False),
            ("status", "status", str, False, None, True),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("valueAttachment", "valueAttachment", attachment.Attachment, False, "value", False),
            ("valueCodeableConcept", "valueCodeableConcept", codeableconcept.CodeableConcept, False, "value", False),
            ("valueDateTime", "valueDateTime", fhirdate.FHIRDate, False, "value", False),
            ("valuePeriod", "valuePeriod", period.Period, False, "value", False),
            ("valueQuantity", "valueQuantity", quantity.Quantity, False, "value", False),
            ("valueRange", "valueRange", range.Range, False, "value", False),
            ("valueRatio", "valueRatio", ratio.Ratio, False, "value", False),
            ("valueSampledData", "valueSampledData", sampleddata.SampledData, False, "value", False),
            ("valueString", "valueString", str, False, "value", False),
            ("valueTime", "valueTime", fhirdate.FHIRDate, False, "value", False),
        ])
        return js

import backboneelement

class ObservationReferenceRange(backboneelement.BackboneElement):
    """ Provides guide for interpretation.
    
    Guidance on how to interpret the value by comparison to a normal or
    recommended range.
    """
    
    resource_name = "ObservationReferenceRange"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.age = None
        """ Applicable age range, if relevant.
        Type `Range` (represented as `dict` in JSON). """
        
        self.high = None
        """ High Range, if relevant.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.low = None
        """ Low Range, if relevant.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.meaning = None
        """ Indicates the meaning/use of this range of this range.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.text = None
        """ Text based reference range in an observation.
        Type `str`. """
        
        super(ObservationReferenceRange, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ObservationReferenceRange, self).elementProperties()
        js.extend([
            ("age", "age", range.Range, False, None, False),
            ("high", "high", quantity.Quantity, False, None, False),
            ("low", "low", quantity.Quantity, False, None, False),
            ("meaning", "meaning", codeableconcept.CodeableConcept, False, None, False),
            ("text", "text", str, False, None, False),
        ])
        return js


class ObservationRelated(backboneelement.BackboneElement):
    """ Observations related to this observation.
    
    Related observations - either components, or previous observations, or
    statements of derivation.
    """
    
    resource_name = "ObservationRelated"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.target = None
        """ Observation that is related to this one.
        Type `FHIRReference` referencing `Observation` (represented as `dict` in JSON). """
        
        self.type = None
        """ has-component | has-member | derived-from | sequel-to | replaces |
        qualified-by | interfered-by.
        Type `str`. """
        
        super(ObservationRelated, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ObservationRelated, self).elementProperties()
        js.extend([
            ("target", "target", fhirreference.FHIRReference, False, None, True),
            ("type", "type", str, False, None, False),
        ])
        return js


import attachment
import codeableconcept
import fhirdate
import fhirreference
import identifier
import period
import quantity
import range
import ratio
import sampleddata
