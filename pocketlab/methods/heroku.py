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
            'virtualbox_name': 'default',
            'site_folder': 'site/'
        }
    }
    
    def __init__(self, account_email, account_password, app_subdomain, verbose=True):
        
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
    
    # print response and return
        self.printer('done.')
        
        return True
        
    def _handle_command(self, sys_command, pipe=False, handle_error=False):

        ''' a method to handle system commands which require connectivity '''

        import sys
        from subprocess import Popen, PIPE, check_output, STDOUT, CalledProcessError

        try:
            if pipe:
                response = Popen(sys_command, shell=True, stdout=PIPE, stderr=STDOUT)
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
                if handle_error:
                    return err.output.decode('ascii', 'ignore')
            except:
                from requests import Request
                from labpack.handlers.requests import handle_requests
                request_object = Request(method='GET', url='https://www.google.com')
                request_details = handle_requests(request_object)
                self.printer('ERROR')
                raise ConnectionError(request_details['error'])
            self.printer('ERROR')
            raise
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
        self.printer('ERROR')
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
                child = pexpect.spawn('heroku login', timeout=2)
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
                    self.printer('ERROR')
                    raise Exception(login_fail)
            
    # confirm existence of subdomain
        sys_command = 'heroku ps -a %s' % self.subdomain
        heroku_response = self._handle_command(sys_command, handle_error=True)
        if heroku_response.find('find that app') > -1:
            self.printer('ERROR')
            raise Exception('%s does not exist. Try: heroku create -a %s' % (self.subdomain, self.subdomain))
        elif heroku_response.find('have access to the app') > -1:
            self.printer('ERROR')
            raise Exception('%s belongs to another account. Try: heroku login' % self.subdomain)
        elif heroku_response.find('your Heroku credentials') > -1:
            self.printer('ERROR')
            raise Exception('On Windows, you need to login to heroku using cmd.exe.\nWith cmd.exe, Try: heroku login')
       
        self.printer('done.')
        
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

    # validate dockerfile
        if not path.exists('Dockerfile'):
            raise Exception('heroku requires a Dockerfile in working directory to deploy using Docker.')

    # validate container plugin
        from os import devnull
        from subprocess import check_output
        self.printer('Checking heroku plugin requirements ... ', flush=True)
        sys_command = 'heroku plugins'
        heroku_plugins = check_output(sys_command, shell=True, stderr=open(devnull, 'wb')).decode('utf-8')
        if heroku_plugins.find('heroku-container-registry') == -1:
            self.printer('ERROR')
            raise Exception(
                'heroku container plugin required. Try: heroku plugins:install heroku-container-registry')
        self.printer('done.')
            
    # verify container login
        self.printer('Checking heroku container login ... ', flush=True)
        import pexpect
        try:
            child = pexpect.spawn('heroku container:login', timeout=2)
            child.expect('Email:\s?')
            child.sendline(self.email)
            i = child.expect([pexpect.EOF, pexpect.TIMEOUT])
            if i == 0:
                child.terminate()
            elif i == 1:
                child.terminate()
                raise Exception('Some unknown issue prevents Heroku from accepting credentials.\nTry first: heroku login')
        except Exception as err:
            self._check_connectivity(err)
        self.printer('done.')
        
    # verbosity
        self.printer('Building docker image ...')
    
    # build docker image
        sys_command = 'heroku container:push web --app %s' % self.subdomain
        heroku_response = self._handle_command(sys_command, pipe=True)

        return heroku_response

    def deploy_static(self, site_folder):

        ''' a method to deploy a static html page to heroku using php '''

        title = '%s.deploy_php' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'site_folder': site_folder
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # validate existence of static files
        from os import path
        if not path.exists(site_folder):
            raise ValueError('%s is not a valid path on localhost.' % site_folder)
        index_file = path.join(site_folder, 'index.html')
        if not path.exists(index_file):
            raise Exception('%s must contain an index.html file.' % site_folder)

    # validate container plugin
        from os import devnull
        from subprocess import check_output
        self.printer('Checking heroku plugin requirements ... ', flush=True)
        sys_command = 'heroku plugins'
        heroku_plugins = check_output(sys_command, shell=True, stderr=open(devnull, 'wb')).decode('utf-8')
        if heroku_plugins.find('heroku-builds') == -1:
            self.printer('ERROR')
            raise Exception(
                'heroku builds plugin required. Try: heroku plugins:install heroku-builds')
        self.printer('done.')
    
    # construct temporary file folder
        self.printer('Creating temporary files ... ', flush=True)
        try:
            from shutil import copytree, move
            from os import makedirs
            from time import time
            from labpack import __module__
            from labpack.storage.appdata import appdataClient
            client_kwargs = {
                'collection_name': 'TempFiles',
                'prod_name': __module__
            }
            tempfiles_client = appdataClient(**client_kwargs)
            temp_folder = path.join(tempfiles_client.collection_folder, 'heroku%s' % time())
            makedirs(temp_folder)
            site_root, site_name = path.split(path.abspath(site_folder))
            build_path = path.join(temp_folder, site_name)
            copytree(site_folder, build_path)
            index_path = path.join(build_path, 'index.html')
            home_path = path.join(build_path, 'home.html')
            compose_path = path.join(build_path, 'compose.json')
            php_path = path.join(build_path, 'index.php')
            with open(compose_path, 'wt') as f:
                f.write('{}')
                f.close()
            with open(php_path, 'wt') as f:
                f.write('<?php include_once("home.html"); ?>')
                f.close()
            move(index_path, home_path)
        except:
            self.printer('ERROR')
            raise
        self.printer('done.')
    
    # define cleanup function
        def _cleanup_temp():
            self.printer('Cleaning up temporary files ... ', flush=True)
            from shutil import rmtree
            rmtree(temp_folder, ignore_errors=True)
            self.printer('done.')
            
    # deploy site to heroku
        self.printer('Deploying %s to heroku ... ' % site_folder, flush=True)
        try:
            sys_command = 'cd %s; heroku builds:create -a %s' % (temp_folder, self.subdomain)
            self._handle_command(sys_command, pipe=True)
        except:
            self.printer('ERROR')
            _cleanup_temp()
            raise
        self.printer('Deployment complete.')
        
    # remove temporary files
        _cleanup_temp()
        
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
    