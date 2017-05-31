__author__ = 'rcj1492'
__created__ = '2016.10'
__license__ = 'MIT'

def retrieve_service_root(service_name, command_context=''):

# construct registry client
    from os import path
    from pocketlab import __module__
    from labpack.storage.appdata import appdataClient
    registry_client = appdataClient(collection_name='Registry Data', prod_name=__module__)

# validate service name exists in registry
    file_name = '%s.yaml' % service_name
    filter_function = registry_client.conditional_filter([{0:{'discrete_values':[file_name]}}])
    service_list = registry_client.list(filter_function=filter_function)
    if not file_name in service_list:
        error_msg = '"%s" not found in the registry.' % service_name
        if command_context:
            error_msg += ' %s' % command_context
        raise ValueError(error_msg)

# retrieve root path to service
    service_details = registry_client.read(file_name)
    if not 'service_root' in service_details.keys():
        error_msg = 'Record for project "%s" has been corrupted.' % service_name
        if command_context:
            error_msg += ' %s' % command_context
        raise ValueError(error_msg)
    service_root = service_details['service_root']
    if not path.exists(service_root):
        error_msg = 'Path %s to project "%s" no longer exists.' % (service_root, service_name)
        if command_context:
            error_msg += ' %s' % command_context
        raise ValueError(error_msg)

    return service_root

def retrieve_services(service_list=None, all=False):
    
    '''
        a method to generate the root path for one or more services
        
    :param service_list: list of strings with name of services
    :param all: boolean to indicate the retrieve all paths in registry
    :return: list of dictionaries, string with exit message insert
    '''
    
# define default returns
    path_list = []
    msg_insert = 'local service'
    
# add named service to service list
    if service_list:
        msg_insert = ''
        for i in range(len(service_list)):
            service = service_list[i]
            if msg_insert:
                if i + 1 == len(service_list):
                    msg_insert += ' and '
                else:
                    msg_insert += ', '
            msg_insert += '"%s"' % service
            service_root = retrieve_service_root(service)
            service_details = {
                'name': service,
                'path': service_root
            }
            path_list.append(service_details)

# add all services in registry to service list
    elif all:
        msg_insert = 'all services'
        from pocketlab import __module__
        from labpack.storage.appdata import appdataClient
        registry_client = appdataClient(collection_name='Registry Data', prod_name=__module__)
        from labpack.records.settings import load_settings
        for file_path in registry_client.localhost.walk(registry_client.collection_folder):
            try:
                details = load_settings(file_path)
                service_details = {
                    'name': details['service_name'],
                    'path': details['service_root']
                }
                path_list.append(service_details)
            except:
                pass

# add local path to service list
    else:
        path_list.append({'name': '', 'path': './'})
    
    return path_list, msg_insert