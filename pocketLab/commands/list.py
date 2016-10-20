__author__ = 'rcj1492'
__created__ = '2016.03'

_cmd_model_list = {
    'command': 'list',
    'description': 'generates a list of current resources',
    'brief': 'generates a list of current resources',
    'args': [
        {
            'name': 'resource',
            'default_value': '',
            'max_length': 64,
            'must_not_contain': [ '[^\w\-_]' ],
            'field_description': 'Type of resources',
            'exclusive_group': '',
            'cli_flags': [ ],
            'cli_help': 'type of resources to list',
            'cli_metavar': 'RESOURCE_TYPE'
        }
    ]
}

def list(**cmd_kwargs):
    print(cmd_kwargs)
# import dependencies
    from time import time
    from os import path
    from pocketlab.clients.registry_client import registryClient