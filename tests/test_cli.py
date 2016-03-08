__author__ = 'rcj1492'
__created__ = '2016.03'

import sys
from labMgmt.cli import cli

class testCli(object):

    def __init__(self):
        pass

    def command(self, sys_cmd):
        sys.argv = []
        args = sys_cmd.split()
        for arg in args:
            sys.argv.append(arg)
        cli()

    def unitTests(self):
        self.command('lab stop')
        self.command('lab home')
        return self

if __name__ == '__main__':
    testCli().unitTests()