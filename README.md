[![Django CSV generator on pypi](https://img.shields.io/badge/pypi-0.1.0-green.svg)](https://pypi.python.org/pypi/csv_generator)
![MIT license](https://img.shields.io/badge/licence-MIT-blue.svg)
![Build status](https://travis-ci.org/fatboystring/csv_generator.svg?branch=master)

# CSV Generator

A configurable CSV Generator for Django


## Installation

`pip install csv_generator`

Add 'csv_generator' to the `INSTALLED_APPS` setting in your django project

`INSTALLED_APPS += ('csv_generator',)`

### Pre Django 1.9

`python manage.py syncdb`

### Django 1.9 and above

`python manage.py migrate`


## Configuration

By default csv_generator uses the [unicode CSV writer class](https://github.com/fatboystring/csv_generator/blob/master/csv_generator/utils.py) bundled with the app.
However, you can use your own CSV Writer class by specifying the import path for your custom writer class (as a string) using the `CSV_GENERATOR_WRITER_CLASS` setting:

```
CSV_GENERATOR_WRITER_CLASS = 'my_app.utils.MyCustomCsvGeneratorClass'
```

Any custom CSV writer class must implement the same methods (with the same signatures) as the UnicodeWriter class bundled with this app.


## Usage

### Django Admin integration

To integrate CSV generator admin functionality for your models just call `admin.register` passing `csv_generator.admin.CsvExportAdmin` as the ModelAdmin class
This will add an extra action to the listing view allowing you to export selected records as a csv file using one of your configured CSV generators.

#### Example

```
from csv_generator.admin import CsvExportAdmin
from django.contrib import admin
from my_app.models import MyModel

admin.site.register(MyModel, CsvExportAdmin)
```


### Setting up a csv generator

Once logged into the Django admin you can create a csv generator instance.  Each CSV generator has the following fields:

 - title: Human readable name used to identify the CSV writer in form fields etc
 - include_headings: Whether or not to write column headings to the generated csv file
 - content_type: The content type this csv_generator can process

Once the CSV generator has been created you will be able to specify the columns on the specified content_type model to write out to generated CSV files.
Each column has the following fields:

 - column_heading: Will be used instead of the model fields verbose_name if it has been specified (verbose name is the default)
 - model_field: The name of the field from the specified content type to write into the column
 - order: The order of the csv column relative to other columns belonging to the specified csv generator instance
 - generator: A foreign key to the generator instance that uses this column (not visible in the django admin)


### Using the generators in your app

You can use the csv_generator in your own app.


#### Retrieving CsvGenerator models

##### For a particular model class or instance
```
from csv_generator.models import CsvGenerator
from my_app.models import MyModel

generators = CsvGenerator.objects.for_model(MyModel)
generators = CsvGenerator.objects.for_model(MyModel())
```

##### For a particular content_type
```
from csv_generator.models import CsvGenerator
from django.contrib.contenttypes.models import ContentType
from my_app.models import MyModel

ctype = ContentType.objects.get_for_model(MyModel)
generators = CsvGenerator.objects.for_content_type(ctype)
```

##### For a particular content_type id
```
from csv_generator.models import CsvGenerator
from django.contrib.contenttypes.models import ContentType
from my_app.models import MyModel

ctype = ContentType.objects.get_for_model(MyModel)
generators = CsvGenerator.objects.for_content_type_id(ctype.pk)
```


#### Generating CSV files

##### Write to file

```
from csv_generator.models import CsvGenerator
from my_app.models import MyModel

generator = CsvGenerator.objects.get(pk=1)  # Assume this is a generator instance for MyModel content type
file_handle = open('my_csv.csv', 'wB')
queryset = MyModel.objects.all()
csv_file = generator.generate(file_handle, queryset)
```

##### Write to Http Response

```
from csv_generator.models import CsvGenerator
from django.http import HttpResponse
from my_app.models import MyModel

generator = CsvGenerator.objects.get(pk=1)  # Assume this is a generator instance for MyModel content type
response = HttpResponse(content_type='text/csv')
response['Content-Disposition'] = 'attachment; filename="my_csv.csv"'
queryset = MyModel.objects.all()
response = generator.generate(response, queryset)
```



