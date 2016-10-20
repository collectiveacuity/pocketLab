__author__ = 'rcj1492'
__created__ = '2016.03'

from jsonmodel.exceptions import InputValidationError

def validFile(file_details, valid_model, kwargs, title=''):

# construct error dictionary with keywords
    error = { 'kwargs': kwargs }

    try:
        file_details = valid_model.validate(file_details)
    except InputValidationError as err:
        from pocketlab.exceptions.lab_exception import labException
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

    return file_details