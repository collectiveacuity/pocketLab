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
        'usage': '%s <command> [options]' % __command__,
        'formatter_class': SubcommandHelpFormatter # remove sub-command braces in help
    }
    parser = ArgumentParser(**module_args)
    current_version = '%s %s' % (__command__, __version__)
    parser.add_argument('-v', '--version', action='version', version=current_version)

# replace stderr message with help output
    def error_msg(err):
        print('Errr! %s\n' % err)
        cli(error=True)
        sys.exit(2)
    parser.error = error_msg

# construct sub-command parsing method
    help_details = {
        'title': 'list of commands' # title for sub-commands list in help
    }
    subparsers = parser.add_subparsers(**help_details)

# define sub-command scope from commands sub-folder
    command_list = []
    module_path = find_spec(__module__).submodule_search_locations[0]
    commands_folder = listdir('%s/commands/' % module_path)
    py_file = compile('\\.pyc?$')
    for file in commands_folder:
         if py_file.findall(file):
            command_list.append(py_file.sub('',file))

# customize the order of sub-commands in help
    preferred_order = ['home', 'start', 'enter', 'stop']
    for i in range(len(preferred_order)):
        if preferred_order[i] not in command_list:
            preferred_order.pop(i)
    for command in command_list:
        if command not in preferred_order:
            preferred_order.append(command)
    command_list = preferred_order

# construct sub-commands & options
    for command in command_list:
        command_module = import_module('%s.commands.%s' % (__module__, command))
        try:
            sub_cmd = getattr(command_module, '_cmd_model_%s' % command)
            cmd_details = {
                'usage': '%s %s' % (__command__, sub_cmd['usage']),
                'description': sub_cmd['description'],
                'help': sub_cmd['brief'],
                'formatter_class': lambda prog: HelpFormatter(prog, max_help_position=30, width=80) # adjusts column width to options
            }
            sub_commands = subparsers.add_parser(sub_cmd['command'], **cmd_details)
            sub_commands.set_defaults(command=sub_cmd['command'], model=sub_cmd, **sub_cmd['defaults'])
            for option in sub_cmd['options']:
                sub_commands.add_argument(*option['args'], **option['kwargs'])
        except:
            pass

# call parsing function and run sub-command function with keyword arguments
    args = parser.parse_args(argv)
    opt_dict = vars(args)
    command_module = import_module('%s.commands.%s' % (__module__, args.command))
    run_cmd = getattr(command_module, args.command)
    run_cmd(**opt_dict)

if __name__ == '__main__':
    cli()