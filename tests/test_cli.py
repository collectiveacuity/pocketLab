__author__ = 'rcj1492'
__created__ = '2016.03'

import sys
from pocketLab.cli import cli
from copy import deepcopy
from jsonmodel.validators import jsonModel
from pocketLab.commands.devtest import _cmd_kwargs_devtest

class testCli(object):

    def __init__(self):
        pass

    def command(self, sys_cmd):
        sys.argv = []
        args = sys_cmd.split()
        for arg in args:
            sys.argv.append(arg)
        return cli()

    def unitTests(self):

    # test that command works
        cmd_kwargs = self.command('lab devtest test1 test2 test3')

        original_model = jsonModel(_cmd_kwargs_devtest)
        processed_model = jsonModel(cmd_kwargs['model'])

    # test that values returned by command can be ingested by original model
        copy_kwargs = deepcopy(cmd_kwargs)
        original_ingested = original_model.ingest(**copy_kwargs)
        for key, value in cmd_kwargs.items():
            assert original_ingested[key] == value

    # test that model returned by command can ingest original schema values
        original_kwargs = deepcopy(_cmd_kwargs_devtest['schema'])
        processed_ingested = processed_model.ingest(**original_kwargs)
        original_ingested = original_model.ingest(**original_kwargs)
        for key, value in original_ingested.items():
            assert processed_ingested[key] == value

    # test that schema of original model matches processed model
        for key, value in original_model.schema.items():
            assert processed_model.schema[key] == value

    # test that components of original model match processed model
        for key, value in original_model.components.items():
            assert processed_model.components[key] == value

        del copy_kwargs['model']
        print(copy_kwargs)

    # test help menu (causes system exit)
        # self.command('lab devtest -h')

        return self

if __name__ == '__main__':
    testCli().unitTests()