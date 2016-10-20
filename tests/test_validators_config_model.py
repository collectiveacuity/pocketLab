__author__ = 'rcj1492'
__created__ = '2016.03'

import json
from pocketlab.validators.config_model import configModel

class testValidatorsConfigModel(object):

    def __init__(self, config_details, model_file, kwargs, title=''):
        self.configDetails = config_details
        self.modelFile = model_file
        self.kwargs = kwargs
        self.title=''
        if title:
            self.title = title

    def unitTests(self):

        assert configModel(self.configDetails, self.modelFile, self.kwargs, self.title)

        return self

if __name__ == '__main__':
    json_file = '../pocketLab/rules/lab-component-model.json'
    model_details = json.loads(open(json_file).read())['schema']
    model_file = 'rules/lab-component-model.json'
    minKwargs = { 'event': 'observation', 'channel': 'terminal', 'logging': True, 'exit': True, 'msg': 'test' }
    testValidatorsConfigModel(model_details, model_file, minKwargs, 'unittest').unitTests()