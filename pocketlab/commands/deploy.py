__author__ = 'rcj1492'
__created__ = '2017.06'
__license__ = 'MIT'


# TODO: handle heroku error:
# error parsing HTTP 400 response body: unexpected end of JSON input: ""
# failed to do heroku container:login (Windows requires login in docker shell)

# TODO: error on heroku caused from not committing dynos (ps:scale web=1 --app <subdomain>)

_deploy_details = {
    'title': 'Deploy',
    'description': 'Deploys one or more services as Docker containers to a remote platform. Deploy is currently only available for the heroku platform. Deploy can also deploy static html sites and apps using their dependencies if the root folder is added to one of the runtime type flags (ex. lab deploy heroku --html site/)',
    'help': 'deploys services to a remote platform',
    'benefit': 'Makes services available online.'
}

from pocketlab.init import fields_model

def deploy(platform_name, service_list, verbose=True, virtualbox='default', html_folder='', php_folder='', python_folder='', java_folder='', ruby_folder='', node_folder=''):
    
    '''
        a method to deploy the docker image of a service to a remote host
        
    :param platform_name: string with name of remote platform to host service
    :param service_list: list of strings with name of services to deploy
    :param verbose: [optional] boolean to toggle process messages
    :param virtualbox: [optional] string with name of virtualbox image (win7/8)
    :param html_folder: [optional] string with path to static html site folder root
    :param php_folder: [optional] string with path to php app folder root
    :param python_folder: [optional] string with path to python app folder root
    :param java_folder: [optional] string with path to java app folder root
    :param ruby_folder: [optional] string with path to ruby app folder root
    :param node_folder: [optional] string with path to node app folder root
    :return: string with exit message
    '''
    
    title = 'deploy'

# validate inputs
    if isinstance(service_list, str):
        if service_list:
            service_list = [service_list]
    input_fields = {
        'service_list': service_list,
        'verbose': verbose,
        'platform_name': platform_name,
        'virtualbox': virtualbox,
        'html_folder': html_folder,
        'php_folder': php_folder,
        'python_folder': python_folder,
        'java_folder': java_folder,
        'ruby_folder': ruby_folder,
        'node_folder': node_folder
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
        from pocketlab.methods.validation import validate_platform, validate_lab
        from pocketlab import __module__
        from jsonmodel.loader import jsonLoader
        from jsonmodel.validators import jsonModel
        heroku_schema = jsonLoader(__module__, 'models/heroku-config.json')
        heroku_model = jsonModel(heroku_schema)
        lab_schema = jsonLoader(__module__, 'models/lab-config.json')
        lab_model = jsonModel(lab_schema)
        for details in deploy_list:
            service_name = details['name']
            heroku_details = validate_platform(heroku_model, details['path'], service_name)
            lab_path = path.join(details['path'], 'lab.yaml')
            lab_details = validate_lab(lab_model, lab_path, service_name)
            details['config'] = heroku_details
            details['config'].update(lab_details)
            heroku_list.append(details)

    # define site folder path function
        def _site_path(site_folder, service_root, service_insert, runtime_type):
            from os import path
            if path.isabs(site_folder):
                raise Exception('--%s %s must be a path relative to root of service %s' % (runtime_type, site_folder, service_insert))
            site_path = path.join(service_root, site_folder)
            return site_path
            
    # process deployment sequence
        from labpack.platforms.heroku import herokuClient
        for service in heroku_list:
            service_insert = 'in working directory'
            if service['name']:
                service_insert = '"%s"' % service['name']
            heroku_kwargs = {
                'account_email': service['config']['heroku_account_email'],
                'auth_token': service['config']['heroku_auth_token'],
                'verbose': verbose
            }
            heroku_client = herokuClient(**heroku_kwargs)
            heroku_client.access(service['config']['heroku_app_subdomain'])
            heroku_insert = "service %s deployed to heroku.\nIf you haven't already, you must allocate resources to this heroku service.\nTry: heroku ps:scale web=1 --app %s" % (service_insert, service['config']['heroku_app_subdomain'])
            
            if html_folder:
                html_folder = _site_path(html_folder, service['path'], service_insert, 'html')
                heroku_client.deploy_app(html_folder)
                exit_msg = 'Static site of %s' % heroku_insert
            elif php_folder:
                php_folder = _site_path(php_folder, service['path'], service_insert, 'php')
                heroku_client.deploy_app(php_folder, 'php')
                exit_msg = 'Php app of %s' % heroku_insert
            elif python_folder:
                python_folder = _site_path(python_folder, service['path'], service_insert, 'python')
                heroku_client.deploy_app(python_folder, 'python')
                exit_msg = 'Python app of %s' % heroku_insert
            elif java_folder:
                java_folder = _site_path(java_folder, service['path'], service_insert, 'java')
                heroku_client.deploy_app(java_folder, 'java')
                exit_msg = 'Java app of %s' % heroku_insert
            elif ruby_folder:
                ruby_folder = _site_path(ruby_folder, service['path'], service_insert, 'ruby')
                heroku_client.deploy_app(ruby_folder, 'ruby')
                exit_msg = 'Ruby app of %s' % heroku_insert
            elif node_folder:
                node_folder = _site_path(node_folder, service['path'], service_insert, 'node')
                heroku_client.deploy_app(node_folder, 'node')
                exit_msg = 'Node app of %s' % heroku_insert
            else:
                docker_kwargs = {
                    'dockerfile_path': path.join(service['path'], 'Dockerfile'),
                    'virtualbox_name': virtualbox
                }
                heroku_client.deploy_docker(**docker_kwargs)
                exit_msg = 'Docker image of %s' % heroku_insert
            if len(heroku_list) > 1:
                print(exit_msg)
    
    # TODO consider rollback options   
    # TODO consider build versioning/storage
            
        
# placeholder aws
    elif platform_name == 'ec2':
        
        raise Exception('ec2 is coming. Only heroku deployment is currently available.')
        
    # what is the state of the system that is trying to be achieved?
        # single instance vs. load balancer/auto-scaling group
        # create/replace instance vs. update existing instance
        # web routing vs closed ip
        # fresh account vs. account configuration exists
        # add/subtract services vs update services
        # ephemeral vs persistent data (service that backs-up data)
        # single container vs multiple containers
    
    # from awsDocker.awsCompose import awsCompose
    # from awsDocker.awsSSH import awsSSH
    # from pocketlab.platforms.docker import dockerClient
        from labpack.platforms.aws.ec2 import ec2Client
        from labpack.platforms.aws.ssh import sshClient
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

    if len(service_list) > 1:
        exit_msg = 'Finished deploying %s to %s.' % (msg_insert, platform_name)
        
    return exit_msg