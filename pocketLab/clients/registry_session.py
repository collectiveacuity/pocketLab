__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab import __team__, __module__
from os import path
from pocketLab.clients.localhost_session import localhostSession

class registrySession(localhostSession):

    def __init__(self, **kwargs):

        localhostSession.__init__(self)
        self.kwargs = kwargs
        self.error = { 'kwargs': kwargs }
        self.verbose = True
        if 'verbose' in self.kwargs.keys():
            if not self.kwargs['verbose']:
                self.verbose = False

    # validate existence of module local user data folder (or create)
        self.regFolder = self.userData(org_name=__team__, prod_name=__module__)
        if not path.exists(self.regFolder):
            from os import makedirs
            makedirs(self.regFolder)

    # validate existence of local project registry (or create)
        self.regName = 'projectRegistry.yaml'
        self.regPath = path.join(self.regFolder, self.regName)
        if not path.exists(self.regPath):
            from jsonmodel.loader import jsonLoader
            registry_rules = jsonLoader(__module__, 'rules/project-registry-model.json')
            registry_details = registry_rules['schema']
            registry_details['project_list'].pop()
            with open(self.regPath, 'wb') as f:
                import yaml
                f.write(yaml.dump(registry_details).encode('utf-8'))
                f.close()
            if self.verbose:
                from pocketLab.handlers.success_handler import successHandler
                success = {
                    'verbose': self.verbose,
                    'kwargs': self.kwargs,
                    'message': '%s created in local user data.' % self.regName,
                    'operation': 'registrySession.__init__'
                }
                successHandler(**success)

    def load(self):

    # import dependencies
        from pocketLab.importers.config_file import configFile
        from pocketLab.validators.valid_file import validFile
        from jsonmodel.loader import jsonLoader
        from jsonmodel.validators import jsonModel

    # construct valid model
        self.regRules = 'rules/project-registry-model.json'
        config_model = jsonLoader(__module__, self.regRules)
        self.regModel = jsonModel(config_model)

    # ingest & validate the home registry file
        self.regDetails = configFile(self.regPath, self.kwargs)
        self.regDetails = validFile(self.regDetails, self.regModel, self.kwargs, 'home registry')

        return self

    def save(self):

    # import dependencies
        import yaml

    # save details to registry file
        with open(self.regPath, 'wb') as f:
            f.write(yaml.dump(self.regDetails).encode('utf-8'))
            f.close()

        return self

    def list(self):

    # retrieve the details from the registry
        reg_details = self.load().regDetails

    # construct header and project lists
        header_list = [ 'NAME', 'HOME', 'REMOTE' ]
        project_list = []

    # populate project list with details from registry
        for i in range(len(reg_details['project_list'])):
            project_details = {
                'NAME': reg_details['project_list'][i]['project_name'],
                'HOME': reg_details['project_list'][i]['project_home'],
                'REMOTE': reg_details['project_list'][i]['project_remote']
            }
            if reg_details['default_project'] == i:
                project_details['NAME'] += ' (default)'
            project_list.append(project_details)

    # alphabetize the list and return results
        project_list = sorted(project_list, key=lambda k: k['NAME'])

        return header_list, project_list

    def validate(self, input, valid_model):

        '''
            placeholder for upgrade to jsonmodel

        '''

        return input

    def details(self, project_name):

    # retrieve the details from the registry
        reg_details = self.load().regDetails

    # validate argument parameters
        project_name = self.validate(project_name, self.regModel.keyMap['.project_list[0].project_name'])

    # find project in index
        project_details = ''
        for project in reg_details['project_list']:
            if project_name == project['project_name']:
                project_details = project

        return project_details

    def update(self, project_name, project_home='', project_remote=''):

    # retrieve the details from the registry
        reg_details = self.load().regDetails

    # validate argument parameters
        project_name = self.validate(project_name, self.regModel.keyMap['.project_list[0].project_name'])
        if project_home:
            project_home = self.validate(project_home, self.regModel.keyMap['.project_list[0].project_home'])
        if project_remote:
            project_remote = self.validate(project_remote, self.regModel.keyMap['.project_list[0].project_remote'])

    # update project details
        for i in range(len(reg_details['project_list'])):
            if project_name == reg_details['project_list'][i]['project_name']:
                reg_details['default_project'] = i
                if project_home:
                    reg_details['project_list'][i]['project_home'] = project_home
                if project_remote:
                    reg_details['project_list'][i]['project_remote'] = project_remote
                self.regDetails = reg_details
                self.save()
                from pocketLab.handlers.success_handler import successHandler
                success = {
                    'verbose': self.verbose,
                    'kwargs': self.kwargs,
                    'message': '"%s" updated in project registry.' % project_name,
                    'operation': 'registrySession.update',
                    'outcome': 'success'
                }
                successHandler(**success)
                return self

    # add project if not there
        project_details = {
            'project_name': project_name,
            'project_home': '',
            'project_remote': ''
        }
        if project_home:
            project_details['project_home'] = project_home
        if project_remote:
            project_details['project_remote'] = project_remote
        reg_details['project_list'].append(project_details)
        reg_details['default_project'] = len(reg_details['project_list']) - 1
        self.regDetails = reg_details
        self.save()
        from pocketLab.handlers.success_handler import successHandler
        success = {
            'verbose': self.verbose,
            'kwargs': self.kwargs,
            'message': '"%s" added to project registry.' % project_name,
            'operation': 'registrySession.update'
        }
        successHandler(**success)
        return self

    def delete(self, project_name):

    # retrieve the details from the registry
        reg_details = self.load().regDetails

    # validate argument parameters
        project_name = self.validate(project_name, self.regModel.keyMap['.project_list[0].project_name'])

    # find project in index
        project_index = None
        for i in range(len(reg_details['project_list'])):
            if project_name == reg_details['project_list'][i]['project_name']:
                project_index = i

    # report non-existence of project
        if not isinstance(project_index, int):
            from pocketLab.handlers.success_handler import successHandler
            success = {
                'verbose': self.verbose,
                'kwargs': self.kwargs,
                'message': '"%s" never existed in project registry.' % project_name,
                'operation': 'registrySession.delete'
            }
            successHandler(**success)
            return self

    # delete project from index and update default
        reg_details['project_list'].pop(project_index)
        reg_details['default_project'] = 0
        self.regDetails = reg_details
        self.save()
        from pocketLab.handlers.success_handler import successHandler
        success = {
            'verbose': self.verbose,
            'kwargs': self.kwargs,
            'message': '"%s" removed from project registry.' % project_name,
            'operation': 'registrySession.remove'
        }
        successHandler(**success)
        return self

    def home(self):

    # retrieve the details from the registry
        reg_details = self.load().regDetails

    # validate entries in registry
        if not reg_details['project_list']:
            from pocketLab.exceptions.lab_exception import labException
            error = {
                'kwargs': self.kwargs,
                'message': 'Project registry is empty. Try first running: lab home',
                'error_value': 'empty_data',
                'failed_test': 'available_resource'
            }
            raise labException(**error)

    # validate that default project index is not out of range
        home_index = reg_details['default_project']
        if home_index > len(reg_details['project_list']) - 1:
            from pocketLab.exceptions.lab_exception import labException
            error = {
                'kwargs': self.kwargs,
                'message': 'Project registry has been altered oddly. Try running again: lab home',
                'error_value': 'empty_data',
                'failed_test': 'available_resource'
            }
            raise labException(**error)

    # construct home string from default project index
        home_path = reg_details['project_list'][home_index]['project_home']

        return home_path

