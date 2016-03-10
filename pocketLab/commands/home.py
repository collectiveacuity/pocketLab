__author__ = 'rcj1492'
__created__ = '2016.03'

_cmd_details_home = {
    'command': 'home',
    'usage': 'home [options]',
    'description': 'transports you to the project root folder',
    'brief': 'transports you to the project root folder',
    'defaults': {},
    'options': [
        {   'args': [ '-s', '--set' ],
            'kwargs': {
                'type': str,
                'metavar': 'PATH',
                'dest': 'newPath',
                'help': '(re)set path to project root (default: %(default)s)' }
        }
    ]
}

def home(**kwargs):
    print(kwargs)