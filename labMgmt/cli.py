__author__ = 'rcj1492'
__created__ = '2016.03'
__command__ = 'lab'
__version__ = '0.1.0'

'''
https://docs.python.org/3.5/library/argparse.html?highlight=argparse#module-argparse
'''

import sys
from argparse import ArgumentParser
from labMgmt.commands import *

def cli(error=False):

# handle optional error argument
    if error:
        argv = ['-h']
    else:
        argv = sys.argv[1:]
# construct main module
    module_args = {
        'description': 'A sample command line input parser.',
        'epilog': '%s can also make coffee.' % __command__,
        'usage': '%s command [options]' % __command__
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

# construct sub-command methods
    subparsers = parser.add_subparsers(title='list of commands')

# define start sub-command & options
    start_args = {
        'usage': '%s start [options]' % __command__,
        'description': 'initiates the program',
        'help': 'initiates the program'
    }
    parser_start = subparsers.add_parser('start', **start_args)
    parser_start.set_defaults(func=start, command='start')
    parser_start.add_argument(
        '-q', '--quiet', default=True,
        dest='verbose', help="don't print status messages to stdout (default: %(default)s)",
        action='store_false'
    )
    parser_start.add_argument(
        '-g', '--group', type=int, default=1,
        dest='gid', help='group id %(type)s for billing (default: %(default)s)'
    )

# define stop sub-command & options
    stop_args = {
        'usage': '%s stop [options]' % __command__,
        'description': 'terminates the program',
        'help': 'terminates the program'
    }
    parser_stop = subparsers.add_parser('stop', **stop_args)
    parser_stop.set_defaults(func=stop, command='stop')
    parser_stop.add_argument(
        '-f', '--file', type=str, default='',
        dest='filename', help='write log report to FILE',
        metavar='FILE'
    )

# define pause sub-command
    pause_args = {
        'usage': '%s pause [options]' % __command__,
        'description': 'pauses the program',
        'help': 'pauses the program'
    }
    parser_pause = subparsers.add_parser('pause', **pause_args)
    parser_pause.set_defaults(func=pause, command='pause')

# call parsing function and print output as dictionary
    args = parser.parse_args(argv)
    opt_dict = vars(args)
    args.func(**opt_dict)

if __name__ == '__main__':
    cli()