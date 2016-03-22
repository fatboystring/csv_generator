# -*- coding: utf-8 -*-
"""
Admin for the csv_generator app
"""
from __future__ import unicode_literals
from csv_generator.forms import CsvGeneratorForm, CsvGeneratorColumnForm
from csv_generator.forms import CsvGeneratorColumnFormSet
from csv_generator.models import CsvGenerator, CsvGeneratorColumn
from csv_generator.views import CsvExportView
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType


class ContentTypeListFilter(admin.SimpleListFilter):
    """
    List filter to filter results by content type
    Backwards compatible to django 1.7
    """
    title = 'Content Type'

    parameter_name = 'content_type'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each tuple is the
        coded value for the option that will appear in the URL query.
        The second element is the human-readable name for the option that
        will appear in the right sidebar.

        :param request: Http Request instance
        :type request: django.http.HttpRequest

        :param model_admin: Django modeladmin instance
        :type model_admin: django.contrib.admin.ModelAdmin

        :return: List of tuples
        """
        content_type_ids = model_admin.model.objects.values_list(
            'content_type', flat=True
        ).distinct()
        return map(
            lambda x: (x.pk, x.name),
            ContentType.objects.filter(pk__in=content_type_ids)
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value provided
        in the query string and retrievable via `self.value()`.

        :param request: Http Request instance
        :type request: django.http.HttpRequest

        :param queryset: Queryset of model instances
        :type queryset: django.db.models.query.QuerySet

        :return: Queryset of model instances
        """
        if self.value():
            return queryset.filter(content_type=self.value())
        else:
            return queryset


class CsvExportAdmin(admin.ModelAdmin):
    """
    Custom ModelAdmin class
    """
    actions = ['export_to_csv']

    @staticmethod
    def export_to_csv_view(request, **kwargs):
        """
        Helper method for rendering a view to export a queryset to csv

        :param request: Http Request instance
        :type request: django.http.HttpRequest

        :param kwargs: Default keyword args
        :type kwargs: {}

        :return: HttpResponse instance
        """
        return CsvExportView.as_view()(request, **kwargs)

    def export_to_csv(self, request, queryset):
        """
        Admin action allowing selected items to be exported as a csv file

        :param request: Http Request instance
        :type request: django.http.HttpRequest

        :param queryset: QuerySet of model instances to export
        :type queryset: django.db.models.query.QuerySet

        :return: Http response
        """
        return self.export_to_csv_view(
            request,
            queryset=queryset,
            generators=CsvGenerator.objects.for_model(self.model)
        )
    export_to_csv.short_description = "Export the selected items to csv"


class CsvGeneratorColumnInline(admin.TabularInline):
    """
    Inline model admin for CsvGeneratorColumn models
    """
    model = CsvGeneratorColumn
    form = CsvGeneratorColumnForm
    formset = CsvGeneratorColumnFormSet
    verbose_name = 'Column'
    verbose_name_plural = 'Columns'
    extra = 1


class CsvGeneratorAdmin(CsvExportAdmin):
    """
    Admin class for CsvGenerator models
    """
    form = CsvGeneratorForm
    list_filter = (ContentTypeListFilter,)

    def get_readonly_fields(self, request, obj=None):
        """
        Custom method for getting readonly fields
        We don't allow the content type to be changed after creation

        :param request: Http Request instance
        :param obj: Model instance we're editing

        :return: Tuple of readonly fields
        """
        readonly_fields = super(CsvGeneratorAdmin, self).get_readonly_fields(
            request, obj=obj
        )
        if obj and obj.pk:
            readonly_fields += ('content_type',)
        return readonly_fields

    def add_view(self, request, form_url='', extra_context=None):
        """
        Ensures the CsvGeneratorColumnInline is not in the inlines

        :param request: HttpRequest instance
        :param form_url: URL for the form
        :param extra_context: Extra context to pass to the template

        :return: HttpResponse
        """
        self.inlines = ()
        return super(CsvGeneratorAdmin, self).add_view(
            request,
            form_url=form_url,
            extra_context=extra_context
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Adds the CsvGeneratorColumnInline for the change view only

        :param request: HttpRequest instance
        :param object_id: ID of the object we're editing
        :param form_url: URL for the form
        :param extra_context: Extra context to pass to the template

        :return: HttpResponse
        """
        self.inlines = (CsvGeneratorColumnInline,)
        return super(CsvGeneratorAdmin, self).change_view(
            request,
            object_id,
            form_url=form_url,
            extra_context=extra_context
        )


admin.site.register(CsvGenerator, CsvGeneratorAdmin)
