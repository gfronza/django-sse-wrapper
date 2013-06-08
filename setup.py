# -*- coding: utf-8 -*-
"""Setup file for easy installation"""
from os.path import join, dirname
from setuptools import setup


version = __import__('sse_wrapper').__version__

LONG_DESCRIPTION = """
A simple wrapper of the sse python implementation for django.
With this helper, you are able to create views that respond with
'text/event-stream' content type, allowing you to send events
to the clients from all over you app.
"""


def long_description():
    try:
        return open(join(dirname(__file__), 'README.rst')).read()
    except IOError:
        return LONG_DESCRIPTION


setup(name='django-sse-wrapper',
      version=version,
      author='Germano Fronza',
      author_email='germano.inf@gmail.com',
      description='A simple wrapper of the sse python implementation for django',
      license='BSD',
      keywords='django, sse, xhr, polling, redis',
      url='https://github.com/gfronza/django-sse-wrapper',
      packages=['sse_wrapper',
                'sse_wrapper.backends'],
      long_description=long_description(),
      install_requires=['Django>=1.2.5', 'sse>=1.2'],
      zip_safe=False)
