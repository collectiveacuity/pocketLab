__author__ = 'rcj1492'
__created__ = '2016.03'

from os import path
from re import compile
from labMgmt.exceptions.lab_exception import labException

def configFile(file_name, kwargs):

# construct error dictionary with keywords
    error = { 'kwargs': kwargs }

# validate existence of file
    if not path.exists(file_name):
        error['message'] = '%s does not exist.' % file_name
        error['failed_test'] = 'missing_file'
        error['error_value'] = file_name
        raise labException(**error)

# open file based upon extension
    file_dict = {}
    json_pattern = compile('\\.json$')
    yaml_pattern = compile('\\.ya?ml$')
    ini_pattern = compile('\\.ini$')
    if json_pattern.findall(file_name):
        import json
        try:
            file_dict = json.loads(open(file_name).read())
        except Exception as err:
            error['exception'] = err
            error['message'] = '%s is not a valid json file.' % file_name
            error['failed_test'] = 'invalid_type'
            error['error_value'] = file_name
            raise labException(**error)
    elif yaml_pattern.findall(file_name):
        import yaml
        try:
            file_dict = yaml.load(open(file_name).read())
        except Exception as err:
            error['exception'] = err
            error['message'] = '%s is not a valid yaml file.' % file_name
            error['failed_test'] = 'invalid_type'
            error['error_value'] = file_name
            raise labException(**error)
    elif ini_pattern.findall(file_name):
        from configparser import ConfigParser
        try:
            config = ConfigParser()
            config.optionxform = str
            config.read(file_name)
            section_list = config.sections()
            for section in section_list:
                file_dict[section] = dict(config.items(section))
        except Exception as err:
            error['exception'] = err
            error['message'] = '%s is not a valid ini file.' % file_name
            error['failed_test'] = 'invalid_type'
            error['error_value'] = file_name
            raise labException(**error)
    else:
        error['message'] = '%s is not a valid configuration file type.' % file_name
        error['failed_test'] = 'invalid_type'
        error['error_value'] = file_name
        raise labException(**error)

# validate data in file and return dictionary
    if not file_dict:
        error['message'] = '%s contains no data.' % file_name
        error['failed_test'] = 'empty_file'
        error['error_value'] = file_name
        raise labException(**error)

    return file_dict
