__author__ = 'rcj1492'
__created__ = '2016.03'

_cmd_details_new = {
    'command': 'new',
    'usage': 'new [options]',
    'description': 'creates a new project in workdir',
    'brief': 'creates a new project in workdir',
    'defaults': { },
    'options': [
        {   'args': [ '-q', '--quiet' ],
            'kwargs': {
                'dest': 'verbose',
                'default': True,
                'help': 'turn off setup process messages',
                'action': 'store_false'
            }
        },
        {   'args': [ '-p', '--project' ],
            'kwargs': {
                'type': str,
                'default': '',
                'metavar': 'NAME',
                'dest': 'project',
                'help': 'name of new project'
            }
        }
    ]
}

def new(**kwargs):

# import dependencies
    from re import compile
    from pocketLab import __module__, __team__
    from jsonmodel.loader import jsonLoader
    from os import path, makedirs
    from pocketLab.importers.config_file import configFile
    from pocketLab.clients.localhost_session import localhostSession
    from pocketLab.validators.config_model import configModel

# determine project name
    verbose = kwargs['verbose']
    project_name = kwargs['project']

    def nameProject(msg):
        project_name = input(msg)
        space_pattern = compile('\s')
        if len(project_name) > 64:
            project_name = nameProject('Name for project (shorter & sweeter): ')
        elif space_pattern.findall(project_name):
            project_name = nameProject('Name for project (without spaces): ')
        return project_name

    if not project_name:
        project_name = nameProject('Name for project (short & sweet): ')

# construct localhost session
    localhost = localhostSession()

# validate existence of module local user data folder (or create)
    data_path = localhost.userData(org_name=__team__, prod_name=__module__)
    if not path.exists(data_path):
        makedirs(data_path)

# validate existence of local project registry (or create)
    registry_name = 'projectRegistry.yaml'
    registry_path = path.join(data_path, registry_name)
    if path.exists(registry_path):
        registry_details = configFile(registry_path, kwargs)
        registry_details = configModel(registry_details, 'rules/lab-registry-model.json', kwargs, 'project registry')
    else:
        registry_rules = jsonLoader(__module__, 'rules/lab-registry-model.json')
        registry_details = registry_rules['schema']
        registry_details['project_list'].pop()
        with open(registry_path, 'wb') as f:
            import yaml
            f.write(yaml.dump(registry_details).encode('utf-8'))
            f.close()
        if verbose:
            print('Sweet! %s created in local user data.' % registry_name)

# check availability of namespace in project registry
    for project in registry_details['project_list']:
        if project_name == project['project_name']:
            from pocketLab.exceptions.lab_exception import labException
            from pocketLab.constructors.list_projects import listProjects
            header_list, project_list = listProjects(registry_details)
            error = {
                'kwargs': kwargs,
                'message': 'Project "%s" already exists.' % project_name,
                'tprint': { 'headers': header_list, 'rows': project_list },
                'error_value': project_name,
                'failed_test': 'available_resource'
            }
            if path.abspath('.') != path.abspath(project['project_home']):
                error['message'] += '\n\nTo change the home for "%s" to this directory, try: lab home -s %s' % (project_name, project_name)
            raise labException(**error)

# add project to project registry
    project_details = {
        'project_name': project_name,
        'project_home': path.abspath('.'),
        'project_remote': '',
    }
    registry_details['project_list'].append(project_details)
    registry_details['default_project'] = len(registry_details['project_list']) - 1
    with open(registry_path, 'wb') as f:
        import yaml
        f.write(yaml.dump(registry_details).encode('utf-8'))
        f.close()
    if verbose:
        print('Sweet! "%s" added to project registry.' % project_name)

    return True

