__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.clients.labbot_client import labBotClient

class testClientslabBotClient(labBotClient):

    def __init__(self, **kwargs):
        labBotClient.__init__(self, **kwargs)

    def unitTests(self):

        exp_details = self.analyze()

        return self

if __name__ == '__main__':
    testKwargs = { 'event': 'observation', 'channel': 'terminal', 'logging': False, 'exit': True, 'msg': 'test', 'verbose': True }
    testClientslabBotClient(**testKwargs).unitTests()