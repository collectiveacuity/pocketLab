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
    'description': 'Deploys a service to a remote platform. Deploy is currently only available for the heroku and ec2 platforms. Deploy can also deploy static html sites and apps using their dependencies if the root folder is added to one of the runtime type flags (ex. lab deploy heroku --html site/)\n\nPLEASE NOTE: deploy uses the service name specified in the docker-compose.yaml configuration file to determine which instance to connect to. The service name will be added as part of ```lab launch ec2```. Otherwise, a tag must be added to the instance with key "Services" and value "<service1>,<service2>".',
    'help': 'deploys service to a remote platform',
    'benefit': 'Makes a service available online.'
}

from pocketlab.init import fields_model

def deploy(platform_name, service_option, environ_type='test', resource_tag='', region_name='', verbose=True, overwrite=False, ssl=True, resume_routine=False, print_terminal=False, mount_volumes=False, virtualbox='default', html_folder='', php_folder='', python_folder='', java_folder='', ruby_folder='', node_folder='', jingo_folder=''):
    
    '''
        a method to deploy the docker image of a service to a remote host
        
    :param platform_name: string with name of remote platform to host service
    :param service_option: [optional] string with name of service in lab registry
    :param verbose: [optional] boolean to toggle process messages
    :param overwrite: [optional] boolean to overwrite existing container
    :param ssl: [optional] boolean to enable ssl certification
    :param resume_routine: [optional] boolean to resume from last sub-routine
    :param mount_volumes: [optional] boolean to mount volumes in docker-compose.yaml
    :param virtualbox: [optional] string with name of virtualbox image (win7/8)
    :param html_folder: [optional] string with path to static html site folder root
    :param php_folder: [optional] string with path to php app folder root
    :param python_folder: [optional] string with path to python app folder root
    :param java_folder: [optional] string with path to java app folder root
    :param ruby_folder: [optional] string with path to ruby app folder root
    :param node_folder: [optional] string with path to node app folder root
    :param jingo_folder: [optional] string with path to jingo app folder root
    :param print_terminal: [optional] boolean to print ssh commands and conf values
    :return: string with exit message
    '''
    
    title = 'deploy'

# ingest service option
    if isinstance(service_option, str):
        if service_option:
            service_option = [service_option]
            
