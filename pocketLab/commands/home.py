__author__ = 'rcj1492'
__created__ = '2016.03'

_home = {
    'title': 'home',
    'description': 'creates a resource home in workdir',
    'metadata': {
        'cli_help': 'creates a resource home in workdir'
    },
    'schema': {
        'project': '',
        'print_path': ''
    },
    'components': {
        '.project': {
            'field_description': 'Name of project',
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
            'field_description': 'Name of resource for home alias in .bashrc',
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

def home(**cmd_kwargs):
    print(cmd_kwargs)

# def home(**cmd_kwargs):
#
# # import dependencies
#     from time import time
#     from os import path
#     from pocketlab.clients.registry_client import registryClient
#     from pocketlab.clients.labbot_client import labBotClient
#
# # construct lab bot input from cmd kwargs
#     lab_kwargs = {
#         'kwargs': cmd_kwargs,
#         'logging': cmd_kwargs['logging'],
#         'verbose': cmd_kwargs['verbose'],
#         'event': 'observation',
#         'interface': 'command line',
#         'channel': 'terminal',
#         'dT': time()
#     }
#
# # resolve print path request
#     if cmd_kwargs['print_path']:
#         import sys
#         rS = registryClient()
#         resource_details = rS.describe(resource_name=cmd_kwargs['print_path'])
#         home_path = './'
#         lab_kwargs['verbose'] = False
#         lab_kwargs['exit'] = False
#         lab_kwargs['operation'] = 'home %s' % cmd_kwargs['print_path']
#         lab_kwargs['outcome'] = 'error'
#
# # handle possible print path request outcomes
#         if not resource_details:
#             lab_kwargs['msg'] = '"%s" not found in registry. Try running "lab home" first from its root.' % cmd_kwargs['print_path'],
#         else:
#             if not 'resource_home' in resource_details:
#                 lab_kwargs['msg'] = 'Record for "%s" has been corrupted. Try running "lab home" again from its root.' % cmd_kwargs['print_path']
#             else:
#                 if not path.exists(resource_details['resource_home']):
#                     lab_kwargs['msg'] = 'Path %s to "%s" no longer exists. Try running "lab home" again from its root.' % (resource_details['resource_home'], cmd_kwargs['print_path'])
#                 else:
#                     lab_kwargs['msg'] = 'Transport to "%s" underway.' % cmd_kwargs['print_path']
#                     lab_kwargs['outcome'] = 'success'
#                     home_path = resource_details['resource_home']
#         lab_exp = labBotClient(**lab_kwargs).analyze()
#         exit_message = '%s;%s' % (lab_exp['msg'], home_path)
#         print(exit_message)
#         sys.exit()
#
# # resolve project home request
#     if not cmd_kwargs['project']:
#         from copy import deepcopy
#         copy_lab_kwargs = deepcopy(lab_kwargs)
#         copy_lab_kwargs['outcome'] = 'input'
#         copy_lab_kwargs['exit'] = False
#         copy_lab_kwargs['msg'] = 'Name of project (short & sweet)'
#         cmd_kwargs['project'] = labBotClient(**copy_lab_kwargs).analyze()
#
# # define recursive input method to obtain project name
#     def ingest_project_name(lab_kwargs, args_model):
#         from jsonmodel.validators import jsonModel
#         from jsonmodel.exceptions import InputValidationError
#         cmd_model = jsonModel(args_model)
#         try:
#             project_name = cmd_model.validate(lab_kwargs['kwargs']['project'], '.project')
#             return project_name
#         except InputValidationError as err:
#             from copy import deepcopy
#             copy_lab_kwargs = deepcopy(lab_kwargs)
#             copy_lab_kwargs['outcome'] = 'input'
#             copy_lab_kwargs['exit'] = False
#             copy_lab_kwargs['error_report'] = err.error
#             copy_lab_kwargs['msg'] = cmd_model.components['.project']['field_description']
#             project_name = labBotClient(**copy_lab_kwargs).analyze()
#             lab_kwargs['kwargs']['project'] = project_name
#             return ingest_project_name(lab_kwargs, args_model)
#
# # determine project name
#     from pocketlab.compilers.args_model import argsModel
#     args_model = argsModel(cmd_kwargs['model'])
#     project_name = ingest_project_name(lab_kwargs, args_model)
#
# # determine project home
#     project_home = path.abspath('.')
#
# # determine project remote
#
# # update project registry
#     rS = registryClient()
#     project_details = {
#         'resource_name': project_name,
#         'resource_type': 'project',
#         'resource_home': project_home,
#         'resource_tags': [ project_name ]
#     }
#     rS.add(project_details)
#
# # log & report success
#     lab_kwargs['msg'] = 'Project "%s" added to lab registry. To return to workdir run: home %s' % (project_name, project_name)
#     lab_kwargs['outcome'] = 'success'
#     lab_kwargs['exit'] = False
#     labBotClient(**lab_kwargs).analyze()
#
# # add home alias to .bashrc or .bash_profile (or create)
#     home_alias = "alias home='function _home(){ lab_output=\"$(lab home --print_path $1)\"; IFS=\";\" read -ra LINES <<< \"$lab_output\"; echo \"${LINES[0]}\"; cd \"${LINES[1]}\"; };_home'"


