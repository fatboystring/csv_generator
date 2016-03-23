# -*- coding: utf-8 -*-
"""
Forms for the csv_generator app
"""
from __future__ import unicode_literals
from csv_generator.models import CsvGenerator, CsvGeneratorColumn
from django import forms


class SelectCsvGeneratorForm(forms.Form):
    """
    Form class for selecting a csv generator
    """
    generator = forms.ModelChoiceField(queryset=CsvGenerator.objects.none())

    def __init__(self, *args, **kwargs):
        """
        Custom init method
        Sets the queryset on the generator field

        :param args: Default positional arguments
        :type args: ()

        :param kwargs: Default keyword arguments
        :type kwargs: {}
        """
        generators = kwargs.pop('generators')
        super(SelectCsvGeneratorForm, self).__init__(*args, **kwargs)
        self.fields['generator'].queryset = generators


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
    model_field = forms.ChoiceField(label='Field', choices=[])

    def __init__(self, *args, **kwargs):
        """
        Sets the choices for the model_field field

        :param args: Default positional args
        :type args: ()

        :param kwargs: Default keyword args
        :type kwargs: {}
        """
        generator = kwargs.pop('csv_generator')
        super(CsvGeneratorColumnForm, self).__init__(*args, **kwargs)
        self.fields['model_field'].choices = generator.all_attributes.items()

    class Meta(object):
        """
        Django properties
        """
        model = CsvGeneratorColumn
        exclude = ()


class CsvGeneratorColumnFormSet(forms.BaseInlineFormSet):
    """
    Formset for the CsvGeneratorColumn model
    """
    model = CsvGeneratorColumn

    def get_form_kwargs(self, index):
        """
        Adds the csv_generator instance to the form kwargs

        :param index: Form index
        :type index: int

        :return: Dict for form kwargs
        """
        kwargs = super(CsvGeneratorColumnFormSet, self).get_form_kwargs(index)
        kwargs.update({'csv_generator': self.instance})
        return kwargs

    def _construct_form(self, i, **kwargs):
        """
        Construct form method
        Backwards compatible to django 1.7

        :param i: Form index
        :type i: int

        :param kwargs: Default form kwargs
        :type kwargs: {}

        :return: Form instance
        """
        kwargs.update({'csv_generator': self.instance})
        return super(CsvGeneratorColumnFormSet, self)._construct_form(
            i, **kwargs
        )

    @property
    def empty_form(self):
        """
        Constructs an empty form for the formset
        Backwards compatible to django 1.7

        :return: Form instance
        """
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix('__prefix__'),
            empty_permitted=True,
            csv_generator=self.instance
        )
        self.add_fields(form, None)
        return form
