__author__ = 'rcj1492'
__created__ = '2016.03'

from jsonmodel.loader import jsonLoader
from jsonmodel.validators import jsonModel
from jsonmodel.exceptions import InputValidationError
from labMgmt.exceptions import LabPrettyException

def projectModel(project_details):
    project_model = jsonLoader('labMgmt', 'rules/lab-project-model.json')
    valid_model = jsonModel(project_model)
    try:
        project_details = valid_model.validate(project_details)
    except InputValidationError as err:
        error_report = err.error
        raise LabPrettyException('Schema in project settings file is invalid. It should follow this schema:\n', printout=error_report['model_schema'], error='invalid_schema')
    return project_details

def credModel(cred_details, model_file, title):
    cred_model = jsonLoader('labMgmt', model_file)
    valid_model = jsonModel(cred_model)
    try:
        cred_details = valid_model.validate(cred_details)
    except InputValidationError as err:
        error_report = err.error
        raise LabPrettyException('Schema in %s credentials file is invalid. It should follow this schema:\n' % title, printout=error_report['model_schema'], error='invalid_schema')
    return cred_details