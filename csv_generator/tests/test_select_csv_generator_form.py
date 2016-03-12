# -*- coding: utf-8 -*-
"""
Tests the csv_generator SelectCsvGeneratorForm
"""
from __future__ import unicode_literals
from csv_generator.forms import SelectCsvGeneratorForm
from csv_generator.models import CsvGenerator
from csv_generator.tests.utils import CsvGeneratorTestCase
from django import forms


class SelectCsvGeneratorFormTestCase(CsvGeneratorTestCase):
    """
    Tests the SelectCsvGeneratorForm
    """
    def setUp(self):
        super(SelectCsvGeneratorFormTestCase, self).setUp()
        self.generators = CsvGenerator.objects.all()
        self.form = SelectCsvGeneratorForm(generators=self.generators)

    def test_extends_form(self):
        """
        The form should extend django.forms.Form
        """
        self.assertTrue(issubclass(SelectCsvGeneratorForm, forms.Form))

    def test_generator_field(self):
        """
        The form should define a generator field
        """
        field = self.form.fields['generator']
        self.assertIsInstance(field, forms.ModelChoiceField)
        self.assertTrue(field.required)

    def test_generator_field_queryset(self):
        """
        The queryset should be overridden with the data passed to the form
        """
        self.assertEqual(
            self.form.fields['generator'].queryset,
            self.generators
        )
