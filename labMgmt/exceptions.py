__author__ = 'rcj1492'
__created__ = '2016.03'

import sys
from pprint import pprint

class LabException(Exception):

    def __init__(self, message='', error=None):
        text = 'Errr! %s' % message
        self.error = error
        print(text)
        # super(LabException, self).__init__(text)
        sys.exit(2)

class LabPrettyException(Exception):

    def __init__(self, message='', printout=None, error=None):
        text = 'Errr! %s' % message
        self.error = error
        print(text)
        if printout:
            pprint(printout)
        # super(LabException, self).__init__(text)
        sys.exit(2)
