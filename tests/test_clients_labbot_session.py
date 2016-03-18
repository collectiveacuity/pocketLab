__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.clients.labbot_session import labBot

class testClientsLabbotSession(labBot):

    def __init__(self, **kwargs):
        labBot.__init__(self, **kwargs)

    def unitTests(self):

        exp_details = self.analyze()
        assert exp_details['msg'] == 'test'

        return self

if __name__ == '__main__':
    minKwargs = { 'event': 'observation', 'channel': 'terminal', 'logging': True, 'exit': True, 'msg': 'test' }
    testClientsLabbotSession(**minKwargs).unitTests()