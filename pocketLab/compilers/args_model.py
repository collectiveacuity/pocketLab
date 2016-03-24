__author__ = 'rcj1492'
__created__ = '2016.03'

from jsonmodel.validators import jsonModel

def argsModel(cmd_model):

    schema_map = {}
    components_map = {}
    for argument in cmd_model['args']:
        argument_details = {}
        comp_key = '.%s' % argument['name']
        schema_map[argument['name']] = argument['default_value']
        rules_key = ''
        if isinstance(argument['default_value'], bool):
            rules_key = '.boolean_fields'
        elif isinstance(argument['default_value'], int):
            rules_key = '.number_fields'
        elif isinstance(argument['default_value'], float):
            rules_key = '.number_fields'
        elif isinstance(argument['default_value'], str):
            rules_key = '.string_fields'
        if rules_key:
            for key, value in argument.items():
                if key in jsonModel.__rules__['components'][rules_key].keys():
                    argument_details[key] = value
        if argument_details:
            components_map[comp_key] = argument_details

    args_model = {
        'schema': schema_map,
        'components': components_map
    }

    return args_model