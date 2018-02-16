__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

'''
add .ignore file
add lab.yaml file
add cred & data folders
copy cred files from notes to cred
add setup.py
add docs folder
add index.md to docs folder
add <module> folder
add __init__ to <module> folder)
TODO: add --heroku as a flag to create heroku.yaml
'''

_init_details = {
    'title': 'Init',
    'description': 'Init adds a number of files to the working directory which are required for other lab processes. If not present, it will create a ```lab.yaml``` file and a ```.lab``` folder in the root directory to manage various configuration options. It will also create, if missing, ```cred/``` and ```data/``` folders to store sensitive project information outside version control along with a ```.gitignore``` (or ```.hgignore```) file to escape out standard non-VCS files.\n\nPLEASE NOTE: With the option ```--module <module_name>```, init creates instead a standard framework for publishing a python module.',
    'help': 'creates a lab framework in workdir',
    'benefit': 'Init adds the config files for other lab commands.'
}

from pocketlab.init import fields_model

def init(module_name='', vcs_service='', license_type='MIT', init_heroku=False, init_aws=False, verbose=True):

    '''
        a method to add lab framework files to the current directory
    
    :param module_name: [optional] string with name of module to create
    :param vcs_service: [optional] string with name of version control service
    :param license_type: [optional] string with name of software license type
    :param init_heroku: [optional] boolean to add heroku.yaml to .lab folder
    :param init_aws: [optional] boolean to add aws.yaml to .lab folder
    :param verbose: [optional] boolean to toggle process messages
    :return: string with success exit message
    '''

    title = 'init'

# validate inputs
    input_fields = {
        'module_name': module_name,
        'vcs_service': vcs_service,
        'license_type': license_type
    }
    for key, value in input_fields.items():
        if value:
            object_title = '%s(%s=%s)' % (title, key, str(value))
            fields_model.validate(value, '.%s' % key, object_title)

# import dependencies
    from os import path

# define printer submethod
    def _printer(file_path, node_type='file'):
        if verbose:
            from os import path
            folder, file = path.split(file_path)
            if not folder:
                folder = 'working directory'
            else:
                folder = '%s folder' % folder
            print('%s %s created in %s.' % (file, node_type, folder))

# setup module architecture
    if module_name:

    # create vcs ignore files
        import re
        from pocketlab.methods.vcs import load_ignore
        vcs_regex = re.compile('#+\s+version\scontrol\s+#+')
        git_insert = '#############  version control  ################\n.hgignore\n.hg/\ndev/\ntests_dev/'
        hg_insert = '#############  version control  ################\n\\\.git/'
        git_path = '.gitignore'
        hg_path = '.hgignore'
        if not path.exists(git_path):
            git_text = load_ignore()
            git_text = vcs_regex.sub(git_insert, git_text)
            with open(git_path, 'wt') as f:
                f.write(git_text)
                f.close()
            _printer(git_path)
        if not path.exists(hg_path):
            hg_text = load_ignore(vcs='mercurial')
            hg_text = vcs_regex.sub(hg_insert, hg_text)
            with open(hg_path, 'wt') as f:
                f.write(hg_text)
                f.close()
            _printer(hg_path)

    # create module folder
        if not path.exists(module_name):
            from os import makedirs
            makedirs(module_name)
            _printer(module_name, 'folder')

    # create init file
        init_path = path.join(module_name, '__init__.py')
        if not path.exists(init_path):
            from pocketlab.methods.config import construct_init
            init_text = construct_init(module_name)
            with open(init_path, 'wt', encoding='utf-8') as f:
                f.write(init_text)
                f.close()
            _printer(init_path)

    # create docs folders
        if not path.exists('docs'):
            from os import makedirs
            makedirs('docs')
            _printer('docs', 'folder')
        if not path.exists('docs_dev'):
            from os import makedirs
            makedirs('docs_dev')
            _printer('docs_dev', 'folder')

    # create mkdocs markdown file
        mkdocs_path = path.join('docs', 'mkdocs.md')
        if not path.exists(mkdocs_path):
            from pocketlab.methods.config import retrieve_template
            mkdocs_text = retrieve_template('models/mkdocs.md.txt')
            with open(mkdocs_path, 'wt') as f:
                f.write(mkdocs_text)
                f.close()
            _printer(mkdocs_path)

    # create roadmap markdown files
        roadmap_docs = path.join('docs', 'roadmap.md')
        roadmap_temp = path.join('docs_dev', 'roadmap.md')
        roadmap_list = [ roadmap_docs, roadmap_temp ]
        for file_path in roadmap_list:
            if not path.exists(file_path):
                from pocketlab.methods.config import retrieve_template
                roadmap_text = retrieve_template('models/roadmap.md.txt')
                with open(file_path, 'wt') as f:
                    f.write(roadmap_text)
                    f.close()
                _printer(file_path)

    # create components yaml file
        components_path = path.join('docs_dev', 'components.csv')
        if not path.exists(components_path):
            from pocketlab.methods.config import retrieve_template
            components_text = retrieve_template('models/components.csv.txt')
            with open(components_path, 'wt') as f:
                f.write(components_text)
                f.close()
            _printer(components_path)

    # create generate script file
        generate_path = path.join('docs_dev', 'generate.py')
        if not path.exists(generate_path):
            from pocketlab.methods.config import retrieve_template
            generate_text = retrieve_template('models/generate.py.txt')
            with open(generate_path, 'wt') as f:
                f.write(generate_text)
                f.close()
            _printer(generate_path)

    # create index markdown file
        index_path = path.join('docs', 'index.md')
        if not path.exists(index_path):
            from pocketlab.methods.config import construct_index
            index_text = construct_index(module_name)
            with open(index_path, 'wt') as f:
                f.write(index_text)
                f.close()
            _printer(index_path)

    # create other root files
        license_type = license_type.lower()
        from pocketlab.methods.config import construct_changes, construct_license, construct_manifest, construct_readme, construct_mkdocs, construct_setup
        module_files = {
            'CHANGES.rst': construct_changes(),
            'LICENSE.txt': construct_license(license_type),
            'MANIFEST.in': construct_manifest(module_name),
            'README.rst': construct_readme(module_name=module_name),
            'mkdocs.yml': construct_mkdocs(module_name),
            'setup.py': construct_setup(module_name)
        }
        for key, value in module_files.items():
            if not path.exists(key):
                with open(key, 'wt', encoding='utf-8') as f:
                    f.write(value)
                    f.close()
                _printer(key)

        exit_msg = 'Framework for "%s" setup in current directory.' % module_name

