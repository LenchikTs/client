#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 on 2016-03-29.
#  2016, SMART Health IT.


import os
import io
import unittest
import json
import basic
from .fhirdate import FHIRDate


class BasicTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("Basic", js["resourceType"])
        return basic.Basic(js)
    
    def testBasic1(self):
        inst = self.instantiate_from("basic-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a Basic instance")
        self.implBasic1(inst)
        
        js = inst.as_json()
        self.assertEqual("Basic", js["resourceType"])
        inst2 = basic.Basic(js)
        self.implBasic1(inst2)
    
    def implBasic1(self, inst):
        self.assertEqual(inst.code.coding[0].code, "REFERRAL")
        self.assertEqual(inst.code.coding[0].system, "http://hl7.org/fhir/basic-resource-type")
        self.assertEqual(inst.extension[0].url, "http://example.org/do-not-use/fhir-extensions/referral#requestingPractitioner")
        self.assertEqual(inst.extension[1].url, "http://example.org/do-not-use/fhir-extensions/referral#notes")
        self.assertEqual(inst.extension[1].valueString, "The patient had fever peaks over the last couple of days. He is worried about these peaks.")
        self.assertEqual(inst.extension[2].url, "http://example.org/do-not-use/fhir-extensions/referral#fulfillingEncounter")
        self.assertEqual(inst.id, "referral")
        self.assertEqual(inst.modifierExtension[0].url, "http://example.org/do-not-use/fhir-extensions/referral#referredForService")
        self.assertEqual(inst.modifierExtension[0].valueCodeableConcept.coding[0].code, "11429006")
        self.assertEqual(inst.modifierExtension[0].valueCodeableConcept.coding[0].display, "Consultation")
        self.assertEqual(inst.modifierExtension[0].valueCodeableConcept.coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.modifierExtension[1].url, "http://example.org/do-not-use/fhir-extensions/referral#targetDate")
        self.assertEqual(inst.modifierExtension[1].valuePeriod.end.date, FHIRDate("2013-04-15").date)
        self.assertEqual(inst.modifierExtension[1].valuePeriod.end.as_json(), "2013-04-15")
        self.assertEqual(inst.modifierExtension[1].valuePeriod.start.date, FHIRDate("2013-04-01").date)
        self.assertEqual(inst.modifierExtension[1].valuePeriod.start.as_json(), "2013-04-01")
        self.assertEqual(inst.modifierExtension[2].url, "http://example.org/do-not-use/fhir-extensions/referral#status")
        self.assertEqual(inst.modifierExtension[2].valueCode, "complete")
        self.assertEqual(inst.text.status, "generated")
    
    def testBasic2(self):
        inst = self.instantiate_from("basic-example-adverseevent-qicore.json")
        self.assertIsNotNone(inst, "Must have instantiated a Basic instance")
        self.implBasic2(inst)
        
        js = inst.as_json()
        self.assertEqual("Basic", js["resourceType"])
        inst2 = basic.Basic(js)
        self.implBasic2(inst2)
    
    def implBasic2(self, inst):
        self.assertEqual(inst.code.coding[0].code, "ADVEVENT")
        self.assertEqual(inst.code.coding[0].system, "http://hl7.org/fhir/other-resource-type")
        self.assertEqual(inst.extension[0].extension[0].url, "http://hl7.org/fhir/StructureDefinition/adverseevent-qicore-cause-item")
        self.assertEqual(inst.extension[0].extension[1].url, "http://hl7.org/fhir/StructureDefinition/adverseevent-qicore-cause-certainty")
        self.assertEqual(inst.extension[0].extension[1].valueCodeableConcept.coding[0].code, "415684004")
        self.assertEqual(inst.extension[0].extension[1].valueCodeableConcept.coding[0].display, "Suspected (qualifier)")
        self.assertEqual(inst.extension[0].extension[1].valueCodeableConcept.coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.extension[0].url, "http://hl7.org/fhir/StructureDefinition/adverseevent-qicore-cause")
        self.assertEqual(inst.extension[1].url, "http://hl7.org/fhir/StructureDefinition/adverseevent-qicore-type")
        self.assertEqual(inst.extension[1].valueCodeableConcept.coding[0].code, "28926001")
        self.assertEqual(inst.extension[1].valueCodeableConcept.coding[0].display, "Eruption due to drug (disorder)")
        self.assertEqual(inst.extension[1].valueCodeableConcept.coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.extension[2].url, "http://hl7.org/fhir/StructureDefinition/adverseevent-qicore-period")
        self.assertEqual(inst.extension[2].valuePeriod.end.date, FHIRDate("2014-01-15").date)
        self.assertEqual(inst.extension[2].valuePeriod.end.as_json(), "2014-01-15")
        self.assertEqual(inst.extension[2].valuePeriod.start.date, FHIRDate("2014-01-14").date)
        self.assertEqual(inst.extension[2].valuePeriod.start.as_json(), "2014-01-14")
        self.assertEqual(inst.id, "qicore")
        self.assertEqual(inst.modifierExtension[0].url, "http://hl7.org/fhir/StructureDefinition/adverseevent-qicore-didNotOccur")
        self.assertFalse(inst.modifierExtension[0].valueBoolean)
        self.assertEqual(inst.text.status, "generated")
    
    def testBasic3(self):
        inst = self.instantiate_from("basic-example2.json")
        self.assertIsNotNone(inst, "Must have instantiated a Basic instance")
        self.implBasic3(inst)
        
        js = inst.as_json()
        self.assertEqual("Basic", js["resourceType"])
        inst2 = basic.Basic(js)
        self.implBasic3(inst2)
    
    def implBasic3(self, inst):
        self.assertEqual(inst.code.coding[0].code, "UMLCLASSMODEL")
        self.assertEqual(inst.code.coding[0].system, "http://example.org/do-not-use/fhir-codes#resourceTypes")
        self.assertEqual(inst.extension[0].extension[0].url, "name")
        self.assertEqual(inst.extension[0].extension[0].valueString, "Class1")
        self.assertEqual(inst.extension[0].extension[1].extension[0].url, "name")
        self.assertEqual(inst.extension[0].extension[1].extension[0].valueString, "attribute1")
        self.assertEqual(inst.extension[0].extension[1].extension[1].url, "minOccurs")
        self.assertEqual(inst.extension[0].extension[1].extension[1].valueInteger, 1)
        self.assertEqual(inst.extension[0].extension[1].extension[2].url, "maxOccurs")
        self.assertEqual(inst.extension[0].extension[1].extension[2].valueCode, "*")
        self.assertEqual(inst.extension[0].extension[1].url, "attribute")
        self.assertEqual(inst.extension[0].extension[2].extension[0].url, "name")
        self.assertEqual(inst.extension[0].extension[2].extension[0].valueString, "attribute2")
        self.assertEqual(inst.extension[0].extension[2].extension[1].url, "minOccurs")
        self.assertEqual(inst.extension[0].extension[2].extension[1].valueInteger, 0)
        self.assertEqual(inst.extension[0].extension[2].extension[2].url, "maxOccurs")
        self.assertEqual(inst.extension[0].extension[2].extension[2].valueInteger, 1)
        self.assertEqual(inst.extension[0].extension[2].url, "attribute")
        self.assertEqual(inst.extension[0].url, "http://example.org/do-not-use/fhir-extensions/UMLclass")
        self.assertEqual(inst.id, "classModel")
        self.assertEqual(inst.text.div, "<div>\n      \n      <p>\n        <b>Class1</b>\n      </p>\n      \n      <ul>\n        \n        <li>Attribute1: 1..*</li>\n        \n        <li>Attribute2: 0..1</li>\n      \n      </ul>\n    \n    </div>")
        self.assertEqual(inst.text.status, "generated")
    
    def testBasic4(self):
        inst = self.instantiate_from("basic-example-narrative.json")
        self.assertIsNotNone(inst, "Must have instantiated a Basic instance")
        self.implBasic4(inst)
        
        js = inst.as_json()
        self.assertEqual("Basic", js["resourceType"])
        inst2 = basic.Basic(js)
        self.implBasic4(inst2)
    
    def implBasic4(self, inst):
        self.assertEqual(inst.code.text, "Example Narrative Tester")
        self.assertEqual(inst.id, "basic-example-narrative")
        self.assertEqual(inst.text.status, "additional")

