__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketlab.clients.localhost_client import localhostClient

class testClientsLocalhostClient(localhostClient):

    def __init__(self):
        localhostClient.__init__(self)

    def unitTests(self):

        os = self.os
        assert os
        username = self.username
        assert username
        ip = self.ip
        print(ip)
        data_path = self.appData('Collective Acuity', 'pocketLab')
        assert data_path
        self.os = 'Linux'
        data_path = self.appData('Collective Acuity', 'pocketLab')
        assert data_path
        self.os = 'Mac'
        data_path = self.appData('Collective Acuity', 'pocketLab')
        assert data_path

        return self

if __name__ == '__main__':
    testClientsLocalhostClient().unitTests()