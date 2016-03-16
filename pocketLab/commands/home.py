__author__ = 'rcj1492'
__created__ = '2016.03'

_cmd_model_home = {
    'command': 'home',
    'usage': 'home [options]',
    'description': 'creates a project home in workdir',
    'brief': 'creates a project home in workdir',
    'defaults': {},
    'options': [
        {   'args': [ '-q', '--quiet' ],
            'kwargs': {
                'dest': 'verbose',
                'default': True,
                'help': 'turn off stdout lab messages',
                'action': 'store_false'
            }
        },
        {   'args': [ '-z', '--zzz' ],
            'kwargs': {
                'dest': 'labLogging',
                'default': True,
                'help': 'turn off lab logging (logging helps lab bot learn)',
                'action': 'store_false'
            }
        },
        {   'args': [ '-p', '--project' ],
            'kwargs': {
                'type': str,
                'default': '',
                'metavar': 'PROJ',
                'dest': 'project',
                'help': '(re)set PROJect home to workdir' }
        },
        {   'args': [ '--print_path' ],
            'kwargs': {
                'type': str,
                'default': '',
                'metavar': 'PROJ',
                'dest': 'print_path',
                'help': 'prints path to PROJect home' }
        }
    ]
}

def home(**kwargs):

# import dependencies
    from re import compile
    from os import path
    from pocketLab.clients.registry_session import registrySession

# handle print_path request
    print_path = kwargs['print_path']
    if print_path:
        home_path = './'
        import sys
        rS = registrySession(**kwargs)
        resource_list = rS.find(resource_name=print_path)
        if resource_list:
            if path.exists(resource_list[0]['resource_home']):
                home_path = resource_list[0]['resource_home']
        from pocketLab.handlers.success_handler import successHandler
        success = {
            'verbose': False,
            'kwargs': kwargs,
            'message': '',
            'operation': 'home.print_path',
            'outcome': 'success'
        }
        successHandler(**success)
        print(home_path)
        sys.exit()

# determine project name
    lab_logging = kwargs['labLogging']
    verbose = kwargs['verbose']
    project_name = kwargs['project']

    def nameProject(msg, lab_logging, cmd_kwargs):
        project_name = input(msg)
        space_pattern = compile('\s')
        if len(project_name) > 64:
            input_kwargs = {
                'message': 'Name for project (shorter & sweeter): ',
                'kwargs': kwargs,
                'failed_test': 'max_size',
                'error_value': project_name,
                'operation': 'input',
                'outcome': 'clarification'
            }
            input_msg = inputHandler(**input_kwargs).msg()
            project_name = nameProject(input_msg, lab_logging, cmd_kwargs)
        elif space_pattern.findall(project_name):
            input_kwargs = {
                'message': 'Name for project (without spaces): ',
                'kwargs': kwargs,
                'failed_test': 'must_not_contain',
                'error_value': project_name,
                'operation': 'input',
                'outcome': 'clarification'
            }
            input_msg = inputHandler(**input_kwargs).msg()
            project_name = nameProject(input_msg, lab_logging, cmd_kwargs)
        return project_name

# differentiate between resource options

# validate the resource value
    space_pattern = compile('\s')
    if not project_name or len(project_name) > 64 or space_pattern.findall(project_name):
        from pocketLab.handlers.input_handler import inputHandler
        input_kwargs = {
            'message': 'Name for project (short & sweet): ',
            'kwargs': kwargs,
            'operation': 'input',
            'outcome': 'input'
        }
        input_msg = inputHandler(**input_kwargs).msg()
        project_name = nameProject(input_msg, lab_logging, kwargs)

# determine project home
    project_home = path.abspath('.')

# determine project remote

# update project registry
    rS = registrySession(**kwargs)
    project_details = {
        'resource_name': project_name,
        'resource_type': 'project',
        'resource_home': project_home
    }
    rS.update(**project_details)

# add home alias to .bashrc or .bash_profile (or create)
    home_alias = "alias home='function _home(){ file_path=\"$(lab home --print_path $1)\"; cd \"$file_path\"; };_home'"


