__author__ = 'rcj1492'
__created__ = '2016.03'

from os import path
from re import compile
from labMgmt.exceptions import LabException

def configFile(file_name):

# validate existence of file
    if not path.exists(file_name):
        raise LabException('%s does not exist.' % file_name, error='missing_file')

# open file based upon extension
    file_dict = {}
    json_pattern = compile('\\.json$')
    yaml_pattern = compile('\\.ya?ml$')
    ini_pattern = compile('\\.ini$')
    if json_pattern.findall(file_name):
        import json
        try:
            file_dict = json.loads(open(file_name).read())
        except:
            raise LabException('%s is not a valid json file.' % file_name, error='invalid_type')
    elif yaml_pattern.findall(file_name):
        import yaml
        try:
            file_dict = yaml.load(open(file_name).read())
        except:
            raise LabException('%s is not a valid yaml file.' % file_name, error='invalid_type')
    elif ini_pattern.findall(file_name):
        from configparser import ConfigParser
        try:
            config = ConfigParser()
            config.optionxform = str
            config.read(file_name)
            section_list = config.sections()
            for section in section_list:
                file_dict[section] = dict(config.items(section))
        except:
            raise LabException('%s is not a valid ini file.' % file_name, error='invalid_type')
    else:
        raise LabException('%s is not a valid configuration file type.' % file_name, error='invalid_type')

# validate data in file and return dictionary
    if not file_dict:
        raise LabException('%s contains no data.' % file_name, error='empty_file')
    return file_dict
