__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.clients.labbot_session import labBot

class testClientsLabbotSession(labBot):

    def __init__(self, **kwargs):
        labBot.__init__(self, **kwargs)

    def unitTests(self):

        return self

if __name__ == '__main__':
    minKwargs = { "exit": True }
    testClientsLabbotSession(**minKwargs).unitTests()