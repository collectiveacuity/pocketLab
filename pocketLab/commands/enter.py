__author__ = 'rcj1492'
__created__ = '2016.03'

'''
    local (no platform option) - opens up a pseudo-tty to a running container
    # TODO: remote - opens up a pseudo-tty to a running instance
'''

_cmd_model_enter = {
    'command': 'enter',
    'usage': 'enter [options]',
    'description': 'opens up a shell cli inside a running container',
    'brief': 'opens up a shell cli inside a running container',
    'defaults': { },
    'options': [
        {   'args': [ '-a', '--alias' ],
            'kwargs': {
                'type': str,
                'default': '',
                'metavar': 'ALIAS',
                'dest': 'alias',
                'help': 'name of container ALIAS (default: "container_alias" value in local labComponent.yaml)'
            }
        },
        {   'args': [ '--virtualbox' ],
            'kwargs': {
                'type': str,
                'default': 'default',
                'metavar': 'IMAGE',
                'dest': 'virtualbox',
                'help': 'name of docker virtualbox IMAGE (default: %(default)s)' }
        }
    ]
}

def enter(**kwargs):

# import dependencies
    from pocketLab.importers.config_file import configFile
    from pocketLab.clients.localhost_client import localhostClient
    from pocketLab.clients.docker_session import dockerSession
    from pocketLab.validators.config_model import configModel
    from pocketLab.validators.available_container import availableContainer

# determine system properties
    localhost = localhostClient()

# ingest & validate virtualbox property
    vbox_name = kwargs['virtualbox']
    if not localhost.os in ('Windows','Mac'):
        vbox_name = ''

# check for docker installation
    docker_session = dockerSession(kwargs, vbox_name)

# retrieve list of container aliases
    container_list = docker_session.ps()

# ingest & validate alias name
    alias_name = kwargs['alias']
    if alias_name == '':
        comp_details = configFile('labComponent.yaml', kwargs)
        comp_details = configModel(comp_details, 'rules/lab-component-model.json', kwargs, 'component settings')
        alias_name = comp_details['container_alias']

# validate availability of container
    availableContainer(alias_name, container_list, kwargs)

# tty command
    docker_session.enter(localhost.os, alias_name)

    return True