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

def list(resource_type, platform_option, region_name='', paginate=False):

    title = 'list'

# validate inputs
    if isinstance(platform_option, str):
        if platform_option:
            platform_option = [platform_option]
    input_fields = {
        'resource_type': resource_type,
        'platform_option': platform_option,
        'region_name': region_name
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

    # walk registry to compile list of services
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

    # format list of services
        formatted_rows = []
        for row in service_list:
            row_width = left_width + 2 + len(row[1])
            path_text = row[1]
            if row_width > console_columns:
                cut_char = row_width - console_columns
                left_index = (len(row[1]) - cut_char - 12) * -1
                if left_index > -1:
                    path_text = '%s...' % row[1]
                else:
                    path_text = '%s...%s' % (row[1][0:9], row[1][left_index:])
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

# list instances
    elif resource_type == 'instances':
    
    # determine platform name
        if not platform_option:
            from copy import deepcopy
            from labpack.parsing.grammar import join_words
            platform_list = deepcopy(fields_model.components['.platform_name']['discrete_values'])
            if len(platform_list) > 2:
                platform_list = platform_list[0:2]
            platform_options = join_words(platform_list, operator='disjunctive')
            raise ValueError('list instances requires a platform name (eg. %s)' % platform_options)
        platform_name = platform_option[0]
    
    # construct registry client
        from pocketlab import __module__
        from labpack.storage.appdata import appdataClient
        registry_client = appdataClient(collection_name='Registry Data', prod_name=__module__)

    # walk registry to compile list of services
        service_list = []
        from labpack.records.settings import load_settings
        for file_path in registry_client.localhost.walk(registry_client.collection_folder):
            try:
                details = load_settings(file_path)
                service_name = details['service_name']
                service_root = details['service_root']
                service_list.append({
                    'name': service_name, 
                    'path': service_root}
                )
            except:
                pass

    # TODO add state information to instances

    # construct empty instance list
        instance_list = []

    # process heroku
        if platform_name == 'heroku':

        # import dependencies
            from pocketlab.methods.validation import validate_platform
            from pocketlab import __module__
            from jsonmodel.loader import jsonLoader
            from jsonmodel.validators import jsonModel
            heroku_schema = jsonLoader(__module__, 'models/heroku-config.json')
            heroku_model = jsonModel(heroku_schema)

        # construct account map
            account_map = {}
            for service in service_list:
                try:
                # retrieve services with heroku credentials
                    heroku_details = validate_platform(heroku_model, service['path'], service['name'])
                    instance_details = {
                        'id': '',
                        'updated': '',
                        'state': '',
                        'login': heroku_details['heroku_account_email'],
                        'machine': '',
                        'image': '',
                        'region': '',
                        'access': heroku_details['heroku_auth_token'],
                        'ip_address': heroku_details['heroku_app_subdomain'] + '.herokuapp.com',
                        'name': heroku_details['heroku_app_subdomain'],
                        'environment': 'prod',
                        'services': service['name']
                    }
                # add service to account map
                    instance_list.append(instance_details)
                    if not heroku_details['heroku_account_email'] in account_map.keys():
                        account_map[heroku_details['heroku_account_email']] = {
                            'token': heroku_details['heroku_auth_token'],
                            'apps': {}
                        }
                    app_name = heroku_details['heroku_app_subdomain']
                    account_map[heroku_details['heroku_account_email']]['apps'][app_name] = instance_details
                except:
                    pass

        # construct instance list
            for key, value in account_map.items():

            # initialize heroku client
                from labpack.platforms.heroku import herokuClient
                heroku_kwargs = {
                    'account_email': key,
                    'auth_token': value['token'],
                    'verbose': False
                }
                heroku_client = herokuClient(**heroku_kwargs)
                for app in heroku_client.apps:
                    app_name = app['name']
                    if app_name in value['apps'].keys():
                        instance_details = value['apps'][app_name]
                        instance_details['region'] = app['region']['name']
                        instance_details['id'] = app['id']
                        instance_details['updated'] = app['update_at']
                        instance_details['ip_address'] = app['web_url'].replace('https://','').replace('/','')
                        instance_details['image'] = app['build_stack']['id']

                    # find state of first non-idle dyno
                        import json
                        state_cmd = 'heroku ps -a %s --json' % app_name
                        response = heroku_client._handle_command(state_cmd)
                        dyno_list = json.loads(response)
                        for dyno in dyno_list:
                            instance_details['state'] = dyno['state']
                            if dyno['state'] != 'idle':
                                break

                    # find machine
                        scale_cmd = 'heroku ps:scale -a %s' % app_name
                        response = heroku_client._handle_command(scale_cmd)
                        instance_details['machine'] = response.strip()

                    # add details to list
                        instance_list.append(instance_details)

    # process ec2
        elif platform_name == 'ec2':

        # check for dependencies
            from pocketlab.methods.dependencies import import_boto3
            import_boto3('ec2 platform')

        # TODO support compilation of accounts and regions

        # retrieve aws config
            service_root = './'
            service_name = ''
            service_insert = 'in working directory'
            from pocketlab import __module__
            from jsonmodel.loader import jsonLoader
            from jsonmodel.validators import jsonModel
            from pocketlab.methods.validation import validate_platform
            aws_schema = jsonLoader(__module__, 'models/aws-config.json')
            aws_model = jsonModel(aws_schema)
            aws_config = validate_platform(aws_model, service_root, service_name)
    
        # retrieve instance details from ec2
            from pocketlab.init import logger
            logger.disabled = True
            ec2_config = {
                'access_id': aws_config['aws_access_key_id'],
                'secret_key': aws_config['aws_secret_access_key'],
                'region_name': aws_config['aws_default_region'],
                'owner_id': aws_config['aws_owner_id'],
                'user_name': aws_config['aws_user_name'],
                'verbose': False
            }
            from pocketlab.methods.aws import construct_client_ec2
            ec2_client = construct_client_ec2(ec2_config, region_name, service_insert)
            ec2_list = ec2_client.list_instances()
            for instance_id in ec2_list:
                instance_details = {
                    'id': instance_id,
                    'updated': '',
                    'state': '',
                    'name': '',
                    'login': '',
                    'services': '',
                    'environment': '',
                    'machine': '',
                    'image': '',
                    'ip_address': '',
                    'region': '',
                    'access_key': ''
                }
                ec2_details = ec2_client.read_instance(instance_id)
                if ec2_details['tags']:
                    for tag in ec2_details['tags']:
                        if tag['key'] == 'Containers':
                            instance_details['services'] = tag['value'].strip()
                        if tag['key'] == 'Env':
                            instance_details['environment'] = tag['value'].strip()
                        if tag['key'] == 'Name':
                            instance_details['name'] = tag['value'].strip()
                        if tag['key'] == 'LoginName':
                            instance_details['login'] = tag['value'].strip()
                if 'instance_type' in ec2_details.keys():
                    instance_details['machine'] = ec2_details['instance_type'].strip()
                if 'key_name' in ec2_details.keys():
                    instance_details['access_key'] = ec2_details['key_name']
                if 'image_id' in ec2_details.keys():
                    instance_details['image'] = ec2_details['image_id']
                if 'region' in ec2_details.keys():
                    instance_details['region'] = ec2_details['region']
                if 'public_ip_address' in ec2_details.keys():
                    instance_details['ip_address'] = ec2_details['public_ip_address']
                if 'state' in ec2_details.keys():
                    instance_details['state'] = ec2_details['state']['name']

                instance_list.append(instance_details)

            logger.disabled = False

    # format list of instances
        instance_rows = []
        instance_headers = [ 'Machine', 'Services', 'Env', 'Region', 'IP Address', 'State' ]
        instance_keys = [ 'machine', 'services', 'environment', 'region', 'ip_address', 'state' ]
        for instance in instance_list:
            instance_row = []
            for key in instance_keys:
                instance_row.append(instance[key])
            instance_rows.append(instance_row)

    # print table
        from tabulate import tabulate
        table_text = tabulate(instance_rows, headers=instance_headers)
        print(table_text)

# list images
    elif resource_type == 'images':
        pass

# list containers
    elif resource_type == 'containers':

        container_headers = [ 'NAMES', 'STATUS', 'IMAGE', 'PORTS']

    return exit_msg
