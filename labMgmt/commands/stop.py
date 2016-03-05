__author__ = 'rcj1492'
__created__ = '2016.03'

_cmd_details = {
    'command': 'stop',
    'usage': 'stop [options]',
    'description': 'terminates container running a project component',
    'defaults': { },
    'options': [
        {   'args': [ '-f', '--file' ],
            'kwargs': {
                'type': str,
                'metavar': 'FILE',
                'default': 'project-logs',
                'dest': 'logfile',
                'help': 'append log report to FILE (default: %(default)s)' }
        }
    ]
}

def run(**kwargs):
    print(kwargs)