# -*- coding: utf-8 -*-
"""
csv_generator app test Models
"""
from __future__ import unicode_literals
from csv_generator.admin import CsvExportAdmin
from django.contrib import admin
from django.db import models


class TestModel(models.Model):
    """
    Dummy model for testing
    """
    title = models.CharField(
        max_length=255,
        verbose_name='Model title'
    )
    text = models.TextField()
    other_model = models.ForeignKey('TestModel2', blank=True, null=True)
    other_model_2 = models.OneToOneField('TestModel3', blank=True, null=True)
    other_models = models.ManyToManyField('TestModel4', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def test_attr(self):
        return 'This is a callable test attr for \'{0}\''.format(self.title)


class TestModel2(models.Model):
    """
    Dummy model for testing
    """
    title = models.CharField(
        max_length=255,
        verbose_name='Model title'
    )
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)


class TestModel3(models.Model):
    """
    Dummy model for testing
    """
    title = models.CharField(
        max_length=255,
        verbose_name='Model title'
    )
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)


class TestModel4(models.Model):
    """
    Dummy model for testing
    """
    title = models.CharField(
        max_length=255,
        verbose_name='Model title'
    )
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

admin.site.register(TestModel2, CsvExportAdmin)
