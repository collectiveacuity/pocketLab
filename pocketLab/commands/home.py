__author__ = 'rcj1492'
__created__ = '2016.03'

_home_schema = {
    'title': 'home',
    'description': 'manages the local path information for a project',
    'metadata': {
        'cli_help': 'creates a project home in workdir'
    },
    'schema': {
        'project_name': 'lab',
        'print_path': False,
        'overwrite': False
    },
    'components': {
        '.overwrite': {
            'field_description': 'Overwrite an existing project registration',
            'default_value': False,
            'field_metadata': {
                'cli_flags': [ '-f', '--force' ],
                'cli_help': 'overwrites existing project registration'
            }
        },
        '.project_name': {
            'field_description': 'Name of project to add to registry',
            'default_value': '',
            'max_length': 64,
            'must_not_contain': [ '[^\w\-_]' ],
            'field_metadata': {
                # 'cli_group': 'A',
                # 'cli_flags': [ '-p', '--project' ],
                'cli_help': 'name of project to add to registry',
                'cli_metavar': 'project'
            }
        },
        '.print_path': {
            'field_description': 'Path to project for home alias in .bashrc',
            'default_value': False,
            # 'max_length': 64,
            # 'must_not_contain': [ '[^\w\-_]' ],
            'field_metadata': {
                # 'cli_group': 'A',
                'cli_flags': [ '--print_path' ],
                'cli_help': 'prints path to project home',
                # 'cli_metavar': 'RESOURCE'
            }
        }
    }
}

def home(project_name, print_path=False, overwrite=False):

    '''
        a method to manage the local path information for a project

    :param project_name: string with name of project to add to registry
    :param print_path: [optional] boolean to retrieve local path of project from registry
    :param overwrite: [optional] boolean to overwrite existing project registration
    :return: string with local path to project
    '''

    title = 'home'

# validate inputs
    from jsonmodel.validators import jsonModel
    input_model = jsonModel(_home_schema)
    input_map = {
        'project_name': project_name
    }
    for key, value in input_map.items():
        try:
            value_name = str(value)
        except:
            value_name = value.__name__
        object_title = '%s(%s=%s)' % (title, key, value_name)
        input_model.validate(value, '.%s' % key, object_title)

# construct registry client
    from os import path
    from pocketlab import __module__
    from labpack.storage.appdata import appdataClient
    registry_client = appdataClient(collection_name='Registry Data', prod_name=__module__)

# resolve print path request
    if print_path:

    # validate project name exists in registry
        suggest_msg = 'Try running "lab home %s" first from its root.' % project_name
        file_name = '%s.yaml' % project_name
        filter_function = registry_client.conditionalFilter([{0:{'discrete_values':[file_name]}}])
        project_list = registry_client.list(filter_function=filter_function)
        if not file_name in project_list:
            raise ValueError('"%s" not found in the registry. %s' % (project_name, suggest_msg))

    # retrieve root path to project
        suggest_msg = 'Try running "lab home %s" again from its root.' % project_name
        project_details = registry_client.read(file_name)
        if not 'project_root' in project_details.keys():
            raise ValueError('Record for project "%s" has been corrupted. %s' % (project_name, suggest_msg))
        project_root = project_details['project_root']
        if not path.exists(project_root):
            raise ValueError('Path %s to project "%s" no longer exists. %s' % (project_root, project_name, suggest_msg))

    # return root path to bash command
        import sys
        exit_msg = 'Transport to "%s" underway.;%s' % (project_name, project_root)
        print(exit_msg)
        sys.exit()

# resolve project request

# validate existence of home alias
    from os import path
    from labpack.platforms.localhost import localhostClient
    localhost_client = localhostClient()
    home_alias = "alias home='function _home(){ lab_output=\"$(lab home --print_path $1)\"; IFS=\";\" read -ra LINES <<< \"$lab_output\"; echo \"${LINES[0]}\"; cd \"${LINES[1]}\"; };_home'"
    config_list = [ localhost_client.bashConfig, localhost_client.shConfig ]
    for i in range(len(config_list)):
        if config_list[i]:
            if not path.exists(config_list[i]):
                with open(config_list[i], 'wt') as f:
                    f.write('# alias for pocketlab home command\n')
                    f.write(home_alias)
                    f.close()
            else:
                import re
                home_pattern = re.compile('alias home\=')
                lab_pattern = re.compile('alias home\=\'function _home\(\)\{\slab_output')
                home_match = False
                lab_match = False
                with open(config_list[i], 'rt') as f:
                    for line in f:
                        line = line.partition('#')[0]
                        line = line.rstrip()
                        if home_pattern.findall(line):
                            home_match = True
                        if lab_pattern.findall(line):
                            lab_match = True
                if not home_match:
                    with open(config_list[i], 'a') as f:
                        f.write('\n\n# alias for pocketlab home command\n')
                        f.write(home_alias)
                        f.close()
                elif not lab_match:
                    raise ValueError('the "home" alias is being used by another program.')
                else:
                    pass
    # TODO allow declaration of different alias
    # TODO check system path for home command

# validate project name is not already in registry
    file_name = '%s.yaml' % project_name
    filter_function = registry_client.conditionalFilter([{0:{'discrete_values':[file_name]}}])
    project_list = registry_client.list(filter_function=filter_function)
    if file_name in project_list:
        if not overwrite:
            suggest_msg = 'Add -f to overwrite.'
            raise ValueError('"%s" already exists in the registry. %s' % (project_name, suggest_msg))

# add project to registry
    from os import path
    file_details = {
        'project_name': project_name,
        'project_root': path.abspath('./')
    }
    registry_client.create(file_name, file_details)
    exit_msg = '"%s" added to registry. To return to workdir, run "home %s"' % (project_name, project_name)
    return exit_msg




