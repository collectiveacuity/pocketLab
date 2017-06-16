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

def connect(platform_name, service_name='', environment_type='prod', resource_tag='',verbose=True):

    title = 'connect'

# validate inputs
    input_fields = {
        'service_name': service_name,
        'verbose': verbose,
        'platform_name': platform_name,
        'environment_type': environment_type,
        'resource_tag': resource_tag
    }
    for key, value in input_fields.items():
        if value:
            object_title = '%s(%s=%s)' % (title, key, str(value))
            fields_model.validate(value, '.%s' % key, object_title)

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
    from pocketlab.methods.validation import validate_lab, validate_config
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

    # retrieve aws config
        aws_schema = jsonLoader(__module__, 'models/aws-config.json')
        aws_model = jsonModel(aws_schema)
        aws_config = validate_config(aws_model, service_root, service_name)

    # verify access to ec2
        ec2_config = {
            'access_id': aws_config['aws_access_key_id'],
            'secret_key': aws_config['aws_secret_access_key'],
            'region_name': aws_config['aws_default_region'],
            'owner_id': aws_config['aws_owner_id'],
            'user_name': aws_config['aws_user_name'],
            'verbose': False
        }
    # TODO add region support
        from labpack.platforms.aws.ec2 import ec2Client
        from pocketlab.init import logger
        logger.disabled = True
        ec2_client = ec2Client(**ec2_config)
        try:
            ec2_client.list_keypairs()
        except:
            raise Exception('Service %s does not have privileges to access EC2.' % service_insert)

    # retrieve instance ip and pem file details from ec2
        tag_values = [ environment_type ]
        resource_insert = ''
        if resource_tag:
            resource_insert = ' with a %s tag value.'
            tag_values.append(resource_tag)
        instance_list = ec2_client.list_instances(tag_values=tag_values)
        error_msg = 'No instances found in AWS region %s in the "%s" environment' % (ec2_config['region_name'], environment_type)
        if not instance_list:
            raise Exception('%s%s.' % (error_msg, resource_insert))
        instance_id = instance_list[0]
        instance_details = ec2_client.read_instance(instance_id)
        pem_name = instance_details['keypair']
        from os import path
        pem_folder = path.join(service_root, '.lab')
        pem_file = path.join(pem_folder, '%s.pem' % pem_name)
        if not path.exists(pem_file):
            raise Exception('Pem file %s.pem missing from .lab folder of service %s.' % (pem_name, service_insert))

    # construct ssh client and open terminal
        ssh_config = {
            'instance_id': instance_id,
            'pem_file': pem_file
        }
        ssh_config.update(ec2_config)
        # ssh_client = sshClient(**client_kwargs)
        # ssh_client.terminal()

        print(ssh_config)
        logger.disabled = False

# handle heroku error
    elif platform_name == 'heroku':
        raise Exception('It is not possible to connect to instances on heroku.')





    return input_fields