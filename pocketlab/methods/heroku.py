__author__ = 'rcj1492'
__created__ = '2017.06'
__license__ = 'MIT'

class herokuClient(object):
    
    _class_fields = {
        'schema': {
            'account_email': 'noreply@collectiveacuity.com',
            'account_password': 'abcDEF123GHI!!!',
            'app_subdomain': 'mycoolappsubdomain',
            'docker_image': 'appimage',
            'virtualbox_name': 'default'
        }
    }
    
    def __init__(self, account_email, account_password, app_subdomain, verbose=False):
        
        ''' a method to initialize the herokuClient class '''

        title = '%s.__init__' % self.__class__.__name__
        
    # construct fields model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # validate inputs
        input_fields = {
            'account_email': account_email,
            'account_password': account_password,
            'app_subdomain': app_subdomain
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
        self.email = account_email
        self.password = account_password
        self.subdomain = app_subdomain

    # construct class properties
        self.verbose = verbose
        self.printer_on = True
        def _printer(msg, flush=False):
            if self.verbose:
                if self.printer_on:
                    if flush:
                        print(msg, end='', flush=True)
                    else:
                        print(msg)
        self.printer = _printer
        
    # construct localhost
        from labpack.platforms.localhost import localhostClient
        self.localhost = localhostClient()
    
    # validate installation
        self._validate_install()
    
    # validate access
        self._validate_access()
        
    def _validate_install(self):

        ''' a method to validate heroku is installed '''

        self.printer('Checking heroku installation ... ', flush=True)
    
    # import dependencies
        from os import devnull
        from subprocess import call, check_output
        
    # validate cli installation        
        sys_command = 'heroku --version'
        try:
            call(sys_command, shell=True, stdout=open(devnull, 'wb'))
        except Exception as err:
            self.printer('ERROR')
            raise Exception('"heroku cli" not installed. GoTo: https://devcenter.heroku.com/articles/heroku-cli')
            
    # validate container plugin
        sys_command = 'heroku plugins'
        heroku_plugins = check_output(sys_command, shell=True, stderr=open(devnull, 'wb')).decode('utf-8')
        if heroku_plugins.find('heroku-container-registry') == -1:
            self.printer('ERROR')
            raise Exception('heroku container plugin required. Try: heroku plugins:install heroku-container-registry')
        if self.verbose:
            self.printer('done.')
            
        return True

    def _cli_input(self, sys_command, answer_func, return_func=None):
        
        ''' a method to answer command line interface inputs '''

        from subprocess import Popen, PIPE, CalledProcessError
        try:
            with Popen(sys_command, stdin=PIPE, stdout=PIPE, shell=True, universal_newlines=True) as p:
                for line in p.stdout:
                    if return_func:
                        return_value = return_func(line)
                        if return_value:
                            return return_value
                    answer = answer_func(line)
                    if answer: 
                        print(answer, file=p.stdin)
                        p.stdin.flush()
                              
        except CalledProcessError as err:
            try:
                import requests
                requests.get('https://www.google.com')
                return err.output.decode('ascii', 'ignore')
            except:
                from requests import Request
                from labpack.handlers.requests import handle_requests
                request_object = Request(method='GET', url='https://www.google.com')
                request_details = handle_requests(request_object)
                self.printer('ERROR')
                raise ConnectionError(request_details['error'])
        except:
            self.printer('ERROR')
            raise
        
    def _request_command(self, sys_command, pipe=False):

        ''' a method to handle system commands which require connectivity '''

        import sys
        from subprocess import Popen, PIPE, check_output, STDOUT, CalledProcessError
        
        try:
            if pipe:
                response = Popen(sys_command, shell=True, stdout=PIPE)
                for line in response.stdout:
                    self.printer(line.decode('utf-8').rstrip('\n'))
                    sys.stdout.flush()
                response.wait()
                return response
            else:
                response = check_output(sys_command, shell=True, stderr=STDOUT).decode('utf-8')
                return response
        except CalledProcessError as err:
            try:
                import requests
                requests.get('https://www.google.com')
                return err.output.decode('ascii', 'ignore')
            except:
                from requests import Request
                from labpack.handlers.requests import handle_requests
                request_object = Request(method='GET', url='https://www.google.com')
                request_details = handle_requests(request_object)
                self.printer('ERROR')
                raise ConnectionError(request_details['error'])
        except:
            self.printer('ERROR')
            raise
    
    def _check_connectivity(self, err):

        ''' a method to check connectivity as source of error '''
        
        try:
            import requests
            requests.get('https://www.google.com')
        except:
            from requests import Request
            from labpack.handlers.requests import handle_requests
            request_object = Request(method='GET', url='https://www.google.com')
            request_details = handle_requests(request_object)
            self.printer('ERROR')
            raise ConnectionError(request_details['error'])
        raise err

    def _validate_access(self):
        
        ''' a method to validate user can access resource '''
        
        title = '%s.validate_access' % self.__class__.__name__
            
    # verbosity
        self.printer('Checking heroku credentials and access to "%s" subdomain ... ' % self.subdomain, flush=True)

    # confirm access to account
        if not self.localhost.os.sysname in ('Windows'):
        
            import sys
            import pexpect
            login_fail = ''
            try:
                child = pexpect.spawn('heroku login', encoding='utf-8', timeout=2)
                child.delaybeforesend = 0.5
                child.expect('Email:\s?')
                child.sendline(self.email)
                child.expect('Password:\s?')
                child.sendline(self.password)
    # TODO fix heroku login timeout issue
                i = child.expect(['Email:\s?', 'not\sa\stty', 'Logged in', pexpect.EOF, pexpect.TIMEOUT])
                if i == 0:
                    child.terminate()
                    raise Exception('Permission denied. Heroku login credentials are not valid.')
                elif i == 1:
                    child.terminate()
                    raise Exception('Heroku is retarded.')
                elif i < 4:
                    child.terminate()
                else:
                    child.terminate()
                    login_fail = 'Some unknown issue prevents Heroku from accepting credentials.\nTry first: heroku login'
            except Exception as err:
               self._check_connectivity(err)
            
            if login_fail:
                try:
                    from subprocess import check_output
                    check_output('heroku auth:token', shell=True).decode('utf-8')
                except:
                    raise Exception(login_fail)
            
    # confirm existence of subdomain
        sys_command = 'heroku ps -a %s' % self.subdomain
        heroku_response = self._request_command(sys_command)    
        if heroku_response.find('find that app') > -1:
            self.printer('ERROR')
            raise Exception('%s does not exist. Try: heroku create -a %s' % (self.subdomain, self.subdomain))
        elif heroku_response.find('have access to the app') > -1:
            self.printer('ERROR')
            raise Exception('%s belongs to another account. Try: heroku login' % self.subdomain)
        elif heroku_response.find('your Heroku credentials') > -1:
            self.printer('ERROR')
            raise Exception('On Windows, you need to login to heroku using cmd.exe.\nWith cmd.exe, Try: heroku login')
    
    # return self
        self.printer('done.')
        
        return True

    def _validate_docker(self):

    # confirm access to docker registry
        def login_logic(line):
            if line.find('Email') > -1:
                return self.email
            elif line.find('Password') > -1:
                return self.password

        self._cli_input('heroku container:login', login_logic)
        
    def deploy_docker(self, docker_image, virtualbox_name='default'):

        ''' a method to deploy app to heroku using docker '''

        title = '%s.deploy_docker' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'docker_image': docker_image,
            'virtualbox_name': virtualbox_name
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # import dependencies
        from os import path

    # validate docker client
        from pocketlab.methods.docker import dockerClient
        dockerClient(virtualbox_name, self.verbose)

    # validate dockerfile
        if not path.exists('Dockerfile'):
            raise Exception('heroku requires a Dockerfile in working directory to deploy using Docker.')

    # verbosity
        self.printer('Building docker image ...')
    
    # build docker image
        sys_command = 'heroku container:push web --app %s' % self.subdomain
        self._request_command(sys_command, pipe=True)

        return True


if __name__ == '__main__':
    
    from labpack.records.settings import load_settings
    heroku_config = load_settings('../../../cred/heroku.yaml')
    heroku_kwargs = {
        'account_email': heroku_config['heroku_account_email'],
        'account_password': heroku_config['heroku_account_password'],
        'app_subdomain': heroku_config['heroku_app_subdomain'],
        'verbose': True
    }
    heroku_client = herokuClient(**heroku_kwargs)
    