"""
Tests the csv_generator CsvGeneratorColumn Form
"""
from csv_generator.forms import CsvGeneratorColumnForm
from csv_generator.models import CsvGeneratorColumn
from csv_generator.tests.utils import CsvGeneratorTestCase
from django import forms


class CsvGeneratorColumnFormTestCase(CsvGeneratorTestCase):
    """
    Tests the CsvGeneratorForm
    """
    def setUp(self):
        super(CsvGeneratorColumnFormTestCase, self).setUp()
        self.form = CsvGeneratorColumnForm()

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

    def test_model_field(self):
        """
        The 'model_field' field should be defined
        """
        field = self.form.fields['model_field']
        self.assertIsInstance(field, forms.ChoiceField)
        self.assertEqual(field.label, 'Field')
