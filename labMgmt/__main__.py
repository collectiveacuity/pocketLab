# -*- coding: utf-8 -*-
__author__ = 'rcj1492'
__created__ = '2016.03'

'''
labMgmt.__main__: executed when labMgmt directory is called as script.
'''

import sys
from .cli import cli
cli(sys.argv[1:])
