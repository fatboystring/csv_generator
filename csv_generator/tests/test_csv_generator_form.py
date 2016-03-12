# -*- coding: utf-8 -*-
"""
Tests the csv_generator CsvGenerator Form
"""
from __future__ import unicode_literals
from csv_generator.forms import CsvGeneratorForm
from csv_generator.models import CsvGenerator
from django import forms
from django.test import TestCase


class CsvGeneratorFormTestCase(TestCase):
    """
    Tests the CsvGeneratorForm
    """
    def test_is_model_form(self):
        """
        The form should be a model form
        """
        self.assertTrue(issubclass(CsvGeneratorForm, forms.ModelForm))

    def test_model(self):
        """
        The form should use the correct model
        """
        self.assertEqual(CsvGeneratorForm._meta.model, CsvGenerator)
