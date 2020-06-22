"""
Tests the csv_generator CsvGenerator Form
"""
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

    def test_content_type_choices_ordered(self):
        """
        Content type choices should be ordered alphabetically
        """
        field = CsvGeneratorForm().fields['content_type']
        previous_name = ''
        for instance in field.queryset:
            self.assertTrue(previous_name < instance.model)
            previous_name = instance.model
