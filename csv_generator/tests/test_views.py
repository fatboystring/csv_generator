# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from csv_generator.forms import SelectCsvGeneratorForm
from csv_generator.models import CsvGenerator
from csv_generator.views import CsvExportView
from csv_generator.tests.models import TestModel
from csv_generator.tests.utils import CsvGeneratorTestCase
from django.test import RequestFactory
from django.views.generic import FormView
from mock import patch


class CsvExportViewTestCase(CsvGeneratorTestCase):
    """
    Tests the SelectCsvGeneratorForm
    """
    def setUp(self):
        super(CsvExportViewTestCase, self).setUp()
        self.factory = RequestFactory()
        self.view = CsvExportView.as_view()

    def test_extends_form_view(self):
        """
        The view should extend django FormView
        """
        self.assertTrue(issubclass(CsvExportView, FormView))

    def test_inaccessible_via_get(self):
        """
        The view should not be accessible via HTTP GET
        """
        response = self.view(self.factory.get('/fake-path/'))
        self.assertEqual(response.status_code, 405)

    def test_renders(self):
        """
        The view should render
        """
        queryset = TestModel.objects.all()
        generators = CsvGenerator.objects.for_model(TestModel)
        request = self.factory.post('/fake-path/')
        response = self.view(request, generators=generators, queryset=queryset)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('admin/csv_generator/csv_generator_select.html')
        self.assertEqual(response.context_data['title'], 'Export to CSV')
        self.assertEqual(response.context_data['queryset'], queryset)
        self.assertIsInstance(
            response.context_data['form'],
            SelectCsvGeneratorForm
        )

    @patch('csv_generator.views.CsvExportView.render_csv_to_response')
    def test_calls_render_csv_to_response_if_one_generator(self, patched):
        """
        The view should call render_csv_to_response if only one generator exists
        """
        queryset = TestModel.objects.all()
        generators = CsvGenerator.objects.filter(pk__in=[self.generator_1.pk])
        request = self.factory.post('/fake-path/')
        self.view(request, generators=generators, queryset=queryset)
        patched.assert_called_with(self.generator_1, queryset)

    @patch('csv_generator.views.CsvExportView.render_csv_to_response')
    def test_calls_render_csv_to_response_if_generator_selected(self, patched):
        """
        The view should call render_csv_to_response if a generator was selected
        """
        raise Exception('Not yet implemented')

    def test_render_csv_to_response(self):
        """
        The render_csv_to_response method should return a csv response
        """
        raise Exception('Not yet implemented')
