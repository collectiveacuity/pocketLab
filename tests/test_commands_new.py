__author__ = 'rcj1492'
__created__ = '2016.03'

from dev.commands.new import new

class testCommandsNew(object):

    def __init__(self, kwargs):
        self.kwargs = kwargs

    def unitTests(self):
        new(**self.kwargs)
        return self

if __name__ == '__main__':
    testKwargs = {'command': 'new', 'project': 'test'}
    testCommandsNew(testKwargs).unitTests()