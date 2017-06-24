__author__ = 'rcj1492'
__created__ = '2017.06'
__licence__ = 'MIT'

'''
transfer to aws instance
TODO: transfer to other platforms (bluemix, azure, gcp)
'''

_transfer_details = {
    'title': 'transfer',
    'description': 'Copies a local file or folder to user home on remote host. Connect is currently only available to the Amazon ec2 platform.\n\nPLEASE NOTE: connect uses the docker container alias value specified in the lab.yaml configuration file to determine which instance to connect to. A tag must be added manually to the instance with key "Containers" and value "<container_alias>".',
    'help': 'transfer a file to remote host through scp',
    'benefit': 'Copy files from your local machine.'
}

from pocketlab.init import fields_model

def transfer(platform_name, service_option, environment_type='', resource_tag='', region_name='', verbose=True):

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
        from platform import uname
        local_os = uname()
        if local_os.system in ('Windows'):
            raise Exception('%s command is not available for Windows. Try using instead: putty.exe' % title)

    # retrieve aws config
        aws_schema = jsonLoader(__module__, 'models/aws-config.json')
        aws_model = jsonModel(aws_schema)
        aws_config = validate_platform(aws_model, service_root, service_name)

    # verify access to ec2
        ec2_config = {
            'access_id': aws_config['aws_access_key_id'],
            'secret_key': aws_config['aws_secret_access_key'],
            'region_name': aws_config['aws_default_region'],
            'owner_id': aws_config['aws_owner_id'],
            'user_name': aws_config['aws_user_name'],
            'verbose': False
        }
        if region_name:
            ec2_config['region_name'] = region_name
        from labpack.authentication.aws.iam import AWSConnectionError
        from labpack.platforms.aws.ec2 import ec2Client
        from pocketlab.init import logger
        logger.disabled = True
        try:
            ec2_client = ec2Client(**ec2_config)
        except AWSConnectionError as err:
            error_lines = str(err).splitlines()
            raise Exception('AWS configuration has the following problem:\n%s' % error_lines[-1])
        try:
            ec2_client.list_keypairs()
        except:
            raise Exception('Service %s does not have privileges to access EC2.' % service_insert)

    # retrieve instance list using filter criteria
        valid_instances = []
        filter_insert = 'for container "%s" in AWS region %s' % (container_alias, ec2_client.iam.region_name)
        tag_values = []
        if environment_type:
            filter_insert += ' in the "%s" env' % environment_type
            tag_values.append(environment_type)
        if resource_tag:
            filter_insert += ' with a "%s" tag' % resource_tag
            tag_values.append(resource_tag)
        if tag_values:
            instance_list = ec2_client.list_instances(tag_values=tag_values)
        else:
            instance_list = ec2_client.list_instances()
        for instance_id in instance_list:
            instance_details = ec2_client.read_instance(instance_id)
            if instance_details['tags']:
                for tag in instance_details['tags']:
                    if tag['Key'] == 'Containers':
                        if tag['Value'].find(container_alias) > -1:
                            valid_instances.append(instance_details)
                            break

    # verify only one instance exists
        if not valid_instances:
            raise Exception('No instances found %s. Try: lab list instances aws' % filter_insert)
        elif len(valid_instances) > 1:
            raise Exception('More than one instance was found %s. Try adding optional flags as filters.')

    # verify pem file exists
        from os import path
        instance_details = valid_instances[0]
        pem_name = instance_details['keypair']
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
        ssh_client = sshClient(**ssh_config)
        logger.disabled = False
        ssh_client.terminal()

# handle heroku error
    elif platform_name == 'heroku':
        raise Exception('It is not possible to connect to instances on heroku.')

    exit_msg = 'Code is growing like gangbusters.'

    return exit_msg