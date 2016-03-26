__author__ = 'rcj1492'
__created__ = '2016.03'

'''
https://docs.python.org/3.5/library/argparse.html?highlight=argparse#module-argparse
'''

import sys
from pocketLab import __command__, __module__, __version__
from importlib import import_module
from importlib.util import find_spec
from os import listdir
from re import compile
from jsonmodel.loader import jsonLoader
from jsonmodel.validators import jsonModel
from argparse import ArgumentParser, HelpFormatter, RawDescriptionHelpFormatter, PARSER

class SubcommandHelpFormatter(RawDescriptionHelpFormatter):
    def _format_action(self, action):
        parts = super(RawDescriptionHelpFormatter, self)._format_action(action)
        if action.nargs == PARSER:
            parts = "\n".join(parts.split("\n")[1:])
        return parts

def cli(error=False):

# handle optional error argument
    if error:
        argv = ['-h']
    else:
        argv = sys.argv[1:]

# construct main module
    module_args = {
        'description': 'A laboratory assistant bot.',
        'epilog': '%s can also make coffee.' % __command__,
        'usage': __command__,
        'formatter_class': SubcommandHelpFormatter # remove sub-command braces in help
    }
    parser = ArgumentParser(**module_args)
    current_version = '%s %s' % (__module__, __version__)
    parser.add_argument('-v', '--version', action='version', version=current_version)

# replace stderr message with help output
    def error_msg(err):
        print('Errr! %s\n' % err)
        cli(error=True)
        sys.exit(2)
    parser.error = error_msg

# construct command parsing method
    help_details = {
        'title': 'list of commands' # title for sub-commands list in help
    }
    subparsers = parser.add_subparsers(**help_details)

# define command scope from commands sub-folder
    command_list = []
    module_path = find_spec(__module__).submodule_search_locations[0]
    commands_folder = listdir('%s/commands/' % module_path)
    py_file = compile('\\.pyc?$')
    for file in commands_folder:
         if py_file.findall(file):
            command_list.append(py_file.sub('',file))

# customize the order of commands in help
    preferred_order = ['home', 'start', 'enter', 'stop']
    for i in range(len(preferred_order)):
        if preferred_order[i] not in command_list:
            preferred_order.pop(i)
    for command in command_list:
        if command not in preferred_order:
            preferred_order.append(command)
    command_list = preferred_order

# construct cli metadata model
    cli_file = jsonLoader(__module__, 'rules/lab-cli-model.json')
    cli_model = jsonModel(cli_file)

# construct each command
    for command in command_list:
        command_module = import_module('%s.commands.%s' % (__module__, command))
        try:

# construct command model with cli fields
            ex_int = 1
            ex_float = 1.1
            cmd_dict = getattr(command_module, '_cmd_kwargs_%s' % command)
            kwargs_model = jsonModel(cmd_dict)
            for key, value in kwargs_model.keyMap.items():
                rules_key = ''
                if value['value_datatype'] == True.__class__:
                    rules_key = '.boolean_fields'
                elif value['value_datatype'] == ex_int.__class__:
                    rules_key = '.number_fields'
                elif value['value_datatype'] == ex_float.__class__:
                    rules_key = '.number_fields'
                elif value['value_datatype'] == ''.__class__:
                    rules_key = '.string_fields'
                elif value['value_datatype'] == [].__class__:
                    rules_key = '.list_fields'
                elif value['value_datatype'] == {}.__class__:
                    rules_key = '.map_fields'
                for k, v in jsonModel.__rules__['components'][rules_key].items():
                    if not k in value:
                        value[k] = v
                value['field_metadata'] = cli_model.ingest(**value['field_metadata'])

            # print(kwargs_model.keyMap)

# add command details to parser
            cmd_details = {
                'description': 'replace this message with model description declaration',
                'help': 'replace this message with "cli_help" in model metadata declaration',
                'formatter_class': lambda prog: HelpFormatter(prog, max_help_position=30, width=80) # adjusts column width to options
            }
            if 'cli_help' in kwargs_model.metadata.keys():
                if isinstance(kwargs_model.metadata['cli_help'], str):
                    cmd_details['help'] = kwargs_model.metadata['cli_help']
            if kwargs_model.description:
                cmd_details['description'] = kwargs_model.description
            cmd_args = subparsers.add_parser(command, **cmd_details)

            # print(cmd_details)

# construct empty argument lists
            arg_list = [ 'command', 'model' ]
            default_args = {}
            optional_args = []
            required_args = []
            exclusive_args = {}

# construct default argument dictionary
            if 'cli_defaults' in kwargs_model.metadata.keys():
                if kwargs_model.metadata['cli_defaults']:
                    if isinstance(kwargs_model.metadata['cli_defaults'], dict):
                        for k, v in kwargs_model.metadata['cli_defaults']:
                            if not k in arg_list:
                                arg_list.append(k)
                                default_args[k] = v

            # print(default_args)

