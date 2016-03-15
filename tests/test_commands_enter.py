__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.commands.enter import enter

class testCommandsEnter(object):

    def __init__(self, kwargs):
        self.kwargs = kwargs

    def unitTests(self):
        enter(**self.kwargs)
        return self

if __name__ == '__main__':
    testKwargs = {'command': 'enter', 'virtualbox': 'default', 'alias': 'test' }
    testCommandsEnter(testKwargs).unitTests()