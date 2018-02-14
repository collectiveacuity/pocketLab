__author__ = 'rcj1492'
__created__ = '2017.06'
__license__ = 'MIT'

'''
connect to aws instance
TODO: connect to other platforms (bluemix, azure, gcp)
'''

_connect_details = {
    'title': 'connect',
    'description': 'Opens up a direct ssh connection to remote host. Connect is currently only available to the Amazon ec2 platform and only on systems running ssh natively. To connect to a remote host on Windows, try using Putty instead.\n\nPLEASE NOTE: connect uses the docker container alias value specified in the docker-compose.yaml configuration file to determine which instance to connect to. A tag must be added manually to the instance with key "Containers" and value "<container_alias>".',
    'help': 'connects to remote host through ssh',
    'benefit': 'Edit settings on remote host manually.'
}

from pocketlab.init import fields_model

def connect(platform_name, service_option, environment_type='', resource_tag='', region_name='', verbose=True):

    title = 'connect'

# validate inputs
    if isinstance(service_option, str):
        if service_option:
            service_option = [service_option]
    input_fields = {
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

# retrieve service configurations
    from pocketlab.methods.service import retrieve_service_config
    service_title = '%s %s' % (title, platform_name)
    service_config, service_name = retrieve_service_config(service_root, service_name, service_title)

# handle ec2 platform
    if platform_name == 'ec2':

    # check for dependencies
        from pocketlab.methods.dependencies import import_boto3
        import_boto3('ec2 platform')
        from platform import uname
        local_os = uname()
        if local_os.system in ('Windows'):
            raise Exception('%s command is not available for Windows. Try using instead: putty.exe' % title)

    # retrieve aws config
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
            'verbose': verbose
        }
        from pocketlab.methods.aws import construct_client_ec2, retrieve_instance_details
        ec2_client = construct_client_ec2(ec2_config, region_name, service_insert)
        instance_details = retrieve_instance_details(ec2_client, service_name, environment_type, resource_tag)

    # verify pem file exists
        from os import path
        pem_name = instance_details['key_name']
        pem_folder = path.join(service_root, '.lab')
        pem_file = path.join(pem_folder, '%s.pem' % pem_name)
        if not path.exists(pem_file):
            raise Exception('SSH requires %s.pem file in the .lab folder of service %s.' % (pem_name, service_insert))

    # construct ssh client and open terminal
        ssh_config = {
            'instance_id': instance_details['instance_id'],
            'pem_file': pem_file
        }
        ssh_config.update(ec2_config)
        ssh_config['verbose'] = verbose
        from labpack.platforms.aws.ssh import sshClient
        try:
            ssh_client = sshClient(**ssh_config)
        except Exception as err:
            error_msg = str(err)
            if str(error_msg).find('private key files are NOT accessible by others'):
                error_msg += '\nTry: "chmod 600 %s.pem" in the .lab folder of service %s.' % (pem_name, service_insert)
                raise Exception(error_msg)
            else:
                raise
        logger.disabled = False
        ssh_client.terminal()

# handle heroku error
    elif platform_name == 'heroku':
        raise Exception('It is not possible to connect to instances on heroku.')

    exit_msg = 'Code is growing like gangbusters.'

    return exit_msg