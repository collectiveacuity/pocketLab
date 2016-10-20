__author__ = 'rcj1492'
__created__ = '2016.03'

from os import devnull, environ, system
from re import compile
from subprocess import check_output, call

class dockerSession(object):

    def __init__(self, cmd_kwargs, vbox_name=''):

        '''

        :param cmd_kwargs: dictionary with request keywords
        :param vbox_name: string with name of virtualbox (on Mac & Windows)
        :return: dockerConfig object

        self.error : dictionary with error handling information
        self.vbox : string with name of virtual box (on Mac & Windows)
        '''

    # construct error method and add kwargs
        self.error = { 'kwargs': cmd_kwargs, }

    # validate installation of docker
        sys_command = 'docker --help'
        try:
            call(sys_command, stdout=open(devnull, 'wb'))
        except Exception as err:
            from pocketlab.exceptions.lab_exception import labException
            self.error['exception'] = err
            self.error['error_value'] = sys_command
            self.error['failed_test'] = 'required_module'
            self.error['message'] = '"docker" not installed. GoTo: https://www.docker.com'
            raise labException(**self.error)

    # validate installation of docker-machine
        if vbox_name:
            sys_command = 'docker-machine --help'
            try:
                call(sys_command, stdout=open(devnull, 'wb'))
            except Exception as err:
                from pocketlab.exceptions.lab_exception import labException
                self.error['exception'] = err
                self.error['error_value'] = sys_command
                self.error['failed_test'] = 'required_module'
                self.error['message'] = '"docker-machine" not installed. GoTo: https://www.docker.com'
                raise labException(**self.error)

    # construct basic methods
        self.vbox = vbox_name

    # test status of virtualbox
        if self.vbox:
            sys_command = 'docker-machine status %s' % self.vbox
            self.error['error_value'] = sys_command
            self.error['failed_test'] = 'required_resource'
            try:
                vbox_status = check_output(sys_command, stderr=open(devnull, 'wb')).decode('utf-8').replace('\n','')
            except Exception as err:
                from pocketlab.exceptions.lab_exception import labException
                self.error['exception'] = err
                if self.vbox == "default":
                    self.error['message'] = 'Virtualbox "default" not found. Container will not start without a valid virtualbox.'
                    raise labException(**self.error)
                else:
                    self.error['message'] = 'Virtualbox "%s" not found. Try using "default" instead.' % self.vbox
                    raise labException(**self.error)
            if 'Stopped' in vbox_status:
                from pocketlab.exceptions.lab_exception import labException
                self.error['message'] = 'Virtualbox "%s" is stopped. Try first running: docker-machine start %s' % (self.vbox, self.vbox)
                raise labException(**self.error)

    # inject variables to connect to docker
            if not environ.get('DOCKER_CERT_PATH'):
                sys_command = 'docker-machine env %s' % self.vbox
                cmd_output = check_output(sys_command).decode('utf-8')
                variable_list = [ 'DOCKER_TLS_VERIFY', 'DOCKER_HOST', 'DOCKER_CERT_PATH', 'DOCKER_MACHINE_NAME' ]
                for variable in variable_list:
                    env_start = '%s="' % variable
                    env_end = '"\\n'
                    env_regex = '%s.*?%s' % (env_start, env_end)
                    env_pattern = compile(env_regex)
                    env_statement = env_pattern.findall(cmd_output)
                    env_var = env_statement[0].replace(env_start,'').replace('"\n','')
                    environ[variable] = env_var

    def images(self):

        '''

        :return: list of docker images available

        [ {
            'CREATED': '7 days ago',
            'TAG': 'latest',
            'IMAGE ID': '2298fbaac143',
            'VIRTUAL SIZE': '302.7 MB',
            'REPOSITORY': 'test1'
        } ]
        '''

        gap_pattern = compile('\t|\s{2,}')
        image_list = []
        sys_command = 'docker images'
        output_lines = check_output(sys_command).decode('utf-8').split('\n')
        column_headers = gap_pattern.split(output_lines[0])
        for i in range(1,len(output_lines)):
            columns = gap_pattern.split(output_lines[i])
            if len(columns) == len(column_headers):
                image_details = {}
                for j in range(len(columns)):
                    image_details[column_headers[j]] = columns[j]
                image_list.append(image_details)

        return image_list

    def ps(self):

        '''

        :return: list of active docker containers

        [{
            'CREATED': '6 minutes ago',
            'NAMES': 'flask',
            'PORTS': '0.0.0.0:5000->5000/tcp',
            'CONTAINER ID': '38eb0bbeb2e5',
            'STATUS': 'Up 6 minutes',
            'COMMAND': '"gunicorn --chdir ser"',
            'IMAGE': 'rc42/flaskserver'
        }]
        '''

        gap_pattern = compile('\t|\s{2,}')
        container_list = []
        sys_command = 'docker ps -a'
        output_lines = check_output(sys_command).decode('utf-8').split('\n')
        column_headers = gap_pattern.split(output_lines[0])
        for i in range(1,len(output_lines)):
            columns = gap_pattern.split(output_lines[i])
            container_details = {}
            if len(columns) > 1:
                for j in range(len(column_headers)):
                    container_details[column_headers[j]] = ''
                    if j <= len(columns) - 1:
                        container_details[column_headers[j]] = columns[j]
        # stupid hack for possible empty port column
                if container_details['PORTS'] and not container_details['NAMES']:
                    from copy import deepcopy
                    container_details['NAMES'] = deepcopy(container_details['PORTS'])
                    container_details['PORTS'] = ''
                container_list.append(container_details)

        return container_list

    def inspect(self, container_alias='', docker_image='', image_tag=''):

        '''

        :param container_alias: string with name of container
        :return: dictionary of settings of container

        { TOO MANY TO LIST }
        '''

        sys_arg = container_alias
        if docker_image:
            sys_arg = docker_image
            if image_tag:
                sys_arg += ':%s' % image_tag
        import json
        sys_command = 'docker inspect %s' % sys_arg
        output_dict = json.loads(check_output(sys_command).decode('utf-8'))
        container_settings = output_dict[0]

        return container_settings

    def run(self, run_script):

        output_lines = check_output(run_script).decode('utf-8').split('\n')
        container_id = output_lines[0]

        return container_id

    def rm(self, container_alias):

        sys_cmd = 'docker rm -f %s' % container_alias
        output_lines = check_output(sys_cmd).decode('utf-8').split('\n')

        return output_lines[0]

    def rmi(self, image_id):

        sys_cmd = 'docker rmi %s' % image_id
        output_lines = check_output(sys_cmd).decode('utf-8').split('\n')

        return output_lines

    def ip(self):

        '''

        :return: string with ip address of system
        '''

        if self.vbox:
            sys_command = 'docker-machine ip %s' % self.vbox
            system_ip = check_output(sys_command).decode('utf-8').replace('\n','')
        else:
            system_ip = 'hostname --ip-address'

        return system_ip

    def command(self, sys_command):

        '''

        :param sys_command: string with docker command
        :return: raw output from docker
        '''

        return check_output(sys_command).decode('utf-8')

    def synopsis(self, container_settings):

        '''

        :param container_settings: dictionary returned from dockerConfig.inspect
        :return: dictionary with values required for module configurations
        '''

        settings = {
            'container_status': container_settings['State']['Status'],
            'container_ip': container_settings['NetworkSettings']['IPAddress'],
            'docker_image': container_settings['Config']['Image'],
            'container_alias': container_settings['Name'].replace('/',''),
            'container_variables': {},
            'mapped_ports': {},
            'mounted_volumes': {}
        }
        num_pattern = compile('\d+')
        if container_settings['NetworkSettings']['Ports']:
            for key, value in container_settings['NetworkSettings']['Ports'].items():
                port = num_pattern.findall(value[0]['HostPort'])[0]
                settings['mapped_ports'][port] = num_pattern.findall(key)[0]
        if container_settings['Config']['Env']:
            for variable in container_settings['Config']['Env']:
                k, v = variable.split('=')
                settings['container_variables'][k] = v
        for volume in container_settings['Mounts']:
            system_path = volume['Source']
            container_path = volume['Destination']
            settings['mounted_volumes'][system_path] = container_path

        return settings

    def enter(self, local_os, container_alias):

        sys_cmd = 'docker exec -it %s sh' % container_alias
        if local_os in ('Windows'):
            sys_cmd = 'winpty %s' % sys_cmd

        system(sys_cmd)

    def cleanup(self):

        '''
            a method to remove all Exited containers and <none> Images

        :return: boolean
        '''

        return True