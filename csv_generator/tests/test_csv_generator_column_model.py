# -*- coding: utf-8 -*-
"""
Tests the csv_generator CsvGeneratorColumn model
"""
from __future__ import unicode_literals
from csv_generator.models import CsvGenerator, CsvGeneratorColumn
from csv_generator.tests.models import TestModel
from csv_generator.tests.utils import CsvGeneratorColumnTestCase
from django.db import models
from django.test import override_settings, TestCase


class SimpleCsvGeneratorColumnTestCase(TestCase):
    """
    Tests the CsvGenerator model
    """
    def test_column_heading_field(self):
        """
        The column_heading field should be defined
        """
        field = CsvGeneratorColumn._meta.get_field('column_heading')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 255)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_model_field_field(self):
        """
        The model_field field should be defined
        """
        field = CsvGeneratorColumn._meta.get_field('model_field')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 255)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_generator_field(self):
        """
        The generator field should be defined
        """
        field = CsvGeneratorColumn._meta.get_field('generator')
        self.assertIsInstance(field, models.ForeignKey)
        self.assertEqual(field.rel.to, CsvGenerator)
        self.assertEqual(field.related_query_name(), 'columns')
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_date_created_field(self):
        """
        The date_created field should be defined
        """
        field = CsvGeneratorColumn._meta.get_field('date_created')
        self.assertIsInstance(field, models.DateTimeField)
        self.assertTrue(field.auto_now_add)

    def test_date_updated_field(self):
        """
        The date_updated field should be defined
        """
        field = CsvGeneratorColumn._meta.get_field('date_updated')
        self.assertIsInstance(field, models.DateTimeField)
        self.assertTrue(field.auto_now)


class CsvGeneratorColumnModelTestCase(CsvGeneratorColumnTestCase):
    """
    Tests the CsvGenerator model
    """
    def test_get_column_heading(self):
        """
        The get_column_heading method should return the defined title
        """
        self.column_1.column_heading = 'Test column title'
        self.column_1.save()
        self.assertEqual(
            self.column_1.get_column_heading(),
            'Test column title'
        )

    def test_get_column_heading_verbose(self):
        """
        The get_column_heading method should return the fields verbose name
        """
        self.column_1.model_field = 'title'
        self.assertEqual(
            self.column_1.get_column_heading(),
            TestModel._meta.get_field('title').verbose_name
        )

    @override_settings(CSV_GENERATOR_AVAILABLE_ATTRIBUTES={
        'tests.testmodel': {'test_attr': 'Test Attribute'}
    })
    def test_get_column_heading_model_attribute(self):
        """
        The get_column_heading method should return the model attributes name
        """
        self.column_1.model_field = 'test_attr'
        self.assertEqual(self.column_1.get_column_heading(), 'Test Attribute')


class CsvGeneratorColumnQuerySetTestCase(CsvGeneratorColumnTestCase):
    """
    Tests the CsvGeneratorColumn queryset methods
    """
    def setUp(self):
        super(CsvGeneratorColumnQuerySetTestCase, self).setUp()
        CsvGeneratorColumn.objects.filter(pk=self.column_1.pk).update(order=4)
        CsvGeneratorColumn.objects.filter(pk=self.column_2.pk).update(order=6)
        CsvGeneratorColumn.objects.filter(pk=self.column_3.pk).update(order=3)
        CsvGeneratorColumn.objects.filter(pk=self.column_4.pk).update(order=5)
        CsvGeneratorColumn.objects.filter(pk=self.column_5.pk).update(order=7)
        CsvGeneratorColumn.objects.filter(pk=self.column_6.pk).update(order=2)
        CsvGeneratorColumn.objects.filter(pk=self.column_7.pk).update(order=8)
        CsvGeneratorColumn.objects.filter(pk=self.column_8.pk).update(order=1)
        CsvGeneratorColumn.objects.filter(pk=self.column_9.pk).update(order=10)
        CsvGeneratorColumn.objects.filter(pk=self.column_10.pk).update(order=9)

    def test_queryset_ordering(self):
        """
        The queryset should be ordered according to the order field
        """
        qs = CsvGeneratorColumn.objects.all()
        self.assertEqual(qs[0].pk, self.column_8.pk)
        self.assertEqual(qs[1].pk, self.column_6.pk)
        self.assertEqual(qs[2].pk, self.column_3.pk)
        self.assertEqual(qs[3].pk, self.column_1.pk)
        self.assertEqual(qs[4].pk, self.column_4.pk)
        self.assertEqual(qs[5].pk, self.column_2.pk)
        self.assertEqual(qs[6].pk, self.column_5.pk)
        self.assertEqual(qs[7].pk, self.column_7.pk)
        self.assertEqual(qs[8].pk, self.column_10.pk)
        self.assertEqual(qs[9].pk, self.column_9.pk)

    def test_column_headings(self):
        """
        The column_headings method should return column headings
        """
        self.assertEqual(
            CsvGeneratorColumn.objects.column_headings(),
            [
                self.column_8.get_column_heading(),
                self.column_6.get_column_heading(),
                self.column_3.get_column_heading(),
                self.column_1.get_column_heading(),
                self.column_4.get_column_heading(),
                self.column_2.get_column_heading(),
                self.column_5.get_column_heading(),
                self.column_7.get_column_heading(),
                self.column_10.get_column_heading(),
                self.column_9.get_column_heading()
            ]
        )
