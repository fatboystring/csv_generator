# -*- coding: utf-8 -*-
"""
Tests the csv_generator CsvGenerator model
"""
from __future__ import unicode_literals
from csv_generator.models import CsvGenerator
from csv_generator.tests.factories import TestModelFactory, TestModel2Factory
from csv_generator.tests.models import TestModel, TestModel2
from csv_generator.tests.utils import CsvGeneratorTestCase
from csv_generator.tests.utils import CsvGeneratorColumnTestCase
from csv_generator.utils import UnicodeWriter
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.http import HttpResponse
from django.test import TestCase, override_settings
from mock import Mock, patch
import StringIO


class SimpleCsvGeneratorTestCase(TestCase):
    """
    Tests the CsvGenerator model
    """
    def test_title_field(self):
        """
        The title field should be defined
        """
        field = CsvGenerator._meta.get_field('title')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 255)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_include_headings_field(self):
        """
        The include_headings field should be defined
        """
        field = CsvGenerator._meta.get_field('include_headings')
        self.assertIsInstance(field, models.BooleanField)
        self.assertTrue(field.default)

    def test_content_type_field(self):
        """
        The content_type field should be defined
        """
        field = CsvGenerator._meta.get_field('content_type')
        self.assertIsInstance(field, models.ForeignKey)
        self.assertEqual(field.rel.to, ContentType)
        self.assertEqual(field.related_query_name(), '+')
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_date_created_field(self):
        """
        The date_created field should be defined
        """
        field = CsvGenerator._meta.get_field('date_created')
        self.assertIsInstance(field, models.DateTimeField)
        self.assertTrue(field.auto_now_add)

    def test_date_updated_field(self):
        """
        The date_updated field should be defined
        """
        field = CsvGenerator._meta.get_field('date_updated')
        self.assertIsInstance(field, models.DateTimeField)
        self.assertTrue(field.auto_now)

    def test_unicode(self):
        """
        The models title should be used as its unicode representation
        """
        instance = CsvGenerator(title='test title')
        self.assertEqual('test title', str(instance))


class CsvGeneratorModelTestCase(CsvGeneratorTestCase):
    """
    Tests the CsvGenerator Model
    """
    def test_get_meta_class(self):
        """
        The method should return the meta class for the associated content type
        """
        self.assertEqual(self.generator_1.get_meta_class(), TestModel._meta)

    @override_settings(
        CSV_GENERATOR_WRITER_CLASS='csv_generator.utils.UnicodeWriter'
    )
    def test_get_csv_writer_class(self):
        """
        The method should return the correct CSV Writer class
        """
        self.assertEqual(
            UnicodeWriter,
            self.generator_1._get_csv_writer_class()
        )

    @override_settings(
        CSV_GENERATOR_WRITER_CLASS='csv_generator.utils.UnicodeWriter'
    )
    def test_get_csv_writer(self):
        """
        The method should return a CSV Writer instance
        """
        mocked_file = Mock()
        instance = self.generator_1._get_csv_writer(mocked_file)
        self.assertIsInstance(instance, UnicodeWriter)
        self.assertEqual(instance.stream, mocked_file)

    def test__resolve_attribute(self):
        """
        The _resolve_attribute method should return the correct value
        """
        self.assertEqual(
            self.generator_1._resolve_attribute(
                TestModel(title='Test title'),
                'title'
            ),
            'Test title'
        )

    def test__resolve_attribute_returns_empty_string(self):
        """
        The method should return an empty string for a missing attribute
        """
        self.assertEqual(
            self.generator_1._resolve_attribute(
                TestModel(title='Test title'),
                'phantom_attribute'
            ),
            ''
        )

    @override_settings(CSV_GENERATOR_AVAILABLE_ATTRIBUTES={
        'all': {'all_attr': 'All Attribute'},
        'tests.testmodel': {'test_attr': 'Test Attribute'}
    })
    def test__resolve_attribute_calls_method(self):
        """
        The method should return an empty string for a missing attribute
        """
        instance = TestModel(title='Test title')
        self.assertEqual(
            self.generator_1._resolve_attribute(instance, 'test_attr'),
            instance.test_attr()
        )

    @override_settings(CSV_GENERATOR_AVAILABLE_ATTRIBUTES={
        'all': {'all_attr': 'All Attribute'},
        'tests.testmodel': {'test_attr': 'Test Attribute'}
    })
    def test_all_attributes(self):
        """
        Gets all attributes for the instance
        """
        attributes = {}
        for descriptor_class in self.generator_1.CSV_GENERATOR_ATTRIBUTE_DESCRIPTOR_CLASSES:
            attributes.update(descriptor_class.for_model(TestModel))
        self.assertEqual(attributes, self.generator_1.all_attributes)