# setup service architecture
    else:

    # determine version control service
        if not vcs_service:
            vcs_service = 'git'
            if path.exists('.git'):
                if path.isdir('.git'):
                    vcs_service = 'git'
            elif path.exists('.hg'):
                if path.isdir('.hg'):
                    vcs_service = 'mercurial'
        else:
            vcs_service = vcs_service.lower()

    # add a vcs ignore file
        from pocketlab.methods.vcs import load_ignore
        if vcs_service == 'git':
            vcs_path = '.gitignore'
            vcs_type = 'git'
        else:
            vcs_path = '.hgignore'
            vcs_type = 'mercurial'
        if not path.exists(vcs_path):
            file_text = load_ignore(vcs=vcs_type)
            with open(vcs_path, 'wt') as f:
                f.write(file_text)
                f.close()
            _printer(vcs_path)

    # add docker ignore file
        docker_path = '.dockerignore'
        if not path.exists(docker_path):
            file_text = load_ignore(vcs='docker')
            with open(docker_path, 'wt') as f:
                f.write(file_text)
                f.close()
            _printer(docker_path)

    # add docker compose file
        config_path = 'docker-compose.yaml'
        if not path.exists(config_path):

        # retrieve config schemas
            from pocketlab import __module__
            from jsonmodel.loader import jsonLoader
            compose_schema = jsonLoader(__module__, 'models/compose-config.json')
            service_schema = jsonLoader(__module__, 'models/service-config.json')
    
        # add default values to schemas
            default_volume_1 = {'type': 'bind', 'source': './cred', 'target': '/opt/cred'}
            default_volume_2 = {'type': 'bind', 'source': './data', 'target': '/opt/data'}
            service_schema['schema']['volumes'].insert(0, default_volume_2)
            service_schema['schema']['volumes'].insert(0, default_volume_1)

        # modify config schema defaults from values in registry
            from pocketlab.methods.service import retrieve_service_name
            service_name = retrieve_service_name('./')
            if service_name:
                service_schema['schema']['image'] = service_name
            else:
                service_name = 'server'

        # compile yaml
            from pocketlab.methods.config import compile_compose
            config_text = compile_compose(compose_schema, service_schema, service_name)

        # save config text
            with open(config_path, 'wt') as f:
                f.write(config_text)
                f.close()
            _printer(config_path)

    # add lab folder
        from os import makedirs
        lab_path = '.lab'
        if not path.exists(lab_path):
            makedirs(lab_path)
            _printer(lab_path, 'folder')

    # add a data folder
        data_path = 'data'
        if not path.exists(data_path):
            makedirs(data_path)
            _printer(data_path, 'folder')

    # add a credential folder
        cred_path = 'cred'
        notes_path = 'notes'
        if not path.exists(cred_path):
            makedirs(cred_path)
            _printer(cred_path, 'folder')
            if path.exists(notes_path):
                if path.isdir(notes_path):
                    src_list = []
                    dst_list = []
                    from os import listdir
                    from shutil import copyfile
                    for file_name in listdir(notes_path):
                        file_path = path.join(notes_path, file_name)
                        if path.isfile(file_path):
                            if file_name.find('.json') > -1 or file_name.find('.yaml') > -1 or file_name.find('.yml') > -1:
                                src_list.append(file_path)
                                dst_list.append(path.join(cred_path, file_name))
                    for i in range(len(src_list)):
                        copyfile(src_list[i], dst_list[i])
                        _printer(dst_list[i])
    
    # add config files
        config_map = {
            'heroku.yaml': { 
                'toggle': init_heroku, 
                'schema_path': 'models/heroku-config.json'
            },
            'aws.yaml': {
                'toggle': init_aws,
                'schema_path': 'models/aws-config.json'
            }
        }
        for key, value in config_map.items():
            if value['toggle']:
                config_path = '.lab/%s' % key
                if not path.exists(config_path):
                    from pocketlab import __module__
                    from jsonmodel.loader import jsonLoader
                    from pocketlab.methods.config import compile_yaml
                    config_schema = jsonLoader(__module__, value['schema_path'])
                    config_text = compile_yaml(config_schema)
                    with open(config_path, 'wt') as f:
                        f.write(config_text)
                        f.close()
                    _printer(config_path)
                            
    # add readme file
        readme_path = 'README.md'
        if not path.exists(readme_path):
            from pocketlab.methods.config import construct_readme
            readme_text = construct_readme(vcs_service=vcs_service)
            with open(readme_path, 'wt', encoding='utf-8') as f:
                f.write(readme_text)
                f.close()
            _printer(readme_path)

        exit_msg = 'Lab framework setup in current directory.'

    return exit_msg

if __name__ == "__main__":

    from labpack.records.settings import load_settings
    from jsonmodel.validators import jsonModel
    config_path = '../models/lab-config.json'
    config_model = jsonModel(load_settings(config_path))
    print(config_model.ingest())
