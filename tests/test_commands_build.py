__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.commands.build import *

class testCommandsBuild(object):

    def __init__(self, kwargs):
        self.kwargs = kwargs

    def unitTests(self):
        run(**self.kwargs)
        return self

if __name__ == '__main__':
    testKwargs = {'projectFile': 'lab-project.json', 'service': 'aws', 'verbose': True, 'command': 'build'}
    testCommandsBuild(testKwargs).unitTests()