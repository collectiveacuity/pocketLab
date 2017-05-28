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
