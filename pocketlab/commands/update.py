__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

'''
update the .ignore file
update the lab.yaml file
'''

_update_schema = {
    'title': 'update',
    'description': 'Updates the config files for a project with the latest pocketlab configurations.',
    'metadata': {
        'cli_help': 'updates a project\'s config files',
        'docs_benefit': 'Updates projects to latest pocketlab configurations.'
    },
    'schema': {
        'project_name': '',
        'update_all': False,
        'verbose': False
    },
    'components': {
        '.project_name': {
            'field_description': 'Name in registry of project to update',
            'default_value': '',
            'max_length': 64,
            'must_not_contain': [ '[^\w\-_]' ],
            'field_metadata': {
                'cli_group': 'A',
                'cli_flags': [ '-p', '--project' ],
                'cli_help': 'name in registry of project to update',
                'cli_metavar': 'PROJ'
            }
        },
        '.update_all': {
            'field_description': 'Apply update to all projects in registry.',
            'default_value': False,
            'field_metadata': {
                'cli_group': 'A',
                'cli_flags': [ '-a', '--all' ],
                'cli_help': 'updates all projects in registry'
            }
        },
        '.verbose': {
            'field_description': 'Toggle to enable/disable lab messages.',
            'default_value': True,
            'field_metadata': {
                'cli_flags': [ '-q', '--quiet' ],
                'cli_help': 'turn off lab process messages'
            }
        }
    }
}

def update(project_name='', update_all=False, verbose=True):

    title = 'update'

# validate inputs
    from jsonmodel.validators import jsonModel
    input_model = jsonModel(_update_schema)
    input_map = {
        'project_name': project_name
    }
    for key, value in input_map.items():
        object_title = '%s(%s=%s)' % (title, key, str(value))
        input_model.validate(value, '.%s' % key, object_title)

# define message insert
    msg_insert = 'project'
    if project_name:
        msg_insert = 'project "%s"' % project_name

# retrieve vcs templates
    from pocketlab.methods.vcs import load_ignore
    vcs_templates = {
        'git': load_ignore(vcs='git'),
        'mercurial': load_ignore(vcs='mercurial')
    }

    def _apply_update(root_path, project_name=''):

    # construct message
        msg_insert = 'project'
        if project_name:
            msg_insert = 'project "%s"' % project_name

    # update vcs ignore
        import hashlib
        from os import path
        from pocketlab.methods.vcs import merge_ignores
        vcs_files = {
            'git': {
                'path': path.join(root_path, '.gitignore'),
                'name': '.gitignore'
            },
            'mercurial': {
                'path': path.join(root_path, '.hgignore'),
                'name': '.hgignore'
            }
        }
        for key, value in vcs_files.items():
            if path.exists(value['path']):
                old_text = open(value['path']).read()
                old_hash = hashlib.sha1(old_text.encode('utf-8')).hexdigest()
                new_text = merge_ignores(old_text, vcs_templates[key])
                new_hash = hashlib.sha1(new_text.encode('utf-8')).hexdigest()
                if old_hash != new_hash:
                    if verbose:
                        print('%s file for %s updated.' % (value['name'], msg_insert))
                    # with open(value['path'], 'rt') as f:
                    #     f.write(new_text)
                    #     f.close()

    # update lab yaml
        from pocketlab import __module__
        from jsonmodel.loader import jsonLoader
        from labpack.records.settings import save_settings, load_settings
        config_schema = jsonLoader(__module__, 'models/lab-config.json')
        config_model = jsonModel(config_schema)
        template_config = config_model.ingest(**{})
        config_path = path.join(root_path, 'lab.yaml')
        if path.exists(config_path):
            try:
                old_config = load_settings(config_path)
                template_config.update(**old_config)
                if old_config != template_config:
                    if verbose:
                        print('lab.yaml file for %s updated.' % msg_insert)
                        # save_settings(config_path, template_config)
            except:
                 print('lab.yaml file for %s is corrupted. Skipped.' % msg_insert)

# construct project list
    project_list = []

# add named project to project list
    if project_name:
        from pocketlab.methods.project import retrieve_project_root
        project_root = retrieve_project_root(project_name)
        project_details = {
            'name': project_name,
            'path': project_root
        }
        project_list.append(project_details)

# add all projects in registry to project list
    elif update_all:
        from pocketlab import __module__
        from labpack.storage.appdata import appdataClient
        registry_client = appdataClient(collection_name='Registry Data', prod_name=__module__)
        from labpack.records.settings import load_settings
        for file_path in registry_client.localhost.walk(registry_client.collection_folder):
            try:
                details = load_settings(file_path)
                project_details = {
                    'name': details['project_name'],
                    'path': details['project_root']
                }
                project_list.append(project_details)
            except:
                pass

# add local path to project list
    else:
        project_list.append({'name':'', 'path':'./'})

# apply updates
    for project in project_list:
        update_kwargs = {
            'root_path': project['path'],
            'project_name': project['name']
        }
        _apply_update(**update_kwargs)

# construct exit message
    if update_all:
        msg_insert = 'all projects'
    exit_msg = 'Configurations for %s have been updated.' % msg_insert

    return exit_msg
