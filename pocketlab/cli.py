__author__ = 'rcj1492'
__created__ = '2016.03'

'''
https://docs.python.org/3.5/library/argparse.html?highlight=argparse#module-argparse
'''

import sys
from pocketlab.utils import compile_commands, compile_arguments
from pocketlab import __command__, __module__, __version__, __order__
from importlib import import_module
from importlib.util import find_spec
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

# retrieve command line metadata schema
    cli_schema = jsonLoader(__module__, 'models/lab-cli.json')
    module_path = find_spec(__module__).submodule_search_locations[0]

# compile command models
    compile_kwargs = {
        'folder_path': '%s/commands/' % module_path,
        'cli_schema': cli_schema,
        'module_name': __module__,
        'preferred_order': __order__
    }
    command_list = compile_commands(**compile_kwargs)

# construct each command
    for command_model in command_list:

    # add command details to parser
        try:
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
            cmd_args = subparsers.add_parser(command_model.title, **cmd_details)

            # print(cmd_details)

    # construct argument lists
            def_args, req_args, opt_args, exc_args = compile_arguments(command_model)

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