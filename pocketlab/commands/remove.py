__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

'''
remove projects
'''

_remove_details = {
    'title': 'Remove',
    'description': 'Removes a project from the lab registry.',
    'help': 'removes a project from the registry',
    'benefit': 'Removes a project from the lab registry.'
}

from pocketlab.init import fields_model

def remove(project_name):

    title = 'remove'

# validate inputs
    input_fields = {
        'project_name': project_name
    }
    for key, value in input_fields.items():
        if value:
            object_title = '%s(%s=%s)' % (title, key, str(value))
            fields_model.validate(value, '.%s' % key, object_title)

# construct registry client
    from pocketlab import __module__
    from labpack.storage.appdata import appdataClient
    registry_client = appdataClient(collection_name='Registry Data', prod_name=__module__)

# search for project name
    exit_msg = ''
    project_key = '%s.yaml' % project_name
    search_condition = [{ 0: { 'discrete_values':[project_key] } }]
    search_filter = registry_client.conditional_filter(search_condition)
    search_results = registry_client.list(search_filter)
    if not search_results:
        raise ValueError('"%s" does not exist in project registry.' % project_name)
    else:
        registry_client.delete(search_results[0])
        exit_msg = '"%s" removed from project registry.' % project_name

    return exit_msg
