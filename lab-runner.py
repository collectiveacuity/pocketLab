#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
Convenience wrapper for running lab management directly from source tree.
'''

import sys
from labMgmt.cli import cli

if __name__ == '__main__':
    cli(sys.argv[1:])