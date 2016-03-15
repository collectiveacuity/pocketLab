__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.clients.docker_session import dockerSession
from pocketLab.clients.localhost_session import localhostSession

class testClientsDockerSession(dockerSession):

    def __init__(self, kwargs, vbox_name=''):
        dockerSession.__init__(self, kwargs, vbox_name)

    def unitTests(self):
        self.images()
        container_list = self.ps()
        if container_list:
            self.inspect(container_list[0]['NAMES'])
        # run_script = ''
        # self.run(run_script)
        return self

if __name__ == '__main__':
    localhost = localhostSession()
    testBox = ''
    if localhost.os in ('Windows', 'Mac'):
        testBox = 'default'
    testKwargs = {'command': 'start', 'virtualbox': 'default', 'verbose': True, 'componentFile': 'lab-component.json'}
    testClientsDockerSession(testKwargs, testBox).unitTests()