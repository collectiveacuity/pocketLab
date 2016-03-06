__author__ = 'rcj1492'
__created__ = '2016.03'

from os import devnull, environ
from re import compile
from subprocess import check_output, call, PIPE, Popen
from labMgmt.exceptions import LabException

class dockerConfig(object):

    def __init__(self, vbox_name=''):

    # validate installation of docker
        try:
            sys_command = 'docker --help'
            call(sys_command, stdout=open(devnull, 'wb'))
        except:
            raise Exception('docker not installed. GoTo: https://www.docker.com')

    # validate installation of docker-machine
        if vbox_name:
            try:
                sys_command = 'docker-machine --help'
                call(sys_command, stdout=open(devnull, 'wb'))
            except:
                raise Exception('docker-machine not installed. GoTo: https://www.docker.com')

    # construct basic methods
        self.vbox = vbox_name
        # self.eval = 'eval "$(docker-machine env %s)"; ' % self.vbox

    # test status of virtualbox
        if self.vbox:
            try:
                sys_command = 'docker-machine status %s' % self.vbox
                vbox_status = check_output(sys_command, stderr=open(devnull, 'wb')).decode('utf-8').replace('\n','')
            except:
                if self.vbox == "default":
                    raise LabException('Virtualbox "default" not found. Container will not start without a valid virtualbox.')
                else:
                    raise LabException('Virtualbox "%s" not found. Try using "default" instead.' % self.vbox)
            if 'Stopped' in vbox_status:
                raise LabException('Virtualbox "%s" is stopped. Try first running: docker-machine start %s' % (self.vbox, self.vbox))

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

    def localhost(self):

        if self.vbox:
            sys_command = 'docker-machine ip %s' % self.vbox
            system_ip = check_output(sys_command).decode('utf-8').replace('\n','')
        else:
            system_ip = 'hostname --ip-address'

        return system_ip

    def images(self):

        image_list = []
        sys_command = 'docker images'
        output_lines = check_output(sys_command).decode('utf-8').split('\n')
        column_headers = output_lines[0].split()
        for i in range(1,len(output_lines)):
            columns = output_lines[i].split()
            if len(columns) > 2:
                image_details = {}
                for j in range(0,3):
                    image_details[column_headers[j]] = columns[j]
                image_list.append(image_details)

        return image_list

    def settings(self):
        settings = ''

        return settings