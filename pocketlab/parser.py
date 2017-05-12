__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

'''
REFERENCES
https://docs.python.org/3.6/library/argparse.html#module-argparse
https://docs.python.org/3.5/library/argparse.html?highlight=argparse#module-argparse
'''

from pocketlab import __command__, __module__, __version__, __order__
from pocketlab.fields import cli_schema
from pocketlab.utils import compile_commands, compile_arguments
from importlib.util import find_spec
from argparse import ArgumentParser, HelpFormatter, RawDescriptionHelpFormatter, PARSER

# construct customized formatter class
class SubcommandHelpFormatter(RawDescriptionHelpFormatter):
    def _format_action(self, action):
        parts = super(RawDescriptionHelpFormatter, self)._format_action(action)
        if action.nargs == PARSER:
            parts = "\n".join(parts.split("\n")[1:])
        return parts

# construct argument parser
def construct_parser(description, epilog=''):

# construct main module
    module_args = {
        'description': description,
        'usage': __command__,
        'formatter_class': SubcommandHelpFormatter  # remove sub-command braces in help
    }
    if epilog:
        module_args['epilog'] = epilog
    parser = ArgumentParser(**module_args)
    current_version = '%s %s' % (__module__, __version__)
    parser.add_argument('-v', '--version', action='version', version=current_version)

# construct command parsing method
    help_details = {
        'title': 'list of commands'  # title for sub-commands list in help
    }
    subparsers = parser.add_subparsers(**help_details)

# retrieve module path
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
                'formatter_class': lambda prog: HelpFormatter(prog, max_help_position=30, width=80)
    # adjusts column width to options
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

    return parser

parser_kwargs = {
    'description': 'A laboratory assistant bot.',
    'epilog': '%s can also make coffee.' % __command__
}
argument_parser = construct_parser(**parser_kwargs)


