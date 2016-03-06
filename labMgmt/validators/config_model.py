__author__ = 'rcj1492'
__created__ = '2016.03'
__module__ = 'labMgmt'

from jsonmodel.loader import jsonLoader
from jsonmodel.validators import jsonModel
from jsonmodel.exceptions import InputValidationError
from labMgmt.exceptions.lab_pretty_exception import LabPrettyException

def configModel(config_details, model_file, title=''):
    config_model = jsonLoader(__module__, model_file)
    valid_model = jsonModel(config_model)
    try:
        config_details = valid_model.validate(config_details)
    except InputValidationError as err:
        error_report = err.error
        raise LabPrettyException('Schema of %s file is invalid. File should follow this schema:\n' % title, printout=error_report['model_schema'], error='invalid_schema')
    return config_details
