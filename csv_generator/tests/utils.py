# -*- coding: utf-8 -*-
"""
Test utils for the csv_generator app
"""
from __future__ import unicode_literals
from csv_generator.tests.factories import CsvGeneratorFactory
from csv_generator.tests.factories import CsvGeneratorColumnFactory
from django.test import TestCase


class CsvGeneratorTestCase(TestCase):
    """
    Test case for CsvGenerator models
    """
    def setUp(self):
        """
        Sets up the test case
        """
        super(CsvGeneratorTestCase, self).setUp()
        self.generator_1 = CsvGeneratorFactory.create()
        self.generator_2 = CsvGeneratorFactory.create()
        self.generator_3 = CsvGeneratorFactory.create()
        self.generator_4 = CsvGeneratorFactory.create()
        self.generator_5 = CsvGeneratorFactory.create()


class CsvGeneratorColumnTestCase(CsvGeneratorTestCase):
    """
    Test case for CsvGeneratorColumn models
    """
    def setUp(self):
        """
        Sets up the test case
        """
        super(CsvGeneratorColumnTestCase, self).setUp()
        self.column_1 = CsvGeneratorColumnFactory.create(
            generator=self.generator_1,
            model_field='title'
        )
        self.column_2 = CsvGeneratorColumnFactory.create(
            generator=self.generator_1,
            model_field='text'
        )
        self.column_3 = CsvGeneratorColumnFactory.create(
            generator=self.generator_1,
            model_field='date_created'
        )
        self.column_4 = CsvGeneratorColumnFactory.create(
            generator=self.generator_2,
            model_field='title'
        )
        self.column_5 = CsvGeneratorColumnFactory.create(
            generator=self.generator_2,
            model_field='text'
        )
        self.column_6 = CsvGeneratorColumnFactory.create(
            generator=self.generator_3,
            model_field='title'
        )
        self.column_7 = CsvGeneratorColumnFactory.create(
            generator=self.generator_3,
            model_field='text'
        )
        self.column_8 = CsvGeneratorColumnFactory.create(
            generator=self.generator_4,
            model_field='title'
        )
        self.column_9 = CsvGeneratorColumnFactory.create(
            generator=self.generator_4,
            model_field='text'
        )
        self.column_10 = CsvGeneratorColumnFactory.create(
            generator=self.generator_4,
            model_field='date_created'
        )
