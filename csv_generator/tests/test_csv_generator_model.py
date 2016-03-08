from __future__ import unicode_literals
from csv_generator.models import CsvGenerator
from csv_generator.tests.factories import TestModel2Factory
from csv_generator.tests.models import TestModel, TestModel2
from csv_generator.tests.utils import CsvGeneratorTestCase
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.test import TestCase
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
        self.assertEqual('test title', unicode(instance))


class CsvGeneratorModelTestCase(CsvGeneratorTestCase):
    """
    Tests the CsvGenerator Model
    """
    def test_available_fields(self):
        """
        The available_fields property should return a dict of model fields
        """
        self.assertIsInstance(
            self.generator_1.available_fields['title'],
            models.CharField
        )
        self.assertIsInstance(
            self.generator_1.available_fields['text'],
            models.TextField
        )
        self.assertIsInstance(
            self.generator_1.available_fields['date_created'],
            models.DateTimeField
        )

    def test_available_field_names(self):
        """
        The available_field_names property should return a list of field names
        """
        self.assertIn('title', self.generator_1.available_field_names)
        self.assertIn('text', self.generator_1.available_field_names)
        self.assertIn('date_created', self.generator_1.available_field_names)

    def test_get_meta_class(self):
        """
        The method should return the meta class for the associated content type
        """
        self.assertEqual(self.generator_1.get_meta_class(), TestModel._meta)

    def test_generate_raises_exception(self):
        """
        The method should raise an exception if passed an invalid queryset
        """
        TestModel2Factory.create()
        TestModel2Factory.create()
        TestModel2Factory.create()
        self.assertRaises(
            ImproperlyConfigured,
            self.generator_1.generate,
            StringIO.StringIO(),
            TestModel2.objects.all()
        )
