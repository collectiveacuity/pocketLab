__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

_init_schema = {
    'title': 'init',
    'description': 'add lab framework files to the current directory',
    'metadata': {
        'cli_help': 'creates a lab framework in workdir'
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
            'must_not_contain': [ '[^\w\-_/]' ],
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

    '''
        a method to add lab framework files to the current directory
        
    :param container_alias: [optional] string with alias for project's docker container
    :param image_name: [optional] string with name for project's docker image
    :param vcs_service: [optional] string with name of version control service
    :return: string with success exit message
    '''

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

# import dependencies
    from os import path

# add a vcs ignore file
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

# add a lab config file
    config_path = 'lab.yaml'
    if not path.exists(config_path):
        from pocketlab import __module__
        from jsonmodel.loader import jsonLoader
        from labpack.records.settings import save_settings
        config_schema = jsonLoader(__module__, 'models/lab-config.json')
        config_model = jsonModel(config_schema)
        input_details = {}
        if container_alias:
            input_details['docker_container_alias'] = container_alias
        if image_name:
            input_details['docker_image_name'] = image_name
        config_details = config_model.ingest(**input_details)
        save_settings(config_path, config_details)

# add a data folder
    data_path = 'data'
    from os import makedirs
    if not path.exists(data_path):
        makedirs(data_path)

# add a credential folder
    cred_path = 'cred'
    notes_path = 'notes'
    if not path.exists(cred_path):
        makedirs(cred_path)
        if path.exists(notes_path):
            if path.isdir(notes_path):
                src_list = []
                dst_list = []
                from os import listdir
                from shutil import copyfile
                for file_name in listdir(notes_path):
                    file_path = path.join(notes_path, file_name)
                    if path.isfile(file_path):
                        if file_name.find('.json') > -1 or file_name.find('.yaml') > -1 or file_name.find('.yml') > -1:
                            src_list.append(file_path)
                            dst_list.append(path.join(cred_path, file_name))
                for i in range(len(src_list)):
                    copyfile(src_list[i], dst_list[i])

    msg_insert = ''
    if container_alias:
        msg_insert = ' for "%s"' % container_alias
    exit_msg = 'Lab framework%s setup in current directory.' % msg_insert

    return exit_msg

if __name__ == "__main__":
    from labpack.records.settings import load_settings
    from jsonmodel.validators import jsonModel
    config_path = '../models/lab-config.json'
    config_model = jsonModel(load_settings(config_path))
    print(config_model.ingest(**{}))