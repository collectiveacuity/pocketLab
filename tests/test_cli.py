__author__ = 'rcj1492'
__created__ = '2016.03'

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from labMgmt.cli import cli
if __name__ == '__main__':
    cli(sys.argv[1:])