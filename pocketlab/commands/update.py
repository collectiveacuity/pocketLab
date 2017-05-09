__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

_update_schema = {
    'title': 'update',
    'description': 'Updates the config files for a project with the latest pocketlab configurations.',
    'metadata': {
        'cli_help': 'updates a project\'s config files'
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
                    print(new_text)

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
        registry_list = []
        registry_results = registry_client.list(max_results=1000)
        registry_list.extend(registry_results)
        while len(registry_list) == 1000:
            registry_results = registry_client.list(max_results=1000, previous_key=registry_results[999])
            registry_list.extend(registry_results)
        for project in registry_list:
            try:
                details = registry_client.read(project)
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
    exit_msg = project_name

    return exit_msg
