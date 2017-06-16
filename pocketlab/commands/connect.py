__author__ = 'rcj1492'
__created__ = '2017.06'
__license__ = 'MIT'

'''
connect to aws instance
TODO: connect to other platforms
'''

_connect_details = {
    'title': 'connect',
    'description': 'Opens up a direct ssh connection to remote host.',
    'help': 'connects to remote host through ssh',
    'benefit': 'Edit settings on remote host manually.'
}

from pocketlab.init import fields_model

def connect(platform_name, service_list=None, environment_type='prod', resource_tag='',verbose=True):

    title = 'connect'

# validate inputs
    if isinstance(service_list, str):
        if service_list:
            service_list = [service_list]
    input_fields = {
        'service_list': service_list,
        'verbose': verbose,
        'platform_name': platform_name,
        'environment_type': environment_type,
        'resource_tag': resource_tag
    }
    for key, value in input_fields.items():
        if value:
            object_title = '%s(%s=%s)' % (title, key, str(value))
            fields_model.validate(value, '.%s' % key, object_title)

    return input_fields