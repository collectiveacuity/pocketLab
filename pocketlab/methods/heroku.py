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
        
    # construct localhost
        from labpack.platforms.localhost import localhostClient
        self.localhost = localhostClient()
    
    # validate installation
        self._validate_install()
    
    # validate access
        self._validate_access()
        
    def _validate_install(self):

        ''' a method to validate heroku is installed '''

        if self.verbose:
            print('Checking heroku installation...', end='', flush=True)
    
    # import dependencies
        from os import devnull
        from subprocess import call, check_output
        
    # validate cli installation        
        sys_command = 'heroku --version'
        try:
            call(sys_command, stdout=open(devnull, 'wb'))
        except Exception as err:
            raise Exception('"heroku cli" not installed. GoTo: https://devcenter.heroku.com/articles/heroku-cli')
        if self.verbose:
            print('.', end='', flush=True)
            
    # validate container plugin
        sys_command = 'heroku plugins'
        heroku_plugins = check_output(sys_command, stderr=open(devnull, 'wb')).decode('utf-8')
        if heroku_plugins.find('heroku-container-registry') == -1:
            raise Exception('heroku container plugin required. Try: heroku plugins:install heroku-container-registry')
        if self.verbose:
            print(' done.')
            
        return True

    def _cli_input(self, sys_command, lambda_sequence):
        
        ''' a method to answer command line interface inputs '''

        from subprocess import Popen, PIPE, CalledProcessError
        try:
            with Popen(sys_command, stdin=PIPE, stdout=PIPE, universal_newlines=True) as p:
                count = 0
                for line in p.stdout:
                    answer = lambda_sequence[0](line)
                    count += 1
                    if not answer:
                        continue
                    print(answer, file=p.stdin)
                    p.stdin.flush()
        except CalledProcessError:
            from requests import Request
            from labpack.handlers.requests import handle_requests
            test_url = 'http://collectiveacuity.com'
            request_object = Request(method='GET', url=test_url)
            request_details = handle_requests(request_object)
            raise ConnectionError(request_details['error'])
        except:
            raise
        
    def _request_command(self, sys_command, pipe=False):

        ''' a method to handle system commands which require connectivity '''

        import sys
        from subprocess import Popen, PIPE, check_output
        
        try:
            if pipe:
                response = Popen(sys_command, shell=True, stdout=PIPE)
                for line in response.stdout:
                    if self.verbose:
                        print(line.decode('utf-8').rstrip('\n'))
                    sys.stdout.flush()
                response.wait()
                return response
            else:
                response = check_output(sys_command).decode('utf-8')
                return response
        except Exception as err:
            from requests import Request
            from labpack.handlers.requests import handle_requests
            test_url = 'http://www.google.com'
            request_object = Request(method='GET', url=test_url)
            request_details = handle_requests(request_object)
            if request_details['error']:
                raise ConnectionError(request_details['error'])
            else:
                raise err
        
    def _validate_access(self):
        
        ''' a method to validate user can access resource '''
        
        title = '%s.validate_access' % self.__class__.__name__
            
    # verbosity
        wait_msg = 'Checking heroku credentials and access to "%s" subdomain...' % self.subdomain
        if self.verbose:
            print(wait_msg, end='', flush=True)

    # confirm access to account
    # TODO fix error handling for login on LINUX, MAC
        if not self.localhost.os.sysname in ('Windows'):
            lambda_sequence = [
                lambda x: self.email,
                lambda x: self.password
            ]
            self._cli_input('heroku login', lambda_sequence)
            if self.verbose:
                print('.', end='', flush=True)
            lambda_sequence = [
                lambda x: self.email
            ]
            self._cli_input('heroku container:login', lambda_sequence)
            if self.verbose:
                print('.', end='', flush=True)
                
    # confirm existence of subdomain
        sys_command = 'heroku ps -a %s' % self.subdomain
        heroku_response = self._request_command(sys_command)    
        if heroku_response.find('find that app') > -1:
            raise Exception('%s does not exist. Try: heroku create -a %s' % (self.subdomain, self.subdomain))
        elif heroku_response.find('have access to the app') > -1:
            raise Exception('%s belongs to another account.' % self.subdomain)
        elif heroku_response.find('your Heroku credentials') > -1:
            raise Exception('On Windows, you need to login to heroku using cmd.exe.\nWith cmd.exe, try: heroku login')

    # return self
        if self.verbose:
            print(' done.')
        
        return True
    
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

    # verbosity
        if self.verbose:
            print('Building docker image...')
            
    # validate dockerfile
        if not path.exists('Dockerfile'):
            raise Exception('heroku requires a Dockerfile in working directory to deploy using Docker.')
    
    # build docker image
        sys_command = 'heroku container:push %s --app %s' % (docker_image, self.subdomain)
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
    