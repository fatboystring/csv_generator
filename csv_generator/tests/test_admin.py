# -*- coding: utf-8 -*-
"""
Tests the csv_generator CsvGeneratorColumn Form
"""
from __future__ import unicode_literals
from csv_generator.admin import CsvGeneratorColumnInline, CsvGeneratorAdmin
from csv_generator.admin import CsvExportAdmin, ContentTypeListFilter
from csv_generator.forms import CsvGeneratorForm
from csv_generator.forms import CsvGeneratorColumnForm
from csv_generator.forms import CsvGeneratorColumnFormSet
from csv_generator.models import CsvGenerator, CsvGeneratorColumn
from csv_generator.tests.factories import CsvGeneratorFactory
from csv_generator.tests.models import TestModel
from csv_generator.tests.utils import CsvGeneratorTestCase
from django.contrib.admin import TabularInline
from django.contrib.admin import ModelAdmin
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, RequestFactory
from mock import Mock, patch


class CsvGeneratorColumnInlineTestCase(TestCase):
    """
    Tests the CsvGeneratorColumnInline class
    """
    def test_extends_tabular_inline(self):
        """
        The class should extend django.contrib.admin.TabularInline
        """
        self.assertTrue(issubclass(CsvGeneratorColumnInline, TabularInline))

    def test_model(self):
        """
        The class should use the CsvGeneratorColumn model
        """
        self.assertEqual(CsvGeneratorColumnInline.model, CsvGeneratorColumn)

    def test_form(self):
        """
        The class should use the CsvGeneratorColumnForm form
        """
        self.assertEqual(CsvGeneratorColumnInline.form, CsvGeneratorColumnForm)

    def test_formset(self):
        """
        The class should use the CsvGeneratorColumn model
        """
        self.assertEqual(
            CsvGeneratorColumnInline.formset,
            CsvGeneratorColumnFormSet
        )

    def test_verbose_name(self):
        """
        The class should use the correct verbose names
        """
        self.assertEqual(CsvGeneratorColumnInline.verbose_name, 'Column')
        self.assertEqual(
            CsvGeneratorColumnInline.verbose_name_plural,
            'Columns'
        )

    def test_extra(self):
        """
        The class should provide 0 extra forms
        """
        self.assertEqual(CsvGeneratorColumnInline.extra, 1)


class CsvGeneratorAdminTestCase(TestCase):
    """
    Tests the CsvGeneratorAdmin class
    """
    def setUp(self):
        super(CsvGeneratorAdminTestCase, self).setUp()
        self.admin = CsvGeneratorAdmin(CsvGenerator, Mock())
        self.request = RequestFactory().post('/fake-path/')
        self.instance = CsvGeneratorFactory.create()

    def test_extends_export_admin(self):
        """
        The class should extend CsvExportAdmin
        """
        self.assertTrue(issubclass(CsvGeneratorAdmin, CsvExportAdmin))

    def test_form(self):
        """
        The class should use the correct form
        """
        self.assertEqual(CsvGeneratorAdmin.form, CsvGeneratorForm)

    def test_filters(self):
        """
        content_type should be used as a list filter
        """
        self.assertEqual(
            CsvGeneratorAdmin.list_filter[0],
            ContentTypeListFilter
        )

    def test_get_readonly_fields_update(self):
        """
        The method should make the content_type field readonly
        """
        readonly_fields = self.admin.get_readonly_fields(
            self.request,
            obj=self.instance
        )
        self.assertIn('content_type', readonly_fields)

    def test_get_readonly_fields_create(self):
        """
        The method should make the content_type field readonly
        """
        self.instance.pk = None
        readonly_fields = self.admin.get_readonly_fields(
            self.request,
            obj=self.instance
        )
        self.assertNotIn('content_type', readonly_fields)

    def test_add_view_inlines(self):
        """
        The add_view should remove CsvGeneratorColumnInline from the inlines
        """
        self.admin.add_view(self.request)
        self.assertNotIn(CsvGeneratorColumnInline, self.admin.inlines)

    def test_change_view_inlines(self):
        """
        The change_view should add CsvGeneratorColumnInline to the inlines
        """
        self.admin.change_view(self.request, self.instance.pk)
        self.assertIn(CsvGeneratorColumnInline, self.admin.inlines)


