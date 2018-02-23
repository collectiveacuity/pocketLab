''' a package of helper methods to tackle common aws client interactions '''
__author__ = 'rcj1492'
__created__ = '2017.06'
__licence__ = 'MIT'

def construct_client_ec2(ec2_config, region_name, service_insert):
    
    if region_name:
        ec2_config['region_name'] = region_name
    from labpack.authentication.aws.iam import AWSConnectionError
    from labpack.platforms.aws.ec2 import ec2Client
    try:
        ec2_client = ec2Client(**ec2_config)
    except AWSConnectionError as err:
        error_lines = str(err).splitlines()
        raise Exception('AWS configuration has the following problem:\n%s' % error_lines[-1])
    ec2_client.list_keypairs()
    
    return ec2_client

def retrieve_instance_details(ec2_client, container_alias, environment_type, resource_tag):

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
                if tag['key'] == 'Containers':
                    if tag['value'].find(container_alias) > -1:
                        valid_instances.append(instance_details)
                        break

# verify only one instance exists
    if not valid_instances:
        raise Exception('No instances found %s.\nTry: lab list instances ec2' % filter_insert)
    elif len(valid_instances) > 1:
        raise Exception('More than one instance was found %s.\nTry adding optional flags as filters.')

    instance_details = valid_instances[0]
    
    return instance_details

def compile_instances(region_name='', service_list=None):

    instance_list = []

# check for dependencies
    from pocketlab.methods.dependencies import import_boto3
    import_boto3('ec2 platform')

# TODO support compilation of accounts and regions

# define service fields
    service_name = ''
    service_root = './'
    service_insert = ' in working directory'
    if service_list and isinstance(service_list, list):
        service_name = service_list[0]['name']
        service_root = service_list[0]['path']
        service_insert = service_list[0]['insert']

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
        'verbose': False
    }
    ec2_client = construct_client_ec2(ec2_config, region_name, service_insert)
    ec2_list = ec2_client.list_instances()

# construct instance details
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
    
    return instance_list

def establish_connection(aws_config, service_name, service_insert, service_root, region_name, environment_type, resource_tag, verbose):
    
# retrieve instance details from ec2
    from pocketlab.init import logger
    logger.disabled = True
    if verbose:
        print('Retrieving ec2 instance details ... ', end='', flush=True)
    try:
        ec2_config = {
            'access_id': aws_config['aws_access_key_id'],
            'secret_key': aws_config['aws_secret_access_key'],
            'region_name': aws_config['aws_default_region'],
            'owner_id': aws_config['aws_owner_id'],
            'user_name': aws_config['aws_user_name'],
            'verbose': False
        }
        ec2_client = construct_client_ec2(ec2_config, region_name, service_insert)
        instance_details = retrieve_instance_details(ec2_client, service_name, environment_type, resource_tag)
        if verbose:
            print('done.')
    except Exception:
        if verbose:
            print('ERROR.')
        raise

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
    ssh_config['verbose'] = False
    from labpack.platforms.aws.ssh import sshClient
    if verbose:
        print('Establishing ssh connection ... ', end='', flush=True)
    try:
        ssh_client = sshClient(**ssh_config)
        if verbose:
            print('done.')
    except Exception as err:
        if verbose:
            print('ERROR.')
        error_msg = str(err)
        if str(error_msg).find('private key files are NOT accessible by others'):
            error_msg += '\nTry: "chmod 600 %s.pem" in the .lab folder of service %s.' % (pem_name, service_insert)
            raise Exception(error_msg)
        else:
            raise
    logger.disabled = False
    ssh_client.ec2.iam.verbose = verbose

    return ec2_client, ssh_client, instance_details
