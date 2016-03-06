__author__ = 'rcj1492'
__created__ = '2016.03'

import sys

class LabException(Exception):

    def __init__(self, message='', error=None):
        text = 'Errr! %s' % message
        self.error = error
        print(text)
        sys.exit(2)
