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
            dummy_int = 1
            dummy_float = 1.1
            cmd_dict = getattr(command_module, '_cmd_kwargs_%s' % command)
            kwargs_model = jsonModel(cmd_dict)
            for key, value in kwargs_model.keyMap.items():
                rules_key = ''
                if value['value_datatype'] == True.__class__:
                    rules_key = '.boolean_fields'
                elif value['value_datatype'] == dummy_int.__class__:
                    rules_key = '.number_fields'
                elif value['value_datatype'] == dummy_float.__class__:
                    rules_key = '.number_fields'
                elif value['value_datatype'] == ''.__class__:
                    rules_key = '.string_fields'
                elif value['value_datatype'] == [].__class__:
                    rules_key = '.list_fields'
                elif value['value_datatype'] == {}.__class__:
                    rules_key = '.map_fields'
                for k, v in jsonModel.__rules__['components'][rules_key].items():
                    if not k in value:
                        if value['value_datatype'] == dummy_int.__class__ and k == 'default_value':
                            value[k] = 0
                        else:
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

    # construct argument lists
            from pocketLab.compilers.argument_lists import argumentLists
            compiler_args = {
                'kwargs_model': kwargs_model,
                'command': command,
                'cmd_dict': cmd_dict
            }
            def_args, req_args, opt_args, exc_args = argumentLists(**compiler_args)

            # print(req_args)
            # print(opt_args)
            # print(exc_args)

    # construct default arguments
            cmd_args.set_defaults(**def_args)

    # construct positional arguments
            for argument in req_args:
                cmd_args.add_argument(argument['args'], **argument['kwargs'])

    # construct optional arguments
            for argument in opt_args:
                cmd_args.add_argument(*argument['args'], **argument['kwargs'])

    # construct mutually exclusive arguments
            for key in exc_args.keys():
                exclusive_options = cmd_args.add_mutually_exclusive_group()
                for argument in exc_args[key]:
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
    exit_data = run_cmd(**opt_dict)
    if exit_data:
        return exit_data

if __name__ == '__main__':
    cli()