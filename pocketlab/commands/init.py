__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

'''
add .ignore file
add docker-compose.yaml file
add cred & data folders
copy cred files from notes to cred
add setup.py
add docs folder
add index.md to docs folder
add <module> folder
add __init__ to <module> folder
add .lab folders
add --heroku as a flag to create heroku.yaml .lab
add --aws as a flag to create aws.yaml in .lab
'''

_init_details = {
    'title': 'Init',
    'description': 'Init adds files to the working directory which are required for lab projects.\n\nBy default, init creates a framework for a flask service. Additional options can be selected to produce frameworks for other types of services, such as ```--jquery``` for a client-side ES6 framework using webpack and ```--express``` for a service-side ES6 framework using node.js. With the options ```--pypi``` (or ```--npm```), init creates instead a standard framework for publishing a python (or node) module and other stuff.  The options ```--heroku```, ```--ec2``` and ```--gae``` create configuration files used by other lab processes for cloud deployment on heroku, ec2 and gae (respectively).\n\nNOTE: Init only creates files which are not already present.',
    'help': 'creates a lab framework in workdir',
    'benefit': 'Init adds the config files for other lab commands.'
}

from pocketlab.init import fields_model

def init(service_option, vcs_service='', license_type='', init_flask=False, init_express=False, init_jquery=False, init_python=False, init_node=False, init_heroku=False, init_ec2=False, init_gae=False, init_docker=False, init_aws=False, init_asg=False, verbose=True, overwrite=False):

    '''
        a method to add lab framework files to the current directory
    
    :param service_option: [optional] string with name of service in lab registry
    :param vcs_service: [optional] string with name of version control service
    :param license_type: [optional] string with name of software license type
    :param init_flask: [optional] boolean to initialize a flask service framework
    :param init_express: [optional] boolean to initialize an express service framework
    :param init_jquery: [optional] boolean to initialize a jquery-webpack service framework
    :param init_python: [optional] boolean to initialize a python module framework
    :param init_node: [optional] boolean to initialize a node module framework
    :param init_heroku: [optional] boolean to add heroku deploy configs
    :param init_ec2: [optional] boolean to add ec2 deploy configs to working directory
    :param init_gae [optional] boolean to add gae deploy configs to working directory
    :param init_docker [optional] boolean to add .docker-compose.yaml to working directory
    :param init_aws: [optional] boolean to add aws.yaml to .lab folder
    :param init_asg: [optional] boolean to add asg.yaml to working directory
    :param verbose: [optional] boolean to toggle process messages
    :param overwrite: [optional] boolean to overwrite existing service registration
    :return: string with success exit message
    '''

    title = 'init'

# ingest service option
    if isinstance(service_option, str):
        if service_option:
            service_option = [service_option]

