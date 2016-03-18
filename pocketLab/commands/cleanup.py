__author__ = 'rcj1492'
__created__ = '2016.03'

_cmd_details_cleanup = {
    'command': 'cleanup',
    'usage': 'cleanup [options]',
    'description': 'removes stranded resources in an environment',
    'brief': 'removes stranded resources in an environment',
    'defaults': { },
    'options': [
        {   'args': [ '--environment' ],
            'kwargs': {
                'type': str,
                'default': '',
                'metavar': 'TAG',
                'dest': 'environment',
                'help': 'value of an environment TAG (ie. dev, test, prod)'
            }
        },
        {   'args': [ '--layer' ],
            'kwargs': {
                'type': str,
                'default': '',
                'metavar': 'TAG',
                'dest': 'layer',
                'help': 'value of a layer TAG (interface, processor, persistence)'
            }
        },
        {   'args': [ '--platform' ],
            'kwargs': {
                'type': str,
                'default': 'local',
                'metavar': 'SERVICE',
                'dest': 'platform',
                'help': 'name of platform SERVICE (ie. local, aws, github.io)'
            }
        },
        {   'args': [ '--virtualbox' ],
            'kwargs': {
                'type': str,
                'default': 'default',
                'metavar': 'IMAGE',
                'dest': 'virtualbox',
                'help': 'name of docker virtualbox IMAGE (default: %(default)s)' }
        },
        {   'args': [ '--region' ],
            'kwargs': {
                'type': str,
                'default': 'service default',
                'metavar': 'REGION',
                'dest': 'region',
                'help': 'name of platform service REGION (default: %(default)s)'
            }
        },
    ]
}

def cleanup(**kwargs):

# import dependencies
    from pocketLab.importers.config_file import configFile
    from pocketLab.clients.localhost_client import localhostClient
    from pocketLab.clients.docker_session import dockerSession
    from pocketLab.validators.config_model import configModel

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
        from pocketLab.exceptions.lab_exception import labException
        header_list = [ 'NAMES', 'STATUS', 'IMAGE', 'PORTS']
        error = {
            'kwargs': kwargs,
            'message': 'Container "%s" does not exist. Containers currently active:' % alias_name,
            'tprint': { 'headers': header_list, 'rows': container_list },
            'error_value': alias_name,
            'failed_test': 'required_resource'
        }
        raise labException(**error)

# remove container
    end_command = docker_session.rm(alias_name)
    start_text = 'Sweet! Container "%s" stopped.' % alias_name
    print(start_text)

    return end_command