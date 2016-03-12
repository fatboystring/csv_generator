# -*- coding: utf-8 -*-
"""
Views for the csv_generator app
"""
from __future__ import unicode_literals
from csv_generator.forms import SelectCsvGeneratorForm
from django.contrib import admin
from django.http import HttpResponse
from django.views.generic import FormView

import datetime


class CsvExportView(FormView):
    """
    View for exporting a CSV file through the django admin
    """
    form_class = SelectCsvGeneratorForm
    template_name = 'admin/csv_generator/csv_generator_select.html'
    http_method_names = ['post']

    @staticmethod
    def render_csv_to_response(generator, queryset):
        """
        Method for rendering a CSV response

        :param generator: Generator model instance
        :type generator: csv_generator.models.CsvGenerator

        :param queryset: QuerySet of model instances to generate the CSV from
        :type queryset: django.db.models.query.QuerySet

        :return: HttpResponse instance
        """
        response = HttpResponse(content_type='text/csv')
        content_disposition = 'attachment; filename="{0}-{1}.csv"'.format(
            generator.title, datetime.datetime.now()
        )
        response['Content-Disposition'] = content_disposition
        return generator.generate(response, queryset)

    def post(self, request, *args, **kwargs):
        """
        Custom post method
        Either exports a CSV or displays a form with errors

        :param request: Http Request instance
        :type request: django.http.HttpRequest

        :param args: Default positional args
        :type args: ()

        :param kwargs: Default keyword args
        :type kwargs: {}

        :return: Http Response instance
        """
        queryset = kwargs.get('queryset')
        generators = kwargs.get('generators')

        if generators.count() == 1:
            return self.render_csv_to_response(generators[0], queryset)

        form = self.form_class(generators=generators)
        if 'post' in request.POST:
            form = self.form_class(data=request.POST, generators=generators)
            if form.is_valid():
                generator = form.cleaned_data.get('generator')
                return self.render_csv_to_response(generator, queryset)

        return self.render_to_response({
            'title': 'Export to CSV',
            'form': form,
            'opts': queryset.model._meta,
            'queryset': queryset,
            'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME
        })
