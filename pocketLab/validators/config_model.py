__author__ = 'rcj1492'
__created__ = '2016.03'
__module__ = 'pocketLab'

from jsonmodel.loader import jsonLoader
from jsonmodel.validators import jsonModel
from jsonmodel.exceptions import InputValidationError
from pocketLab.exceptions.lab_exception import labException

def configModel(config_details, model_file, kwargs, title=''):

# construct error dictionary with keywords
    error = { 'kwargs': kwargs }

    config_model = jsonLoader(__module__, model_file)
    valid_model = jsonModel(config_model)
    try:
        config_details = valid_model.validate(config_details)
    except InputValidationError as err:
        if err.error['input_path'] == '.':
            field = 'Top level dictionary'
        else:
            field = 'Field %s' % err.error['input_path']
        error['exception'] = err.error
        error['message'] = '%s in %s file failed %s test. File should follow this schema:' % (field, title, err.error['failed_test'])
        error['failed_test'] = 'invalid_schema'
        error['error_value'] = err.error['error_value']
        error['pprint'] = err.error['model_schema']
        raise labException(**error)

    return config_details
