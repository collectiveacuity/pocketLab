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
                'action': 'store_true',
                'dest': 'resetPath',
                'help': 'reset path of project root to workdir' }
        },
        {   'args': [ '-p', '--project' ],
            'kwargs': {
                'type': str,
                'metavar': 'NAME',
                'dest': 'projectName',
                'help': 'NAME of project to reset as default home' }
        }
    ]
}

def home(**kwargs):
    print(kwargs)