class CsvGeneratorGenerateModelTestCase(CsvGeneratorColumnTestCase):
    """
    Tests the CsvGenerator Models generate method
    """
    def setUp(self):
        super(CsvGeneratorGenerateModelTestCase, self).setUp()
        self.instance_1 = TestModelFactory.create()
        self.instance_2 = TestModelFactory.create()
        self.instance_3 = TestModelFactory.create()
        self.instance_4 = TestModel2Factory.create()
        self.instance_5 = TestModel2Factory.create()
        self.instance_6 = TestModel2Factory.create()

    def test_generate_raises_exception(self):
        """
        The method should raise an exception if passed an invalid queryset
        """
        self.assertRaises(
            ImproperlyConfigured,
            self.generator_1.generate,
            StringIO.StringIO(),
            TestModel2.objects.all()
        )

    @patch('csv_generator.models.CsvGenerator._get_csv_writer')
    def test_generate_instantiates_csv_writer(self, patched_method):
        """
        The generate method should call _get_csv_writer
        """
        file_mock = Mock()
        self.generator_1.generate(file_mock, TestModel.objects.all())
        patched_method.assert_called_with(file_mock)

    @patch('csv_generator.models.CsvGenerator._get_csv_writer')
    def test_generate_instantiates_csv_writer(self, patched_method):
        """
        The generate method should call _get_csv_writer
        """
        file_mock = Mock()
        self.generator_1.generate(file_mock, TestModel.objects.all())
        patched_method.assert_called_with(file_mock)

    @patch('csv_generator.models.CsvGenerator._get_csv_writer')
    def test_generate_returns_handle(self, patched_method):
        """
        The generate method should return the handle
        """
        patched_method.return_value = Mock(methods=['writerow', 'writerows'])
        file_mock = Mock()
        self.assertEqual(
            file_mock,
            self.generator_1.generate(file_mock, TestModel.objects.all())
        )

    @patch('csv_generator.models.CsvGenerator._get_csv_writer')
    def test_generate_writes_headings(self, patched_method):
        """
        The generate method should write csv headings
        """
        patched_method.return_value = Mock(methods=['writerow', 'writerows'])
        self.generator_1.include_headings = True
        self.generator_1.save()
        self.generator_1.generate(Mock(), TestModel.objects.all())
        patched_method.return_value.writerow.assert_any_call(
            self.generator_1.columns.column_headings()
        )
        self.assertEqual(
            patched_method.return_value.writerow.call_count,
            self.generator_1.columns.count() + 1
        )

    @patch('csv_generator.models.CsvGenerator._get_csv_writer')
    def test_generate_not_writes_headings(self, patched_method):
        """
        The generate method should not write csv headings
        """
        patched_method.return_value = Mock(methods=['writerow', 'writerows'])
        self.generator_1.include_headings = False
        self.generator_1.save()
        self.generator_1.generate(Mock(), TestModel.objects.all())
        self.assertEqual(
            patched_method.return_value.writerow.call_count,
            self.generator_1.columns.count()
        )

    @patch('csv_generator.models.CsvGenerator._get_csv_writer')
    def test_generate_writes_rows(self, patched_method):
        """
        The generate method should write rows to the CSV
        """
        patched_method.return_value = Mock(methods=['writerow', 'writerows'])
        field_names = map(
            lambda x: x.model_field,
            self.generator_1.columns.all()
        )
        self.generator_1.generate(Mock(), TestModel.objects.all())
        patched_method.return_value.writerow.assert_any_call(map(
            lambda x: '{0}'.format(getattr(self.instance_1, x, '')), field_names
        ))
        patched_method.return_value.writerow.assert_any_call(map(
            lambda x: '{0}'.format(getattr(self.instance_2, x, '')), field_names
        ))
        patched_method.return_value.writerow.assert_any_call(map(
            lambda x: '{0}'.format(getattr(self.instance_3, x, '')), field_names
        ))

    def test_handles_unicode(self):
        """
        The csv generator should not error when accented characters are passed to the csv generator
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="my_csv.csv"'
        self.instance_1.title = 'áéíóúüñ¿¡'
        self.instance_1.save()
        self.instance_2.title = '会意字 / 會意字'
        self.instance_2.save()
        self.generator_1.generate(response, TestModel.objects.all())


class CsvGeneratorQuerySetTestCase(CsvGeneratorTestCase):
    """
    Tests the CsvGenerator queryset methods
    """
    def setUp(self):
        super(CsvGeneratorQuerySetTestCase, self).setUp()
        CsvGenerator.objects.filter(pk__in=[
            self.generator_1.pk,
            self.generator_3.pk,
            self.generator_5.pk
        ]).update(content_type=ContentType.objects.get_for_model(TestModel))
        CsvGenerator.objects.filter(pk__in=[
            self.generator_2.pk,
            self.generator_4.pk
        ]).update(content_type=ContentType.objects.get_for_model(TestModel2))

    def test_for_content_type(self):
        """
        The content_type method should return instances for the content type
        """
        content_type = ContentType.objects.get_for_model(TestModel)
        qs = CsvGenerator.objects.for_content_type(content_type)
        self.assertEqual(qs.count(), 3)
        self.assertIn(self.generator_1, qs)
        self.assertIn(self.generator_3, qs)
        self.assertIn(self.generator_5, qs)

    def test_for_content_type_id(self):
        """
        The for_content_type_id method should return the correct instances
        """
        content_type = ContentType.objects.get_for_model(TestModel)
        qs = CsvGenerator.objects.for_content_type_id(content_type.pk)
        self.assertEqual(qs.count(), 3)
        self.assertIn(self.generator_1, qs)
        self.assertIn(self.generator_3, qs)
        self.assertIn(self.generator_5, qs)

    def test_for_model(self):
        """
        The for_model method should return instances for the provided model
        """
        qs = CsvGenerator.objects.for_model(TestModel)
        self.assertEqual(qs.count(), 3)
        self.assertIn(self.generator_1, qs)
        self.assertIn(self.generator_3, qs)
        self.assertIn(self.generator_5, qs)
