"""
Forms for the csv_generator app
"""
from csv_generator.models import CsvGenerator, CsvGeneratorColumn
from django import forms
from django.contrib.contenttypes.models import ContentType


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
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.all().order_by('model')
    )

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

    @property
    def model_field_choices(self):
        """
        Returns 'model' field choices for the formsets form

        :return: Tuple of model field choices
        """
        return self.instance.all_attributes.items()

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
        form = super(
            CsvGeneratorColumnFormSet,
            self
        )._construct_form(i, **kwargs)
        form.fields['model_field'].choices = self.model_field_choices
        return form

    @property
    def empty_form(self):
        """
        Constructs an empty form for the formset
        Backwards compatible to django 1.7

        :return: Form instance
        """
        form = super(CsvGeneratorColumnFormSet, self).empty_form
        form.fields['model_field'].choices = self.model_field_choices
        return form
