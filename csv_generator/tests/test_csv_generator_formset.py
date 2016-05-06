# -*- coding: utf-8 -*-
"""
Tests the csv_generator CsvGenerator Formset
"""
from __future__ import unicode_literals
from csv_generator.forms import CsvGeneratorColumnFormSet
from csv_generator.forms import CsvGeneratorColumnForm
from csv_generator.models import CsvGenerator, CsvGeneratorColumn
from csv_generator.tests.utils import CsvGeneratorTestCase
from django import get_version
from django import forms
from django.test.utils import skipUnless


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

    @skipUnless(get_version() > '1.8', 'Not implemented in django < 1.8')
    def test_get_form_kwargs(self):
        """
        The method should add the csv_generator instance to the form kwargs
        """
        instance = self.formset(instance=self.generator_1)
        form_kwargs = instance.get_form_kwargs(1)
        self.assertEqual(form_kwargs['csv_generator'], self.generator_1)

    @skipUnless(get_version() < '1.8', 'Not implemented in django > 1.7')
    def test__construct_form(self):
        """
        The method should add the csv generator to the form kwargs
        """
        instance = self.formset(instance=self.generator_1)
        form = instance._construct_form(1)
        self.assertIsInstance(form, CsvGeneratorColumnForm)
        self.assertEqual(
            form.fields['model_field'].choices,
            self.generator_1.all_attributes.items()
        )

    @skipUnless(get_version() < '1.8', 'Not implemented in django > 1.7')
    def test_empty_form(self):
        """
        The property should add the csv generator to the form kwargs
        """
        instance = self.formset(instance=self.generator_1)
        form = instance.empty_form
        self.assertIsInstance(form, CsvGeneratorColumnForm)
        self.assertEqual(
            form.fields['model_field'].choices,
            self.generator_1.all_attributes.items()
        )
