__author__ = 'rcj1492'
__created__ = '2016.10'
__license__ = 'MIT'

from jsonmodel.validators import jsonModel

def inject_defaults(command_schema, default_schema):

    default_model = jsonModel(default_schema)
    for key, value in default_model.schema.items():
        if not key in command_schema['schema'].keys():
            command_schema['schema'][key] = value
    for key, value in default_model.components.items():
        if not key in command_schema['components'].keys():
            command_schema['components'][key] = value

    return command_schema

def compile_model(command_schema, cli_schema):
    
    '''
        a method to create a jsonmodel object for command fields with cli metadata
         
    :param command_schema: dictionary with jsonmodel valid schema for command arguments
    :param cli_schema: dictionary with jsonmodel valid schema for command line interface metadata
    :return: jsonmodel object for command fields
    '''

# validate model structure
    if not 'components' in command_schema.keys():
        command_schema['components'] = {}
    if not 'metadata' in command_schema.keys():
        command_schema['metadata'] = {}

# construct cli_model
    cli_model = jsonModel(cli_schema)

# inject cli fields into the metadata for each field
    for key, value in command_schema['schema'].items():
        field_key = '.%s' % key
        if not field_key in command_schema['components'].keys():
            command_schema['components'][field_key] = {}
        if not 'field_metadata' in command_schema['components'][field_key].keys():
            command_schema['components'][field_key]['field_metadata'] = {}
        cli_fields = command_schema['components'][field_key]['field_metadata']
        command_schema['components'][field_key]['field_metadata'] = cli_model.ingest(**cli_fields)

# inject cli fields into metadata field
    command_schema['metadata'] = cli_model.ingest(**command_schema['metadata'])

    return jsonModel(command_schema)

def compile_commands(folder_path, cli_schema, module_name, preferred_order=None):

    import re
    from importlib import import_module
    from os import path, listdir

# validate inputs
    if not isinstance(folder_path, str):
        raise ValueError('folder_path must be a string.')
    elif not path.exists(folder_path):
        raise ValueError('%s is not a valid folder path.' % str(folder_path))
    elif not isinstance(cli_schema, dict):
        raise ValueError('cli_schema must be a dictionary.')
    elif preferred_order:
        if not isinstance(preferred_order, list):
            raise ValueError('preferred_order must be a list of commands.')

# retrieve list of commands
    command_list = []
    py_file = re.compile('\\.pyc?$')
    for file in listdir(folder_path):
        if py_file.findall(file):
            command_list.append(py_file.sub('', file))

# customize the order of commands in help
    for i in range(len(preferred_order)):
        if preferred_order[i] not in command_list:
            preferred_order.pop(i)
    for command in command_list:
        if command not in preferred_order:
            preferred_order.append(command)
    command_list = preferred_order

    # construct each command model
    command_models = []
    for command in command_list:
        command_module = import_module('%s.commands.%s' % (module_name, command))
        try:
            command_schema = getattr(command_module, '_%s_schema' % command)
            command_model = compile_model(command_schema, cli_schema)
            command_models.append(command_model)
        except:
            pass

    return command_models

def compile_arguments(command_model):

    '''
        a method to compile command arguments into argparse argument categories

    :param command_model: jsonmodel object with model from full schema for cli arguments
    :param command_schema: dictionary with schema for method arguments
    :param command: string with name of command
    :return: tuple with dictionary of default args, list of optional args, list of positional args,
            dictionary with exclusive args
    '''

# construct default arguments
    arg_list = ['command']
    # arg_list = ['command', 'model', 'interface', 'medium', 'channel']
    default_args = {
        # 'model': command_schema,
        # 'interface': 'terminal',
        # 'medium': 'command_line',
        # 'channel': 'user',
        'command': command_model.title
    }
    optional_args = []
    positional_args = []
    exclusive_args = {}

# define dummy variables
    empty_defaults = {
        'string': '',
        'boolean': False,
        'number': 0.0,
        'list': [],
        'map': {},
        'null': None
    }
    ifs_set = {'number', 'string'}

