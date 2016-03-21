__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.commands.home import home, _cmd_model_home

class testCommandsHome(object):

    def __init__(self):
        self.cmdModel = _cmd_model_home

    def unitTests(self):
        test_kwargs = {'command': 'home'}
        home(**test_kwargs)

        return self

if __name__ == '__main__':
    testCommandsHome().unitTests()