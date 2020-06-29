"""
Tests the csv_generator CsvGenerator Formset
"""
from csv_generator.forms import CsvGeneratorColumnFormSet
from csv_generator.forms import CsvGeneratorColumnForm
from csv_generator.models import CsvGenerator, CsvGeneratorColumn
from csv_generator.tests.utils import CsvGeneratorTestCase
from django import forms


class CsvGeneratorColumnFormSetTestCase(CsvGeneratorTestCase):
    """
    Tests the CsvGeneratorColumnFormSet
    """
    def setUp(self):
        super(CsvGeneratorColumnFormSetTestCase, self).setUp()
        self.formset = forms.inlineformset_factory(
            CsvGenerator,
            CsvGeneratorColumn,
            formset=CsvGeneratorColumnFormSet,
            form=CsvGeneratorColumnForm,
            exclude=()
        )

    def test_extends_base_inline_formset(self):
        """
        The formset should extend django.forms.BaseInlineFormSet
        """
        self.assertTrue(issubclass(
            CsvGeneratorColumnFormSet,
            forms.BaseInlineFormSet
        ))