# construct cli dictionary for each argument from model
            for key, value in kwargs_model.schema.items():
                arg_option = 'optional'
                arg_details = {
                    'args': [],
                    'kwargs': {
                        'dest': '',
                        'metavar': '',
                        'action': '',
                        'nargs': None, # int or '*', '?', '+'
                        'choices': None, # range() or []
                        'type': None, # datatypes
                        'default': None, # datatypes
                        # 'const': object(),
                        'help': 'replace this message with "cli_help" in field metadata declaration'
                    }
                }
                keymap_key = '.%s' % key
                arg_criteria = kwargs_model.keyMap[keymap_key]
                cli_details = arg_criteria['field_metadata']

                # print(cli_details)

            # help
                if cli_details['cli_help']:
                    arg_details['kwargs']['help'] = cli_details['cli_help']

            # flags
                if arg_criteria['required_field'] and arg_criteria['value_datatype'] != True.__class__:
                    arg_details['args'] = key
                    del arg_details['kwargs']['dest']
                    arg_option = 'required'
                elif cli_details['cli_flags']:
                    arg_details['args'] = cli_details['cli_flags']
                    arg_details['kwargs']['dest'] = key
                else:
                    key_flag = '--%s' % key
                    arg_details['args'] = [ key_flag ]
                    arg_details['kwargs']['dest'] = key

            # metavar
                if cli_details['cli_metavar']:
                    arg_details['kwargs']['metavar'] = cli_details['cli_metavar']
                else:
                    del arg_details['kwargs']['metavar']

            # construct int, float and str class set
                ifs_set = { ex_int.__class__, ex_float.__class__, ''.__class__}

            # boolean specific
                if arg_criteria['value_datatype'] == True.__class__:
                    del arg_details['kwargs']['nargs']
                    del arg_details['kwargs']['default']
                    del arg_details['kwargs']['choices']
                    del arg_details['kwargs']['type']
                    if arg_criteria['default_value']:
                        arg_details['kwargs']['action'] = 'store_false'
                    else:
                        arg_details['kwargs']['action'] = 'store_true'

            # str, int and float specific
                elif arg_criteria['value_datatype'] in ifs_set:
                    del arg_details['kwargs']['nargs']
                    arg_details['kwargs']['default'] = arg_criteria['default_value']
                    if arg_criteria['value_datatype'] == ex_int.__class__:
                        arg_details['kwargs']['type'] = int
                        if not arg_details['kwargs']['default']:
                            arg_details['kwargs']['default'] = 0
                    elif arg_criteria['value_datatype'] == ex_float.__class__:
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
                    elif 'max_value' in arg_criteria.keys() and arg_criteria['value_datatype'] == ex_int.__class__:
                        if arg_criteria['min_value']:
                            low = int(arg_criteria['min_value'])
                            high = int(arg_criteria['max_value']) + 1
                            arg_details['kwargs']['choices'] = range(low, high)
                        else:
                            high = int(arg_criteria['max_value']) + 1
                            arg_details['kwargs']['choices'] = range(high)
                    else:
                        del arg_details['kwargs']['choices']

            # list specific
                elif arg_criteria['value_datatype'] == [].__class__:
                    item_key = '.%s[0]' % key
                    item_criteria = kwargs_model.keyMap[item_key]
                    arg_details['kwargs']['default'] = []
                    if item_criteria['value_datatype'] == ex_int.__class__:
                        arg_details['kwargs']['type'] = int
                    elif item_criteria['value_datatype'] == ex_float.__class__:
                        arg_details['kwargs']['type'] = float
                    elif item_criteria['value_datatype'] == ''.__class__:
                        arg_details['kwargs']['type'] = str
                    else:
                        del arg_details['kwargs']['type']
                    if item_criteria['discrete_values']:
                        value_list = item_criteria['discrete_values']
                        arg_details['kwargs']['choices'] = value_list
                    elif 'max_value' in item_criteria.keys() and item_criteria['value_datatype'] == ex_int.__class__:
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

            # dict specific
                elif arg_criteria['value_datatype'] == {}.__class__:
                    arg_details = {}

# assign details to an argument list
                if arg_details:
                    if not key in arg_list:
                        arg_list.append(key)
                        if not cli_details['cli_group']:
                            if arg_option == 'required':
                                required_args.append(arg_details)
                            else:
                                optional_args.append(arg_details)
                        else:
                            if not cli_details['cli_group'] in exclusive_args.keys():
                                exclusive_args[cli_details['cli_group']] = []
                            exclusive_args[cli_details['cli_group']].append(arg_details)

            # print(required_args)
            # print(optional_args)
            # print(exclusive_args)

# construct default arguments
            cmd_args.set_defaults(command=command, model=cmd_dict, **default_args)

# construct positional arguments
            for argument in required_args:
                cmd_args.add_argument(argument['args'], **argument['kwargs'])

# construct optional arguments
            for argument in optional_args:
                cmd_args.add_argument(*argument['args'], **argument['kwargs'])

# construct mutually exclusive arguments
            for key in exclusive_args.keys():
                exclusive_options = cmd_args.add_mutually_exclusive_group()
                for argument in exclusive_args[key]:
                    exclusive_options.add_argument(*argument['args'], **argument['kwargs'])

# remove command from module if there is model parsing error
        except Exception as err:
            # print(err)
            pass

# call parsing function and run appropriate command function with keyword arguments
    args = parser.parse_args(argv)
    opt_dict = vars(args)
    command_module = import_module('%s.commands.%s' % (__module__, args.command))
    run_cmd = getattr(command_module, args.command)
    run_cmd(**opt_dict)

if __name__ == '__main__':
    cli()