__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.clients.registry_session import registrySession

class testClientsRegistrySession(registrySession):

    def __init__(self, **kwargs):
        registrySession.__init__(self, **kwargs)

    def unitTests(self):

        self.verbose = False
        header_list, project_list = self.list()
        assert project_list
        self.delete('unittestPlaceholder')
        self.update('unittestPlaceholder','C:\\Users\\Lab\\Test')
        assert self.details('unittestPlaceholder')
        assert self.home() == 'C:\\Users\\Lab\\Test'
        self.update('unittestPlaceholder','C:\\Users\\Lab\\New')
        self.delete('unittestPlaceholder')
        home = self.home()
        assert home
        header_list, project_list = self.list()
        assert project_list
        # print(home)
        # print(project_list)

        return self

if __name__ == '__main__':
    testKwargs = {
        'command': 'home',
        'project': 'unittest',
        'verbose': True,
        'logging': True
    }
    testClientsRegistrySession(**testKwargs).unitTests()