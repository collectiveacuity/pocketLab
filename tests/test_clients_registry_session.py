__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.clients.registry_session import registrySession

class testClientsRegistrySession(registrySession):

    def __init__(self, **kwargs):
        registrySession.__init__(self, **kwargs)

    def unitTests(self):

        self.verbose = True
        resource_details = {
            'resource_name': 'unittestPlaceholder',
            'resource_type': 'project',
            'resource_home': 'C:\\Users\\Lab\\Test'
        }
        self.delete(resource_details['resource_name'])
        self.update(**resource_details)
        assert self.find(resource_details['resource_name'])
        assert self.default()['resource_home'] == 'C:\\Users\\Lab\\Test'
        resource_details['resource_home'] = 'C:\\Users\\Lab\\New'
        resource_details['resource_tags'] = [ 'unittestPlaceholder' ]
        self.update(**resource_details)
        home = self.default()
        assert home
        resource_list = self.find(resource_tags=['unittestPlaceholder'])
        assert resource_list
        self.delete(resource_details['resource_name'])
        print(home)
        print(resource_list)

        return self

if __name__ == '__main__':
    testKwargs = {
        'command': 'home',
        'project': 'unittestPlaceholder',
        'verbose': True,
        'labLogging': True,
        'print_path': ''
    }
    testClientsRegistrySession(**testKwargs).unitTests()