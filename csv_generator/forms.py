# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from csv_generator.models import CsvGenerator, CsvGeneratorColumn
from django import forms


class CsvGeneratorForm(forms.ModelForm):
    """
    Model form for CsvGenerator
    """
    class Meta(object):
        """
        Django properties
        """
        model = CsvGenerator
        exclude = ()


class CsvGeneratorColumnForm(forms.ModelForm):
    """
    Model form for CsvGeneratorColumn
    """
    class Meta(object):
        """
        Django properties
        """
        model = CsvGeneratorColumn
        exclude = ()