class CsvExportAdminTestCase(CsvGeneratorTestCase):
    """
    Tests the CsvExportAdmin class
    """
    def setUp(self):
        super(CsvExportAdminTestCase, self).setUp()
        self.admin = CsvExportAdmin(CsvGenerator, Mock())
        self.request = RequestFactory().post('/fake-path/')
        self.instance = CsvGeneratorFactory.create()

    def test_extends_model_admin(self):
        """
        The class should extend ModelAdmin
        """
        self.assertTrue(issubclass(CsvExportAdmin, ModelAdmin))

    def test_actions(self):
        """
        The classes actions list should include 'export_to_csv'
        """
        self.assertIn('export_to_csv', CsvExportAdmin.actions)

    @patch('csv_generator.admin.CsvExportView.as_view')
    def test_export_to_csv_view(self, patched):
        """
        The export_to_csv_view returns view
        """
        patched.return_value = Mock()
        self.admin.export_to_csv_view(self.request, foo='bar')
        patched.return_value.assert_called_with(self.request, foo='bar')

    @patch('csv_generator.admin.CsvGenerator.objects.for_model')
    @patch('csv_generator.admin.CsvExportAdmin.export_to_csv_view')
    def test_export_to_csv(self, patched, for_model):
        """
        The method should call down to export_to_csv_view
        """
        queryset = CsvGenerator.objects.all()
        for_model.return_value = Mock()
        self.admin.export_to_csv(self.request, queryset)
        patched.assert_called_with(
            self.request,
            queryset=queryset,
            generators=for_model.return_value
        )


class ContentTypeListFilterTestCase(CsvGeneratorTestCase):
    """
    Tests the ContentTypeListFilter
    """
    def setUp(self):
        super(ContentTypeListFilterTestCase, self).setUp()
        self.admin = CsvGeneratorAdmin(CsvGenerator, Mock())
        self.request = RequestFactory().post('/fake-path/')
        self.filter = ContentTypeListFilter(
            self.request, {}, CsvGenerator, self.admin
        )

    def test_title(self):
        """
        The filters title should be 'Content Type'
        """
        self.assertEqual(ContentTypeListFilter.title, 'Content Type')

    def test_parameter_name(self):
        """
        The parameter name should be 'content_type'
        """
        self.assertEqual(ContentTypeListFilter.parameter_name, 'content_type')

    def test_lookups(self):
        """
        The lookups method should return only available content types
        """
        content_type = ContentType.objects.get_for_model(TestModel)
        lookups = self.filter.lookups(self.request, self.admin)
        self.assertEqual(len(lookups), 1)
        self.assertEqual(lookups[0][0], content_type.pk)
        self.assertEqual(lookups[0][1], content_type.name)

    def test_queryset(self):
        """
        The lookups method should return only available content types
        """
        content_type = ContentType.objects.get_for_model(TestModel)
        list_filter = ContentTypeListFilter(
            self.request,
            {'content_type': content_type.pk},
            CsvGenerator,
            self.admin
        )
        request = RequestFactory().post('/fake-path/')
        queryset = list_filter.queryset(request, CsvGenerator.objects.all())
        self.assertEqual(queryset.count(), 5)

    def test_queryset_fails(self):
        """
        The lookups method should return only available content types
        """
        list_filter = ContentTypeListFilter(
            self.request,
            {'content_type': 1},
            CsvGenerator,
            self.admin
        )
        request = RequestFactory().post('/fake-path/')
        queryset = list_filter.queryset(request, CsvGenerator.objects.all())
        self.assertEqual(queryset.count(), 0)
