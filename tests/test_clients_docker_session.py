__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.clients.docker_session import dockerConfig
from pocketLab.importers.local_os import localOS


class testImportersDockerConfig(dockerConfig):

    def __init__(self, vbox_name=''):
        dockerConfig.__init__(self, vbox_name)

    def unitTests(self):
        return self

if __name__ == '__main__':
    testBox = ''
    if localOS() in ('Windows','Mac'):
        testBox = 'default'
    testImportersDockerConfig(testBox).unitTests()