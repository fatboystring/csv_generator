# -*- coding: utf-8 -*-
"""
Utils for the csv_generator app
"""
from __future__ import unicode_literals
import codecs
import csv
import cStringIO


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
