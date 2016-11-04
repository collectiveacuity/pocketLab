__author__ = 'rcj1492'
__created__ = '2016.10'
__license__ = 'MIT'

def retrieve_project_root(project_name, command_context=''):

# construct registry client
    from os import path
    from pocketlab import __module__
    from labpack.storage.appdata import appdataClient
    registry_client = appdataClient(collection_name='Registry Data', prod_name=__module__)

# validate project name exists in registry
    file_name = '%s.yaml' % project_name
    filter_function = registry_client.conditionalFilter([{0:{'discrete_values':[file_name]}}])
    project_list = registry_client.list(filter_function=filter_function)
    if not file_name in project_list:
        error_msg = '"%s" not found in the registry.' % project_name
        if command_context:
            error_msg += ' %s' % command_context
        raise ValueError(error_msg)

# retrieve root path to project
    project_details = registry_client.read(file_name)
    if not 'project_root' in project_details.keys():
        error_msg = 'Record for project "%s" has been corrupted.' % project_name
        if command_context:
            error_msg += ' %s' % command_context
        raise ValueError(error_msg)
    project_root = project_details['project_root']
    if not path.exists(project_root):
        error_msg = 'Path %s to project "%s" no longer exists.' % (project_root, project_name)
        if command_context:
            error_msg += ' %s' % command_context
        raise ValueError(error_msg)

    return project_root
