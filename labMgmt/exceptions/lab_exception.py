__author__ = 'rcj1492'
__created__ = '2016.03'

import sys
from pprint import pprint

class labException(Exception):

    '''
        a class for parsing exception context and reporting messages
    '''

    def __init__(self, **kwargs):
        self.error = {
            'message': '',
            'pprint': None,
            'exception': None,
            'kwargs': None,
            'error_value': None,
            'failed_test': '',
            'thread': None
        }
        for key, value in kwargs.items():
            if key in self.error.keys():
                self.error[key] = value
        self.print = ''
        self.pprint = None
        if self.error['message']:
            if isinstance(self.error['message'], str):
                self.print = self.error['message']
        if self.error['pprint']:
            self.pprint = self.error['pprint']
        text = 'Errr! %s' % self.print
        print(text)
        if self.pprint:
            print('\n')
            pprint(self.pprint)
        sys.exit(2)
