__author__ = 'rcj1492'
__created__ = '2016.03'

from importlib import import_module

buildCommand = import_module('jsonmodel.validators')
method = getattr(buildCommand, 'jsonModel')

sample_schema = {
    "schema": {
        "test": "key"
    }
}

sampleModel = method(sample_schema)