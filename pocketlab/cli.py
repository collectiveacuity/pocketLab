__author__ = 'rcj1492'
__created__ = '2016.03'

'''
https://docs.python.org/3.5/library/argparse.html?highlight=argparse#module-argparse
'''

import re
import sys
from pocketlab.utils import compile_command_model, compile_argument_lists
from pocketlab import __command__, __module__, __version__
from importlib import import_module
from importlib.util import find_spec
from os import listdir
from jsonmodel.loader import jsonLoader
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
    py_file = re.compile('\\.pyc?$')
    for file in commands_folder:
         if py_file.findall(file):
            command_list.append(py_file.sub('',file))

# customize the order of commands in help
    preferred_order = ['home', 'start']
    for i in range(len(preferred_order)):
        if preferred_order[i] not in command_list:
            preferred_order.pop(i)
    for command in command_list:
        if command not in preferred_order:
            preferred_order.append(command)
    command_list = preferred_order

# retrieve command line metadata schema
    cli_schema = jsonLoader(__module__, 'models/lab-cli.json')

# construct each command
    for command in command_list:
        command_module = import_module('%s.commands.%s' % (__module__, command))
        try:

# construct command model with cli fields
            command_schema = getattr(command_module, '_%s_schema' % command)
            command_model = compile_command_model(command_schema, cli_schema)

# add command details to parser
            cmd_details = {
                'description': 'replace this message with model description declaration',
                'help': 'replace this message with "cli_help" in model metadata declaration',
                'formatter_class': lambda prog: HelpFormatter(prog, max_help_position=30, width=80) # adjusts column width to options
            }
            if 'cli_help' in command_model.metadata.keys():
                if isinstance(command_model.metadata['cli_help'], str):
                    cmd_details['help'] = command_model.metadata['cli_help']
            if command_model.description:
                cmd_details['description'] = command_model.description
            cmd_args = subparsers.add_parser(command, **cmd_details)

            # print(cmd_details)

# construct argument lists
            def_args, req_args, opt_args, exc_args = compile_argument_lists(command_model)

            # print(def_args)
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
            print(err)
            pass

# call parsing function and run appropriate command function with keyword arguments
    sys_args = parser.parse_args(argv)
    opt_dict = vars(sys_args)
    command_module = import_module('%s.commands.%s' % (__module__, sys_args.command))
    run_cmd = getattr(command_module, sys_args.command)
    del opt_dict['command']
    exit_data = None
    try:
        exit_data = run_cmd(**opt_dict)
    except Exception as err:
        print('Errr! %s' % err)
    if exit_data:
        if isinstance(exit_data, str):
            exit_data = 'Sweet! %s' % exit_data
        return exit_data

if __name__ == '__main__':
    cli()