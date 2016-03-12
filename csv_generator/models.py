# -*- coding: utf-8 -*-
"""
Models for the csv_generator app
"""
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.module_loading import import_string


class CsvGeneratorQueryset(models.QuerySet):
    """
    QuerySet for CsvGenerator
    """
    def for_content_type_id(self, content_type_id):
        """
        Method to return a queryset of CsvGenerator
        model instances for a given content type

        :param content_type_id: ContentType model id
        :type content_type_id: int

        :return: QuerySet of CsvGenerator model instances
        """
        return self.filter(content_type_id=content_type_id)

    def for_content_type(self, content_type):
        """
        Method to return a queryset of CsvGenerator
        model instances for a given content type

        :param content_type: ContentType model
        :type content_type: django.contrib.contenttype.models.ContentType

        :return: QuerySet of CsvGenerator model instances
        """
        return self.filter(content_type=content_type)

    def for_model(self, model):
        """
        Method to return a queryset of CsvGenerator
        model instances for a given type of model

        :param model: Model class or instance
        :type model: django.db.models.Model

        :return: QuerySet of CsvGenerator model instances
        """
        return self.for_content_type(ContentType.objects.get_for_model(model))


class CsvGenerator(models.Model):
    """
    Model for storing a CSV Generator profile
    """
    title = models.CharField(max_length=255)
    include_headings = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, related_name='+')

    objects = CsvGeneratorQueryset.as_manager()

    def __unicode__(self):
        """
        Unicode representation of the instance

        :return: title
        """
        return self.title

    def get_meta_class(self):
        """
        Method to get the meta class for the linked content type

        :return: Meta class
        """
        return self.content_type.model_class()._meta

    @property
    def available_fields(self):
        """
        Method for getting available fields on the model

        :return: Dict of available fields on the model
        """
        return dict(map(lambda x: (x.name, x), self.get_meta_class().fields))

    @property
    def available_field_names(self):
        """
        Gets a list of available field names

        :return: List of field names for the linked model
        """
        return self.available_fields.keys()

    def get_field(self, field_name):
        """
        Method for getting a field from the associated model by its name

        :param field_name: The name of the field to retrieve
        :type field_name: str|unicode

        :return: Field
        """
        if field_name not in self.available_field_names:
            return None
        return self.get_meta_class().get_field(field_name)

    @property
    def csv_headings(self):
        """
        Gets the csv headings for the generator

        :return: List of CSV headings
        """
        return map(lambda x: x.get_column_heading(), self.columns.all())

    @staticmethod
    def _get_csv_writer_class():
        """
        Helper method to get the csv writer class

        :return: Csv Writer Class
        """
        csv_generator_writer_class_path = getattr(
            settings,
            'CSV_GENERATOR_WRITER_CLASS',
            'csv_generator.utils.UnicodeWriter'
        )
        return import_string(csv_generator_writer_class_path)

    def _get_csv_writer(self, handle, **kwargs):
        """
        Helper method to get a csv writer instance

        :return: Csv Writer instance
        """
        return self._get_csv_writer_class()(handle, **kwargs)

    def generate(self, handle, queryset, **kwargs):
        """
        Generates a csv file writing its contents to 'handle'

        :param handle: File like object to write contents of the CSV to
        :param queryset: Queryset of model instances to generate the CSV from
        :return: handle with csv contents written to it
        """
        expected_model = self.content_type.model_class()
        if queryset.model != expected_model:
            raise ImproperlyConfigured(
                'CSV Generator \'{0}\' generate method must be passed a '
                'queryset containing \'{1}\' model instances.  Received '
                'Queryset of \'{2}\' model instances instead'.format(
                    self, expected_model.__name__, queryset.model.__name__
                )
            )

        # Get a CSV writer
        writer = self._get_csv_writer(handle, **kwargs)
        # Write CSV headings if required
        if self.include_headings:
            writer.writerow(self.columns.column_headings())

        # Get a list of field names
        field_names = map(lambda x: x.model_field, self.columns.all())
        for instance in queryset:
            csv_row = map(
                lambda x: unicode(getattr(instance, x, '')),
                field_names
            )
            writer.writerow(csv_row)

        return handle


class CsvGeneratorColumnQueryset(models.QuerySet):
    """
    QuerySet for CsvGeneratorColumn
    """
    def column_headings(self):
        """
        Method to return a list of column headings for the CSV file

        :return: list of column heading strings
        """
        return map(lambda x: x.get_column_heading(), self)


class CsvGeneratorColumn(models.Model):
    """
    Model for storing a CSV Generator columns
    """
    column_heading = models.CharField(max_length=255, blank=True, null=True)
    model_field = models.CharField(max_length=255)
    generator = models.ForeignKey(CsvGenerator, related_name='columns')
    order = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = CsvGeneratorColumnQueryset.as_manager()

    class Meta(object):
        """
        Django properties
        """
        ordering = ['order']

    def get_column_heading(self):
        """
        Method to get the heading of the column

        :return: The column heading for the linked field
        """
        if self.column_heading:
            return self.column_heading
        else:
            return self.generator.get_field(self.model_field).verbose_name
