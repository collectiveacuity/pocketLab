__author__ = 'rcj1492'
__created__ = '2016.03'

_devtest_schema_raw = {
        'title': 'devtest',
        'description': 'test the command structure',
        'metadata': {
            'cli_help': 'test the command structure',
            'docs_benefit': 'Devtest documents command-line interface options.'
        },
        'schema': {
            'integer': 0,
            'float': 0.0,
            'string_a': '',
            'string_b': '',
            'required_arg1': 'position1',
            'required_arg2': 'position2',
            'required_arg3': 'position3',
            'list_str': [ 'e' ],
            'list_int': [ 7 ]
        },
        'components': {
            '.integer': {
                'min_value': 1,
                'max_value': 10,
                'field_description': 'Test integer argument',
                'field_metadata': {
                    'cli_flags': [ '-i', '--integer' ],
                    'cli_group': 'A',
                    'cli_help': 'integer argument for devtest',
                    'cli_metavar': 'INT'
                }
            },
            '.float': {
                'min_value': 1.1,
                'max_value': 10.1,
                'field_description': 'Test integer argument',
                'field_metadata': {
                    'cli_flags': [ '-f', '--float' ],
                    'cli_group': 'A',
                    'cli_help': 'float argument for devtest',
                    'cli_metavar': 'FLOAT'
                }
            },
            '.string_a': {
                'discrete_values': [ 'a', 'b', 'c' ],
                'field_description': 'Test string argument',
                'field_metadata': {
                    'cli_group': 'B',
                    'cli_flags': [ '--string_a' ],
                    'cli_help': 'string a argument for devtest',
                    'cli_metavar': 'STR'
                }
            },
            '.string_b': {
                'default_value': 'lab',
                'min_length': 1,
                'max_length': 64,
                'must_not_contain': [ '[^\w\-_]' ],
                'field_description': 'Test string argument',
                'field_metadata': {
                    'cli_group': 'B',
                    'cli_flags': [ '--string_b' ],
                    'cli_help': 'string b argument for devtest',
                    'cli_metavar': 'STR'
                }
            },
            '.required_arg1': {
                'min_length': 1,
                'max_length': 64,
                'must_not_contain': [ '[^\w\-_]' ],
                'field_description': 'Test required argument',
                'field_metadata': {
                    'cli_help': 'required argument for devtest',
                    'cli_metavar': 'POSITIONAL ARG 1',
                    'cli_position': 1
                }
            },
            '.required_arg2': {
                'field_description': 'Test required argument in second position',
                'field_metadata': {
                    'cli_help': 'second required argument for devtest',
                    'cli_metavar': 'POSITIONAL ARG 2',
                    'cli_position': 2
                }
            },
            '.required_arg3': {
                'field_description': 'Test required argument in third position',
                'field_metadata': {
                    'cli_help': 'third required argument for devtest',
                    'cli_metavar': 'POSITIONAL ARG 3',
                    'cli_position': 3
                }
            },
            '.list_str': {
                'required_field': False,
                'field_description': 'Test list argument',
                'field_metadata': {
                    'cli_flags': [ '--list_str' ],
                    'cli_help': 'list argument for devtest',
                    'cli_metavar': 'LIST',
                    'cli_group': 'C'
                }
            },
            '.list_str[0]': {
                'discrete_values': [ 'd', 'e', 'f' ]
            },
            '.list_int': {
                'required_field': False,
                'field_description': 'Test list argument',
                'field_metadata': {
                    'cli_help': 'list argument for devtest',
                    'cli_metavar': 'LIST',
                    'cli_group': 'C'
                }
            },
            '.list_int[0]': {
                'min_value': 1,
                'max_value': 10
            }
        }
    }

from pocketlab import __module__
from pocketlab.utils import inject_defaults
from jsonmodel.loader import jsonLoader

_default_schema_raw = jsonLoader(__module__, 'models/lab-defaults.json')
_devtest_schema = inject_defaults(_devtest_schema_raw, _default_schema_raw)

def devtest(**cmd_kwargs):
    # print(cmd_kwargs)
    return cmd_kwargs

if __name__ == '__main__':
    from pocketlab import __module__
    from pocketlab.utils import compile_argument_lists, compile_command_model
    from jsonmodel.loader import jsonLoader
    cli_schema = jsonLoader(__module__, 'models/lab-cli.json')
    devtest_model = compile_command_model(_devtest_schema, cli_schema)
    d, p, o, e = compile_argument_lists(devtest_model)





