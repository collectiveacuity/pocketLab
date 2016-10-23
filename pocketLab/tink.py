__author__ = 'rcj1492'
__created__ = '2016.10'
__license__ = 'MIT'

import os
import sys
from pocketlab import __module__
from importlib.util import find_spec

def retrieve_path(root_path=''):
    if root_path:
        if not os.path.exists(root_path):
            raise ValueError('%s is not a valid path.' % root_path)
        return os.path.abspath(root_path)
    return os.path.abspath('.')

def load_model(model_path):
    from labpack.records.settings import load_settings
    from jsonmodel.validators import jsonModel
    module_path = find_spec(__module__).submodule_search_locations[0]
    model_path = os.path.join(module_path, model_path)
    project_schema = load_settings(model_path)
    model_object = jsonModel(project_schema)
    return model_object

def validate_settings(model_object, settings_dict):
    from jsonmodel.exceptions import InputValidationError
    project_settings = {}
    for key in model_object.schema.keys():
        if key in settings_dict.keys():
            object_path = '.%s' % key
            try:
                project_settings[key] = model_object.validate(settings_dict[key], object_path)
            except InputValidationError as err:
                if err.error['error_value'] == None and err.error['input_criteria']['value_datatype'] == 'map':
                    pass
                else:
                    field_name = 'Value %s for field %s' % (err.error['error_value'], err.error['input_path'][1:])
                    raise ValueError('%s in lab.yaml file is not valid.' % field_name)
    return project_settings

def register_project(root_path, override=False):

# validate path has lab file
    file_list = os.listdir(root_path)
    if not 'lab.yaml' in file_list:
        raise ValueError('%s does not contain a lab.yaml file.' % root_path)
    file_path = os.path.join(root_path, 'lab.yaml')

# validate lab file
    from labpack.records.settings import load_settings
    project_settings = load_settings(file_path)
    project_model = load_model('models/lab_project_model.json')
    project_settings = validate_settings(project_model, project_settings)
    if not 'lab_project_name' in project_settings.keys():
        raise ValueError('Registry requires a value for the lab_project_name in lab.yaml file.')

# construct client to registry
    from labpack.storage.appdata import appdataClient
    registry_client = appdataClient(collection_name='Project Registry', prod_name=__module__)

# validate project name is not already in registry
    project_list = registry_client.list()
    project_name = project_settings['lab_project_name']
    file_name = '%s.yaml' % project_name
    if file_name in project_list:
        if not override:
            raise ValueError('%s project already exists in the registry.' % project_name)

# add project to registry
    file_details = {
        'lab_project_name': project_name,
        'lab_project_root': root_path
    }
    registry_client.create(file_name, file_details)
    return '%s project added to registry.' % project_name

def change_directory(*args):

# validate args came from bash script
    if not '--print_path' in args:
        raise ValueError('Try typing home <project_name> instead.')
    elif not len(args) > 1:
        raise ValueError('Try typing home <project_name> instead.')

# construct client to registry
    from labpack.storage.appdata import appdataClient
    registry_client = appdataClient(collection_name='Project Registry', prod_name=__module__)

# validate project name exists in registry
    project_list = registry_client.list()
    project_name = args[1]
    file_name = '%s.yaml' % project_name
    if not file_name in project_list:
        raise ValueError('%s project not found in the registry.' % project_name)

# retrieve root path to project
    project_details = registry_client.read(file_name)
    if not 'lab_project_root' in project_details.keys():
        raise ValueError('Record for project %s has been corrupted.' % project_name)
    project_root = project_details['lab_project_root']
    if not os.path.exists(project_root):
        raise ValueError('Path %s to project %s no longer exists.' % (project_root, project_name))

# return root path to bash command
    exit_message = 'Transport to %s underway.;%s' % (project_name, project_root)
    print(exit_message)
    sys.exit()

def cli():
    '''
        the command line interface entry point for pocketlab methods

        method accepts the string input added to the 'lab' command in a terminal
        and determines the best guess
    :return: None
    '''

# ingest system input
    cli_args = sys.argv[1:]

# debug
    if cli_args:
        if not cli_args[0] == 'home':
            print(cli_args)

# determine override flag
    command_override = False
    if 'override' in cli_args:
        command_override = True

# construct active path
    active_path = retrieve_path()
    if cli_args:
        for token in cli_args:
            if os.path.exists(token):
                active_path = retrieve_path(token)
                break

# determine method
    if cli_args:
        confirmation_msg = ''
        if cli_args[0] == 'test':
            from labpack.records.settings import load_settings
            confirmation_msg = load_settings(cli_args[1])
        elif cli_args[0] == 'register':
            confirmation_msg = register_project(active_path, command_override)
        elif cli_args[0] == 'home':
            confirmation_msg = change_directory(*cli_args[1:])
        print(confirmation_msg)

if __name__ == '__main__':
    cli()