__author__ = 'rcj1492'
__created__ = '2016.06'
__license__ = 'MIT'

import os
from re import compile
from importlib.util import spec_from_file_location, module_from_spec
from jsonmodel.validators import jsonModel
from pocketlab.clients.localhost_client import localhostClient

class actionCompiler(localhostClient):

    def __init__(self, action_client=None):
        localhostClient.__init__(self)
        self.actions = {}
        if isinstance(action_client, actionCompiler):
            self.actions = action_client.actions
        self.map = {}

    def compileLocal(self, local_path):

    # construct list of files
        action_list = os.listdir(local_path)

    # add methods in files to actions
        for action in action_list:
            action_path = os.path.abspath(os.path.join(local_path, action))
            action_name = action.replace('.py','')
            model_name = '_model_%s' % action_name
            try:
                method_details = {
                    'channel': 'internal',
                    'interface': 'localhost',
                    'language': 'python'
                }
                spec_file = spec_from_file_location(action_name, action_path)
                action_module = module_from_spec(spec_file)
                spec_file.loader.exec_module(action_module)
                method_details['method'] = getattr(action_module, action_name)
                method_details['model'] = jsonModel(getattr(action_module, model_name))
                unique_name = '%s_%s' % (str(method_details['interface']), action_name)
                self.actions[unique_name] = method_details
                if 'example_statements' in method_details['model'].metadata.keys():
                    for statement in method_details['model'].metadata['example_statements']:
                        self.map[statement] = unique_name
            except:
                pass

        return self

    def compileJS(self, javascript_file):

    # define javascript function regex pattern
        js_pattern = compile('function\s(\w*?)\((.*?)\)')
        kwargs_pattern = compile('_kwargs')
        list_pattern = compile('_list')
        internal_pattern = compile('^_')

    # open up javascript file
        js_text = open(javascript_file).read()

    # construct a list of functions from file text
        function_list = js_pattern.findall(js_text)

    # add methods in list to actions
        for function in function_list:
            if not internal_pattern.findall(function[0]):
                try:
                    method_schema = {
                        'schema': {},
                    }
                    method_kwargs = function[1].split(', ')

                    for keyword in method_kwargs:
                        method_schema['schema'][keyword] = ''
                        if kwargs_pattern.findall(keyword):
                            method_schema['schema'][keyword] = {}
                        elif list_pattern.findall(keyword):
                            method_schema['schema'][keyword] = []
                    method_details = {
                        'channel': 'web',
                        'interface': 'browser',
                        'language': 'javascript',
                        'method': function[0],
                        'model': jsonModel(method_schema)
                    }
                    unique_name = '%s_%s' % (str(method_details['interface']), method_details['method'])
                    self.actions[unique_name] = method_details
                except:
                    pass

        return self


if __name__ == '__main__':
    from pprint import pprint
    js_file = '../../notes/lab.js'
    action_client = actionCompiler().compileJS(js_file)
    pprint(action_client.actions['browser_updateContext']['model'].schema)
    print(action_client.map)