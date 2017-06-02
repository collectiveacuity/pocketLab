__author__ = 'rcj1492'
__created__ = '2017.06'
__license__ = 'MIT'

_stop_details = {
    'title': 'Stop',
    'description': 'Stops and removes a running container for the service.',
    'help': 'terminates running Docker containers',
    'benefit': 'WIP'
}

from pocketlab.init import fields_model

def stop(service_list, verbose=True, virtualbox='default'):
    
    title = 'stop'

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
    from pocketlab.methods.docker import dockerClient
    docker_client = dockerClient(virtualbox_name=virtualbox, verbose=verbose)

# construct list of paths to services
    from pocketlab.methods.service import retrieve_services
    stop_list, msg_insert = retrieve_services(service_list)

# construct lab list
    lab_list = []

# validate lab files
    from os import path
    from pocketlab.methods.validation import validate_lab
    from pocketlab import __module__
    from jsonmodel.loader import jsonLoader
    from jsonmodel.validators import jsonModel
    lab_model = jsonModel(jsonLoader(__module__, 'models/lab-config.json'))
    for details in stop_list:
        file_path = path.join(details['path'], 'lab.yaml')
        service_name = details['name']
        lab_details = validate_lab(lab_model, file_path, service_name)
        details['config'] = lab_details
        lab_list.append(details)

        # retrieve list of docker containers

        # validate lab config container exists
        # TODO resolve name discovery when namespace transmutes

        if verbose:
            print('.', end='', flush=True)

            # end validations
    if verbose:
        print(' done.')

# stop containers
    exit_msg = ''
    for service in lab_list:
        container_alias = service['config']['docker_container_alias']
        docker_status = docker_client.rm(container_alias)
        if docker_status == container_alias:
            exit_msg = 'Container "%s" terminated.' % docker_status
        else:
            raise ValueError(docker_status)
        
    return exit_msg