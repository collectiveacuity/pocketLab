__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.commands.stop import stop

class testCommandsStop(object):

    def __init__(self, kwargs):
        self.kwargs = kwargs

    def unitTests(self):
        stop(**self.kwargs)
        return self

if __name__ == '__main__':
    testKwargs = {'logfile': 'project-logs', 'command': 'stop'}
    testCommandsStop(testKwargs).unitTests()