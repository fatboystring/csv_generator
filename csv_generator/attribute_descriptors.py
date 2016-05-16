# -*- coding: utf-8 -*-
"""
Attribute descriptors for the csv_generator app
"""
from __future__ import unicode_literals
from django.conf import settings
from django.db import models


class DescriptorException(Exception):
    """
    Custom exception class for resolver errors
    """


class BaseDescriptor(dict):
    """
    Base class for attribute descriptors
    """
    def check_attr(self, attr_name):
        """
        Custom method for checking that a given attr exists

        :raises: DescriptorException
        """
        if attr_name not in self:
            raise DescriptorException('Attribute does not exist')

    def resolve(self, instance, attr_name):
        """
        Custom method for resolving an attribute on the model instance

        :param instance: The model instance to resolve the attribute from
        :type instance: django.db.models.Model

        :param attr_name: The name of the model attribute to resolve
        :type attr_name: unicode|str

        :return: unicode|str
        """
        self.check_attr(attr_name)
        value = getattr(instance, attr_name, '')
        if callable(value):
            value = value()
        return '{0}'.format(value)

    @classmethod
    def for_model(cls, model):
        """
        Method stub for generating a Descriptor instance for a CsvGenerator model instance

        :param model: CsvGenerator model
        :type model: csv_generator.models.CsvGenerator

        :raises: NotImplementedError
        """
        raise NotImplementedError('Not implemented')


class FieldDescriptor(BaseDescriptor):
    """
    Descriptor class for model fields on the model instance
    """

    @classmethod
    def get_fields(cls, model):
        """
        Method for getting the fields required for processing by the descriptor

        :param model: The model the get fields for
        :type model: django.db.models.Model

        :return: list of model fields
        """
        return filter(
            lambda x: not isinstance(x, (models.ForeignKey, models.ManyToManyField, models.OneToOneField)),
            model._meta.fields
        )

    @classmethod
    def for_model(cls, model):
        """
        Class method for creating a descriptor instance
        for a given CsvGenerator model instance

        :param model: Model instance
        :type model: csv_generator.models.CsvGenerator

        :return: FieldDescriptor instance
        """
        return FieldDescriptor(map(
            lambda x: (x.name, x.verbose_name.capitalize()),
            FieldDescriptor.get_fields(model)
        ))


class AttributeDescriptor(BaseDescriptor):
    """
    Descriptor class for attributes on the model class
    """
    @classmethod
    def get_available_attributes(cls):
        """
        Helper method to get extra attributes defined in the settings

        :return: dict
        """
        return getattr(
            settings,
            'CSV_GENERATOR_AVAILABLE_ATTRIBUTES',
            {}
        )

    @classmethod
    def for_model(cls, model):
        """
        Class method for creating a descriptor instance
        for a given CsvGenerator model instance

        :param model: CsvGenerator model
        :type model: csv_generator.models.CsvGenerator

        :return: AttributeDescriptor instance
        """
        model_label = '{0}.{1}'.format(
            model._meta.app_label,
            model._meta.model_name
        )
        attributes = cls.get_available_attributes()
        all_attrs = attributes.get('all', {})
        model_attrs = attributes.get(model_label, {})
        all_attrs.update(model_attrs)
        return AttributeDescriptor(all_attrs)


class ForeignKeyDescriptor(BaseDescriptor):
    """
    Descriptor for traversing foreign key relationships
    """
    @classmethod
    def get_descriptor_classes(cls):
        """
        Method for getting a tuple of descriptor classes that apply to related models

        :return: Tuple of descriptor classes
        """
        return FieldDescriptor, AttributeDescriptor, ForeignKeyDescriptor

    @classmethod
    def get_fields(cls, model):
        """
        Method for getting fields for the descriptor

        :param model: model instance
        :type model: django.db.models.Model

        """
        return filter(
            lambda x: isinstance(x, models.ForeignKey),
            model._meta.fields
        )

    @classmethod
    def field_data(cls, parent_field, child_field):
        """
        Generates and returns a tuple containing: (field_value, field_label)

        :param parent_field: The parent model field
        :param child_field: The child field

        :return: tuple[unicode, unicode]
        """
        return (
            '{0}__{1}'.format(parent_field.name, child_field[0]),
            '{0} ---> {1}'.format(
                parent_field.verbose_name.capitalize(),
                child_field[1].capitalize()
            )
        )

    @classmethod
    def process_field(cls, field):
        """
        Processes a given field on the model
        Resolves attributes/fields from the fields related model

        :param field: ForeignKey field from the parent model
        :return: Dict of related field data
        """
        field_map = {}

        for descriptor_class in cls.get_descriptor_classes():
            descriptor = descriptor_class.for_model(field.rel.to)
            field_map.update(descriptor)

        return dict([
            ForeignKeyDescriptor.field_data(field, other_model_field)
            for other_model_field in field_map.items()
        ])

    @classmethod
    def for_model(cls, model):
        """
        Class method for creating a descriptor instance
        for a given CsvGenerator model instance

        :param model: CsvGenerator model
        :type model: csv_generator.models.CsvGenerator

        :return: ForeignKeyDescriptor instance
        """
        fields_map = {}
        for field in ForeignKeyDescriptor.get_fields(model):
            fields_map.update(ForeignKeyDescriptor.process_field(field))
        return ForeignKeyDescriptor(**fields_map)

    def resolve(self, instance, attr_name):
        """
        Custom method for resolving an attribute across relations on the model instance

        :param instance: The model instance to resolve the attribute from
        :type instance: django.db.models.Model

        :param attr_name: The name of the model attribute to resolve
        :type attr_name: unicode|str

        :return: unicode|str
        """
        self.check_attr(attr_name)
        attr_names = attr_name.split('__')
        attr_name = attr_names.pop(0)
        value = getattr(instance, attr_name)

        if value:
            for descriptor_class in self.get_descriptor_classes():
                descriptor = descriptor_class.for_model(value.__class__)
                try:
                    value = descriptor.resolve(value, '__'.join(attr_names))
                except DescriptorException:
                    pass
                else:
                    break

        return '{0}'.format(value or '')


class NoopDescriptor(BaseDescriptor):
    """
    Class method for creating a descriptor instance
    for a given CsvGenerator model instance

    :param model: CsvGenerator model
    :type model: csv_generator.models.CsvGenerator

    :return: AttributeDescriptor instance
    """
    @classmethod
    def for_model(cls, model):
        """
        Class method for creating a descriptor instance
        for a given CsvGenerator model instance

        :param model: CsvGenerator model
        :type model: csv_generator.models.CsvGenerator

        :return: NoopResolver instance
        """
        return NoopDescriptor({'__empty__': 'Empty cell'})

    def resolve(self, instance, attr_name):
        """
        Custom method for resolving an attribute on the model instance

        :param instance: The model instance to resolve the attribute from
        :type instance: django.db.models.Model

        :param attr_name: The name of the model attribute to resolve
        :type attr_name: unicode|str

        :return: unicode|str
        """
        self.check_attr(attr_name)
        return ''
