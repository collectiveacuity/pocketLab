__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

'''
list projects
TODO: list images
TODO: list containers
'''

_list_schema = {
    'title': 'list',
    'description': 'Generates a list of the resources of a specific type.',
    'metadata': {
        'cli_help': 'lists the instances of a resource type'
    },
    'schema': {
        'resource_type': 'projects'
    },
    'components': {
        '.resource_type': {
            'field_description': 'Type of lab resource. eg. projects, images...',
            'default_value': 'projects',
            'discrete_values': [ 'projects' ],
            'field_metadata': {
                # 'cli_group': 'A',
                # 'cli_flags': [ '-p', '--project' ],
                'cli_help': 'type of lab resource. eg. projects, images...',
                'cli_metavar': 'resource'
            }
        }
    }
}

def list(resource_type):

    title = 'list'

# validate inputs
    from jsonmodel.validators import jsonModel
    input_model = jsonModel(_list_schema)
    input_fields = {
        'resource_type': resource_type
    }
    for key, value in input_fields.items():
        object_title = '%s(%s=%s)' % (title, key, str(value))
        input_model.validate(value, '.%s' % key, object_title)

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