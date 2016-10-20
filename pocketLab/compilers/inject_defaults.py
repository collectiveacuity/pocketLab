__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketlab import __module__
from jsonmodel.loader import jsonLoader

_lab_defaults_model = jsonLoader(__module__, 'rules/lab-defaults-model.json')

def injectDefaults(cmd_dict):

    if isinstance(cmd_dict, dict):
        command_name = ''
        if 'title' in cmd_dict.keys():
            if isinstance(cmd_dict['title'], str):
                command_name = cmd_dict['title']
        if 'schema' in cmd_dict.keys():
            if isinstance(cmd_dict['schema'], dict):
                for key, value in _lab_defaults_model['schema'].items():
                    cmd_dict['schema'][key] = value
        if 'components' in cmd_dict.keys():
            if isinstance(cmd_dict['components'], dict):
                for key, value in _lab_defaults_model['components'].items():
                    cmd_dict['components'][key] = value

    return cmd_dict

