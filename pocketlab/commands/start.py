__author__ = 'rcj1492'
__created__ = '2016.03'

_start_details = {
    'title': 'Start',
    'description': 'Initiates a container with the Docker image for a service.',
    'help': 'initiates a Docker container for service',
    'benefit': 'WIP'
}

from pocketlab.init import fields_model

def start(service_list, verbose=True, virtualbox='default'):

    title = 'start'

# validate inputs
    if isinstance(service_list, str):
        if service_list:
            service_list = [service_list]
    input_fields = {
        'service_list': service_list,
        'verbose': verbose,
        'virtualbox': virtualbox
    }
    for key, value in input_fields.items():
        if value:
            object_title = '%s(%s=%s)' % (title, key, str(value))
            fields_model.validate(value, '.%s' % key, object_title)

# validate requirements
    if verbose:
        print('Checking dependencies...', end='', flush=True)

# validate installation of docker
    from pocketlab.methods.validation import validate_docker
    validate_docker()
    if verbose:
        print('.', end='', flush=True)

# validate virtualbox running
    from pocketlab.methods.validation import validate_virtualbox
    box_running = validate_virtualbox(virtualbox)
    if verbose:
        print('.', end='', flush=True)

# inject variables required to connect to virtualbox
    if box_running:
        from os import environ
        if not environ.get('DOCKER_CERT_PATH'):
            import re
            from subprocess import check_output
            sys_command = 'docker-machine env %s' % virtualbox
            cmd_output = check_output(sys_command).decode('utf-8')
            variable_list = ['DOCKER_TLS_VERIFY', 'DOCKER_HOST', 'DOCKER_CERT_PATH', 'DOCKER_MACHINE_NAME']
            for variable in variable_list:
                env_start = '%s="' % variable
                env_end = '"\\n'
                env_regex = '%s.*?%s' % (env_start, env_end)
                env_pattern = re.compile(env_regex)
                env_statement = env_pattern.findall(cmd_output)
                env_var = env_statement[0].replace(env_start, '').replace('"\n', '')
                environ[variable] = env_var

# construct list of paths to services
    from pocketlab.methods.service import retrieve_services
    start_list, msg_insert = retrieve_services(service_list)

# construct lab list
    lab_list = []
    
# validate lab files
    from os import path
    from pocketlab.methods.validation import validate_lab
    from pocketlab import __module__
    from jsonmodel.loader import jsonLoader
    from jsonmodel.validators import jsonModel
    lab_model = jsonModel(jsonLoader(__module__, 'models/lab-config.json'))
    for details in start_list:
        file_path = path.join(details['path'], 'lab.yaml')
        service_name = details['name']
        lab_details = validate_lab(lab_model, file_path, service_name)
        details['config'] = lab_details
        lab_list.append(details)
        
# retrieve list of docker images

# validate lab config image exists
        
# retrieve list of docker containers

# validate lab config container doesn't already exist
# TODO resolve name conflicts on deploy updating
        
# validate mount paths exist
        
# end validations
    if verbose:
        print(' done.')

# retrieve system ip
    if box_running:
        from subprocess import check_output
        sys_command = 'docker-machine ip %s' % virtualbox
        system_ip = check_output(sys_command).decode('utf-8')
    else:
        from labpack.platforms.localhost import localhostClient
        localhost_client = localhostClient()
        system_ip = localhost_client.ip

# instantiate containers
    exit_msg = ''
    port_list = []
    for service in lab_list:
        service_config = service['config']
        service_name = service['name']
        service_root = service['path']

    # construct environment variables
        container_envvar = { 'SYSTEM_IP_ADDRESS': system_ip }
        if service_config['docker_environment_variables']:
            for key, value in service_config['docker_environment_variables'].items():
                container_envvar[key.upper()] = '"%s"' % value
    
    # construct sys command
        container_name = service_config['docker_container_alias']
        sys_command = 'docker run --name %s' % container_name
        for key, value in container_envvar.items():
            sys_command += ' -e %s=%s' % (key, value)
        if service_config['docker_mount_volumes']:
            for key, value in service_config['docker_mount_volumes'].items():
                sys_command += ' -v "%s":"%s"' % (key, value)
        sys_command += ' -it -d'
        if service_config['docker_port_mapping']:
            for key, value in service_config['docker_port_mapping'].items():
                port_value = value
                if value in port_list:
                    from copy import deepcopy
                    port_value = deepcopy(value)
                    for i in range(1000):
                        port_value += 1
                        if not port_value in port_list:
                            break
                port_list.append(port_value)
                sys_command += ' -p %s:%s' % (str(port_value), key)
        sys_command += ' %s' % service_config['docker_image_name'] 
    
    # run command
        from subprocess import check_output
        docker_response = check_output(sys_command).decode('utf-8')
        exit_msg = 'Container "%s" started.\nTo stop "%s": docker rm -f %s' % (
    container_name, container_name, container_name)

    return exit_msg

