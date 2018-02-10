__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

'''
starts services in docker containers
'''

_start_details = {
    'title': 'Start',
    'description': 'Initiates a container with the Docker image for one or more services.',
    'help': 'initiates Docker containers for services',
    'benefit': 'Makes services available on localhost'
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

# validate installation of docker
    from labpack.platforms.docker import dockerClient
    docker_client = dockerClient(virtualbox_name=virtualbox, verbose=verbose)

# verbosity
    if verbose:
        print('Checking service configurations...', end='', flush=True)

# construct list of paths to services
    from pocketlab.methods.service import retrieve_services
    start_list, msg_insert = retrieve_services(service_list)

# retrieve local docker images
    docker_images = docker_client.images()

# construct lab list
    lab_list = []
    port_list = []

# retrieve docker-compose schemas
    from copy import deepcopy
    from os import path
    from labpack.parsing.grammar import join_words
    from pocketlab.methods.validation import validate_compose
    from pocketlab import __module__
    from jsonmodel.loader import jsonLoader
    from jsonmodel.validators import jsonModel
    compose_model = jsonModel(jsonLoader(__module__, 'models/compose-config.json'))
    service_model = jsonModel(jsonLoader(__module__, 'models/service-config.json'))

# validate docker-compose files
    for details in start_list:
        file_path = path.join(details['path'], 'docker-compose.yaml')
        service_name = deepcopy(details['name'])
        compose_details = validate_compose(compose_model, service_model, file_path, service_name)
        if service_name:
            details['config'] = compose_details['services'][service_name]
        else:
            for key, value in compose_details['services'].items():
                details['config'] = value
                details['name'] = key
                break
        
    # construct message insert
        msg_insert = 'working directory'
        if service_name:
            msg_insert = 'root directory for "%s"' % service_name
        compose_insert = 'docker-compose.yaml file in %s' % msg_insert
        
    # validate image field in docker compose file 
        if not 'image' in details['config'].keys():
            raise ValueError('%s is missing the image field for services.%s' % (compose_insert, details['name']))
        elif not details['config']['image']:
            raise ValueError('%s is missing a value for field service.%s.image' % (compose_insert, details['name']))
        
    # validate image exists in local docker repository
        image_exists = False
        image_name = details['config']['image']
        image_segments = image_name.split(':')
        image_repo = image_segments[0]
        image_tag = ''
        if len(image_segments) > 1:
            image_tag = image_segments[1]
        for image in docker_images:
            if image_repo == image['REPOSITORY']:
                if image_tag:
                    if image_tag == image['TAG']:
                        image_exists = True
                else:
                    image_exists = True
        if not image_exists:
            raise ValueError('%s image "%s" not found on local device.\nTry either: "docker pull %s" or "docker build -t %s ."' % (compose_insert, image_name, image_name, image_name))
        details['image'] = image_repo
        details['tag'] = image_tag
        
    # retrieve list of docker containers
        docker_containers = docker_client.ps()

    # validate container alias does not already exist
        if 'container_name' in details['config'].keys():
            container_alias = details['config']['container_name']
        else:
            container_alias = details['name']
        container_exists = False
        for alias in docker_containers:
            if container_alias == alias['NAMES'].split()[0]:
                container_exists = True
        if container_exists:
            raise ValueError('%s container alias "%s" already exists.\nTry first: "docker rm -f %s"' % (compose_insert, container_alias, container_alias))
        details['alias'] = container_alias
        
    # validate mount paths exist
        if 'volumes' in details['config'].keys():
            for volume in details['config']['volumes']:
                if volume['type'] == 'bind':
                    volume_path = path.join(details['path'], volume['source'])
                    if not path.exists(volume_path):
                        raise ValueError('%s volume.source value "%s" is not a valid path.' % (compose_insert, volume['source']))

    # validate ports are available
        if 'ports' in details['config'].keys():
            for i in range(len(details['config']['ports'])):
                test_ports = []
                port_string = details['config']['ports'][i]
                port_split = port_string.split(':')
                sys_port = port_split[0]
                range_split = sys_port.split('-')
                port_start = range_split[0]
                port_end = ''
                if len(range_split) > 1:
                    port_end = range_split[1]
                if not port_end:
                    test_ports.append(int(port_start))
                else:
                    if port_end <= port_start:
                        raise ValueError('%s ports[%s] value "%s" is invalid port mapping.' % (compose_insert, str(i), port_string))
                    for j in range(int(port_start),int(port_end) + 1):
                        test_ports.append(j)
                for port in test_ports:
                    if port in port_list:
                        raise ValueError('%s ports[%s] value "%s" is already mapped to another container.' % (compose_insert, str(i), str(port)))
                    else:
                        try:
                            docker_client.command('lsof -Pi :%s -sTCP:LISTEN -t' % port)
                            raise ValueError('%s ports[%s] value "%s" is already mapped to a local process.' % (compose_insert, str(i), str(port)))
                        except:
                            pass
                        port_list.append(port)

    # print progress for each service
        lab_list.append(details)
        if verbose:
            print('.', end='', flush=True)

# end validations
    if verbose:
        print(' done.')

# retrieve system ip
    system_ip = docker_client.ip()

# instantiate containers
    exit_msg = ''
    container_list = []
    for service in lab_list:
        service_config = service['config']
        service_alias = service['alias']
        service_image = service['image']
        service_tag = service['tag']
        service_name = service['name']
        service_path = service['path']
        container_list.append(service_alias)

    # construct default docker run kwargs
        run_kwargs = {
            'image_name': service_image, 
            'container_alias': service_alias, 
            'image_tag': service_tag, 
            'environmental_variables': {
                'SYSTEM_LOCALHOST': system_ip
            }, 
            'mapped_ports': None, 
            'mounted_volumes': None, 
            'start_command': '', 
            'network_name': 'host'
        }

    # add optional compose variables
        if 'environment' in service_config.keys():
            run_kwargs['environmental_variables'].update(service_config['environment'])
        if 'ports' in service_config.keys():
            run_kwargs['mapped_ports'] = {}
            for port in service_config['ports']:
                port_split = port.split(':')
                sys_port = port_split[0]
                con_port = port_split[1]
                run_kwargs['mapped_ports'][sys_port] = con_port
        if 'volumes' in service_config.keys():
            run_kwargs['mounted_volumes'] = {}
            for volume in service_config['volumes']:
                if volume['type'] == 'bind':
                    volume_path = path.join(service_path, volume['source'])
                    run_kwargs['mounted_volumes'][volume_path] = volume['target']
        if 'command' in service_config.keys():
            run_kwargs['start_command'] = service_config['command']
        if 'networks' in service_config.keys():
            if service_config['networks']:
                run_kwargs['network_name'] = service_config['networks'][0]

        print(run_kwargs)
        
    # run docker run
        # docker_client.run(**run_kwargs)

    # report outcome
        port_msg = ''
        if 'ports' in service_config.keys():
            if service_config['ports']:
                port_string = ''
                for port in service_config['ports']:
                    if port_string:
                        port_string += ','
                    port_split = port.split(':')
                    sys_port = port_split[0]
                    port_string += sys_port
                port_msg = ' at %s:%s' % (system_ip, port_string)
        service_msg = 'Container "%s" started%s' % (service_alias, port_msg)
        if len(lab_list) > 1:
            if verbose:
                print(service_msg)
        else:
            exit_msg = service_msg

    # TODO consider ROLLBACK options

    if len(lab_list) > 1:
        containers_string = join_words(container_list)
        exit_msg = 'Finished starting containers %s' % containers_string

    return exit_msg