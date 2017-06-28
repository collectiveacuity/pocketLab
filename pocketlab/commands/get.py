__author__ = 'rcj1492'
__created__ = '2017.06'
__licence__ = 'MIT'

'''
get file from aws instance
TODO: get from other platforms (bluemix, azure, gcp)
'''

_get_details = {
    'title': 'get',
    'description': 'Copies a file or folder on remote host to working directory on localhost. Get is currently only available for the Amazon ec2 platform.\n\nPLEASE NOTE: get uses the docker container alias value specified in the lab.yaml configuration file to determine which instance to connect to. A tag must be added manually to the instance with key "Containers" and value "<container_alias>".',
    'help': 'copy a file from remote host through scp',
    'benefit': 'Copies remote files to your local machine.'
}

from pocketlab.init import fields_model


def get(file_path, platform_name, service_option, environment_type='', resource_tag='', region_name='', verbose=True, overwrite=False):
    
    title = 'connect'

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

# retrieve lab config
    from os import path
    from pocketlab.methods.validation import validate_lab, validate_platform
    from pocketlab import __module__
    from jsonmodel.loader import jsonLoader
    from jsonmodel.validators import jsonModel
    lab_schema = jsonLoader(__module__, 'models/lab-config.json')
    lab_model = jsonModel(lab_schema)
    lab_path = path.join(service_root, 'lab.yaml')
    lab_config = validate_lab(lab_model, lab_path, service_name)
    if not lab_config['docker_container_alias']:
        raise Exception('lab.yaml for service %s must container a value for docker_container_alias' % service_insert)
    container_alias = lab_config['docker_container_alias']

# handle ec2 platform
    if platform_name == 'ec2':

    # check for dependencies
        from pocketlab.methods.dependencies import import_boto3
        import_boto3('ec2 platform')

    # retrieve aws config
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
            'verbose': verbose
        }
        from pocketlab.methods.aws import construct_client_ec2, retrieve_instance_details
        ec2_client = construct_client_ec2(ec2_config, region_name, service_insert)
        instance_details = retrieve_instance_details(ec2_client, container_alias, environment_type, resource_tag)

    # verify pem file exists
        pem_name = instance_details['key_name']
        pem_folder = path.join(service_root, '.lab')
        pem_file = path.join(pem_folder, '%s.pem' % pem_name)
        if not path.exists(pem_file):
            raise Exception('SSH requires %s.pem file in the .lab folder of service %s.' % (pem_name, service_insert))

    # construct ssh client and run get
        ssh_config = {
            'instance_id': instance_details['instance_id'],
            'pem_file': pem_file
        }
        ssh_config.update(ec2_config)
        ssh_config['verbose'] = verbose
        from labpack.platforms.aws.ssh import sshClient
        ssh_client = sshClient(**ssh_config)
        logger.disabled = False
        ssh_client.get(file_path, synopsis=False, overwrite=overwrite)

# handle heroku error
    elif platform_name == 'heroku':
        raise Exception('It is not possible to connect to instances on heroku.')

    exit_msg = 'Transfer of %s from %s instance "%s" complete' % (file_path, platform_name, container_alias)

    return exit_msg