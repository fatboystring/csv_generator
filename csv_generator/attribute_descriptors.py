# -*- coding: utf-8 -*-
"""
Attribute descriptors for the csv_generator app
"""
from __future__ import unicode_literals
from django.conf import settings


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
        return str(value)

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
    def for_model(cls, model):
        """
        Class method for creating a descriptor instance
        for a given CsvGenerator model instance

        :param model: CsvGenerator model
        :type model: csv_generator.models.CsvGenerator

        :return: FieldDescriptor instance
        """
        return FieldDescriptor(
            map(
                lambda x: (x.name, x.verbose_name),
                model.get_meta_class().fields
            )
        )


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
            model.get_meta_class().app_label,
            model.get_meta_class().model_name
        )
        attributes = cls.get_available_attributes()
        all_attrs = attributes.get('all', {})
        model_attrs = attributes.get(model_label, {})
        all_attrs.update(model_attrs)
        return AttributeDescriptor(all_attrs)


class NoopResolver(BaseDescriptor):
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
        return NoopResolver({'__empty__': 'Empty cell'})

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
