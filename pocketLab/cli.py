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

# construct commands
    lab_cmd_file = jsonLoader(__module__, 'rules/lab-command-model.json')
    lab_cmd_model = jsonModel(lab_cmd_file)
    for command in command_list:
        command_module = import_module('%s.commands.%s' % (__module__, command))
        try:

# add command details
            cmd_dict = getattr(command_module, '_cmd_model_%s' % command)
            cmd_model = lab_cmd_model.ingest(**cmd_dict)
            for i in range(1, len(lab_cmd_model.schema['args'])):
                cmd_model['args'].insert(0, lab_cmd_model.schema['args'][i])
            cmd_details = {
                'description': cmd_model['description'],
                'help': cmd_model['brief'],
                'formatter_class': lambda prog: HelpFormatter(prog, max_help_position=30, width=80) # adjusts column width to options
            }
            cmd_args = subparsers.add_parser(cmd_model['command'], **cmd_details)

# construct dictionaries for each argument type in command
            default_args = {}
            optional_args = []
            required_args = []
            exclusive_args = {}
            for key, value in cmd_model['defaults'].items():
                default_args[key] = value
            for argument in cmd_model['args']:
                if not argument['cli_flags']:
                    required_args.append(argument)
                elif argument['exclusive_group']:
                    if not argument['exclusive_group'] in exclusive_args.keys():
                        exclusive_args[argument['exclusive_group']] = []
                    exclusive_args[argument['exclusive_group']].append(argument)
                else:
                    optional_args.append(argument)

# construct default arguments
            cmd_args.set_defaults(command=cmd_model['command'], model=cmd_model, **default_args)

# construct positional arguments
            for argument in required_args:
                arg_args = [ argument['name'] ]
                arg_kwargs = {
                    'default': argument['default_value'],
                    'help': argument['cli_help'] }
                if argument['cli_metavar']:
                    arg_kwargs['metavar'] = argument['cli_metavar']
                if isinstance(argument['default_value'], str):
                    arg_kwargs['type'] = str
                elif isinstance(argument['default_value'], int):
                    arg_kwargs['type'] = int
                elif isinstance(argument['default_value'], float):
                    arg_kwargs['type'] = float
                if argument['cli_action']:
                    arg_kwargs['action'] = argument['cli_action']
                cmd_args.add_argument(*arg_args, **arg_kwargs)

# construct optional arguments
            for argument in optional_args:
                arg_args = argument['cli_flags']
                arg_kwargs = {
                    'dest': argument['name'],
                    'help': argument['cli_help'] }
                if argument['cli_metavar']:
                    arg_kwargs['metavar'] = argument['cli_metavar']
                if isinstance(argument['default_value'], bool):
                    if argument['default_value']:
                        arg_kwargs['action'] = 'store_false'
                    else:
                        arg_kwargs['action'] = 'store_true'
                else:
                    arg_kwargs['default'] = argument['default_value']
                    if argument['cli_action']:
                        arg_kwargs['action'] = argument['cli_action']
                    if isinstance(argument['default_value'], str):
                        arg_kwargs['type'] = str
                    elif isinstance(argument['default_value'], int):
                        arg_kwargs['type'] = int
                    elif isinstance(argument['default_value'], float):
                        arg_kwargs['type'] = float
                cmd_args.add_argument(*arg_args, **arg_kwargs)

# construct mutually exclusive arguments
            for key in exclusive_args.keys():
                exclusive_options = cmd_args.add_mutually_exclusive_group()
                for argument in exclusive_args[key]:
                    arg_args = argument['cli_flags']
                    arg_kwargs = {
                        'dest': argument['name'],
                        'help': argument['cli_help'] }
                    if argument['cli_metavar']:
                        arg_kwargs['metavar'] = argument['cli_metavar']
                    if isinstance(argument['default_value'], bool):
                        if argument['default_value']:
                            arg_kwargs['action'] = 'store_false'
                        else:
                            arg_kwargs['action'] = 'store_true'
                    else:
                        arg_kwargs['default'] = argument['default_value']
                        if argument['cli_action']:
                            arg_kwargs['action'] = argument['cli_action']
                        if isinstance(argument['default_value'], str):
                            arg_kwargs['type'] = str
                        elif isinstance(argument['default_value'], int):
                            arg_kwargs['type'] = int
                        elif isinstance(argument['default_value'], float):
                            arg_kwargs['type'] = float
                    exclusive_options.add_argument(*arg_args, **arg_kwargs)
        except Exception as err:
            pass

# call parsing function and run appropriate command function with keyword arguments
    args = parser.parse_args(argv)
    opt_dict = vars(args)
    command_module = import_module('%s.commands.%s' % (__module__, args.command))
    run_cmd = getattr(command_module, args.command)
    run_cmd(**opt_dict)

if __name__ == '__main__':
    cli()