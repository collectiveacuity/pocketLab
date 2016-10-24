__author__ = 'rcj1492'
__created__ = '2016.03'

_home_schema = {
    'title': 'home',
    'description': 'manages the local path information for a project',
    'metadata': {
        'cli_help': 'creates a project home in workdir'
    },
    'schema': {
        'project': '',
        'print_path': '',
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
        '.project': {
            'field_description': 'Name of project to add to registry',
            'default_value': '',
            'max_length': 64,
            'must_not_contain': [ '[^\w\-_]' ],
            'field_metadata': {
                'cli_group': 'A',
                'cli_flags': [ '-p', '--project' ],
                'cli_help': '(re)set home of PROJECT to workdir',
                'cli_metavar': 'PROJ'
            }
        },
        '.print_path': {
            'field_description': 'Name of project for home alias in .bashrc',
            'default_value': '',
            'max_length': 64,
            'must_not_contain': [ '[^\w\-_]' ],
            'field_metadata': {
                'cli_group': 'A',
                'cli_flags': [ '--print_path' ],
                'cli_help': 'prints path to RESOURCE home',
                'cli_metavar': 'RESOURCE'
            }
        }
    }
}

def home(project='', print_path='', overwrite=False):

    '''
        a method to manage the local path information for a project

    :param project: [optional] string with name of project to add to registry
    :param print_path: [optional] string with name of project to retrieve local path
    :return: string with local path to project
    '''

    title = 'home'

# validate inputs
    from jsonmodel.validators import jsonModel
    input_model = jsonModel(_home_schema)
    input_fields = [ project, print_path ]
    input_names = [ 'project', 'print_path' ]
    for i in range(len(input_fields)):
        if input_fields[i]:
            object_title = '%s(%s=%s)' % (title, input_names[i], input_fields[i])
            input_model.validate(input_fields[i], '.%s' % input_names[i], object_title)

# validate requirements
    # TODO boolean algebra method to check not both inputs
    if not print_path and not project:
        raise ValueError('home command requires either a project or print_path argument.')

# resolve print path request
    if print_path:

    # construct registry client
        from os import path
        from pocketlab import __module__
        from labpack.storage.appdata import appdataClient
        registry_client = appdataClient(collection_name='Registry Data', prod_name=__module__)

    # validate project name exists in registry
        suggest_msg = 'Try running "lab home -p %s" first from its root.' % print_path
        file_name = '%s.yaml' % print_path
        filter_function = registry_client.conditionalFilter([{0:{'discrete_values':[file_name]}}])
        project_list = registry_client.list(filter_function=filter_function)
        if not file_name in project_list:
            raise ValueError('"%s" not found in the registry. %s' % (print_path, suggest_msg))

    # retrieve root path to project
        suggest_msg = 'Try running "lab home -p %s" again from its root.' % print_path
        project_details = registry_client.read(file_name)
        if not 'project_root' in project_details.keys():
            raise ValueError('Record for project "%s" has been corrupted. %s' % (print_path, suggest_msg))
        project_root = project_details['project_root']
        if not path.exists(project_root):
            raise ValueError('Path %s to project "%s" no longer exists. %s' % (print_path, print_path, suggest_msg))

    # return root path to bash command
        import sys
        exit_msg = 'Transport to "%s" underway.;%s' % (print_path, project_root)
        print(exit_msg)
        sys.exit()

# resolve project request
    if project:

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

    # construct registry client
        from pocketlab import __module__
        from labpack.storage.appdata import appdataClient
        registry_client = appdataClient(collection_name='Registry Data', prod_name=__module__)

    # validate project name is not already in registry
        file_name = '%s.yaml' % project
        filter_function = registry_client.conditionalFilter([{0:{'discrete_values':[file_name]}}])
        project_list = registry_client.list(filter_function=filter_function)
        if file_name in project_list:
            if not overwrite:
                suggest_msg = 'Add -f to overwrite.'
                raise ValueError('"%s" already exists in the registry. %s' % (project, suggest_msg))

    # add project to registry
        from os import path
        file_details = {
            'project_name': project,
            'project_root': path.abspath('./')
        }
        registry_client.create(file_name, file_details)
        exit_msg = '"%s" added to registry. To return to workdir, run "home %s"' % (project, project)
        return exit_msg

    raise ValueError('home command requires either a project or print_path argument.')