# construct cli kwargs for each argument from kwargs model
    for key, value in command_model.schema.items():
        keymap_key = '.%s' % key
        arg_criteria = command_model.keyMap[keymap_key]
        cli_details = arg_criteria['field_metadata']

    # handle arguments designated as default values
        if cli_details['cli_default']:
            if not key in arg_list:
                if arg_criteria['value_datatype'] in ifs_set:
                    arg_list.append(key)
                    default_args[key] = arg_criteria['default_value']

    # otherwise construct empty arg details
        else:
            arg_option = 'optional'
            arg_details = {
                'args': [],
                'kwargs': {
                    'dest': '',
                    'metavar': '',
                    'action': '',
                    'nargs': None,  # int or '*', '?', '+'
                    'choices': None,  # range() or []
                    'type': None,  # datatypes
                    'default': None,  # datatypes
                    # 'const': object(),
                    'help': 'replace this message with "cli_help" in field metadata declaration'
                }
            }

    # validate existence of certain criteria fields
            if not 'default_value' in arg_criteria.keys():
                if arg_criteria['value_datatype'] == 'number':
                    if isinstance(arg_criteria['declared_value'], int):
                        arg_criteria['default_value'] = 0
                    else:
                        arg_criteria['default_value'] = 0.0
                else:
                    arg_criteria['default_value'] = empty_defaults[arg_criteria['value_datatype']]

    # add help
            if cli_details['cli_help']:
                arg_details['kwargs']['help'] = cli_details['cli_help']

    # add flags
            if arg_criteria['required_field'] and arg_criteria['value_datatype'] != 'boolean':
                arg_details['args'] = key
                del arg_details['kwargs']['dest']
                arg_option = 'positional'
            elif cli_details['cli_flags']:
                arg_details['args'] = cli_details['cli_flags']
                arg_details['kwargs']['dest'] = key
            else:
                key_flag = '--%s' % key
                arg_details['args'] = [key_flag]
                arg_details['kwargs']['dest'] = key

    # add metavar
            if cli_details['cli_metavar']:
                arg_details['kwargs']['metavar'] = cli_details['cli_metavar']
            else:
                del arg_details['kwargs']['metavar']

    # add boolean specific kwargs
            if arg_criteria['value_datatype'] == 'boolean':
                del arg_details['kwargs']['nargs']
                del arg_details['kwargs']['default']
                del arg_details['kwargs']['choices']
                del arg_details['kwargs']['type']
                if arg_criteria['default_value']:
                    arg_details['kwargs']['action'] = 'store_false'
                else:
                    arg_details['kwargs']['action'] = 'store_true'

    # add str, int and float specific kwargs
            elif arg_criteria['value_datatype'] in ifs_set:
                del arg_details['kwargs']['nargs']
                arg_details['kwargs']['default'] = arg_criteria['default_value']
        # toggle type
                if arg_criteria['value_datatype'] == 'number':
                    if isinstance(arg_criteria['declared_value'], int):
                        arg_details['kwargs']['type'] = int
                    else:
                        arg_details['kwargs']['type'] = float
                elif arg_criteria['value_datatype'] == 'string':
                    arg_details['kwargs']['type'] = str
                else:
                    del arg_details['kwargs']['type']
        # toggle action
                if cli_details['cli_action']:
                    arg_details['kwargs']['action'] = cli_details['cli_action']
                else:
                    del arg_details['kwargs']['action']
        # toggle choices
                if 'discrete_values' in arg_criteria.keys():
                    if arg_criteria['discrete_values']:
                        value_list = arg_criteria['discrete_values']
                        arg_details['kwargs']['choices'] = value_list
                elif 'max_value' in arg_criteria.keys() and arg_criteria['value_datatype'] == 'number':
                    if isinstance(arg_criteria['declared_value'], int):
                        if 'min_value' in arg_criteria.keys():
                            if arg_criteria['min_value']:
                                low = int(arg_criteria['min_value'])
                                high = int(arg_criteria['max_value']) + 1
                                arg_details['kwargs']['choices'] = range(low, high)
                        else:
                            high = int(arg_criteria['max_value']) + 1
                            arg_details['kwargs']['choices'] = range(high)
                else:
                    del arg_details['kwargs']['choices']


    # add list specific kwargs
            elif arg_criteria['value_datatype'] == 'list':
                item_key = '.%s[0]' % key
                item_criteria = command_model.keyMap[item_key]
                arg_details['kwargs']['default'] = []
        # toggle type
                if item_criteria['value_datatype'] == 'number':
                    if isinstance(item_criteria['declared_value'], int):
                        arg_details['kwargs']['type'] = int
                    else:
                        arg_details['kwargs']['type'] = float
                elif item_criteria['value_datatype'] == 'string':
                    arg_details['kwargs']['type'] = str
                else:
                    del arg_details['kwargs']['type']
        # toggle choices
                if 'discrete_values' in arg_criteria.keys():
                    if item_criteria['discrete_values']:
                        value_list = item_criteria['discrete_values']
                        arg_details['kwargs']['choices'] = value_list
                elif 'max_value' in item_criteria.keys() and item_criteria['value_datatype'] == 'number':
                    if isinstance(item_criteria['declared_value'], int):
                        if 'min_value' in arg_criteria.keys():
                            if item_criteria['min_value']:
                                low = int(item_criteria['min_value'])
                                high = int(item_criteria['max_value']) + 1
                                arg_details['kwargs']['choices'] = range(low, high)
                        else:
                            high = int(item_criteria['max_value']) + 1
                            arg_details['kwargs']['choices'] = range(high)
                else:
                    del arg_details['kwargs']['choices']
        # toggle action
                if cli_details['cli_action']:
                    arg_details['kwargs']['action'] = cli_details['cli_action']
                else:
                    del arg_details['kwargs']['action']
        # toggle nargs
                if 'min_size' in arg_criteria.keys():
                    if arg_criteria['min_size']:
                        if arg_criteria['min_size'] == 1:
                            arg_details['kwargs']['nargs'] = '+'
                        else:
                            arg_details['kwargs']['nargs'] = arg_criteria['min_size']
                else:
                    arg_details['kwargs']['nargs'] = '*'

    # skip (unsupported) dict kwargs
            elif arg_criteria['value_datatype'] == 'map':
                arg_details = {}

    # assign details to an argument list
            if arg_details:
                if not key in arg_list:
                    arg_list.append(key)
                    if not cli_details['cli_group']:
                        if arg_option == 'positional':
                            arg_details['cli_position'] = cli_details['cli_position']
                            positional_args.append(arg_details)
                        else:
                            optional_args.append(arg_details)
                    else:
                        if not cli_details['cli_group'] in exclusive_args.keys():
                            exclusive_args[cli_details['cli_group']] = []
                        # arg_details['kwargs']['required'] = True
                        exclusive_args[cli_details['cli_group']].append(arg_details)

# sort positional arguments by positional key
    if positional_args:
        positional_args = sorted(positional_args, key=lambda k: k['cli_position'])

# return properly formatted argument lists
    return default_args, positional_args, optional_args, exclusive_args

if __name__ == '__main__':

    from pocketlab import __module__, __order__
    from pocketlab.commands.home import _home_schema as home_schema
    from labpack.records.settings import load_settings
    folder_path = 'commands/'
    cli_schema = load_settings('models/lab-cli.json')
    default_schema = load_settings('models/lab-defaults.json')
    home_schema = inject_defaults(home_schema, default_schema)
    home_model = compile_model(home_schema, cli_schema)
    home_model.validate(home_model.schema)
    command_list = compile_commands(folder_path, cli_schema, __module__, __order__)
    assert command_list
    def_args, pos_args, opt_args, exc_args = compile_arguments(home_model)
    assert def_args
    assert pos_args
    assert opt_args
    defaults_injected = False
    for argument in opt_args:
        if argument['args'][0] == '-q':
            defaults_injected = True
    assert defaults_injected