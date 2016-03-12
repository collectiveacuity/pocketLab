__author__ = 'rcj1492'
__created__ = '2016.03'

_cmd_details_start = {
    'command': 'start',
    'usage': 'start [options]',
    'description': 'initiates a container with a project component',
    'brief': 'initiates a container with a project component',
    'defaults': {},
    'options': [
        {   'args': [ '-q', '--quiet' ],
            'kwargs': {
                'dest': 'verbose',
                'default': True,
                'help': 'turn off pipe of stdout from container',
                'action': 'store_false'
            }
        },
        {   'args': [ '-b', '--box' ],
            'kwargs': {
                'type': str,
                'default': 'default',
                'metavar': 'VBOX',
                'dest': 'virtualbox',
                'help': 'name of docker virtualbox (default: %(default)s)' }
        },
        {   'args': [ '-f', '--file' ],
            'kwargs': {
                'type': str,
                'default': 'lab-component.json',
                'metavar': 'FILE',
                'dest': 'componentFile',
                'help': 'path to component settings FILE (default: %(default)s)' }
        }
    ]
}

def start(**kwargs):

# import dependencies
    from os import path
    from copy import deepcopy
    from pocketLab.importers.config_file import configFile
    from pocketLab.clients.localhost_session import localhostSession
    from pocketLab.clients.docker_session import dockerSession
    from pocketLab.validators.config_model import configModel
    from pocketLab.validators.absolute_path import absolutePath
    from pocketLab.validators.available_image import availableImage
    from pocketLab.compilers.docker_run import dockerRun

# ingest verbose options
    verbose = kwargs['verbose']

# determine system properties
    localhost = localhostSession()

# ingest & validate component file
    component_file = kwargs['componentFile']
    comp_details = configFile(component_file, kwargs)
    comp_details = configModel(comp_details, 'rules/lab-component-model.json', kwargs, 'component settings')

# determine component root from component file
    root_path, file_name = path.split(path.abspath(component_file))

# construct path details to mounted volumes
    mounted_volumes = {}
    for volume in comp_details['mounted_volumes']:
        host_path = absolutePath(volume, root_path, kwargs, 'mounted volume')
        system_path = host_path.replace('\\','/').replace('C:','//c')
        absolute_path = deepcopy(host_path)
        docker_path = absolute_path.replace(root_path,'')
        container_path = docker_path.replace('\\','/')
        mounted_volumes[system_path] = container_path

# ingest & validate virtualbox property
    vbox_name = kwargs['virtualbox']
    if not localhost.os in ('Windows','Mac'):
        vbox_name = ''

# check for docker installation
    docker_session = dockerSession(kwargs, vbox_name)

# check that docker image is available locally
    image_list = docker_session.images()
    availableImage(comp_details['docker_image'], comp_details['image_tag'], image_list, kwargs)

# retrieve list of active container aliases & busy ports
    container_list = docker_session.ps()
    busy_ports = []
    active_containers = []
    for container in container_list:
        active_containers.append(container['NAMES'])
        container_settings = docker_session.inspect(container['NAMES'])
        container_synopsis = docker_session.synopsis(container_settings)
        if container_synopsis['mapped_ports']:
            for key in container_synopsis['mapped_ports'].keys():
                busy_ports.append(key)

# check that alias name is available
    if comp_details['container_alias'] in active_containers:
        from pocketLab.exceptions.lab_exception import labException
        header_list = [ 'NAMES', 'STATUS', 'IMAGE', 'PORTS']
        error = {
            'kwargs': kwargs,
            'message': 'Container "%s" already in use. Containers currently active:' % comp_details['container_alias'],
            'tprint': { 'headers': header_list, 'rows': container_list },
            'error_value': comp_details['container_alias'],
            'failed_test': 'unavailable_resource'
        }
        raise labException(**error)

# construct port mappings for mapped ports
    mapped_ports = {}
    for port in comp_details['exposed_ports']:
        open_port = int(deepcopy(port))
        while str(open_port) in busy_ports:
            open_port += 1
        mapped_ports[str(open_port)] = str(port)

# add system_ip to injected variables
    system_ip = docker_session.ip()
    injected_variables = {
        'SYSTEM_LOCALHOST': system_ip
    }
    for key, value in comp_details['injected_variables']:
        injected_variables[key] = value

# compile docker run script from settings
    run_details = {
        'name': comp_details['container_alias'],
        'injected_variables': injected_variables,
        'mounted_volumes': mounted_volumes,
        'mapped_ports': mapped_ports,
        'docker_image': comp_details['docker_image'],
        'image_tag': comp_details['image_tag'],
        'run_command': comp_details['run_command']
    }
    run_script = dockerRun(run_details)

# start container
    container_id = docker_session.run(run_script)
    if verbose:
        start_text = 'Sweet! Container "%s" started' % comp_details['container_alias']
        if run_details['mapped_ports']:
            start_text += ' on port'
            if len(run_details['mapped_ports'].keys()) > 1:
                start_text += 's'
            previous_port = False
            for key in run_details['mapped_ports'].keys():
                if previous_port:
                    start_text += ','
                start_text += ' %s:%s' % (system_ip, key)
                previous_port = True
            start_text += '.'
        print(start_text)

    container_details = {
        'mapped_ports': mapped_ports,
        'container_alias': comp_details['container_alias'],
        'container_id': container_id
    }

    return container_details