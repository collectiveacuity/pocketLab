__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

'''
update the .ignore file
update the lab.yaml file
TODO: update the setup.py file
TODO: check dependencies and alert new versions
'''

_update_details = {
    'title': 'Update',
    'description': 'Updates the config files for a project with the latest pocketlab configurations.',
    'help': 'updates the config files for a project',
    'benefit': 'Updates projects to latest pocketlab configurations.'
}

from pocketlab.init import fields_model

def update(project_list, all=False, verbose=True):

    title = 'update'

# validate inputs
    if isinstance(project_list, str):
        if project_list:
            project_list = [project_list]
    input_map = {
        'project_list': project_list
    }
    for key, value in input_map.items():
        if value:
            object_title = '%s(%s=%s)' % (title, key, str(value))
            fields_model.validate(value, '.%s' % key, object_title)

# define message insert
    msg_insert = 'project'

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
        from jsonmodel.validators import jsonModel
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
    update_list = []

# add named project to project list
    if project_list:
        msg_insert = ''
        for i in range(len(project_list)):
            project = project_list[i]
            if msg_insert:
                if i + 1 == len(project_list):
                    msg_insert += ' and '
                else:
                    msg_insert += ', '
            msg_insert += '"%s"' % project
            from pocketlab.methods.project import retrieve_project_root
            project_root = retrieve_project_root(project)
            project_details = {
                'name': project,
                'path': project_root
            }
            update_list.append(project_details)

# add all projects in registry to project list
    elif all:
        msg_insert = 'all projects'
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
                update_list.append(project_details)
            except:
                pass

# add local path to project list
    else:
        update_list.append({'name':'', 'path':'./'})

# apply updates
    for project in update_list:
        update_kwargs = {
            'root_path': project['path'],
            'project_name': project['name']
        }
        _apply_update(**update_kwargs)

# construct exit message
    exit_msg = 'Configurations for %s have been updated.' % msg_insert

    return exit_msg