# validate inputs
    input_fields = {
        'service_option': service_option,
        'vcs_service': vcs_service,
        'license_type': license_type
    }
    for key, value in input_fields.items():
        if value:
            object_title = '%s(%s=%s)' % (title, key, str(value))
            fields_model.validate(value, '.%s' % key, object_title)

    # determine service name
    service_name = ''
    if service_option:
        service_name = service_option[0]
    if not service_name:
        from pocketlab.methods.service import retrieve_service_name
        service_name = retrieve_service_name('./')

    # import dependencies
    exit_msg = ''
    from os import path, makedirs
    from pocketlab import __module__
    from jsonmodel.loader import jsonLoader

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

    # handle service name requirement
    named_active = False
    named_files = [ init_flask, init_express, init_jquery, init_python, init_node, init_heroku, init_ec2, init_gae, init_docker, init_asg ]
    for toggle in named_files:
        if toggle:
            named_active = True
    if named_active and not service_name:
        raise ValueError('Lab init option requires a name for the service framework.\nTry: lab init <service>')

    # retrieve username
    import os
    from labpack.platforms.localhost import localhostClient
    localhost_client = localhostClient()
    if localhost_client.os.sysname == 'Windows':
        username = os.environ.get('USERNAME')
    else:
        home_path = os.path.abspath(localhost_client.home)
        root_path, username = os.path.split(home_path)

    # create service name if specified
    if service_name:

        # construct registry client
        from labpack.storage.appdata import appdataClient
        registry_client = appdataClient(collection_name='Registry Data', prod_name=__module__)

        # validate service name is not already associated with a different service in registry
        file_name = '%s.yaml' % service_name
        filter_function = registry_client.conditional_filter([{0: {'discrete_values': [file_name]}}])
        service_list = registry_client.list(filter_function=filter_function)
        if not file_name in service_list:
            from pocketlab.commands.home import home
            home(service_name)
        else:
            from labpack.compilers.encoding import decode_data
            service_details = decode_data(file_name, registry_client.load(file_name))
            if service_details['service_root'] != path.abspath('./'):
                from pocketlab.commands.home import home
                home(service_name, overwrite=overwrite)

    # define default documentation values
    replacement_map = {
        '<service-description>': 'A Vital Service for a Brand New Project',
        '<user-name>': username,
        'pocketlab': service_name,
        '<org-name>': username,
        '<org-title>': username,
        '<org-email>': 'user@domain.com',
        '<org-url>': '',
        '<user-email>': 'user@domain.com'
    }
    if username == 'rcj1492':
        replacement_map['<org-name>'] = 'collectiveacuity'
        replacement_map['<org-title>'] = 'Collective Acuity'
        replacement_map['<org-email>'] = 'support@collectiveacuity.com'
        replacement_map['<org-url>'] = 'https://collectiveacuity.com'
        replacement_map['<user-email>'] = ''

    # determine if ignore files exist
    ignore_map = {
        'git': {
            'type': 'vcs',
            'path': '.gitignore',
            'kwargs': {'vcs': 'git'}
        },
        'mercurial': {
            'type': 'vcs',
            'path': '.hgignore',
            'kwargs': {'vcs': 'mercurial'}
        },
        'docker': {
            'type': 'deploy',
            'path': '.dockerignore',
            'kwargs': {'vcs': 'docker'}
        }
    }
    existing_ignores = set()
    for key, value in ignore_map.items():
        if value['type'] == 'vcs':
            if path.exists(value['path']):
                existing_ignores.add(key) 

    # define default variables
    init_project = False
    platform_names = []
    creating_ignores = []

    # handle docker message
    if init_docker:
        platform_names.append('docker')

    # handle module inits
    if init_python:
        pass
    if init_node:
        pass

    # handle project inits
    if init_jquery:
        pass
    if init_express:
        init_project = True
    if init_flask:
        init_project = True

    # add heroku configs
    if init_heroku:
        init_docker = True

    # TODO add gae configs
    if init_gae:
        pass

    # add ec2 configurations
    if init_ec2:
    
        init_docker = True
        init_aws = True

        config_path = 'ec2.yaml'
        if not path.exists(config_path):
            # compile ec2 config text and save
            from pocketlab.methods.aws import generate_ec2
            config_text = generate_ec2(service_name)
            with open(config_path, 'wt') as f:
                f.write(config_text)
                f.close()
            _printer(config_path)
            platform_names.append('ec2')

    # add asg configurations
    if init_asg:
    
        init_docker = True
        init_aws = True

        config_path = 'asg.yaml'
        if not path.exists(config_path):

            # compile schema
            from pocketlab.methods.aws import compile_schema
            asg_schema = compile_schema('models/asg-config.json')

            # compile asg text
            from pocketlab.methods.config import compile_yaml
            asg_text = compile_yaml(asg_schema)
            from labpack.records.time import labDT
            new_dt = labDT.new()
            dt_string = str(new_dt.date()).replace('-', '')
            asg_text = asg_text.replace('generate-date', dt_string)

            # compile ec2 text
            from pocketlab.methods.aws import generate_ec2
            ec2_text = generate_ec2(service_name)
            ec2_lines = ec2_text.splitlines(keepends=True)
            ec2_splice = []
            for i in range(len(ec2_lines)):
                if i != 1:
                    ec2_splice.append(ec2_lines[i])
            ec2_text = ''.join(ec2_splice)

            # merge yaml
            config_text = asg_text.replace("ec2:\n", 'ec2: ' + ec2_text.replace('\n', '\n  '))
            with open(config_path, 'wt') as f:
                f.write(config_text)
                f.close()
            _printer(config_path)
            platform_names.append('asg')

    # add cloud access configurations
    if init_aws or init_heroku:

        # add .lab folder
        lab_path = '.lab'
        if not path.exists(lab_path):
            makedirs(lab_path)
            _printer(lab_path, 'folder')

        # add config files
        config_map = {
            'heroku.yaml': {
                'toggle': init_heroku,
                'name': 'heroku',
                'schema_path': 'models/heroku-config.json'
            },
            'aws.yaml': {
                'toggle': init_aws,
                'name': 'aws',
                'schema_path': 'models/aws-config.json'
            }
        }
        for key, value in config_map.items():
            if value['toggle']:
                config_path = '.lab/%s' % key
                if not path.exists(config_path):
                    from pocketlab.methods.config import compile_yaml
                    config_schema = jsonLoader(__module__, value['schema_path'])
                    config_text = compile_yaml(config_schema)
                    with open(config_path, 'wt') as f:
                        f.write(config_text)
                        f.close()
                    _printer(config_path)
                    platform_names.append(value['name'])

    # add vcs type to ignore files
    if vcs_service:
        creating_ignores.append(vcs_service.lower())

    # add a license file
    if license_type:
        pass

    # add project folders
    if init_project:

        # add gitignore to projects with no vcs specified
        if not vcs_service and existing_ignores - {'git'} == 0:
            creating_ignores.append('git')

        # add a data folder
        data_path = 'data'
        if not path.exists(data_path):
            makedirs(data_path)
            _printer(data_path, 'folder')

        # add a keys folder
        data_path = 'keys'
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
                            if file_name.find('.json') > -1 or file_name.find('.yaml') > -1 or file_name.find(
                                    '.yml') > -1:
                                src_list.append(file_path)
                                dst_list.append(path.join(cred_path, file_name))
                    for i in range(len(src_list)):
                        copyfile(src_list[i], dst_list[i])
                        _printer(dst_list[i])

        # add readme file
        readme_path = 'README.md'
        if not path.exists(readme_path):
            from pocketlab.methods.config import retrieve_template, replace_text
            readme_text = retrieve_template('models/service.readme.md.txt')
            if vcs_service == 'mercurial' or 'mercurial' in existing_ignores:
                replacement_map['.gitignore'] = '.hgignore'
            readme_text = replace_text(readme_text, replacement_map=replacement_map)
            with open(readme_path, 'wt', encoding='utf-8') as f:
                f.write(readme_text)
                f.close()
            _printer(readme_path)

        exit_msg = 'Framework for "%s" service setup in current directory.' % service_name

    # setup module architecture
        if init_python or init_node or init_jquery or init_express:

        # determine module variables
            from pocketlab.methods.vcs import load_ignore
            from pocketlab.methods.config import replace_text, retrieve_template
            module_type = 'python'
            test_folder = 'tests'
            readme_path = 'README.rst'
            if init_node or init_jquery:
                module_type = 'node'
                test_folder = 'test'
                readme_path = 'README.md'

        # customize replacement map
            if init_python:
                replacement_map['<service-description>'] = 'A Brand New Python Module'
            elif init_jquery:
                replacement_map['<service-description>'] = 'A Brilliant Javascript Module For The Browser'
            elif init_node:
                replacement_map['<service-description>'] = 'A Powerful Javascript Tool for NodeJS'

        # define substitution maps
            gitignore_subsitutions = {
                '#+\s+version\scontrol\s+#+': '################  version control  ################\n.hgignore\n.hg/',
                '#+\s+dev\sfiles\s+#+': '#################    dev files    #################\ndev/\n%s_dev/' % test_folder
            }
            hgignore_subsitutions = {
                '#+\s+version\scontrol\s+#+': '################  version control  ################\n\\\.git/'
            }
            npmignore_substitions = {
                '#+\s+version\scontrol\s+#+': '################  version control  ################\n.hgignore\n.hg/\n.gitignore\n.git/',
                '#+\s+dev\sfiles\s+#+': '#################    dev files    #################\ndev/\ntest/\ntest_dev/\ndocs/\ndocs_dev/\n.babelrc\nwebpack.config.js\nkarma.config.js',
                '#+\s+dependencies\s+#+': '#################  dependencies   #################\n*.swp\nnpm-debug.log',
                '#+\s+unit\stesting\s+#+': '#################  unit testing   #################\ncoverage/',
                '#+\s+.gitignore\s+#+': '#################   .npmignore    #################'
            }

        # create .gitignore file
            git_path = '.gitignore'
            if not path.exists(git_path):
                git_text = load_ignore(type=module_type)
                git_text = replace_text(git_text, substitution_map=gitignore_subsitutions)
                with open(git_path, 'wt') as f:
                    f.write(git_text)
                    f.close()
                _printer(git_path)

        # create .hgignore file
            hg_path = '.hgignore'
            if not path.exists(hg_path):
                hg_text = load_ignore(vcs='mercurial', type=module_type)
                hg_text = replace_text(hg_text, substitution_map=hgignore_subsitutions)
                with open(hg_path, 'wt') as f:
                    f.write(hg_text)
                    f.close()
                _printer(hg_path)

        # create .npmignore file
            npm_path = '.npmignore'
            if module_type == 'node' and not path.exists(npm_path):
                npm_text = load_ignore(type=module_type)
                npm_text = replace_text(npm_text, substitution_map=npmignore_substitions)
                with open(npm_path, 'wt') as f:
                    f.write(npm_text)
                    f.close()
                _printer(npm_path)

        # create source folder
            source_path = service_name
            if module_type == 'node':
                source_path = 'src'
            if not path.exists(source_path):
                from os import makedirs
                makedirs(source_path)
                _printer(source_path, 'folder')

        # create init file
            init_path = path.join(source_path, '__init__.py')
            if init_node:
                init_path = path.join(source_path, '__init__.js')
            elif init_jquery:
                init_path = ''
            if init_path and not path.exists(init_path):
                from pocketlab.methods.config import construct_init
                init_text = construct_init(module_type)
                init_text = replace_text(init_text, replacement_map=replacement_map)
                with open(init_path, 'wt', encoding='utf-8') as f:
                    f.write(init_text)
                    f.close()
                _printer(init_path)

        # create source file
            if module_type == 'node':
                source_path = path.join(source_path, '%s.js' % service_name)
                if not path.exists(source_path):
                    if init_jquery:
                        from pocketlab.methods.config import construct_init
                        source_text = retrieve_template('models/jquery.source.js.txt')
                        init_text = construct_init(module_type)
                        init_text = replace_text(init_text, replacement_map=replacement_map)
                        source_text = init_text + '\n' + source_text
                    else:
                        source_text = retrieve_template('models/node.source.js.txt')
                    with open(source_path, 'wt', encoding='utf-8') as f:
                        f.write(source_text)
                        f.close()
                    _printer(source_path)

        # create package json
            if module_type == 'node':
                package_path = 'package.json'
                if not path.exists(package_path):
                    if init_jquery:
                        package_text = retrieve_template('models/jquery.package.json')
                        dependency_text = retrieve_template('models/jquery.global.dependencies.json')
                    else:
                        package_text = retrieve_template('models/node.package.json')
                        dependency_text = retrieve_template('models/node.global.dependencies.json')
                    import json
                    replacement_map['<global-dependencies>'] = ''
                    replacement_map['<local-dependencies>'] = ''
                    package_text = replace_text(package_text, replacement_map=replacement_map)
                    package_json = json.loads(package_text)
                    package_local = package_json['devDependencies']
                    package_global = json.loads(dependency_text)
                    for key in package_local.keys():
                        if replacement_map['<local-dependencies>']:
                            replacement_map['<local-dependencies>'] += ' '
                        replacement_map['<local-dependencies>'] += key
                    for key, value in package_global.items():
                        if replacement_map['<global-dependencies>']:
                            replacement_map['<global-dependencies>'] += ' '
                        replacement_map['<global-dependencies>'] += key
                        package_json['devDependencies'][key] = value
                    package_text = json.dumps(package_json, indent=2)
                    with open(package_path, 'wt', encoding='utf-8') as f:
                        f.write(package_text)
                        f.close()
                    _printer(package_path)

        # create readme file
            readme_text = ''
            if not path.exists(readme_path):
                if module_type == 'node':
                    readme_text = retrieve_template('models/node.readme.md.txt')
                    readme_text = replace_text(readme_text, replacement_map=replacement_map)
                elif init_python:
                    highlight_text = ''
                    for i in range(len(service_name)):
                        highlight_text += '='
                    sub_rst = {
                        '\n=*?\npocketlab.*?=\n': '\n%s\n%s\n%s\n' % (highlight_text, service_name, highlight_text)
                    }
                    readme_text = retrieve_template('models/python.readme.rst.txt')
                    readme_text = replace_text(
                        readme_text, 
                        substitution_map=sub_rst, 
                        replacement_map=replacement_map
                    )
                with open(readme_path, 'wt', encoding='utf-8') as f:
                    f.write(readme_text)
                    f.close()
                _printer(readme_path)

        # create docs folders
            if not path.exists('docs'):
                from os import makedirs
                makedirs('docs')
                _printer('docs', 'folder')

        # create test folder
            if not path.exists(test_folder):
                from os import makedirs
                makedirs(test_folder)
                _printer(test_folder, 'folder')

        # create docsify files
            if module_type == 'node':
                index_path = path.join('docs', 'index.html')
                if not path.exists(index_path):
                    index_text = retrieve_template('models/docsify.index.html.txt')
                    with open(index_path, 'wt') as f:
                        f.write(index_text)
                        f.close()
                    _printer(index_path)
                jekyll_path = path.join('docs', '.nojekyll')
                if not path.exists(jekyll_path):
                    with open(jekyll_path, 'wt') as f:
                        f.write('')
                        f.close()
                    _printer(jekyll_path)
                readme_path = path.join('docs', 'README.md')
                if readme_text and not path.exists(readme_path):
                    with open(readme_path, 'wt') as f:
                        f.write(readme_text)
                        f.close()
                    _printer(readme_path)

        # create mkdocs files
            else:
            # create docs dev folder
                if not path.exists('docs_dev'):
                    from os import makedirs
                    makedirs('docs_dev')
                    _printer('docs_dev', 'folder')

            # create mkdocs markdown file
                mkdocs_path = path.join('docs', 'mkdocs.md')
                if not path.exists(mkdocs_path):
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
                        roadmap_text = retrieve_template('models/mkdocs.roadmap.md.txt')
                        with open(file_path, 'wt') as f:
                            f.write(roadmap_text)
                            f.close()
                        _printer(file_path)
        
            # create components yaml file
                components_path = path.join('docs_dev', 'components.csv')
                if not path.exists(components_path):
                    components_text = retrieve_template('models/mkdocs.components.csv.txt')
                    with open(components_path, 'wt') as f:
                        f.write(components_text)
                        f.close()
                    _printer(components_path)
        
            # create generate script file
                generate_path = path.join('docs_dev', 'generate.py')
                if not path.exists(generate_path):
                    generate_text = retrieve_template('models/mkdocs.generate.py.txt')
                    with open(generate_path, 'wt') as f:
                        f.write(generate_text)
                        f.close()
                    _printer(generate_path)

            # create index markdown file
                index_path = path.join('docs', 'index.md')
                if not path.exists(index_path):
                    index_text = retrieve_template('models/mkdocs.index.md.txt')
                    index_text = replace_text(index_text, replacement_map=replacement_map)
                    with open(index_path, 'wt') as f:
                        f.write(index_text)
                        f.close()
                    _printer(index_path)

        # create test files
            if module_type == 'node':
                test_path = path.join('test', '%s-spec.js' % service_name)
                if not path.exists(test_path):
                    test_text = retrieve_template('models/node.spec.js.txt')
                    test_text= test_text.replace('pocketlab', service_name)
                    with open(test_path, 'wt', encoding='utf-8') as f:
                        f.write(test_text)
                        f.close()
                    _printer(test_path)

        # create other root files
            license_type = license_type.lower()
            from pocketlab.methods.config import construct_changes, construct_license, construct_setup
            if module_type == 'node':
                module_files = {
                    'CHANGELOG.md': construct_changes(module_type),
                    'LICENSE.txt': construct_license(license_type, replacement_map),
                    '.coveralls.yml': retrieve_template('models/coveralls.yml.txt'),
                    '.babelrc': retrieve_template('models/babelrc.txt')
                }
                if init_jquery:
                    webpack_text = retrieve_template('models/webpack.config.js.txt')
                    module_files['karma.config.js'] = retrieve_template('models/karma.config.js.txt')
                    module_files['webpack.config.js'] = replace_text(
                        webpack_text,
                        replacement_map=replacement_map
                    )
            else:
                manifest_text = retrieve_template('models/python.manifest.in.txt')
                mkdocs_text = retrieve_template('models/mkdocs.yaml.txt')
                module_files = {
                    'CHANGES.rst': construct_changes(),
                    'LICENSE.txt': construct_license(license_type, replacement_map),
                    'MANIFEST.in': replace_text(manifest_text, replacement_map=replacement_map),
                    'mkdocs.yml': replace_text(mkdocs_text, replacement_map=replacement_map),
                    'setup.py': construct_setup(service_name, replacement_map['<org-name>'])
                }
            for key, value in module_files.items():
                if not path.exists(key):
                    with open(key, 'wt', encoding='utf-8') as f:
                        f.write(value)
                        f.close()
                    _printer(key)
    
            exit_msg = 'Framework for "%s" module setup in current directory.' % service_name

    # add docker configs
    if init_docker:

        # add docker compose file
        config_path = 'docker-compose.yaml'
        config_alt = 'docker-compose.yml'
        if not path.exists(config_path) and not path.exists(config_alt):

            # retrieve config schemas
            compose_schema = jsonLoader(__module__, 'models/compose-config.json')
            service_schema = jsonLoader(__module__, 'models/service-config.json')
            service_schema['schema']['image'] = service_name

            # add cred, data and keys folders to volumes
            if path.exists('keys/'):
                default_volume_3 = {'type': 'bind', 'source': './keys', 'target': '/opt/keys'}
                service_schema['schema']['volumes'].insert(0, default_volume_3)
            if path.exists('data/'):
                default_volume_2 = {'type': 'bind', 'source': './data', 'target': '/opt/data'}
                service_schema['schema']['volumes'].insert(0, default_volume_2)
            if path.exists('cred/'):
                default_volume_1 = {'type': 'bind', 'source': './cred', 'target': '/opt/cred'}
                service_schema['schema']['volumes'].insert(0, default_volume_1)

            # compile yaml
            from pocketlab.methods.config import compile_compose
            config_text = compile_compose(compose_schema, service_schema, service_name)

            # save config text
            with open(config_path, 'wt') as f:
                f.write(config_text)
                f.close()
            _printer(config_path)

        # add docker ignore file
        creating_ignores.append('docker')

        # add dockerfile file
        # TODO determine dockerfile based upon project language
        dockerfile_path = 'Dockerfile'
        if not path.exists(dockerfile_path):
            from pocketlab.methods.config import retrieve_template, replace_text
            dockerfile_text = retrieve_template('models/dockerfile.flask.txt')
            dockerfile_text = replace_text(dockerfile_text, replacement_map=replacement_map)
            with open(dockerfile_path, 'wt') as f:
                f.write(dockerfile_text)
                f.close()
            _printer(dockerfile_path)

    # add ignore files
    if creating_ignores:
        from pocketlab.methods.vcs import load_ignore
        for key, value in ignore_map.items():
            if key in creating_ignores:
                if not path.exists(value['path']):
                    file_text = load_ignore(**value['kwargs'])
                    with open(value['path'], 'wt') as f:
                        f.write(file_text)
                        f.close()
                    _printer(value['path'])

    # generate message for non service creation
    if not exit_msg:
        from labpack.parsing.grammar import join_words
        platform_insert = join_words(platform_names)
        platform_plural = ''
        if len(platform_names) > -1:
            platform_plural = 's'
        exit_msg = 'Configuration file%s for %s added to working directory.' % (platform_plural, platform_insert)

    return exit_msg

if __name__ == "__main__":

    from labpack.records.settings import load_settings
    from jsonmodel.validators import jsonModel
    config_path = '../models/service-config.json'
    config_model = jsonModel(load_settings(config_path))
    print(config_model.ingest())
