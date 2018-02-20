__author__ = 'rcj1492'
__created__ = '2017.06'
__license__ = 'MIT'


'''
deploy to heroku
TODO: deploy to EC2
TODO: deploy to other platforms (azure, gcp, bluemix, rackspace)
'''

_deploy_details = {
    'title': 'Deploy',
    'description': 'Deploys a service to a remote platform. Deploy is currently only available for the heroku platform. Deploy can also deploy static html sites and apps using their dependencies if the root folder is added to one of the runtime type flags (ex. lab deploy heroku --html site/)',
    'help': 'deploys service to a remote platform',
    'benefit': 'Makes a service available online.'
}

from pocketlab.init import fields_model

def deploy(platform_name, service_option, environment_type='', resource_tag='', region_name='', verbose=True, overwrite=False, mount_volumes=False, virtualbox='default', html_folder='', php_folder='', python_folder='', java_folder='', ruby_folder='', node_folder=''):
    
    '''
        a method to deploy the docker image of a service to a remote host
        
    :param platform_name: string with name of remote platform to host service
    :param service_option: [optional] string with name of service in lab registry
    :param verbose: [optional] boolean to toggle process messages
    :param overwrite: [optional] boolean to overwrite existing container
    :param mount_volumes: [optional] boolean to mount volumes in docker-compose.yaml
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
    if isinstance(service_option, str):
        if service_option:
            service_option = [service_option]
    input_fields = {
        'service_option': service_option,
        'platform_name': platform_name,
        'environment_type': environment_type,
        'resource_tag': resource_tag,
        'region_name': region_name,
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
    details = {
        'name': service_name,
        'insert': service_insert,
        'path': service_root
    }

# construct service list
    service_list = []
    exit_msg = ''
    
# deploy to heroku
    if platform_name == 'heroku':

    # import dependencies
        from os import path
        from pocketlab.methods.validation import validate_platform
        from pocketlab import __module__
        from jsonmodel.loader import jsonLoader
        from jsonmodel.validators import jsonModel
    
    # validate heroku file
        heroku_schema = jsonLoader(__module__, 'models/heroku-config.json')
        heroku_model = jsonModel(heroku_schema)
        heroku_details = validate_platform(heroku_model, service_root, service_name)
        details['config'] = heroku_details
        service_list.append(details)

    # define site folder path function
        def _site_path(site_folder, service_root, service_insert, runtime_type):
            from os import path
            if path.isabs(site_folder):
                raise Exception('--%s %s must be a path relative to root of service %s' % (runtime_type, site_folder, service_insert))
            site_path = path.join(service_root, site_folder)
            return site_path

    # process deployment sequence
        from labpack.platforms.heroku import herokuClient
        for service in service_list:

        # construct message inserts
            service_insert = service['insert']
            msg_insert = 'working directory'
            if service['name']:
                msg_insert = 'root directory for "%s"' % service['name']

        # initialize heroku client
            heroku_kwargs = {
                'account_email': service['config']['heroku_account_email'],
                'auth_token': service['config']['heroku_auth_token'],
                'verbose': verbose
            }
            heroku_client = herokuClient(**heroku_kwargs)
            heroku_client.access(service['config']['heroku_app_subdomain'])
            heroku_insert = "service %s deployed to heroku.\nIf you haven't already, you must allocate resources to this heroku service.\nTry: heroku ps:scale web=1 --app %s" % (service_insert, service['config']['heroku_app_subdomain'])
        
        # deploy app from requirements
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

        # deploy app in docker container
            else:

            # establish path of files
                from os import path
                from time import time
                dockerfile_path = path.join(service['path'], 'Dockerfile')
                platform_path = path.join(service['path'], 'DockerfileHeroku')
                compose_path = path.join(service['path'], 'docker-compose.yaml')
                temp_path = path.join(service['path'], 'DockerfileTemp%s' % int(time()))
    
            # construct system envvar
                system_envvar = {
                    'system_environment': 'prod',
                    'system_platform': 'heroku'
                }

            # compile dockerfile text
                from pocketlab.methods.config import compile_dockerfile
                dockerfile_text = compile_dockerfile(
                    dockerfile_path=dockerfile_path,
                    platform_path=platform_path,
                    compose_path=compose_path,
                    service_details=service,
                    msg_insert=msg_insert,
                    platform_name='heroku',
                    system_envvar=system_envvar,
                    verbose=verbose
                )

            # create temporary Dockerfile
                from os import remove
                from shutil import copyfile
                if path.exists(dockerfile_path):
                    copyfile(dockerfile_path, temp_path)
                with open(dockerfile_path, 'wt') as f:
                    f.write(dockerfile_text)
                    f.close()

            # construct deploy kwargs
                docker_kwargs = {
                    'dockerfile_path': dockerfile_path,
                    'virtualbox_name': virtualbox
                }

            # start build and deployment
                try:
                    heroku_client.deploy_docker(**docker_kwargs)
                except:

                # ROLLBACK Dockerfile
                    if path.exists(temp_path):
                        copyfile(temp_path, dockerfile_path)
                        remove(temp_path)

                    raise

            # restore Dockerfile
                if path.exists(temp_path):
                    copyfile(temp_path, dockerfile_path)
                    remove(temp_path)

                exit_msg = 'Docker image of %s' % heroku_insert

            if len(service_list) > 1:
                print(exit_msg)

# placeholder aws
    elif platform_name == 'ec2':

    # what is the state of the system that is trying to be achieved?
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

    # retrieve aws config
        from pocketlab import __module__
        from jsonmodel.loader import jsonLoader
        from jsonmodel.validators import jsonModel
        from pocketlab.methods.validation import validate_platform
        aws_schema = jsonLoader(__module__, 'models/aws-config.json')
        aws_model = jsonModel(aws_schema)
        aws_config = validate_platform(aws_model, service_root, service_name)
        details['config'] = aws_config
        service_list.append(details)

    # iterate over each service
        for service in service_list:

        # construct message inserts
            service_insert = service['insert']
            msg_insert = 'working directory'
            if service['name']:
                msg_insert = 'root directory for "%s"' % service['name']
            ec2_insert = 'service %s deployed to ec2.' % service_insert

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

        # construct ssh client
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

        # retrieve compose configurations

        # verify port available

        # verify overwrite of existing files

        # construct system envvar
            system_envvar = {
                'system_environment': environment_type,
                'system_platform': 'ec2'
            }
        
        # establish path of files
            from os import path
            from time import time
            dockerfile_path = path.join(service['path'], 'Dockerfile')
            platform_path = path.join(service['path'], 'DockerfileEC2')
            compose_path = path.join(service['path'], 'docker-compose.yaml')
            temp_path = path.join(service['path'], 'DockerfileTemp%s' % int(time()))

        # compile dockerfile text
            from pocketlab.methods.config import compile_dockerfile
            dockerfile_text = compile_dockerfile(
                dockerfile_path=dockerfile_path,
                platform_path=platform_path,
                compose_path=compose_path,
                service_details=service,
                msg_insert=msg_insert,
                platform_name='ec2',
                system_envvar=system_envvar,
                verbose=verbose
            )
            from pprint import pprint
            pprint(dockerfile_text)

        # compose exit message
            exit_msg = 'Docker image of %s' % ec2_insert

            if len(service_list) > 1:
                print(exit_msg)

    # create instance
        ec2_client = None
        ssh_client = None
        docker_client = None
        tempdata_client = None
        if ec2_client:
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
    
    # TODO consider rollback options   
    # TODO consider build versioning/storage

# report composite outcome
    if len(service_list) > 1:
        service_names = []
        for service in service_list:
            service_names.append('"%s"' % service['name'])
        from labpack.parsing.grammar import join_words
        exit_insert = join_words(service_names)
        exit_msg = 'Finished deploying %s to %s.' % (exit_insert, platform_name)

    return exit_msg