# # import dependencies
#     from os import path
#     from copy import deepcopy
#     from pocketlab.importers.config_file import configFile
#     from pocketlab.clients.localhost_client import localhostClient
#     from pocketlab.clients.docker_session import dockerSession
#     from pocketlab.validators.config_model import configModel
#     from pocketlab.validators.absolute_path import absolutePath
#     from pocketlab.validators.available_image import availableImage
#     from pocketlab.compilers.docker_run import dockerRun
#
# # ingest verbose options
#     verbose = kwargs['verbose']
#
# # determine system properties
#     localhost = localhostClient()
#
# # ingest & validate component file
#     component_file = kwargs['componentFile']
#     comp_details = configFile(component_file, kwargs)
#     comp_details = configModel(comp_details, 'rules/lab-component-model.json', kwargs, 'component settings')
#
# # determine component root from component file
#     root_path, file_name = path.split(path.abspath(component_file))
#
# # construct path details to mounted volumes
#     mounted_volumes = {}
#     for volume in comp_details['mounted_volumes']:
#         host_path = absolutePath(volume, root_path, kwargs, 'mounted volume')
#         system_path = host_path.replace('\\','/').replace('C:','//c')
#         absolute_path = deepcopy(host_path)
#         docker_path = absolute_path.replace(root_path,'')
#         container_path = docker_path.replace('\\','/')
#         mounted_volumes[system_path] = container_path
#
# # ingest & validate virtualbox property
#     vbox_name = kwargs['virtualbox']
#     if not localhost.os in ('Windows','Mac'):
#         vbox_name = ''
#
# # check for docker installation
#     docker_session = dockerSession(kwargs, vbox_name)
#
# # check that docker image is available locally
#     image_list = docker_session.images()
#     availableImage(comp_details['docker_image'], comp_details['image_tag'], image_list, kwargs)
#
# # retrieve list of active container aliases & busy ports
#     container_list = docker_session.ps()
#     busy_ports = []
#     active_containers = []
#     for container in container_list:
#         active_containers.append(container['NAMES'])
#         container_settings = docker_session.inspect(container_alias=container['NAMES'])
#         container_synopsis = docker_session.synopsis(container_settings)
#         if container_synopsis['mapped_ports']:
#             for key in container_synopsis['mapped_ports'].keys():
#                 busy_ports.append(key)
#
# # check that alias name is available
#     if comp_details['container_alias'] in active_containers:
#         from pocketlab.exceptions.lab_exception import labException
#         header_list = [ 'NAMES', 'STATUS', 'IMAGE', 'PORTS']
#         error = {
#             'kwargs': kwargs,
#             'message': 'Container "%s" already in use. Containers currently active:' % comp_details['container_alias'],
#             'tprint': { 'headers': header_list, 'rows': container_list },
#             'error_value': comp_details['container_alias'],
#             'failed_test': 'unavailable_resource'
#         }
#         raise labException(**error)
#
# # construct port mappings for mapped ports
#     mapped_ports = {}
#     for port in comp_details['exposed_ports']:
#         open_port = int(deepcopy(port))
#         while str(open_port) in busy_ports:
#             open_port += 1
#         mapped_ports[str(open_port)] = str(port)
#
# # add system_ip to injected variables
#     system_ip = docker_session.ip()
#     injected_variables = {
#         'SYSTEM_LOCALHOST': system_ip
#     }
#     for key, value in comp_details['injected_variables'].items():
#         injected_variables[key] = value
#
# # compile docker run script from settings
#     run_details = {
#         'name': comp_details['container_alias'],
#         'injected_variables': injected_variables,
#         'mounted_volumes': mounted_volumes,
#         'mapped_ports': mapped_ports,
#         'docker_image': comp_details['docker_image'],
#         'image_tag': comp_details['image_tag'],
#         'run_command': comp_details['run_command']
#     }
#     run_script = dockerRun(run_details)
#
# # start container
#     container_id = docker_session.run(run_script)
#     if verbose:
#         start_text = 'Sweet! Container "%s" started' % comp_details['container_alias']
#         if run_details['mapped_ports']:
#             start_text += ' on port'
#             if len(run_details['mapped_ports'].keys()) > 1:
#                 start_text += 's'
#             previous_port = False
#             for key in run_details['mapped_ports'].keys():
#                 if previous_port:
#                     start_text += ','
#                 start_text += ' %s:%s' % (system_ip, key)
#                 previous_port = True
#             start_text += '.'
#         print(start_text)
#
#     container_details = {
#         'mapped_ports': mapped_ports,
#         'container_alias': comp_details['container_alias'],
#         'container_id': container_id
#     }
#
#     return container_details