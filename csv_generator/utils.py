# -*- coding: utf-8 -*-
"""
Utils for the csv_generator app
"""
from __future__ import unicode_literals
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields.related import RelatedField
from django.utils.module_loading import import_string
import codecs
import csv


try:
    import cStringIO

except ImportError:
    class UnicodeWriter(object):
        """
        A CSV writer which will write rows to CSV file "f"
        which is encoded in the given encoding.
        """

        def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwargs):
            """
            Instantiates the UnicodeWriter instance

            :param f: File like object to write CSV data to
            :param dialect: The dialect for the CSV
            :param encoding: The CSV encoding
            :param kwargs: Keyword args
            """
            self.writer = csv.writer(f)

        def writerow(self, row):
            self.writer.writerow(row)

        def writerows(self, rows):
            for row in rows:
                self.writer.writerow(row)

else:
    class UnicodeWriter(object):
        """
        A CSV writer which will write rows to CSV file "f"
        which is encoded in the given encoding.
        """
        def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwargs):
            """
            Instantiates the UnicodeWriter instance

            :param f: File like object to write CSV data to
            :param dialect: The dialect for the CSV
            :param encoding: The CSV encoding
            :param kwargs: Keyword args
            """
            self.queue = cStringIO.StringIO()
            self.writer = csv.writer(self.queue, dialect=dialect, **kwargs)
            self.stream = f
            self.encoder = codecs.getincrementalencoder(encoding)()

        def writerow(self, row):
            """
            Writes a row of CSV data to the file

            :param row: List of values to write to the csv file
            :type row: list[str|unicode]
            """
            self.writer.writerow([s.encode("utf-8") for s in row])
            data = self.queue.getvalue()
            data = self.encoder.encode(data.decode("utf-8"))
            self.stream.write(data)
            self.queue.truncate(0)

        def writerows(self, rows):
            """
            Writes a list of CSV data rows to the target file

            :param rows: List of CSV rows
            :type rows: list[list]
            """
            for row in rows:
                self.writerow(row)


def get_csv_writer_class():
    """
    Helper function to get a csv writer class
    depending on the major python version being used

    :return: class
    """
    writer = UnicodeWriter
    if hasattr(settings, 'CSV_GENERATOR_WRITER_CLASS'):
        try:
            writer = import_string(settings.CSV_GENERATOR_WRITER_CLASS)
        except ImportError:
            pass
    return writer


def get_related_model_for_field(field):
    """
    Helper function for retrieving the related model for a model field

    :param field: Django model field instance
    :return: Django model class
    """
    if not isinstance(field, RelatedField):
        raise ImproperlyConfigured(
            'Expected field "{0}" to be an instance of django.db.models.'
            'fields.related.RelatedField'.format(field.__class__.__name__)
        )

    if hasattr(field, 'related_model'):
        return field.related_model
    return field.rel.to
