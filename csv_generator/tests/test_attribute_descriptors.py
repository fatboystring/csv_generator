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
    NoopDescriptor,
    ForeignKeyDescriptor
)
from csv_generator.tests.models import TestModel, TestModel2, TestModel3
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
        descriptor = FieldDescriptor.for_model(TestModel)
        self.assertEqual(descriptor['title'], TestModel._meta.get_field('title').verbose_name.capitalize())
        self.assertEqual(descriptor['text'], TestModel._meta.get_field('text').verbose_name.capitalize())
        self.assertEqual(
            descriptor['date_created'],
            TestModel._meta.get_field('date_created').verbose_name.capitalize()
        )

    def test_generates_instance(self):
        """
        The for_model class method should return the correct instance
        """
        self.assertIsInstance(FieldDescriptor.for_model(TestModel), FieldDescriptor)

    def test_get_fields_returns_fields(self):
        """
        The get_fields method of the class should return the model fields
        """
        fields = FieldDescriptor.get_fields(TestModel)
        field_names = map(lambda x: x.name, fields)
        self.assertEqual(len(fields), 4)
        self.assertIn('id', field_names)
        self.assertIn('text', field_names)
        self.assertIn('title', field_names)
        self.assertIn('date_created', field_names)


class AttributeDescriptorTestCase(CsvGeneratorTestCase):
    """
    Tests the AttributeDescriptor
    """
    @override_settings(CSV_GENERATOR_AVAILABLE_ATTRIBUTES={'foo': 'bar'})
    def test__get_available_attributes(self):
        """
        The _get_available_attributes method should return attributes
        """
        descriptor = AttributeDescriptor.for_model(TestModel)
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
        descriptor = AttributeDescriptor.for_model(TestModel)
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
        descriptor = AttributeDescriptor.for_model(TestModel)
        self.assertEqual(descriptor['all_attr'], 'Overridden Attribute')

    def test_generates_instance(self):
        """
        The for_model class method should return the correct instance
        """
        self.assertIsInstance(AttributeDescriptor.for_model(TestModel), AttributeDescriptor)


class NoopDescriptorTestCase(CsvGeneratorTestCase):
    """
    Tests the NoopDescriptor
    """
    def test_fields(self):
        """
        The resolver instance should contain the correct fields
        """
        resolver = NoopDescriptor.for_model(TestModel)
        self.assertEqual(resolver['__empty__'], 'Empty cell')

    def test_resolve_returns_empty_string(self):
        """
        The resolve method should return an empty string
        """
        resolver = NoopDescriptor.for_model(TestModel)
        self.assertEqual(resolver.resolve(self.generator_1, '__empty__'), '')

    def test_resolve_raises_exception(self):
        """
        The resolve method should raise an exception
        """
        resolver = NoopDescriptor.for_model(TestModel)
        self.assertRaises(DescriptorException, resolver.resolve, self.generator_1, 'foo')

    def test_generates_instance(self):
        """
        The for_model class method should return the correct instance
        """
        self.assertIsInstance(NoopDescriptor.for_model(TestModel), NoopDescriptor)


class ForeignKeyDescriptorTestCase(CsvGeneratorTestCase):
    """
    Tests the ForeignKeyDescriptor
    """
    def test_get_fields_returns_fields(self):
        """
        The get_fields method of the class should return the correct model fields
        """
        fields = ForeignKeyDescriptor.get_fields(TestModel)
        field_names = map(lambda x: x.name, fields)
        self.assertEqual(len(fields), 2)
        self.assertIn('other_model', field_names)
        self.assertIn('other_model_2', field_names)

    def test_generates_instance(self):
        """
        The for_model class method should return the correct instance
        """
        self.assertIsInstance(ForeignKeyDescriptor.for_model(TestModel), ForeignKeyDescriptor)

    def test_descriptor_follows_relations(self):
        """
        The descriptor should follow relations
        """
        descriptor = ForeignKeyDescriptor.for_model(TestModel)
        self.assertEqual(descriptor['other_model__title'], 'Other model ---> Model title')
        self.assertEqual(descriptor['other_model__text'], 'Other model ---> Text')
        self.assertEqual(descriptor['other_model__id'], 'Other model ---> Id')
        self.assertEqual(descriptor['other_model__date_created'], 'Other model ---> Date created')
        self.assertEqual(descriptor['other_model_2__title'], 'Other model 2 ---> Model title')
        self.assertEqual(descriptor['other_model_2__text'], 'Other model 2 ---> Text')
        self.assertEqual(descriptor['other_model_2__id'], 'Other model 2 ---> Id')
        self.assertEqual(descriptor['other_model_2__date_created'], 'Other model 2 ---> Date created')

    def test_resolve(self):
        """
        The descriptor should be able to resolve the field value across relationships
        """
        instance_3 = TestModel3.objects.create(title='Test Model 3 Title', text='Test text')
        instance_2 = TestModel2.objects.create(title='Test Model 2 Title', text='Test text')
        instance_1 = TestModel.objects.create(
            title='Test Model 1 Title',
            text='Test text',
            other_model=instance_2,
            other_model_2=instance_3
        )
        descriptor = ForeignKeyDescriptor.for_model(TestModel)
        self.assertEqual(descriptor.resolve(instance_1, 'other_model__title'), 'Test Model 2 Title')
        self.assertEqual(descriptor.resolve(instance_1, 'other_model_2__title'), 'Test Model 3 Title')

    def test_resolve_fails_gracefully(self):
        """
        The descriptor should return an empty string if a related model does not exist
        """
        instance_1 = TestModel.objects.create(title='Test Model 1 Title', text='Test text')
        descriptor = ForeignKeyDescriptor.for_model(TestModel)
        self.assertEqual(descriptor.resolve(instance_1, 'other_model__title'), '')
        self.assertEqual(descriptor.resolve(instance_1, 'other_model_2__title'), '')

    def test_get_descriptor_classes(self):
        """
        The get_descriptor_classes method should return a tuple containing the correct Descriptor classes
        """
        descriptor_classes = ForeignKeyDescriptor.get_descriptor_classes()
        self.assertIn(ForeignKeyDescriptor, descriptor_classes)
        self.assertIn(AttributeDescriptor, descriptor_classes)
        self.assertIn(FieldDescriptor, descriptor_classes)
        self.assertNotIn(NoopDescriptor, descriptor_classes)
