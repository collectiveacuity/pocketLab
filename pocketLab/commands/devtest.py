__author__ = 'rcj1492'
__created__ = '2016.03'

_cmd_kwargs_devtest = {
    'title': 'devtest',
    'description': 'test the command structure',
    'metadata': {
        'cli_command': 'devtest',
        'cli_help': 'test the command structure'
    },
    'schema': {
        'verbose': True,
        'logging': True,
        'integer': 0,
        'float': 0.0,
        'string_a': '',
        'string_b': '',
        'required_arg': 'required',
        'list_str': [ 'e' ],
        'list_int': [ 7 ]
    },
    'components': {
        '.logging': {
            'default_value': True,
            'field_description': 'Toggle to enable/disable lab logging',
            'field_metadata': {
                'cli_flags': ['-z', '--zzz'],
                'cli_help': 'turn off lab logging (logging helps lab bot learn)'
            }
        },
        '.verbose': {
            'default_value': True,
            'field_description': 'Toggle to enable/disable lab bot messages',
            'field_metadata': {
                'cli_flags': ['-q', '--quiet'],
                'cli_help': 'turn off lab bot messages'
            }
        },
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
        '.required_arg': {
            'min_length': 1,
            'max_length': 64,
            'must_not_contain': [ '[^\w\-_]' ],
            'field_description': 'Test required argument',
            'field_metadata': {
                'cli_help': 'required argument for devtest',
                'cli_metavar': 'REQUIRED ARG'
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

def devtest(**cmd_kwargs):
    del cmd_kwargs['model']
    print(cmd_kwargs)

