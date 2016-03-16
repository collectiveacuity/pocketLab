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
        self.regFolder = self.sessionData(session_name='Registry Data')
        if not path.exists(self.regFolder):
            from os import makedirs
            makedirs(self.regFolder)

    # validate existence of local project registry (or create)
        self.regName = 'labRegistry.yaml'
        self.regPath = path.join(self.regFolder, self.regName)
        if not path.exists(self.regPath):
            from jsonmodel.loader import jsonLoader
            registry_rules = jsonLoader(__module__, 'rules/lab-registry-model.json')
            registry_details = registry_rules['schema']
            registry_details['resource_list'].pop()
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
        self.regRules = 'rules/lab-registry-model.json'
        config_model = jsonLoader(__module__, self.regRules)
        self.regModel = jsonModel(config_model)

    # ingest & validate the home registry file
        self.regDetails = configFile(self.regPath, self.kwargs)
        self.regDetails = validFile(self.regDetails, self.regModel, self.kwargs, 'lab registry')

        return self

    def save(self):

    # import dependencies
        import yaml

    # save details to registry file
        with open(self.regPath, 'wb') as f:
            f.write(yaml.dump(self.regDetails).encode('utf-8'))
            f.close()

        return self

    def validate(self, input, valid_model):

        '''
            placeholder for upgrade to jsonmodel

        '''

        return input

    def find(self, resource_name='', resource_home='', resource_type='', resource_tags=None):

        '''
            a method for retrieving details of one or more resources from registry

        :param resource_name: [optional] string with name
        :param resource_home: [optional] string with path
        :param resource_type: [optional] string with valid lab resource type
        :param resource_tags: [optional] list with one or more tag strings
        :return: list of headers strings, list of matching resource dictionaries
        '''

    # retrieve the details from the registry
        self.load()

    # validate input
        if resource_name:
            resource_name = self.validate(resource_name, self.regModel.keyMap['.resource_list[0].resource_name'])
        if resource_home:
            resource_home = self.validate(resource_home, self.regModel.keyMap['.resource_list[0].resource_home'])
        if resource_type:
            resource_type = self.validate(resource_type, self.regModel.keyMap['.resource_list[0].resource_type'])
        if resource_tags:
            resource_tags = self.validate(resource_tags, self.regModel.keyMap['.resource_list[0].resource_tags'])

    # construct results list
        resource_list = []

    # populate resource list with details from registry
        for i in reversed(range(len(self.regDetails['resource_list']))):
            resource_details = self.regDetails['resource_list'][i]
            if resource_name:
                if resource_name == self.regDetails['resource_list'][i]['resource_name']:
                    resource_list = []
                    resource_list.append(resource_details)
                    return resource_list
            if resource_home:
                if resource_home != self.regDetails['resource_list'][i]['resource_home']:
                    resource_details = None
            if resource_type:
                if resource_type != self.regDetails['resource_list'][i]['resource_type']:
                    resource_details = None
            if resource_tags:
                if set(resource_tags) - set(self.regDetails['resource_list'][i]['resource_tags']):
                    resource_details = None
            if resource_details:
                resource_list.append(resource_details)

    # alphabetize the list and return results
        resource_list = sorted(resource_list, key=lambda k: k['resource_name'])

        return resource_list

    def update(self, resource_name, resource_type, **kwargs):

        '''
            a method for updating a resource entry in the registry

        :param resource_name: string with unique name of resource
        :param resource_name: string with valid lab resource type
        :param kwargs: keywords with resource details properties
        :return: True
        '''

    # retrieve the details from the registry
        self.load()

    # validate required argument
        resource_details = {
            'resource_name': self.validate(resource_name, self.regModel.keyMap['.resource_list[0].resource_name']),
            'resource_type': self.validate(resource_type, self.regModel.keyMap['.resource_list[0].resource_type'])
        }

    # ingest and validate keyword arguments
        for key, value in kwargs.items():
            if key in self.regModel.schema['resource_list'][0].keys():
                component_key = '.resource_list[0].%s' % key
                resource_details[key] = self.validate(value, self.regModel.keyMap[component_key])

    # update project details
        for i in reversed(range(len(self.regDetails['resource_list']))):
            if resource_name == self.regDetails['resource_list'][i]['resource_name']:
                for k, v in resource_details.items():
                    self.regDetails['resource_list'][i][k] = v
                self.regDetails['default_resource'] = i
                self.save()
                from pocketLab.handlers.success_handler import successHandler
                success = {
                    'verbose': self.verbose,
                    'kwargs': self.kwargs,
                    'message': '"%s" updated in lab registry.' % resource_name,
                    'operation': 'registrySession.update',
                    'outcome': 'success'
                }
                successHandler(**success)
                return self

    # add project if not there
        new_details = {
            'resource_name': resource_name,
            'resource_home': '',
            'resource_remote': '',
            'resource_tags': [],
            'resource_type': resource_type
        }
        for key, value in resource_details.items():
            new_details[key] = value
        self.regDetails['resource_list'].append(new_details)
        self.regDetails['default_resource'] = len(self.regDetails['resource_list']) - 1
        self.save()
        from pocketLab.handlers.success_handler import successHandler
        success = {
            'verbose': self.verbose,
            'kwargs': self.kwargs,
            'message': '"%s" added to lab registry.' % resource_name,
            'operation': 'registrySession.update'
        }
        successHandler(**success)
        return self

    def delete(self, resource_name):

    # retrieve the details from the registry
        self.load()

    # validate input
        resource_name = self.validate(resource_name, self.regModel.keyMap['.resource_list[0].resource_name'])

    # find project in index
        resource_index = None
        for i in reversed(range(len(self.regDetails['resource_list']))):
            if resource_name == self.regDetails['resource_list'][i]['resource_name']:
                resource_index = i

    # report non-existence of resource
        if not isinstance(resource_index, int):
            from pocketLab.handlers.success_handler import successHandler
            success = {
                'verbose': self.verbose,
                'kwargs': self.kwargs,
                'message': '"%s" never existed in lab registry.' % resource_name,
                'operation': 'registrySession.delete'
            }
            successHandler(**success)
            return self

    # delete project from index and update default
        self.regDetails['resource_list'].pop(resource_index)
        if self.regDetails['default_resource'] == resource_index:
            self.regDetails['default_resource'] = 0
        self.save()
        from pocketLab.handlers.success_handler import successHandler
        success = {
            'verbose': self.verbose,
            'kwargs': self.kwargs,
            'message': '"%s" removed from lab registry.' % resource_name,
            'operation': 'registrySession.remove'
        }
        successHandler(**success)
        return self

    def default(self):

    # retrieve the details from the registry
        self.load()

    # validate entries in registry
        if not self.regDetails['resource_list']:
            from pocketLab.exceptions.lab_exception import labException
            error = {
                'kwargs': self.kwargs,
                'message': 'Lab registry is empty. Try first running: lab home',
                'error_value': self.regDetails['resource_list'],
                'failed_test': 'min_size'
            }
            raise labException(**error)

    # validate that default project index is not out of range
        home_index = self.regDetails['default_resource']
        if home_index > len(self.regDetails['resource_list']) - 1:
            from pocketLab.exceptions.lab_exception import labException
            error = {
                'kwargs': self.kwargs,
                'message': 'Lab registry has been altered oddly. Try running again: lab home',
                'error_value': home_index,
                'failed_test': 'max_size'
            }
            raise labException(**error)

    # construct default details from registry
        default_details = self.regDetails['resource_list'][home_index]

        return default_details

