# -*- coding: utf-8 -*-
"""
csv_generator app test Models
"""
from __future__ import unicode_literals
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
    date_created = models.DateTimeField()


class TestModel2(models.Model):
    """
    Dummy model for testing
    """
    title = models.CharField(
        max_length=255,
        verbose_name='Model title'
    )
    text = models.TextField()
    date_created = models.DateTimeField()
