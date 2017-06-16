__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

'''
list services
TODO: list images
TODO: list containers
'''

_list_details = {
    'title': 'List',
    'description': 'Generates a list of the resources of a specific type. Only the service resource type is supported, but docker oriented and remote host kinds of resources are coming.',
    'help': 'lists the instances of a resource type',
    'benefit': 'Provides a way to find existing resources.'
}

from pocketlab.init import fields_model

def list(resource_type, paginate=False):

    title = 'list'

# validate inputs
    input_fields = {
        'resource_type': resource_type
    }
    for key, value in input_fields.items():
        if value:
            object_title = '%s(%s=%s)' % (title, key, str(value))
            fields_model.validate(value, '.%s' % key, object_title)

# retrieve window size
    from os import popen
    console_rows, console_columns = popen('stty size', 'r').read().split()
    console_rows = int(console_rows)
    console_columns = int(console_columns)

# list projects
    exit_msg = ''
    if resource_type == 'services':

    # construct registry client
        from pocketlab import __module__
        from labpack.storage.appdata import appdataClient
        registry_client = appdataClient(collection_name='Registry Data', prod_name=__module__)

    # walk registry to compile list of project
        from tabulate import tabulate
        from labpack.records.settings import load_settings
        service_list = []
        left_width = 0
        table_headers = ['Service', 'Path']
        for file_path in registry_client.localhost.walk(registry_client.collection_folder):
            try:
                details = load_settings(file_path)
                service_name = details['service_name']
                service_root = details['service_root']
                if len(service_name) > left_width:
                    left_width = len(service_name)
                service_list.append([service_name, service_root])
            except:
                pass

    # format list of projects
        formatted_rows = []
        for row in service_list:
            row_width = left_width + 2 + len(row[1])
            path_text = row[1]
            if row_width > console_columns:
                cut_char = row_width - console_columns
                left_index = (len(row[1]) - cut_char - 10) * -1
                if left_index > -1:
                    path_text = '%s...' % row[1]
                else:
                    path_text = '%s...%s' % (row[1][0:7], row[1][left_index:])
            formatted_rows.append([row[0], path_text])

    # print out list
        if paginate and len(formatted_rows) + 5 > console_rows:
            page_rows = []
            for i in range(len(formatted_rows)):
                page_rows.append(formatted_rows[i])
                if len(page_rows) + 4 == console_rows:
                    table_text = tabulate(page_rows, headers=table_headers)
                    table_text += '\n[press any key for more]'
                    print(table_text)
                    page_rows = []
                    input()
                elif i + 1 == len(formatted_rows):
                    table_text = tabulate(page_rows, headers=table_headers)
                    if len(page_rows) + 5 == console_rows:
                        table_text += '\n[press any key for more]'
                    print(table_text)
                    if len(page_rows) + 5 == console_rows:
                        input()
        else:
            table_text = tabulate(formatted_rows, headers=table_headers)
            print(table_text)

# list images
    elif resource_type == 'images':
        pass

    return exit_msg
