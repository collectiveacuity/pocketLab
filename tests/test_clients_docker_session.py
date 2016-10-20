__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketlab.clients.docker_session import dockerSession
from pocketlab.clients.localhost_client import localhostClient

class testClientsDockerSession(dockerSession):

    def __init__(self, kwargs, vbox_name=''):
        dockerSession.__init__(self, kwargs, vbox_name)

    def unitTests(self):
        from pprint import pprint
        self.images()
        container_list = self.ps()
        if container_list:
            settings = self.inspect(container_list[0]['NAMES'])
            synopsis = self.synopsis(settings)
            pprint(settings)
        # run_script = ''
        # self.run(run_script)
        return self

if __name__ == '__main__':
    localhost = localhostClient()
    testBox = ''
    if localhost.os in ('Windows', 'Mac'):
        testBox = 'default'
    testKwargs = {'command': 'start', 'virtualbox': 'default', 'verbose': True, 'componentFile': 'lab-component.json'}
    testClientsDockerSession(testKwargs, testBox).unitTests()