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
                if tag['Key'] == 'Containers':
                    if tag['Value'].find(container_alias) > -1:
                        valid_instances.append(instance_details)
                        break

# verify only one instance exists
    if not valid_instances:
        raise Exception('No instances found %s. Try: lab list instances aws' % filter_insert)
    elif len(valid_instances) > 1:
        raise Exception('More than one instance was found %s. Try adding optional flags as filters.')

    instance_details = valid_instances[0]
    
    return instance_details