# validate inputs
    input_fields = {
        'service_option': service_option,
        'platform_name': platform_name,
        'environ_type': environ_type,
        'resource_tag': resource_tag,
        'region_name': region_name,
        'virtualbox': virtualbox,
        'html_folder': html_folder,
        'php_folder': php_folder,
        'python_folder': python_folder,
        'java_folder': java_folder,
        'ruby_folder': ruby_folder,
        'node_folder': node_folder,
        'jingo_folder': jingo_folder
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
        heroku_details = validate_platform(heroku_model, details['path'], service_name, '.lab')
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
            elif jingo_folder:
                jingo_folder = _site_path(jingo_folder, service['path'], service_insert, 'jingo')
                heroku_client.deploy_app(jingo_folder, 'jingo')
                exit_msg = 'Jingo app of %s' % heroku_insert

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
                    'system_environment': environ_type,
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
                if print_terminal:
                    print(dockerfile_text)

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

# deploy to ec2
    elif platform_name == 'ec2':

    # check for library dependencies
        from pocketlab.methods.dependencies import import_boto3
        import_boto3('ec2 platform')

    # retrieve progress point
        from pocketlab import __module__
        from labpack.storage.appdata import appdataClient
        from labpack.compilers.encoding import encode_data, decode_data
        progress_client = appdataClient(collection_name='Progress Points', prod_name=__module__)
        progress_id = 'deploy.yaml'
        progress_map = { 'step': 0 }
        if resume_routine:
            try:
                progress_map = decode_data(progress_id, progress_client.load(progress_id))
            except:
                pass
        progress_client.save(progress_id, encode_data(progress_id, progress_map))

    # retrieve aws config
        from os import path, remove
        from time import time
        from pocketlab import __module__
        from jsonmodel.loader import jsonLoader
        from jsonmodel.validators import jsonModel
        from pocketlab.methods.validation import validate_platform
        aws_schema = jsonLoader(__module__, 'models/aws-config.json')
        aws_model = jsonModel(aws_schema)
        aws_config = validate_platform(aws_model, details['path'], service_name, '.lab')
        details['config'] = aws_config
        service_list.append(details)

    # construct docker client
        from labpack.platforms.docker import dockerClient
        docker_client = dockerClient()

        from pprint import pprint

    # iterate over each service
        for service in service_list:

        # construct variables
            service_name = service['name']
            service_root = service['path']
            service_insert = service['insert']
            msg_insert = 'working directory'
            if service_name:
                msg_insert = 'root directory for "%s"' % service_name
            ec2_insert = 'service %s deployed to ec2.' % service_insert

        # retrieve instance details from ec2
            from pocketlab.methods.aws import initialize_clients
            ec2_client, ssh_client, instance_details = initialize_clients(
                aws_cred=aws_config,
                service_name=service_name, 
                service_insert=service_insert, 
                service_root=service_root, 
                region_name=region_name, 
                environment_type=environ_type, 
                resource_tag=resource_tag, 
                verbose=verbose
            )

        # define ssh script printer
            def print_script(command, message, error=''):
                if verbose:
                    if print_terminal:
                        print(message)
                    else:
                        print(message, end='', flush=True)
                try:
                    response = ssh_client.script(command)
                    if verbose:
                        if not print_terminal:
                            print('done.')
                except:
                    if verbose:
                        print('ERROR.')
                    if error:
                        raise Exception(error)
                    else:
                        raise
                return response

        # disable normal ssh client printing
            if not print_terminal:
                ssh_client.ec2.iam.verbose = False

        # verify docker installed on ec2
            sys_command = 'docker --help'
            sys_message = 'Verifying docker installed on ec2 image ... '
            sys_error = '"docker" not installed.\nTry using an ECS-Optimized AMI or install docker (https://www.docker.com).'
            print_script(sys_command, sys_message, sys_error)

        # retrieve docker images
            sys_command = 'docker images'
            sys_message = 'Retrieving list of images on ec2 image ... '
            sys_output = print_script(sys_command, sys_message)
            image_list = docker_client._images(sys_output)

        # retrieve docker containers
            sys_command = 'docker ps -a'
            sys_message = 'Retrieving list of containers on ec2 image ... '
            sys_output = print_script(sys_command, sys_message)
            container_list = docker_client._ps(sys_output)

        # retrieve list of ports
            sys_command = 'netstat -lntu'
            sys_message = 'Retrieving list of open ports on ec2 image ... '
            sys_output = print_script(sys_command, sys_message)
            from labpack.parsing.shell import convert_table
            output_lines = sys_output.splitlines()
            sys_output = '\n'.join(output_lines[1:])
            delimiter = '\s(?!A)\s*'
            connection_list = convert_table(sys_output, delimiter)
            port_list = []
            import re
            for connection in connection_list:
                if connection['State'] == 'LISTEN':
                    port_search = re.findall('.*:(\d+)$', connection['Local Address'])
                    port_list.append(int(port_search[0]))

        # retrieve service configurations
            from pocketlab.methods.service import retrieve_service_config
            service_title = '%s %s' % (title, platform_name)
            service_config, service_name = retrieve_service_config(
                service_root=service_root,
                service_name=service_name,
                command_title=service_title
            )

        # verify overwrite of existing container
            existing_container = None
            for container in container_list:
                if service_name == container['NAMES']:
                    import json
                    sys_command = 'docker inspect %s' % service_name
                    response = ssh_client.script(sys_command)
                    settings = json.loads(response)
                    try:
                        sys_command = 'docker logs --tail 1 %s' % service_name
                        ssh_client.script(sys_command)
                        status = 'stopped'
                    except:
                        status = 'exited'
                    synopsis = docker_client._synopsis(settings[0], status)
                    if not overwrite and not resume_routine:
                        raise Exception('"%s" is %s on ec2 image. To replace, add "-f"' % (service_name, synopsis['container_status']))
                    else:
                        existing_container = synopsis

        # verify port availability
            from pocketlab.methods.service import compile_ports
            service_ports = compile_ports(service_config)
            if service_ports:
                container_ports = set()
                if existing_container:
                    for key in existing_container['mapped_ports'].keys():
                        container_ports.add(int(key))
                used_ports = set(port_list) - container_ports
                conflict_ports = used_ports.intersection(service_ports)
                if conflict_ports:
                    from labpack.parsing.grammar import join_words
                    port_names = join_words(list(conflict_ports))
                    port_plural = ''
                    if len(conflict_ports) > 1:
                        port_plural = 's'
                    raise Exception('Port%s %s are already in use by other processes on ec2 image.' % (port_plural, port_names))

        # construct system envvar
            system_envvar = {
                'system_environment': environ_type,
                'system_platform': 'ec2',
                'system_ip': '',
                'public_ip': ''
            }
            if 'public_ip_address' in instance_details.keys():
                system_envvar['public_ip'] = instance_details['public_ip_address']
            if 'private_ip_address' in instance_details.keys():
                system_envvar['system_ip'] = instance_details['private_ip_address']

        # verify image exists
            if mount_volumes:

            # validate image exists in local docker repository
                from pocketlab.methods.validation import validate_image
                docker_images = docker_client.images()
                service_repo, service_tag = validate_image(service_config, docker_images, service_name)

        # or build new image
            else:

            # define service variables and check progress
                service_repo = service_name
                service_tag = ''
                if progress_map['step'] < 1:
                    
                # establish path of files
                    dockerfile_path = path.join(service_root, 'Dockerfile')
                    platform_path = path.join(service_root, 'DockerfileEC2')
                    compose_path = path.join(service_root, 'docker-compose.yaml')
                    temp_path = path.join(service_root, 'DockerfileTemp%s' % int(time()))
        
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
                    if print_terminal:
                        print(dockerfile_text)
    
                # create temporary Dockerfile
                    from os import remove
                    from shutil import copyfile
                    if path.exists(dockerfile_path):
                        copyfile(dockerfile_path, temp_path)
                    with open(dockerfile_path, 'wt') as f:
                        f.write(dockerfile_text)
                        f.close()
    
                # start image build
                    try:
                        if verbose:
                            print('Building docker image ... ')
                            docker_client.verbose = True
                        docker_client.build(service_name, dockerfile_path=dockerfile_path)
                        if verbose:
                            docker_client.verbose = False
                    except Exception as err:
    
                    # ROLLBACK Dockerfile
                        if path.exists(temp_path):
                            copyfile(temp_path, dockerfile_path)
                            remove(temp_path)
    
                        raise
    
                # restore Dockerfile
                    if path.exists(temp_path):
                        copyfile(temp_path, dockerfile_path)
                        remove(temp_path)
                
                # save progress
                    progress_map['step'] = 1
                    progress_client.save(progress_id, encode_data(progress_id, progress_map))

        # copy volumes to ec2 image
            volumes_mounted = False
            if mount_volumes:

                if progress_map['step'] < 1:

                    if 'volumes' in service_config.keys():

                    # create directory for service
                        if service_config['volumes']:
    
                        # verbosity
                            if verbose:
                                print('Copying volumes to ec2 image', end='', flush=True)
    
                        # determine if service folder exists
                            sys_command = 'ls %s' % service_name
                            try:
                                ssh_client.script(sys_command)
                                if not overwrite:
                                    if verbose:
                                        print('ERROR.')
                                    raise Exception('Files for "%s" already exist on ec2 image. To replace, add "-f"' % (service_name))
                        # determine if service node is a folder
                                try:
                                    sys_command = 'cd %s' % service_name
                                    ssh_client.script(sys_command)
                                except:
                                    sys_commands = [
                                        'sudo rm %s' % service_name,
                                        'mkdir %s' % service_name
                                    ]
                                    ssh_client.script(sys_commands)
                            except:
                                ssh_client.script('mkdir %s' % service_name)
    
                        # copy volumes to image
                            from os import path
                            for volume in service_config['volumes']:
                                if volume['type'] == 'bind':
                                    remote_path = path.join(service_name, volume['source'])
                                    local_path = path.join(service_root, volume['source'])
                                    try:
                                        ssh_client.put(local_path, remote_path, overwrite=True)
                                    except:
                                        if verbose:
                                            print(' ERROR.')
                                        raise
                                    if verbose:
                                        print('.', end='', flush=True)
    
                            volumes_mounted = True
    
                        # verbosity
                            if verbose:
                                print(' done.')

                # save progress
                    progress_map['step'] = 1
                    progress_client.save(progress_id, encode_data(progress_id, progress_map))

        # save docker image to local file
            if progress_map['step'] < 2:
                file_name = '%s%s.tar' % (service_name, int(time()))
                file_path = path.relpath(path.join(service_root, file_name))
                if verbose:
                    print('Saving docker image %s as %s ... ' % (service_name, file_name), end='', flush=True)
                try:
                    docker_client.save(service_repo, file_path, service_tag)
                    if verbose:
                        print('done.')
                except:
                    if verbose:
                        print('ERROR.')
                # ROLLBACK local tar file
                    if path.exists(file_path):
                        remove(file_path)
                    raise
    
            # copy local file to ec2 image
                if verbose:
                    print('Copying %s to ec2 image ... ' % file_name, end='', flush=True)
                try:
                    ssh_client.put(file_path, file_name)
                    if verbose:
                        print('done.')
                except:
                    if verbose:
                        print('ERROR.')
                # ROLLBACK local tar file
                    if path.exists(file_path):
                        remove(file_path)
                    raise
    
            # remove local tar file
                if path.exists(file_path):
                    remove(file_path)
    
            # load file into docker on ec2 image
                sys_commands = [ 
                    'docker load -i %s' % file_name,
                    'rm %s' % file_name
                ]
                sys_message = 'Loading %s into docker on ec2 image ... ' % file_name
                print_script(sys_commands, sys_message)

            # save progress
                progress_map['step'] = 2
                progress_client.save(progress_id, encode_data(progress_id, progress_map))

        # check for docker restart command
            sys_command = 'sudo cat /etc/rc3.d/S99local'
            sys_message = 'Checking S99local for service restart command ... '
            s99local_text = print_script(sys_command, sys_message)

        # update docker restart command
            if progress_map['step'] < 3:
                restart_command = 'docker restart %s' % service_name
                if s99local_text.find(restart_command) == -1:
                    sys_command = 'sudo chmod 777 /etc/rc3.d/S99local; echo "%s" >> /etc/rc3.d/S99local' % restart_command
                    sys_message = 'Updating S99local to restart service on system restart ... '
                    print_script(sys_command, sys_message)
    
            # compile run command
                from pocketlab.methods.docker import compile_run_kwargs, compile_run_command
                run_kwargs = compile_run_kwargs(
                    service_config=service_config,
                    service_repo=service_repo,
                    service_alias=service_name,
                    service_tag=service_tag,
                    service_path=service_root,
                    system_envvar=system_envvar
                )
                if not volumes_mounted:
                    run_kwargs['environmental_variables'] = {}
                    run_kwargs['mounted_volumes'] = {}
                    run_kwargs['start_command'] = ''
                run_command = compile_run_command(run_kwargs, root_path='~/%s' % service_name) 

            # remove existing container
                if existing_container:
                    sys_command = 'docker rm -f %s' % existing_container['container_alias']
                    sys_message = 'Removing existing container "%s" on ec2 image ... ' % existing_container['container_alias']
                    print_script(sys_command, sys_message)
    
            # start container
                sys_message = 'Starting container "%s" on ec2 image ... ' % service_name
                print_script(run_command, sys_message)
            
            # save progress
                progress_map['step'] = 3
                progress_client.save(progress_id, encode_data(progress_id, progress_map))

        # add reverse proxies
            if 'labels' in service_config.keys():
                if service_config['labels']:

                # determine domains port mapping
                    domain_map = {}
                    import re
                    for key, value in service_config['labels'].items():
                        if not re.findall('[^\d]+', value):
                            domain_name = ''
                            cert_name = ''
                            domain_segments = key.split('.')
                            segment_count = 0
                            while domain_segments:
                                if domain_name:
                                    domain_name += '.'
                                    cert_name += '.'
                                segment_name = domain_segments.pop()
                                domain_name += segment_name
                                if segment_count < 2:
                                    cert_name += segment_name
                                segment_count += 1
                            domain_map[domain_name] = {
                                'domain': domain_name,
                                'port': int(value),
                                'cert': cert_name
                            }

                # register ssl certificate for domains
                    if progress_map['step'] < 4:
                        if ssl:

                        # verify installation of certbot
                            sys_command = 'certbot-auto --version --debug'
                            sys_message = 'Verifying certbot installed on ec2 image ... '
                            try:
                                print_script(sys_command, sys_message)
                            except:
                                install_commands = [
                                    'sudo yum update -y',
                                    'sudo yum install -y wget',
                                    'wget https://dl.eff.org/certbot-auto',
                                    'sudo chmod a+x certbot-auto',
                                    'sudo mv certbot-auto /usr/local/bin/certbot-auto',
                                    'certbot-auto --version --debug -y'
                                ]
                                sys_message = 'Installing certbot on ec2 image ... '
                                print_script(install_commands, sys_message)
        
                        # retrieve certbot information
                            sys_command = 'certbot-auto certificates --standalone --debug --pre-hook "service nginx stop" --post-hook "service nginx start"'
                            sys_message = 'Retrieving certificate information ... '
                            certbot_text = print_script(sys_command, sys_message)
        
                        # parse renewal domains in certbot information
                            from time import time
                            from pocketlab.methods.certbot import extract_domains
                            certbot_domains = extract_domains(certbot_text)
                            certbot_map = {}
                            renew_certs = False
                            renew_time = time() + 29 * 24 * 3600
                            for domain in certbot_domains:
                                if not domain['cert'] in certbot_map.keys():
                                    certbot_map[domain['cert']] = []
                                certbot_map[domain['cert']].append(domain['domain'])
                                if domain['expires'] < renew_time:
                                    renew_certs = True
        
                        # add new domains to certbot map
                            initial_certs = {}
                            update_certs = []
                            for key, value in domain_map.items():
                                if not key in certbot_map.keys():
                                    initial_certs[key] = []
                                    initial_certs[key].append(key)
                                    initial_certs[key].append('www.%s' % key)
                                elif key in initial_certs.keys():
                                    pass
                                elif not value['domain'] in certbot_map[key]:
                                    certbot_map[key].append(value['domain'])
                                    update_certs.append(key)

                        # register certbot information
                            initial_commands = []
                            for key, value in initial_certs.items():
                                initial_command = 'certbot-auto certonly --standalone -d %s --debug --pre-hook "service nginx stop" --post-hook "service nginx start"' % ','.join(value)
                                initial_commands.append(initial_command)
                            if initial_commands:
                                raise Exception('Registration of a new ssl certificate using CertBot must be done manually.\nTry: lab connect ec2\n%s\nThen exit ssh and run "lab deploy ec2 --resume"' % '\n'.join(initial_commands))
        
                        # update certbot information
                            update_commands = []
                            for cert in update_certs:
                                certbot_command = 'certbot-auto certonly --standalone --debug -n --cert-name %s -d %s --pre-hook "service nginx stop" --post-hook "service nginx start"  --debug' % (cert, ','.join(certbot_map[cert]))
                                update_commands.append(certbot_command)
                            if update_commands:
                                sys_message = 'Updating ssl certificate information ... '
                                print_script(update_commands, sys_message)

                        # renew certbot information
                            if renew_certs:
                                sys_command = 'certbot-auto renew --standalone --debug --pre-hook "service nginx stop" --post-hook "service nginx start"'
                                sys_message = 'Renewing ssl certificates ... '
                                print_script(sys_command, sys_message)
                            
                    # save progress
                        progress_map['step'] = 4
                        progress_client.save(progress_id, encode_data(progress_id, progress_map))
                
                # verify installation of nginx
                    if progress_map['step'] < 5:
                        if s99local_text.find('service nginx restart') == -1:
                            install_commands = [
                                'sudo yum update -y',
                                'sudo yum install -y nginx',
                                'sudo chmod 777 /etc/rc3.d/S99local; echo "service nginx restart" >> /etc/rc3.d/S99local'
                            ]
                            sys_message = 'Installing nginx on ec2 image ... '
                            print_script(install_commands, sys_message)
    
                    # retrieve nginx information
                        nginx_path = '/etc/nginx/nginx.conf'
                        sys_command = 'sudo cat %s' % nginx_path
                        sys_message = 'Reading existing nginx configuration ... '
                        nginx_text = print_script(sys_command, sys_message)
    
                    # update nginx information
                        from pocketlab.methods.nginx import compile_nginx, extract_servers
                        nginx_servers = extract_servers(nginx_text)
                        server_map = {}
                        for server in nginx_servers:
                            server_map[server['domain']] = server
                        for key, value in domain_map.items():
                            server_map[key] = value
                        server_list = []
                        for key, value in server_map.items():
                            server_list.append(value)
                        nginx_updated = compile_nginx(server_list)
                        if ssl:
                            nginx_updated = compile_nginx(
                                server_list=server_list, 
                                ssl_port=443,
                                ssl_gateway='certbot'
                            )
                        if print_terminal:
                            print(nginx_updated)

                    # replace nginx conf and restart nginx on ec2 image
                        nginx_name = 'nginx%s.conf' % int(time())
                        nginx_temp = path.relpath(path.join(service_root, nginx_name))
                        with open(nginx_temp, 'wt') as f:
                            f.write(nginx_updated)
                            f.close()
                        if verbose:
                            print('Updating nginx configurations on ec2 image ... ', end='', flush=True)
                        try:
                            ssh_client.put(nginx_temp, nginx_path, overwrite=True)
                            ssh_client.script('sudo service nginx restart')
                            if verbose:
                                print('done.')
                        except:
                            if verbose:
                                print('ERROR.')
                            remove(nginx_temp)
                            raise

                    # save progress
                        progress_map['step'] = 5
                        progress_client.save(progress_id, encode_data(progress_id, progress_map))

        # TODO cleanup orphaned files and images on ec2
            if progress_map['step'] < 6:
                pass

        # compose exit message
            ssh_client.ec2.iam.verbose = True
            exit_msg = 'Docker image of %s' % ec2_insert

            if len(service_list) > 1:
                print(exit_msg)
        
        # reset progress
            progress_map['step'] = 0
            progress_client.save(progress_id, encode_data(progress_id, progress_map))

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