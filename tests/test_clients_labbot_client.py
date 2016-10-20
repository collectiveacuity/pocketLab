__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketlab import __module__
from pocketlab.clients.labbot_client import labBotClient

class testClientslabBotClient(labBotClient):

    def __init__(self, **kwargs):
        labBotClient.__init__(self, **kwargs)

    def unitTests(self):

        exp_details = self.analyze()

        return self

if __name__ == '__main__':
    from jsonmodel.loader import jsonLoader
    from jsonmodel.validators import jsonModel
    testModel = jsonModel(jsonLoader(__module__, 'rules/cmd-model.json'))
    testKwargs = { 'event': 'observation', 'interface': 'command line', 'channel': 'terminal', 'logging': False, 'exit': True, 'msg': 'test', 'verbose': True }
    testClientslabBotClient(**testKwargs).unitTests()