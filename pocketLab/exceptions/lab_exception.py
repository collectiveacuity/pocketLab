__author__ = 'rcj1492'
__created__ = '2016.03'

import sys

class labException(Exception):

    '''
        a class for parsing exception context and reporting messages
    '''

    def __init__(self, **kwargs):
        self.error = {
            'message': '',
            'tprint': None,
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
        self.tprint = None
        self.pprint = None
        if self.error['message']:
            if isinstance(self.error['message'], str):
                self.print = self.error['message']
        if self.error['tprint']:
            if isinstance(self.error['tprint'], dict):
                t_keys = self.error['tprint'].keys()
                if not ('headers','rows') in t_keys:
                    if isinstance(self.error['tprint']['headers'], list):
                        if isinstance(self.error['tprint']['rows'], list):
                            if not self.error['tprint']['rows']:
                                self.error['tprint']['rows'] = [{}]
                            if isinstance(self.error['tprint']['rows'][0], dict):
                                from pocketLab.compilers.table_print import tablePrint
                                self.tprint =  tablePrint(self.error['tprint']['headers'], self.error['tprint']['rows'])
        if self.error['pprint']:
            self.pprint = self.error['pprint']
        text = 'Errr! %s' % self.print
        print(text)
        if self.tprint:
            print('\n%s' % self.tprint)
        if self.pprint:
            from pprint import pprint
            print('\n')
            pprint(self.pprint)
        sys.exit(2)
