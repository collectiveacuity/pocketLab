__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.compilers.args_model import argsModel
from jsonmodel.loader import jsonLoader
from jsonmodel.validators import jsonModel
from pocketLab.commands.home import _cmd_model_home

if __name__ == '__main__':
    test_file = jsonLoader('pocketLab', 'rules/lab-command-model.json')
    test_model = jsonModel(test_file)
    home_model = test_model.ingest(**_cmd_model_home)
    args_file = argsModel(home_model)
    args_model = jsonModel(args_file)
    assert args_model
    print(args_model.components)