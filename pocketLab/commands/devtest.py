__author__ = 'rcj1492'
__created__ = '2016.03'

_cmd_model_devtest = {
    'command': 'devtest',
    'description': 'test the command structure',
    'brief': 'test the command structure',
    'args': [
        {
            'name': 'integer',
            'default_value': 5,
            'min_value': 1,
            'max_value': 1000,
            'field_description': 'Test integer argument',
            'exclusive_group': 'A',
            'cli_flags': [ '-i', '--integer' ],
            'cli_help': 'integer argument for devtest',
            'cli_metavar': 'INT'
        },
        {
            'name': 'float',
            'default_value': 5.5,
            'min_value': 1.1,
            'max_value': 1001.1,
            'field_description': 'Test float argument',
            'exclusive_group': 'A',
            'cli_flags': [ '-f', '--float' ],
            'cli_help': 'float argument for devtest',
            'cli_metavar': 'FLOAT'
        },
        {
            'name': 'string_a',
            'default_value': 'lab',
            'min_length': 1,
            'max_length': 64,
            'must_not_contain': [ '[^\w\-_]' ],
            'field_description': 'Test string argument',
            'discrete_values': [ 'a', 'b', 'c' ],
            'exclusive_group': 'B',
            'cli_flags': [ '--string_a' ],
            'cli_help': 'string a argument for devtest',
            'cli_metavar': 'STR'
        },
        {
            'name': 'string_b',
            'default_value': 'lab',
            'min_length': 1,
            'max_length': 64,
            'must_not_contain': [ '[^\w\-_]' ],
            'field_description': 'Test string argument',
            'exclusive_group': 'B',
            'cli_flags': [ '--string_b' ],
            'cli_help': 'string b argument for devtest',
            'cli_metavar': 'STR'
        },
        {
            'name': 'required',
            'default_value': '',
            'min_length': 1,
            'max_length': 64,
            'must_not_contain': [ '[^\w\-_]' ],
            'field_description': 'Test required argument',
            'exclusive_group': '',
            'cli_flags': [ ],
            'cli_help': 'required argument for devtest',
            'cli_metavar': 'REQUIRED ARG'
        }
    ]
}

def devtest(**cmd_kwargs):
    print(cmd_kwargs)

