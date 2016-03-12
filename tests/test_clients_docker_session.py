__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.clients.docker_session import dockerConfig
from pocketLab.clients.localhost_session import localhostSession


class testImportersDockerConfig(dockerConfig):

    def __init__(self, vbox_name=''):
        dockerConfig.__init__(self, vbox_name)

    def unitTests(self):
        return self

if __name__ == '__main__':
    testBox = ''
    if localhostSession() in ('Windows', 'Mac'):
        testBox = 'default'
    testImportersDockerConfig(testBox).unitTests()