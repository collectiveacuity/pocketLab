__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.clients.logging_session import loggingSession

class testClientsLoggingSession(loggingSession):

    def __init__(self):
        loggingSession.__init__(self)

    def unitTests(self):

        testKwargs = { 'command': 'home', 'project': 'lab', 'verbose': True }
        self.save(**testKwargs)

        return self

if __name__ == '__main__':
    testClientsLoggingSession().unitTests()