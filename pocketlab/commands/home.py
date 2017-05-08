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
        'overwrite': False,
        'project_path': ''
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
            'field_metadata': {
                'cli_group': 'A',
                'cli_flags': [ '--print' ],
                'cli_help': 'prints path to project home'
            }
        },
        '.project_path': {
            'field_description': 'Name of project to add to registry',
            'default_value': '',
            # 'max_length': 64,
            # 'must_not_contain': [ '[^\w\-_]' ],
            'field_metadata': {
                'cli_group': 'A',
                'cli_flags': [ '--path' ],
                'cli_help': 'path to project root',
                'cli_metavar': 'PATH'
            }
        },
    }
}

def home(project_name, print_path=False, project_path='', overwrite=False):

    '''
        a method to manage the local path information for a project

    :param project_name: string with name of project to add to registry
    :param print_path: [optional] boolean to retrieve local path of project from registry
    :param project_path: [optional] string with path to project root
    :param overwrite: [optional] boolean to overwrite existing project registration
    :return: string with local path to project
    '''

    title = 'home'

# validate inputs
    from jsonmodel.validators import jsonModel
    input_model = jsonModel(_home_schema)
    input_map = {
        'project_name': project_name,
        'project_path': project_path
    }
    for key, value in input_map.items():
        object_title = '%s(%s=%s)' % (title, key, str(value))
        input_model.validate(value, '.%s' % key, object_title)

# validate requirements
    # TODO boolean algebra method to check not both inputs

# resolve print path request
    if print_path:

    # retrieve project root
        from pocketlab.methods.project import retrieve_project_root
        command_context = 'Try running "lab home %s" first from its root.' % project_name
        project_root = retrieve_project_root(project_name, command_context)

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
    home_alias = "alias home='function _home(){ lab_output=\"$(lab home --print $1)\"; IFS=\";\" read -ra LINES <<< \"$lab_output\"; echo \"${LINES[0]}\"; cd \"${LINES[1]}\"; };_home'"
    config_list = [localhost_client.bash_config, localhost_client.sh_config]
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

# construct registry client
    from pocketlab import __module__
    from labpack.storage.appdata import appdataClient
    registry_client = appdataClient(collection_name='Registry Data', prod_name=__module__)

# validate project name is not already in registry
    file_name = '%s.yaml' % project_name
    filter_function = registry_client.conditional_filter([{0:{'discrete_values':[file_name]}}])
    project_list = registry_client.list(filter_function=filter_function)
    if file_name in project_list:
        if not overwrite:
            suggest_msg = 'Add -f to overwrite.'
            raise ValueError('"%s" already exists in the registry. %s' % (project_name, suggest_msg))

# add project to registry
    project_root = './'
    if project_path:
        if not path.exists(project_path):
            raise ValueError('"%s" is not a valid path.' % project_path)
        elif not path.isdir(project_path):
            raise ValueError('"%s" is not a valid directory.' % project_path)
        project_root = project_path
    file_details = {
        'project_name': project_name,
        'project_root': path.abspath(project_root)
    }
    registry_client.create(file_name, file_details)
    exit_msg = '"%s" added to registry. To return to workdir, run "home %s"' % (project_name, project_name)
    return exit_msg

if __name__ == '__main__':

# add dependencies
    try:
        import pytest
    except:
        print('pytest module required to perform unittests. try: pip install pytest')
        exit()
    from time import time
    from pocketlab import __module__
    from labpack.storage.appdata import appdataClient
    registry_client = appdataClient(collection_name='Registry Data', prod_name=__module__)
    unittest_project = 'unittest_project_name_%s' % str(time()).replace('.', '')

# test invalid name exception
    from jsonmodel.exceptions import InputValidationError
    with pytest.raises(InputValidationError):
        home('not valid')

# test new project
    assert home(unittest_project).find(unittest_project)

# test existing project exception
    with pytest.raises(ValueError):
        home(unittest_project)

# test existing project overwrite
    assert home(project_name=unittest_project, overwrite=True).find(unittest_project)
    registry_client.delete('%s.yaml' % unittest_project)

# test path option
    assert home(unittest_project, project_path='../').find(unittest_project)

# test invalid path exception
    with pytest.raises(ValueError):
        home(unittest_project, project_path='./home.py')
    registry_client.delete('%s.yaml' % unittest_project)




