# -*- coding: utf-8 -*-
"""
Tests the attribute_descriptors for the csv_generator
"""
from __future__ import unicode_literals
from csv_generator.attribute_descriptors import (
    DescriptorException,
    BaseDescriptor,
    AttributeDescriptor,
    FieldDescriptor,
    NoopResolver
)
from csv_generator.tests.models import TestModel
from csv_generator.tests.utils import CsvGeneratorTestCase
from django.test import override_settings


class BaseDescriptorTestCase(CsvGeneratorTestCase):
    """
    Tests the BaseDescriptor
    """
    def test_for_model_raises_exception(self):
        """
        The for_model classmethod should raise a NotImplementedError
        """
        self.assertRaises(NotImplementedError, BaseDescriptor.for_model, self.generator_1)

    def test_check_attr_success(self):
        """
        The check_attr method should not raise an exception
        """
        instance = BaseDescriptor(foo='bar')
        instance.check_attr('foo')

    def test_check_attr_fails(self):
        """
        The check_attr method should raise an exception
        """
        instance = BaseDescriptor(foo='bar')
        self.assertRaises(DescriptorException, instance.check_attr, 'bar')

    def test_resolve_returns_attribute(self):
        """
        The resolve method should return the attribute
        """
        instance = BaseDescriptor(title='title')
        self.assertEqual(
            self.generator_1.title,
            instance.resolve(self.generator_1, 'title')
        )

    def test_resolve_calls_method(self):
        """
        The resolve method should return the attribute
        """
        instance = BaseDescriptor(foo='foo')
        self.generator_1.foo = lambda: 'bar'
        self.assertEqual(instance.resolve(self.generator_1, 'foo'), 'bar')


class FieldDescriptorTestCase(CsvGeneratorTestCase):
    """
    Tests the FieldDescriptor
    """
    def test_fields(self):
        """
        The descriptor should be a dict of model fields
        """
        descriptor = FieldDescriptor.for_model(self.generator_1)
        self.assertEqual(descriptor['title'], TestModel._meta.get_field('title').verbose_name)
        self.assertEqual(descriptor['text'], TestModel._meta.get_field('text').verbose_name)
        self.assertEqual(descriptor['date_created'], TestModel._meta.get_field('date_created').verbose_name)

    def test_generates_instance(self):
        """
        The for_model class method should return the correct instance
        """
        self.assertIsInstance(FieldDescriptor.for_model(self.generator_1), FieldDescriptor)


class AttributeDescriptorTestCase(CsvGeneratorTestCase):
    """
    Tests the AttributeDescriptor
    """
    @override_settings(CSV_GENERATOR_AVAILABLE_ATTRIBUTES={'foo': 'bar'})
    def test__get_available_attributes(self):
        """
        The _get_available_attributes method should return attributes
        """
        descriptor = AttributeDescriptor.for_model(self.generator_1)
        attributes = descriptor.get_available_attributes()
        self.assertEqual(attributes, {'foo': 'bar'})

    @override_settings(CSV_GENERATOR_AVAILABLE_ATTRIBUTES={
        'all': {'all_attr': 'All Attribute'},
        'tests.testmodel': {'test_attr': 'Test Attribute'},
        'tests.testmodel2': {'test_attr_2': 'Test Attribute 2'},
    })
    def test_gets_attributes(self):
        """
        Gets available attributes for the instance
        """
        descriptor = AttributeDescriptor.for_model(self.generator_1)
        self.assertEqual(descriptor['all_attr'], 'All Attribute')
        self.assertEqual(descriptor['test_attr'], 'Test Attribute')
        self.assertNotIn('test_attr_2', descriptor)

    @override_settings(CSV_GENERATOR_AVAILABLE_ATTRIBUTES={
        'all': {'all_attr': 'All Attribute'},
        'tests.testmodel': {
            'test_attr': 'Test Attribute',
            'all_attr': 'Overridden Attribute'
        },
        'tests.testmodel2': {'test_attr_2': 'Test Attribute 2'},
    })
    def test_takes_model_attr_over_all(self):
        """
        The model attribute should take precedence over the all attribute
        """
        descriptor = AttributeDescriptor.for_model(self.generator_1)
        self.assertEqual(descriptor['all_attr'], 'Overridden Attribute')

    def test_generates_instance(self):
        """
        The for_model class method should return the correct instance
        """
        self.assertIsInstance(AttributeDescriptor.for_model(self.generator_1), AttributeDescriptor)


class NoopResolverTestCase(CsvGeneratorTestCase):
    """
    Tests the NoopResolver
    """
    def test_fields(self):
        """
        The resolver instance should contain the correct fields
        """
        resolver = NoopResolver.for_model(self.generator_1)
        self.assertEqual(resolver['__empty__'], 'Empty cell')

    def test_resolve_returns_empty_string(self):
        """
        The resolve method should return an empty string
        """
        resolver = NoopResolver.for_model(self.generator_1)
        self.assertEqual(resolver.resolve(self.generator_1, '__empty__'), '')

    def test_resolve_raises_exception(self):
        """
        The resolve method should raise an exception
        """
        resolver = NoopResolver.for_model(self.generator_1)
        self.assertRaises(DescriptorException, resolver.resolve, self.generator_1, 'foo')

    def test_generates_instance(self):
        """
        The for_model class method should return the correct instance
        """
        self.assertIsInstance(NoopResolver.for_model(self.generator_1), NoopResolver)
