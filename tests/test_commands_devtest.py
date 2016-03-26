__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.commands.devtest import _cmd_kwargs_devtest, devtest
from jsonmodel.validators import jsonModel
from jsonmodel.loader import jsonLoader
from pocketLab import __module__
from copy import deepcopy

if __name__ == '__main__':
    cli_file = jsonLoader(__module__, 'rules/lab-cli-model.json')
    cli_model = jsonModel(cli_file)
    kwargs_file = deepcopy(_cmd_kwargs_devtest)
    kwargs_model = jsonModel(kwargs_file)
    for key, value in kwargs_model.keyMap.items():
        rules_key = ''
        ex_int = 1
        ex_float = 1.1
        if value['value_datatype'] == True.__class__:
            rules_key = '.boolean_fields'
        elif value['value_datatype'] == ex_int.__class__:
            rules_key = '.number_fields'
        elif value['value_datatype'] == ex_float.__class__:
            rules_key = '.number_fields'
        elif value['value_datatype'] == ''.__class__:
            rules_key = '.string_fields'
        elif value['value_datatype'] == [].__class__:
            rules_key = '.list_fields'
        elif value['value_datatype'] == {}.__class__:
            rules_key = '.map_fields'
        for k, v in jsonModel.__rules__['components'][rules_key].items():
            if not k in value:
                value[k] = v
        value['field_metadata'] = cli_model.ingest(**value['field_metadata'])

    print(kwargs_model.title)
    print(kwargs_model.description)
    devtest_default = kwargs_model.ingest(**{})
    devtest(**devtest_default)