# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from csv_generator.forms import CsvGeneratorColumnForm
from csv_generator.models import CsvGeneratorColumn
from django import forms
from django.test import TestCase


class CsvGeneratorColumnFormTestCase(TestCase):
    """
    Tests the CsvGeneratorForm
    """
    def test_is_model_form(self):
        """
        The form should be a model form
        """
        self.assertTrue(issubclass(CsvGeneratorColumnForm, forms.ModelForm))

    def test_model(self):
        """
        The form should use the correct model
        """
        self.assertEqual(CsvGeneratorColumnForm._meta.model, CsvGeneratorColumn)
