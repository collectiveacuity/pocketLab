__author__ = 'rcj1492'
__created__ = '2016.03'

def argumentLists(kwargs_model, cmd_dict, command):

# define dummy variables
    dummy_int = 1
    dummy_float = 1.1
    ifs_set = {dummy_int.__class__, dummy_float.__class__, ''.__class__}
    
# construct default arguments
    arg_list = ['command', 'model', 'interface', 'medium', 'channel']
    default_args = {
        'command': command,
        'model': cmd_dict,
        'interface': 'terminal',
        'medium': 'command_line',
        'channel': 'user'
    }
    optional_args = []
    positional_args = []
    exclusive_args = {}

# construct cli kwargs for each argument from kwargs model
    for key, value in kwargs_model.schema.items():
        keymap_key = '.%s' % key
        arg_criteria = kwargs_model.keyMap[keymap_key]
        cli_details = arg_criteria['field_metadata']

    # additional defaults
        if cli_details['cli_default']:
            if not key in arg_list:
                if arg_criteria['value_datatype'] in ifs_set:
                    arg_list.append(key)
                    default_args[key] = arg_criteria['default_value']
        else:

    # construct empty arg details
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

    # add help
            if cli_details['cli_help']:
                arg_details['kwargs']['help'] = cli_details['cli_help']
    
    # add flags
            if arg_criteria['required_field'] and arg_criteria['value_datatype'] != True.__class__:
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
            if arg_criteria['value_datatype'] == True.__class__:
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
                if arg_criteria['value_datatype'] == dummy_int.__class__:
                    arg_details['kwargs']['type'] = int
                    if not arg_details['kwargs']['default']:
                        arg_details['kwargs']['default'] = 0
                elif arg_criteria['value_datatype'] == dummy_float.__class__:
                    arg_details['kwargs']['type'] = float
                elif arg_criteria['value_datatype'] == ''.__class__:
                    arg_details['kwargs']['type'] = str
                else:
                    del arg_details['kwargs']['type']
                if cli_details['cli_action']:
                    arg_details['kwargs']['action'] = cli_details['cli_action']
                else:
                    del arg_details['kwargs']['action']
                if arg_criteria['discrete_values']:
                    value_list = arg_criteria['discrete_values']
                    arg_details['kwargs']['choices'] = value_list
                elif 'max_value' in arg_criteria.keys() and arg_criteria['value_datatype'] == dummy_int.__class__:
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
            elif arg_criteria['value_datatype'] == [].__class__:
                item_key = '.%s[0]' % key
                item_criteria = kwargs_model.keyMap[item_key]
                arg_details['kwargs']['default'] = []
                if item_criteria['value_datatype'] == dummy_int.__class__:
                    arg_details['kwargs']['type'] = int
                elif item_criteria['value_datatype'] == dummy_float.__class__:
                    arg_details['kwargs']['type'] = float
                elif item_criteria['value_datatype'] == ''.__class__:
                    arg_details['kwargs']['type'] = str
                else:
                    del arg_details['kwargs']['type']
                if item_criteria['discrete_values']:
                    value_list = item_criteria['discrete_values']
                    arg_details['kwargs']['choices'] = value_list
                elif 'max_value' in item_criteria.keys() and item_criteria['value_datatype'] == dummy_int.__class__:
                    if item_criteria['min_value']:
                        low = int(item_criteria['min_value'])
                        high = int(item_criteria['max_value']) + 1
                        arg_details['kwargs']['choices'] = range(low, high)
                    else:
                        high = int(item_criteria['max_value']) + 1
                        arg_details['kwargs']['choices'] = range(high)
                else:
                    del arg_details['kwargs']['choices']
                if cli_details['cli_action']:
                    arg_details['kwargs']['action'] = cli_details['cli_action']
                else:
                    del arg_details['kwargs']['action']
                if arg_criteria['min_size']:
                    if arg_criteria['min_size'] == 1:
                        arg_details['kwargs']['nargs'] = '+'
                    else:
                        arg_details['kwargs']['nargs'] = arg_criteria['min_size']
                else:
                    arg_details['kwargs']['nargs'] = '*'
    
    # skip (unsupported) dict kwargs
            elif arg_criteria['value_datatype'] == {}.__class__:
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
    print(exclusive_args)

# sort positional arguments by positional key
    if positional_args:
        positional_args = sorted(positional_args, key=lambda k: k['cli_position'])

# return properly formatted argument lists

    return default_args, positional_args, optional_args, exclusive_args