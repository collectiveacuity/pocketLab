__author__ = 'rcj1492'
__created__ = '2016.03'
__command__ = 'lab'
__version__ = '0.1.0'
__module__ = 'labMgmt'
__testing__ = False

'''
https://docs.python.org/3.5/library/argparse.html?highlight=argparse#module-argparse
'''

import sys
from argparse import ArgumentParser

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

# define command scope & valid sub-command model
    command_list = ['build','home','start','stop']
    cmdModel = None
    if __testing__:
        from jsonmodel.validators import jsonModel
        from jsonmodel.loader import jsonLoader
        cmdModel = jsonModel(jsonLoader(__module__,'rules/cmd-model.json'))

# construct sub-commands & options
    for command in command_list:
        command_module = __import__("labMgmt.commands.%s" % command, fromlist=["labMgmt.commands"])
        sub_cmd = command_module._cmd_details
        if __testing__:
            sub_cmd = cmdModel.validate(sub_cmd)
        cmd_details = {
            'usage': '%s %s' % (__command__, sub_cmd['usage']),
            'description': sub_cmd['description'],
            'help': sub_cmd['description']
        }
        sub_commands = subparsers.add_parser(sub_cmd['command'], **cmd_details)
        sub_commands.set_defaults(command=sub_cmd['command'], **sub_cmd['defaults'])
        for option in sub_cmd['options']:
            sub_commands.add_argument(*option['args'], **option['kwargs'])

# call parsing function and run corresponding sub-command function with keyword arguments
    args = parser.parse_args(argv)
    opt_dict = vars(args)
    run_module = __import__("labMgmt.commands.%s" % args.command, fromlist=["labMgmt.commands"])
    run_module.run(**opt_dict)

if __name__ == '__main__':
    cli()