__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

import sys
from pocketlab.parser import argument_parser
from pocketlab import __module__
from importlib import import_module

def cli(error=False, command=''):

# handle optional error argument
    if error:
        argv = ['-h']
    else:
        argv = sys.argv[1:]

# replace stderr message with help output
    def error_msg(err):
        print('Errr! %s\n' % err)
        cli(error=True)
        sys.exit(2)
    argument_parser.error = error_msg

# call parsing function
    sys_args = argument_parser.parse_args(argv)
    opt_dict = vars(sys_args)

# handle empty command
    if not opt_dict:
        cli(error=True)
        sys.exit(2)

# retrieve appropriate function for sub command
    command_module = import_module('%s.commands.%s' % (__module__, sys_args.command))
    run_cmd = getattr(command_module, sys_args.command)
    del opt_dict['command']

# run function and catch errors
    exit_data = None
    try:
        exit_data = run_cmd(**opt_dict)
    except Exception as err:
        from colorama import Fore, Style
        import re
        def try_sub(x):
            return '%s%s%s' % (Style.RESET_ALL, Fore.CYAN, x.group())
        err_sub = re.sub('[\n\s]Try.*$', try_sub, str(err))
        print('%sErrr! %s%s' % (Fore.RED, err_sub, Style.RESET_ALL))
    if exit_data:
        if isinstance(exit_data, str):
            from colorama import Fore, Style
            exit_data = '%sSweet! %s%s' % (Fore.GREEN, exit_data, Style.RESET_ALL)
        return exit_data

if __name__ == '__main__':
    cli()