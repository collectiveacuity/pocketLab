__author__ = 'rcj1492'
__created__ = '2017.06'
__license__ = 'MIT'

class herokuClient(object):
    
    _class_fields = {
        'schema': {
            'account_email': 'noreply@collectiveacuity.com',
            'account_password': 'abcDEF123GHI!!!',
            'app_subdomain': 'mycoolappsubdomain',
            'docker_image': 'appImage'
        }
    }
    
    def __init__(self, account_email, account_password, verbose=False):
        
        ''' a method to initialize the herokuClient class '''

        title = '%s.__init__' % self.__class__.__name__
        
    # construct fields model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # validate inputs
        input_fields = {
            'account_email': account_email,
            'account_password': account_password
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
        self.email = account_email
        self.password = account_password

    # construct class properties
        self.verbose = verbose
        self.subdomain_list = []
        
    # construct localhost
        from labpack.platforms.localhost import localhostClient
        self.localhost = localhostClient()
    
    # validate installation
        self._validate_install()
        
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
            test_url = 'https://collectiveacuity.com'
            request_object = Request(method='GET', url=test_url)
            request_details = handle_requests(request_object)
            raise ConnectionError(request_details['error'])
        except:
            raise
        
    def _request_command(self, sys_command):

        ''' a method to handle system commands which require connectivity '''
        
        from os import devnull
        from subprocess import check_output
        
        try:
            response = check_output(sys_command, stderr=open(devnull, 'wb')).decode('utf-8')
        except:
            from requests import Request
            from labpack.handlers.requests import handle_requests
            test_url = 'https://collectiveacuity.com'
            request_object = Request(method='GET', url=test_url)
            request_details = handle_requests(request_object)
            raise ConnectionError(request_details['error'])
        
        return response
        
    def validate_access(self, app_subdomain):
        
        ''' a method to validate user can access resource '''
        
        title = '%s.validate_access' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'app_subdomain': app_subdomain
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
        if app_subdomain in self.subdomain_list:
            return self
            
    # verbosity
        if self.verbose:
            print('Checking heroku credentials and access to subdomain...', end='', flush=True)

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
        sys_command = 'heroku ps -a %s' % app_subdomain
        heroku_response = self._request_command(sys_command)    
        if heroku_response.find('find that app') > -1:
            raise Exception('%s does not exist. Try: heroku create -a %s' % (app_subdomain, app_subdomain))
        elif heroku_response.find('have access to the app') > -1:
            raise Exception('%s belongs to another account.' % app_subdomain)
        elif heroku_response.find('your Heroku credentials') > -1:
            raise Exception('On Windows, you need to login to heroku using cmd.exe.\nWith cmd.exe, try: heroku login')

    # return self
        self.subdomain_list.append(app_subdomain)
        if self.verbose:
            print(' done.')
        
        return self
    
    def deploy_docker(self, docker_image, app_subdomain, virtualbox_name=''):
        
        ''' a method to deploy app to heroku using docker '''

        title = '%s.deploy_docker' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'app_subdomain': app_subdomain,
            'docker_image': docker_image
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
                
    # import dependencies
        from os import path
    
    # validate docker client
        from pocketlab.methods.docker import dockerClient
        docker_client = dockerClient(virtualbox_name, self.verbose)

    # verbosity
        if self.verbose:
            print('Building docker image...')
            
    # validate dockerfile
        if not path.exists('Dockerfile'):
            raise Exception('heroku requires a Dockerfile in working directory to deploy using Docker.')
    
    # build docker image
        sys_command = 'heroku container:push %s --app %s' % (docker_image, app_subdomain)
        heroku_response = self._request_command(sys_command)
        print(heroku_response)
        
        return heroku_response
        
if __name__ == '__main__':
    
    from labpack.records.settings import load_settings
    heroku_config = load_settings('../../../cred/heroku.yaml')
    heroku_kwargs = {
        'account_email': heroku_config['heroku_account_email'],
        'account_password': heroku_config['heroku_account_password'],
        'verbose': True
    }
    heroku_client = herokuClient(**heroku_kwargs)
    heroku_client.validate_access(heroku_config['heroku_app_subdomain'])
    