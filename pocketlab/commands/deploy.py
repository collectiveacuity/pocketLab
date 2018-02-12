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

def deploy(platform_name, service_option, verbose=True, virtualbox='default', html_folder='', php_folder='', python_folder='', java_folder='', ruby_folder='', node_folder=''):
    
    '''
        a method to deploy the docker image of a service to a remote host
        
    :param platform_name: string with name of remote platform to host service
    :param service_option: [optional] string with name of service in lab registry
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
    if isinstance(service_option, str):
        if service_option:
            service_option = [service_option]
    input_fields = {
        'service_option': service_option,
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

# deploy to heroku
    if platform_name == 'heroku':

    # import dependencies
        from os import path
        from pocketlab.methods.validation import validate_platform, validate_compose
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
            msg_insert = 'working directory'
            service_insert = 'in working directory'
            if service['name']:
                service_insert = '"%s"' % service['name']
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
            
            # import dependencies
                compose_schema = jsonLoader(__module__, 'models/compose-config.json')
                service_schema = jsonLoader(__module__, 'models/service-config.json')
                compose_model = jsonModel(compose_schema)
                service_model = jsonModel(service_schema)
            
            # establish path of files
                from time import time
                dockerfile_text = ''
                dockerfile_path = path.join(service['path'], 'Dockerfile')
                dockerfile_heroku_path = path.join(service['path'], 'DockerfileHeroku')
                compose_path = path.join(service['path'], 'docker-compose.yaml')
                dockerfile_temp_path = path.join(service['path'], 'DockerfileTemp%s' % int(time()))

                if verbose:
                    print('Checking Dockerfile settings in %s ... ' % msg_insert, end='', flush=True)

            # retrieve dockerfile text from DockerfileHeroku
                if path.exists(dockerfile_heroku_path):
                    try:
                        dockerfile_text = open(dockerfile_heroku_path, 'rt').read()
                        if verbose:
                            print('done.')
                    except:
                        pass

            # fallback to docker compose file
                if not dockerfile_text:
                    if path.exists(compose_path):

                # validate docker compose file
                        compose_details = validate_compose(compose_model, service_model, compose_path, service['name'])

                        if service['name']:
                            service['config'].update(compose_details['services'][service['name']])
                        else:
                            for key, value in compose_details['services'].items():
                                service['config'].update(value)
                                service['name'] = key
                                break

                # retrieve dockerfile in docker compose
                        if 'build' in service['config'].keys():
                            dockerfile_name = service['config']['build'].get('dockerfile', 'Dockerfile')
                            relative_path = path.join(service['config']['build']['context'], dockerfile_name)
                            if not path.isabs(relative_path):
                                relative_path = path.join(service['path'], relative_path)
                            try:
                                dockerfile_text = open(relative_path, 'rt').read()
                                if verbose:
                                    print('done.')
                            except:
                                pass

            # fallback to Dockerfile in root
                if not dockerfile_text:
                    if path.exists(dockerfile_path):
                        try:
                            dockerfile_text = open(dockerfile_path, 'rt').read()
                            if verbose:
                                print('done.')
                        except:
                            pass

            # catch missing Dockerfile error
                if not dockerfile_text:
                    raise ValueError('Deploying %s to heroku using docker requires Dockerfile instructions. Try creating a Dockerfile.' % service_insert)

            # import dependencies
                import re
                import os
                from shutil import copyfile
                system_space_pattern = re.compile('\nENV SYSTEM_ENVIRONMENT\=.*?\s')
                system_newline_pattern = re.compile('\nENV SYSTEM_ENVIRONMENT\=.*?\n')
                system_hash_pattern = re.compile('\nENV SYSTEM_ENVIRONMENT\=.*?#')
                command_pattern = re.compile('\nCMD\s')
                entry_pattern = re.compile('\nENTRYPOINT\s')

            # insert variables into Dockerfile
                dockerfile_text = dockerfile_text.strip() + '\n'
                if system_newline_pattern.findall(dockerfile_text):
                    dockerfile_text = system_newline_pattern.sub('\nENV SYSTEM_ENVIRONMENT=heroku\n', dockerfile_text)
                elif system_space_pattern.findall(dockerfile_text):
                    dockerfile_text = system_space_pattern.sub('\nENV SYSTEM_ENVIRONMENT=heroku ', dockerfile_text)
                elif system_hash_pattern.findall(dockerfile_text):
                    dockerfile_text = system_hash_pattern.sub('\nENV SYSTEM_ENVIRONMENT=heroku#', dockerfile_text)
                else:
                    dockerfile_text += '\nENV SYSTEM_ENVIRONMENT=heroku'
                if 'environment' in service['config'].keys():
                    for key, value in service['config']['environment'].items():
                        if key != 'PORT':
                            dockerfile_text += '\nENV %s=%s' % (key.upper(), str(value))

            # insert copy volumes into Dockerfile
                if 'volumes' in service['config'].keys():
                    for volume in service['config']['volumes']:
                        if volume['type'] == 'bind':
                            volume_line = '\nADD %s %s' % (volume['source'], volume['target'])
                            if not re.findall(volume_line, dockerfile_text):
                                dockerfile_text += volume_line

            # add command or entrypoint if none existent
                if command_pattern.findall(dockerfile_text) or entry_pattern.findall(dockerfile_text):
                    pass
                else:
                    if 'entrypoint' in service['config'].keys():
                        dockerfile_text += '\nENTRYPOINT %s' % str(service['config']['entrypoint'])
                    elif 'command' in service['config'].keys():
                        dockerfile_text += '\nCMD %s' % str(service['config']['command'])
                    else:
                        raise ValueError('Deploying %s to heroku with docker requires a start command or entrypoint.' % service_insert)

            # create temporary Dockerfile
                if path.exists(dockerfile_path):
                    copyfile(dockerfile_path, dockerfile_temp_path)
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
                    if path.exists(dockerfile_temp_path):
                        copyfile(dockerfile_temp_path, dockerfile_path)
                        os.remove(dockerfile_temp_path)

                    raise

            # restore Dockerfile
                if path.exists(dockerfile_temp_path):
                    copyfile(dockerfile_temp_path, dockerfile_path)
                    os.remove(dockerfile_temp_path)

                exit_msg = 'Docker image of %s' % heroku_insert

            if len(service_list) > 1:
                print(exit_msg)

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

    # TODO replace lab.yaml with docker-compose.yml
        
        from pocketlab.methods.validation import validate_lab
        lab_schema = jsonLoader(__module__, 'models/lab-config.json')
        lab_model = jsonModel(lab_schema)
        lab_path = path.join(service_name, 'lab.yaml')
        lab_details = validate_lab(lab_model, lab_path, service_name)
        details['config'].update(lab_details)
        
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

# TODO consider rollback options   
# TODO consider build versioning/storage

# report composite outcome
    if len(service_list) > 1:
        exit_msg = 'Finished deploying %s to %s.' % (msg_insert, platform_name)
        
    return exit_msg