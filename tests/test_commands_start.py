__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.commands.start import start

class testCommandsStart(object):

    def __init__(self, kwargs):
        self.kwargs = kwargs

    def unitTests(self):
        start(**self.kwargs)
        return self

if __name__ == '__main__':
    testKwargs = {'command': 'start', 'virtualbox': 'default', 'verbose': True, 'componentFile': 'labComponent.yaml' }
    testCommandsStart(testKwargs).unitTests()
