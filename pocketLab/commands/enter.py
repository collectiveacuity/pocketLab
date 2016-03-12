__author__ = 'rcj1492'
__created__ = '2016.03'

_cmd_details_enter = {
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
                'dest': 'containerAlias',
                'help': 'name of container ALIAS (default: "container_alias" value in local lab-component.json)'
            }
        },
        {   'args': [ '-b', '--box' ],
            'kwargs': {
                'type': str,
                'default': 'default',
                'metavar': 'VBOX',
                'dest': 'virtualbox',
                'help': 'name of docker virtualbox (default: %(default)s)' }
        }
    ]
}

def enter(**kwargs):

# import dependencies
    from pocketLab.importers.config_file import configFile
    from pocketLab.clients.localhost_session import localhostSession
    from pocketLab.clients.docker_session import dockerSession
    from pocketLab.validators.config_model import configModel
    from pocketLab.exceptions.lab_exception import labException

# determine system properties
    localhost = localhostSession()

# ingest & validate virtualbox property
    vbox_name = kwargs['virtualbox']
    if not localhost.os in ('Windows','Mac'):
        vbox_name = ''

# check for docker installation
    docker_session = dockerSession(kwargs, vbox_name)

# retrieve list of container aliases
    container_list = docker_session.ps()
    alias_list = []
    for container in container_list:
        alias_list.append(container['NAMES'])

# ingest & validate alias name
    alias_name = kwargs['containerAlias']
    if alias_name == '':
        comp_details = configFile('lab-component.json', kwargs)
        comp_details = configModel(comp_details, 'rules/lab-component-model.json', kwargs, 'component settings')
        alias_name = comp_details['container_alias']

# check that container exists
    if not alias_name in alias_list:
        header_list = [ 'NAMES', 'STATUS', 'IMAGE', 'PORTS']
        error = {
            'kwargs': kwargs,
            'message': 'Container "%s" does not exist. Containers currently active:' % alias_name,
            'tprint': { 'headers': header_list, 'rows': container_list },
            'error_value': alias_name,
            'failed_test': 'required_resource'
        }
        raise labException(**error)

# tty command
    docker_session.enter(localhost.os, alias_name)

    return True