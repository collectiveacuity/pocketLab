__author__ = 'rcj1492'
__created__ = '2017.06'
__licence__ = 'MIT'

'''
put file to ec2 instance
TODO: put to other platforms (bluemix, azure, gcp)
'''

_put_details = {
    'title': 'put',
    'description': 'Copies a local file or folder to user home on remote host. Put is currently only available for the Amazon ec2 platform.\n\nPLEASE NOTE: put uses the docker container alias value specified in the docker-compose.yaml configuration file to determine which instance to connect to. A tag must be added manually to the instance with key "Containers" and value "<container_alias>".',
    'help': 'copy a file to remote host through scp',
    'benefit': 'Copy files from your local machine.'
}

from pocketlab.init import fields_model

def put(file_path, platform_name, service_option, environment_type='', resource_tag='', region_name='', verbose=True, overwrite=False):

    title = 'put'

# validate inputs
    if isinstance(service_option, str):
        if service_option:
            service_option = [service_option]
    input_fields = {
        'file_path': file_path,
        'service_option': service_option,
        'verbose': verbose,
        'platform_name': platform_name,
        'environment_type': environment_type,
        'resource_tag': resource_tag
    }
    for key, value in input_fields.items():
        if value:
            object_title = '%s(%s=%s)' % (title, key, str(value))
            fields_model.validate(value, '.%s' % key, object_title)

# verify local path exists
    from os import path
    if not path.exists(file_path):
        raise ValueError('%s is not a valid path on localhost.' % file_path)
    
# determine service name
    service_name = ''
    if service_option:
        service_name = service_option[0]

# construct path to service root
    from pocketlab.methods.service import retrieve_service_root
    if service_name:
        service_insert = '"%s"' % service_name
        service_root = retrieve_service_root(service_name)
    else:
        service_insert = 'in working directory'
        service_root = './'

# retrieve service configurations
    from pocketlab.methods.service import retrieve_service_config
    service_title = '%s %s' % (title, platform_name)
    service_config, service_name = retrieve_service_config(service_root, service_name, service_title)

# handle ec2 platform
    if platform_name == 'ec2':

    # check for dependencies
        from pocketlab.methods.dependencies import import_boto3
        import_boto3('ec2 platform')

    # retrieve aws config
        from pocketlab import __module__
        from jsonmodel.loader import jsonLoader
        from jsonmodel.validators import jsonModel
        from pocketlab.methods.validation import validate_platform
        aws_schema = jsonLoader(__module__, 'models/aws-config.json')
        aws_model = jsonModel(aws_schema)
        aws_config = validate_platform(aws_model, service_root, service_name, '.lab')

    # retrieve instance details from ec2
        from pocketlab.methods.aws import establish_connection
        ec2_client, ssh_client, instance_details = establish_connection(
            aws_cred=aws_config,
            service_name=service_name, 
            service_insert=service_insert, 
            service_root=service_root, 
            region_name=region_name, 
            environment_type=environment_type, 
            resource_tag=resource_tag, 
            verbose=verbose
        )

    # put file to remote through scp
        ssh_client.put(file_path, synopsis=False, overwrite=overwrite)

# handle heroku error
    elif platform_name == 'heroku':
        raise Exception('It is not possible to connect to instances on heroku.')

    exit_msg = 'Transfer of %s to %s instance with service %s complete' % (file_path, platform_name, service_insert)

    return exit_msg