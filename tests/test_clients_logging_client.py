__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.clients.logging_client import loggingClient

class testClientsLoggingClient(loggingClient):

    def __init__(self):
        loggingClient.__init__(self)

    def unitTests(self):

        from time import time
        from copy import deepcopy
        testKey = 'lab-log-unittest'
        testDetails = { 'command': 'home', 'project': 'lab', 'verbose': True }
        for type in self.ext.types:
            test_details = deepcopy(testDetails)
            test_details['type'] = type
            test_details['time'] = time()
            test_key = '%s-%s%s' % (testKey, str(test_details['time']), type)
            self.put(test_key, test_details)
            assert self.get(test_key)
            assert self.delete(test_key)
        assert not self.query(key_query=['exp-'], body_query={'dT': ['1458181175']})
        query_results = self.query(key_query=['exp-'], body_query={'dT': ['1458181174']})
        print(query_results)

        return self

if __name__ == '__main__':
    from timeit import timeit as timer
    t0 = timer()
    print(t0)
    testClientsLoggingClient().unitTests()
    t1 = timer()
    print(t1)
    print(str(t1 - t0))