__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.commands.home import home, _cmd_model_home

class testCommandsHome(object):

    def __init__(self):
        self.cmdModel = _cmd_model_home

    def unitTests(self):
        from timeit import timeit as timer
        t0 = timer()
        test_kwargs = {
            'verbose': True,
            'logging': False,
            'command': 'home',
            'print_path': 'unittest',
            'project': ''
        }
        home(**test_kwargs)
        t1 = timer()
        print(str(t1 - t0))
        return self

if __name__ == '__main__':
    testCommandsHome().unitTests()