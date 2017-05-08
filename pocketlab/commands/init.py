__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

_init_schema = {
    'title': 'init',
    'description': 'adds a lab framework to the current directory',
    'metadata': {
        'cli_help': 'creates a lab config file in workdir'
    },
    'schema': {
        'container_alias': '',
        'image_name': '',
        'vcs_service': ''
    },
    'components': {
        '.container_alias': {
            'field_description': 'Docker container alias to add to config',
            'default_value': '',
            'max_length': 64,
            'must_not_contain': [ '[^\w\-_]' ],
            'field_metadata': {
                # 'cli_group': 'A',
                'cli_flags': [ '--container' ],
                'cli_help': 'container alias to add to project config',
                'cli_metavar': 'ALIAS'
            }
        },
        '.image_name': {
            'field_description': 'Docker image name to add to project config',
            'default_value': '',
            'max_length': 64,
            'must_not_contain': [ '[^\w\-_]' ],
            'field_metadata': {
                # 'cli_group': 'A',
                'cli_flags': [ '--image' ],
                'cli_help': 'image name to add to project config',
                'cli_metavar': 'NAME'
            }
        },
        '.vcs_service': {
            'field_description': 'Version control system to add to framework',
            'default_value': 'git',
            'discrete_values': [ 'git', 'Git', 'mercurial', 'Mercurial' ],
            'field_metadata': {
                # 'cli_group': 'A',
                'cli_flags': [ '--vcs' ],
                'cli_help': 'VCS service to generate ignore file (default: %(default)s)',
                'cli_metavar': 'SERVICE'
            }
        }
    }
}

def init(container_alias='', image_name='', vcs_service='git'):

    title = 'init'

# validate inputs
    from jsonmodel.validators import jsonModel
    input_model = jsonModel(_init_schema)
    input_map = {
        'container_alias': container_alias,
        'image_name': image_name,
        'vcs_service': vcs_service
    }
    for key, value in input_map.items():
        object_title = '%s(%s=%s)' % (title, key, str(value))
        input_model.validate(value, '.%s' % key, object_title)

# add a vcs ignore file
    from os import path
    from pocketlab.methods.vcs import load_ignore
    vcs_path = ''
    vcs_type = ''
    if vcs_service.lower() == 'git':
        vcs_path = '.gitignore'
        vcs_type = 'git'
    elif vcs_service.lower() == 'mercurial':
        vcs_path = '.hgignore'
        vcs_type = 'mercurial'
    if vcs_path:
        if not path.exists(vcs_path):
            file_text = load_ignore(vcs=vcs_type)
            with open(vcs_path, 'wt') as f:
                f.write(file_text)
                f.close()

    exit_msg = 'Framework for "%s" setup in current directory.' % container_alias
    return exit_msg

if __name__ == "__main__":
    from labpack.records.settings import load_settings
    from jsonmodel.validators import jsonModel
    config_path = '../models/lab-config.json'
    config_model = jsonModel(load_settings(config_path))
    print(config_model.ingest(**{}))