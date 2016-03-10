__author__ = 'rcj1492'
__created__ = '2016.03'

from os import path
from pocketLab.commands.home import home

class testCommandsHome(object):

    def __init__(self, kwargs):
        self.kwargs = kwargs

    def unitTests(self):
        home(**self.kwargs)
        return self

if __name__ == '__main__':
    testKwargs = {'newPath': path.abspath('test_commands_home.py'), 'command': 'home'}
    testCommandsHome(testKwargs).unitTests()