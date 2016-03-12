# -*- coding: utf-8 -*-
"""
Tests the csv_generator CsvGenerator Formset
"""
from __future__ import unicode_literals
from csv_generator.forms import CsvGeneratorColumnFormSet
from csv_generator.models import CsvGenerator, CsvGeneratorColumn
from csv_generator.tests.utils import CsvGeneratorTestCase
from django import forms


class CsvGeneratorColumnFormSetTestCase(CsvGeneratorTestCase):
    """
    Tests the CsvGeneratorColumnFormSet
    """
    def test_extends_base_inline_formset(self):
        """
        The formset should extend django.forms.BaseInlineFormSet
        """
        self.assertTrue(issubclass(
            CsvGeneratorColumnFormSet,
            forms.BaseInlineFormSet
        ))

    def test_get_form_kwargs(self):
        """
        The method should add the csv_generator instance to the form kwargs
        """
        formset = forms.inlineformset_factory(
            CsvGenerator,
            CsvGeneratorColumn,
            formset=CsvGeneratorColumnFormSet,
            exclude=()
        )
        instance = formset(instance=self.generator_1)
        form_kwargs = instance.get_form_kwargs(1)
        self.assertEqual(form_kwargs['csv_generator'], self.generator_1)
