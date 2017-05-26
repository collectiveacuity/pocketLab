__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

'''
list projects
TODO: list images
TODO: list containers
'''

_list_details = {
    'title': 'List',
    'description': 'Generates a list of the resources of a specific type.',
    'help': 'lists the instances of a resource type',
    'benefit': 'WIP'
}

from pocketlab.init import fields_model

def list(resource_type):

    title = 'list'

# validate inputs
    input_fields = {
        'resource_type': resource_type
    }
    for key, value in input_fields.items():
        if value:
            object_title = '%s(%s=%s)' % (title, key, str(value))
            fields_model.validate(value, '.%s' % key, object_title)

# construct registry client
    from pocketlab import __module__
    from labpack.storage.appdata import appdataClient
    registry_client = appdataClient(collection_name='Registry Data', prod_name=__module__)

# list projects
    from labpack.records.settings import load_settings
    for file_path in registry_client.localhost.walk(registry_client.collection_folder):
        try:
            details = load_settings(file_path)
            project_name = details['project_name']
            project_root = details['project_root']
            print(project_name, project_root)
        except:
            pass

    exit_msg = resource_type

    return exit_msg