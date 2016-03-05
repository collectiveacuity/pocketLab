__author__ = 'rcj1492'
__created__ = '2016.03'

_cmd_details = {
    'command': 'start',
    'usage': 'start [options]',
    'description': 'initiates a container with project component',
    'defaults': {},
    'options': [
        {   'args': [ '-q', '--quiet' ],
            'kwargs': {
                'dest': 'verbose',
                'default': True,
                'help': 'turn off status messages from (default: %(default)s)',
                'action': 'store_false'
            }
        }
    ]
}

def run(**kwargs):
    print(kwargs)