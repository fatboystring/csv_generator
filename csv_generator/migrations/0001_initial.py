# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-09 15:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='CsvGenerator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('include_headings', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='CsvGeneratorColumn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_heading', models.CharField(blank=True, max_length=255, null=True)),
                ('model_field', models.CharField(max_length=255)),
                ('order', models.PositiveIntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('generator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='csv_generator.CsvGenerator')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
