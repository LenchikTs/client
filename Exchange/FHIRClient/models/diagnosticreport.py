#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/DiagnosticReport) on 2016-03-29.
#  2016, SMART Health IT.


import domainresource

class DiagnosticReport(domainresource.DomainResource):
    """ A Diagnostic report - a combination of request information, atomic results,
    images, interpretation, as well as formatted reports.
    
    The findings and interpretation of diagnostic  tests performed on patients,
    groups of patients, devices, and locations, and/or specimens derived from
    these. The report includes clinical context such as requesting and provider
    information, and some mix of atomic results, images, textual and coded
    interpretation, and formatted representation of diagnostic reports.
    """
    
    resource_name = "DiagnosticReport"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.codedDiagnosis = None
        """ Codes for the conclusion.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.conclusion = None
        """ Clinical Interpretation of test results.
        Type `str`. """
        
        self.diagnosticDateTime = None
        """ Physiologically Relevant time/time-period for report.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.diagnosticPeriod = None
        """ Physiologically Relevant time/time-period for report.
        Type `Period` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Health care event when test ordered.
        Type `FHIRReference` referencing `Encounter` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Id for external references to this report.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.image = None
        """ Key images associated with this report.
        List of `DiagnosticReportImage` items (represented as `dict` in JSON). """
        
        self.imagingStudy = None
        """ Reference to full details of imaging associated with the diagnostic
        report.
        List of `FHIRReference` items referencing `ImagingStudy` (represented as `dict` in JSON). """
        
        self.issued = None
        """ Date this version was released.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.name = None
        """ Name/Code for this diagnostic report.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.performer = None
        """ Responsible Diagnostic Service.
        Type `FHIRReference` referencing `Practitioner, Organization` (represented as `dict` in JSON). """
        
        self.presentedForm = None
        """ Entire Report as issued.
        List of `Attachment` items (represented as `dict` in JSON). """
        
        self.requestDetail = None
        """ What was requested.
        List of `FHIRReference` items referencing `DiagnosticOrder` (represented as `dict` in JSON). """
        
        self.result = None
        """ Observations - simple, or complex nested groups.
        List of `FHIRReference` items referencing `Observation` (represented as `dict` in JSON). """
        
        self.serviceCategory = None
        """ Biochemistry, Hematology etc..
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.specimen = None
        """ Specimens this report is based on.
        List of `FHIRReference` items referencing `Specimen` (represented as `dict` in JSON). """
        
        self.status = None
        """ registered | partial | final | corrected | appended | cancelled |
        entered-in-error.
        Type `str`. """
        
        self.subject = None
        """ The subject of the report, usually, but not always, the patient.
        Type `FHIRReference` referencing `Patient, Group, Device, Location` (represented as `dict` in JSON). """
        
        super(DiagnosticReport, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(DiagnosticReport, self).elementProperties()
        js.extend([
            ("codedDiagnosis", "codedDiagnosis", codeableconcept.CodeableConcept, True, None, False),
            ("conclusion", "conclusion", str, False, None, False),
#            ("diagnosticDateTime", "diagnosticDateTime", fhirdate.FHIRDate, False, "diagnostic", True),
#            ("diagnosticPeriod", "diagnosticPeriod", period.Period, False, "diagnostic", True),

            ("diagnosticDateTime", "diagnosticDateTime", fhirdate.FHIRDate, False, "diagnostic", False),
            ("diagnosticPeriod", "diagnosticPeriod", period.Period, False, "diagnostic", False),

            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("image", "image", DiagnosticReportImage, True, None, False),
            ("imagingStudy", "imagingStudy", fhirreference.FHIRReference, True, None, False),
            ("issued", "issued", fhirdate.FHIRDate, False, None, True),
            ("name", "name", codeableconcept.CodeableConcept, False, None, True),
            ("performer", "performer", fhirreference.FHIRReference, False, None, True),
            ("presentedForm", "presentedForm", attachment.Attachment, False, None, False),
            ("requestDetail", "requestDetail", fhirreference.FHIRReference, True, None, False),
            ("result", "result", fhirreference.FHIRReference, True, None, False),
            ("serviceCategory", "serviceCategory", codeableconcept.CodeableConcept, False, None, False),
            ("specimen", "specimen", fhirreference.FHIRReference, True, None, False),
            ("status", "status", str, False, None, True),
            ("subject", "subject", fhirreference.FHIRReference, False, None, True),
        ])
        return js


import backboneelement

class DiagnosticReportImage(backboneelement.BackboneElement):
    """ Key images associated with this report.
    
    A list of key images associated with this report. The images are generally
    created during the diagnostic process, and may be directly of the patient,
    or of treated specimens (i.e. slides of interest).
    """
    
    resource_name = "DiagnosticReportImage"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.comment = None
        """ Comment about the image (e.g. explanation).
        Type `str`. """
        
        self.link = None
        """ Reference to the image source.
        Type `FHIRReference` referencing `Media` (represented as `dict` in JSON). """
        
        super(DiagnosticReportImage, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(DiagnosticReportImage, self).elementProperties()
        js.extend([
            ("comment", "comment", str, False, None, False),
            ("link", "link", fhirreference.FHIRReference, False, None, True),
        ])
        return js


import attachment
import codeableconcept
import fhirdate
import fhirreference
import identifier
import period