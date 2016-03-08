__author__ = 'rcj1492'
__created__ = '2016.03'

from labMgmt.commands.start import *

class testCommandsStart(object):

    def __init__(self, kwargs):
        self.kwargs = kwargs

    def unitTests(self):
        run(**self.kwargs)
        return self

if __name__ == '__main__':
    testKwargs = {'command': 'start', 'virtualbox': 'default', 'verbose': True, 'componentFile': 'lab-component.json', 'componentRoot': '$(pwd)'}
    testCommandsStart(testKwargs).unitTests()
