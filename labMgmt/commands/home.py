__author__ = 'rcj1492'
__created__ = '2016.03'

_cmd_details = {
    'command': 'home',
    'usage': 'home [options]',
    'description': 'transports you to the project home',
    'defaults': {},
    'options': [
        {   'args': [ '-s', '--set' ],
            'kwargs': {
                'type': str,
                'metavar': 'PATH',
                'dest': 'path',
                'help': '(re)set path to project root (default: %(default)s)' }
        }
    ]
}

def run(**kwargs):
    print(kwargs)