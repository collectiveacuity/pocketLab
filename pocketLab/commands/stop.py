__author__ = 'rcj1492'
__created__ = '2016.03'

_cmd_model_stop = {
    'command': 'stop',
    'usage': 'stop [options]',
    'description': 'terminates container running a project component',
    'brief': 'terminates container running a project component',
    'defaults': { },
    'options': [
        {   'args': [ '-a', '--alias' ],
            'kwargs': {
                'type': str,
                'default': '',
                'metavar': 'ALIAS',
                'dest': 'containerAlias',
                'help': 'name of container ALIAS (default: "container_alias" value in local labComponent.yaml)'
            }
        },
        {   'args': [ '--virtualbox' ],
            'kwargs': {
                'type': str,
                'default': 'default',
                'metavar': '',
                'dest': 'virtualbox',
                'help': 'name of docker virtualbox (default: %(default)s)' }
        }
    ]
}

def stop(**kwargs):

# import dependencies
    from pocketlab.importers.config_file import configFile
    from pocketlab.clients.localhost_client import localhostClient
    from pocketlab.clients.docker_session import dockerSession
    from pocketlab.validators.config_model import configModel
    from pocketlab.validators.removable_container import removableContainer

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
    alias_name = kwargs['containerAlias']
    if alias_name == '':
        comp_details = configFile('labComponent.yaml', kwargs)
        comp_details = configModel(comp_details, 'rules/lab-component-model.json', kwargs, 'component settings')
        alias_name = comp_details['container_alias']

# validate the removability of container
    removableContainer(alias_name, container_list, kwargs)

# remove container
    end_command = docker_session.rm(alias_name)
    stop_text = 'Sweet! Container "%s" stopped.' % alias_name
    print(stop_text)

    return end_command