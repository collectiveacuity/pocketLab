__author__ = 'rcj1492'
__created__ = '2018.02'
__license__ = 'MIT'

_init_details = {
    'title': 'Launch',
    'description': 'Launches an instance or an auto-scaling group on a remote platform. Launch is currently only available for the ec2 platform. To create an configuration file to launch an ec2 instance, run ```lab init --ec2``` and adjust the settings appropriately.',
    'help': 'starts instances on remote platform',
    'benefit': 'Launch creates one or more remote instances to host services.'
}

from pocketlab.init import fields_model

def launch(platform_name, service_option, region_name='', verbose=True, overwrite=False):

    title = 'launch'

# ingest service option
    if isinstance(service_option, str):
        if service_option:
            service_option = [service_option]

# validate inputs
    input_fields = {
        'platform_name': platform_name,
        'service_option': service_option,
        'region_name': region_name
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
    
# catch heroku error
    exit_msg = ''
    if platform_name == 'heroku':
        raise ValueError('It is not possible to launch an instance on heroku.\nTry: lab deploy heroku')

# process ec2 instance
    elif platform_name == 'ec2':
    
    # # what is the state of the system that is trying to be achieved?
        # single instance vs. load balancer/auto-scaling group
        # create/replace instance vs. update existing instance
        # web routing vs closed ip
        # fresh account vs. account configuration exists
        # add/subtract services vs update services
        # ephemeral vs persistent data (service that backs-up data)
        # single container vs multiple containers

    # check for library dependencies
        from pocketlab.methods.dependencies import import_boto3
        import_boto3('ec2 platform')

    # retrieve aws cred and ec2 config
        from pocketlab import __module__
        from jsonmodel.loader import jsonLoader
        from jsonmodel.validators import jsonModel
        from pocketlab.methods.validation import validate_platform
        aws_schema = jsonLoader(__module__, 'models/aws-config.json')
        aws_model = jsonModel(aws_schema)
        aws_cred = validate_platform(aws_model, service_root, service_name, '.lab')
        ec2_schema = jsonLoader(__module__, 'models/ec2-config.json')
        ec2_model = jsonModel(ec2_schema)
        ec2_config = validate_platform(ec2_model, service_root, service_name)

    # construct variables
        msg_insert = 'working directory'
        if service_name:
            msg_insert = 'root directory for "%s"' % service_name
        ec2_insert = 'service %s deployed to ec2.' % service_insert

    # construct ec2 client
        ec2_cred = {
            'access_id': aws_cred['aws_access_key_id'],
            'secret_key': aws_cred['aws_secret_access_key'],
            'region_name': aws_cred['aws_default_region'],
            'owner_id': aws_cred['aws_owner_id'],
            'user_name': aws_cred['aws_user_name'],
            'verbose': verbose
        }
        from pocketlab.methods.aws import construct_client_ec2
        ec2_client = construct_client_ec2(ec2_cred, region_name)

        print(ec2_config)
    
        # ecs_optimized_ami = 'ami-62745007'
        # ec2_client.create_instance(ecs_optimized_ami)
        # dependency_cmds = [
        #     'sudo yum update -y',
        #     'sudo yum install -y nginx',
        #     'sudo chmod 777 /etc/rc3.d/S99local; echo "service nginx restart" >> /etc/rc3.d/S99local'
        # ]
        # ssh_client.script(dependency_cmds, verbose=verbose)
    
    return exit_msg