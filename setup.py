#!/usr/bin/env python
from __future__ import unicode_literals
from setuptools import setup, find_packages

setup(
      name='csv_generator',
      version='0.1',
      description='Configurable CSV Generator for Django',
      author='Dan Stringer',
      author_email='dan.stringer1983@googlemail.com',
      url='https://github.com/fatboystring/csv_generator/',
      packages=find_packages(exclude=['app']),
      license='License :: Public Domain',
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
      ],
      keywords='csv writer queryset django',
      install_requires=[],
)
