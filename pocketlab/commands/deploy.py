__author__ = 'rcj1492'
__created__ = '2017.06'
__license__ = 'MIT'

_start_details = {
    'title': 'Deploy',
    'description': 'Deploys one or more services as Docker containers on a remote platform.',
    'help': 'deploys services to a remote platform',
    'benefit': 'WIP'
}

from pocketlab.init import fields_model

def deploy(platform_name, service_list, verbose=True):
    
    title = 'deploy'

# validate inputs
    if isinstance(service_list, str):
        if service_list:
            service_list = [service_list]
    input_fields = {
        'service_list': service_list,
        'verbose': verbose,
        'platform_name': platform_name
    }
    for key, value in input_fields.items():
        if value:
            object_title = '%s(%s=%s)' % (title, key, str(value))
            fields_model.validate(value, '.%s' % key, object_title)

# construct list of paths to services
    from pocketlab.methods.service import retrieve_services
    deploy_list, msg_insert = retrieve_services(service_list)
        
# deploy to heroku
    if platform_name == 'heroku':

    # construct heroku list
        heroku_list = []

    # validate heroku and lab files
        from os import path
        from pocketlab.methods.validation import validate_heroku, validate_lab
        from pocketlab import __module__
        from jsonmodel.loader import jsonLoader
        from jsonmodel.validators import jsonModel
        heroku_schema = jsonLoader(__module__, 'models/heroku-config.json')
        heroku_model = jsonModel(heroku_schema)
        lab_schema = jsonLoader(__module__, 'models/lab-config.json')
        lab_model = jsonModel(lab_schema)
        for details in deploy_list:
            heroku_path = path.join(details['path'], 'cred/heroku.yaml')
            service_name = details['name']
            heroku_details = validate_heroku(heroku_model, heroku_path, service_name)
            lab_path = path.join(details['path'], 'lab.yaml')
            lab_details = validate_lab(lab_model, lab_path, service_name)
            details['config'] = heroku_details
            details['config'].update(lab_details)
            heroku_list.append(details)
        
        from pocketlab.methods.heroku import herokuClient
        for service in heroku_list:
            heroku_kwargs = {
                'account_email': service['config']['heroku_account_email'],
                'account_password': service['config']['heroku_account_password'],
                'verbose': verbose
            }
            heroku_client = herokuClient(**heroku_kwargs)
        
        # print heroku_list

# placeholder aws
    elif platform_name == 'ec2':
        
    # what is the state of the system that is trying to be achieved?
        # single instance vs. load balancer/auto-scaling group
        # create/replace instance vs. update existing instance
        # web routing vs closed ip
        # fresh account vs. account configuration exists
        # add/subtract services vs update services
        # ephemeral vs persistent data (service that backs-up data)
    
    # from awsDocker.awsCompose import awsCompose
    # from awsDocker.awsSSH import awsSSH
    # from pocketlab.platforms.docker import dockerClient
        ec2_client = None
        ssh_client = None
        docker_client = None
        tempdata_client = None
    
    # create instance
        from os import path
        ecs_optimized_ami = 'ami-62745007'
        ec2_client.create_instance(ecs_optimized_ami)
        dependency_cmds = [
            'sudo yum update -y',
            'sudo yum install -y nginx',
            'sudo chmod 777 /etc/rc3.d/S99local; echo "service nginx restart" >> /etc/rc3.d/S99local'
        ]
        ssh_client.script(dependency_cmds, verbose=verbose)
    
    # add docker image to instance
        container_alias = 'web'
        image_name = 'webserver'
        temp_name = '%s-ec2.tar' % image_name
        local_path = path.join(tempdata_client.collection_folder, temp_name)
        remote_path = '~/%s' % temp_name
        docker_client.save('web', local_path)
        ssh_client.transfer(local_path, remote_path, verbose=verbose)
        docker_cmds = [
            'sudo docker load -i %s' % temp_name,
            'sudo chmod 777 /etc/rc3.d/S99local; echo "docker restart %s" >> /etc/rc3.d/S99local' % container_alias
        ]
        ssh_client.script(docker_cmds, verbose=verbose)
    
    # start image
        run_command = docker_client._generate_run('lab.yaml')
        run_command = 'docker run --name %s -it -d -e PORT=5000 -p 5000:5000 %s' % (container_alias, image_name)
        docker_cmds = [
            'sudo %s' % run_command
        ]
        ssh_client.script(docker_cmds, verbose=verbose)
    
    # update nginx conf
        from pocketlab.methods.nginx import compile_nginx
        container_list = [{'domain': 'collectiveacuity.com', 'port': 5000}]
        nginx_text = compile_nginx(container_list, 'collectiveacuity')
        nginx_name = 'nginx.conf'
        local_path = path.join(tempdata_client.collection_folder, nginx_name)
        with open(local_path, 'wt') as f:
            f.write(nginx_text)
            f.close()
        remote_path = '/etc/nginx/%s' % nginx_name
        ssh_client.transfer(local_path, remote_path, verbose=verbose)

# placeholder exit
    exit_msg = input_fields
    
    return exit_msg