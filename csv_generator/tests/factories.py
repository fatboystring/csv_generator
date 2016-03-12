# -*- coding: utf-8 -*-
"""
csv_generator app model factories
"""
from __future__ import unicode_literals
from csv_generator.models import CsvGenerator, CsvGeneratorColumn
from csv_generator.tests.models import TestModel, TestModel2
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import factory


class CsvGeneratorFactory(factory.DjangoModelFactory):
    """
    Factory for CsvGenerator models
    """
    title = factory.Sequence(lambda x: 'Title {0}'.format(x))
    content_type = ContentType.objects.get_for_model(TestModel)

    class Meta(object):
        """
        Factory config
        """
        model = CsvGenerator


class CsvGeneratorColumnFactory(factory.DjangoModelFactory):
    """
    Factory for CsvGeneratorColumn models
    """
    model_field = factory.Sequence(lambda x: 'field_{0}'.format(x))
    generator = factory.SubFactory(CsvGeneratorFactory)
    order = factory.Sequence(lambda x: x)

    class Meta(object):
        """
        Factory config
        """
        model = CsvGeneratorColumn


class DummyModelFactory(factory.DjangoModelFactory):
    """
    Factory for generating dummy models
    """
    title = factory.Sequence(lambda n: 'Title {0}'.format(n))
    text = factory.Sequence(lambda n: 'Text {0}'.format(n))
    date_created = timezone.now()


class TestModelFactory(DummyModelFactory):
    """
    Factory for generating TestModel instances
    """
    class Meta(object):
        """
        Factory config
        """
        model = TestModel


class TestModel2Factory(DummyModelFactory):
    """
    Factory for generating TestModel2 instances
    """
    class Meta(object):
        """
        Factory config
        """
        model = TestModel2
