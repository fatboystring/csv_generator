# -*- coding: utf-8 -*-
from csv_generator.models import CsvGenerator, CsvGeneratorColumn
from django.contrib import admin


admin.site.register(CsvGenerator)
admin.site.register(CsvGeneratorColumn)
