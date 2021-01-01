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
    'description': 'Init adds files to the working directory which are required for lab projects.\n\nTo create a framework for a webapp project, use the option ```--flask``` for a flask service, ```--webpack``` for a client-side ES6 framework using webpack or ```--express``` for a service-side ES6 server using node.js. With the options ```--pypi```, ```--npm``` or ```--jquery```, init creates instead a standard framework for publishing a module in python, node or jquery (respectively).  The options ```--heroku```, ```--ec2``` and ```--gae``` create configuration files used by other lab processes for cloud deployment on heroku, ec2 and gae (respectively).\n\nNOTE: Init only creates files which are not already present.',
    'help': 'creates a lab framework in workdir',
    'benefit': 'Init adds the config files for other lab commands.'
}

from pocketlab.init import fields_model

def init(service_option, vcs_service='', license_type='', init_flask=False, init_webpack=False, init_express=False, init_jquery=False, init_python=False, init_node=False, init_heroku=False, init_ec2=False, init_gae=False, init_docker=False, init_aws=False, init_asg=False, verbose=True, overwrite=False):

    '''
        a method to add lab framework files to the current directory
    
    :param service_option: [optional] string with name of service in lab registry
    :param vcs_service: [optional] string with name of version control service
    :param license_type: [optional] string with name of software license type
    :param init_flask: [optional] boolean to initialize a flask service framework
    :param init_webpack: [optional] boolean to initialize a client-side webpack framework
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
    named_files = [ init_flask, init_express, init_webpack, init_jquery, init_python, init_node, init_heroku, init_ec2, init_gae, init_docker, init_asg ]
    for toggle in named_files:
        if toggle:
            named_active = True
    if named_active and not service_name:
        raise ValueError('Lab init option requires a name for the service framework.\nTry: lab init <service>')

    # handle no flags (default action)
    flags_active = False
    all_flags = [ init_aws, vcs_service, license_type ]
    all_flags.extend(named_files)
    for toggle in all_flags:
        if toggle:
            flags_active = True
            break
    if not flags_active:
        # add basic project folders
        project_folders = ['cred', 'data', 'keys', 'notes']
        for folder in project_folders:
            if not path.exists(folder):
                makedirs(folder)
                _printer(folder, 'folder')

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

    # retrieve username
    import os
    from labpack.platforms.localhost import localhostClient
    localhost_client = localhostClient()
    if localhost_client.os.sysname == 'Windows':
        username = os.environ.get('USERNAME')
    else:
        home_path = os.path.abspath(localhost_client.home)
        root_path, username = os.path.split(home_path)

    # retrieve current datetime
    from labpack.records.time import labDT
    current_datetime = labDT.new()

    # TODO retrieve latest version of each dependency from system
    
    # TODO add handlebars flag
    
    # define default documentation values
    replacement_map = {
        '<service-description>': 'A Vital Service for a Brand New Project',
        '<user-name>': username,
        'pocketlab': service_name,
        '<org-name>': username,
        '<org-title>': username,
        '<org-email>': 'user@domain.com',
        '<org-url>': '',
        '<user-email>': 'user@domain.com',
        '<creation-date>': '%s' % current_datetime.year,
        '<creation-month>': '%s.%02d' % (current_datetime.year, current_datetime.month),
        '<dependency-manifest>': 'requirements.txt'
    }
    if username == 'rcj1492':
        replacement_map['<org-name>'] = 'collectiveacuity'
        replacement_map['<org-title>'] = 'Collective Acuity'
        replacement_map['<org-email>'] = 'support@collectiveacuity.com'
        replacement_map['<org-url>'] = 'https://collectiveacuity.com'
        replacement_map['<user-email>'] = ''

    # define ignore file modification variables
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
        },
        'gcloud': {
            'type': 'deploy',
            'path': '.gcloudignore',
            'kwargs': {'vcs': 'gcloud'}
        },
        'npm': {
            'type': 'module',
            'path': '.npmignore',
            'kwargs': {'type': 'node'},
            'substitutions': {
                '#+\s+version\scontrol\s+#+': '################  version control  ################\n.hgignore\n.hg/\n.gitignore\n.git/',
                '#+\s+dev\sfiles\s+#+': '#################    dev files    #################\ndev/\ntest/\ntest_dev/\ndocs/\ndocs_dev/\n.babelrc\nwebpack.config.js\nkarma.config.js',
                '#+\s+dependencies\s+#+': '#################  dependencies   #################\n*.swp\nnpm-debug.log',
                '#+\s+unit\stesting\s+#+': '#################  unit testing   #################\ncoverage/',
                '#+\s+.gitignore\s+#+': '#################   .npmignore    #################'
            }
        }
    }

    # determine what ignore files exist
    existing_ignores = set()
    existing_vcs = set()
    for key, value in ignore_map.items():
        existing_ignores.add(key)
        if value['type'] == 'vcs':
            if path.exists(value['path']):
                existing_vcs.add(key)

    # define default variables
    init_module = False
    init_webapp = False
    platform_names = []
    creating_ignores = []

    # add gitignore to default command
    if not flags_active:
        creating_ignores.append('git')

    # handle docker message
    if init_docker:
        platform_names.append('docker')

    # define module variables
    source_path = service_name
    init_path = path.join(source_path, '__init__.py')
    module_type = 'python'
    test_folder = 'tests'
    readme_path = 'README.md'
    license_path = 'LICENSE.txt'
    replacement_map['<service-description>'] = 'A Brand New Python Module'
    if init_python:
        readme_path = 'README.rst'
        init_module = True
    if init_node:
        source_path = 'src'
        init_path = path.join(source_path, '__init__.js')
        module_type = 'node'
        test_folder = 'test'
        replacement_map['<service-description>'] = 'A Powerful Javascript Tool for NodeJS'
        replacement_map['<dependency-manifest>'] = 'package.json'
        creating_ignores.append('npm')
        init_module = True
    if init_jquery:
        source_path = 'src'
        init_path = ''
        module_type = 'node'
        test_folder = 'test'
        replacement_map['<service-description>'] = 'A Brilliant Javascript Module For The Browser'
        replacement_map['<dependency-manifest>'] = 'package.json'
        creating_ignores.append('npm')
        init_module = True

    # add module configs
    if init_module:

        # add gitignore to modules with no vcs specified
        if not vcs_service and not existing_vcs:
            creating_ignores.append('git')

        # add MIT license to modules with no license specified
        if not license_type and not path.exists(license_path):
            license_type = 'mit'

        # add dev files to vcs ignore
        dev_files_ignore = '#################    dev files    #################\ndev/\n%s_dev/' % test_folder
        ignore_map['git']['substitutions'] = { '#+\s+dev\sfiles\s+#+': dev_files_ignore }
        ignore_map['mercurial']['substitutions'] = { '#+\s+dev\sfiles\s+#+': dev_files_ignore }

        # create source folder
        if not path.exists(source_path):
            from os import makedirs
            makedirs(source_path)
            _printer(source_path, 'folder')

        # create init file
        from pocketlab.methods.config import replace_text
        if init_path and not path.exists(init_path):
            from pocketlab.methods.config import construct_init
            init_text = construct_init(module_type)
            init_text = replace_text(init_text, replacement_map=replacement_map)
            with open(init_path, 'wt', encoding='utf-8') as f:
                f.write(init_text)
                f.close()
            _printer(init_path)

        # create source file
        from pocketlab.methods.config import retrieve_template
        if module_type == 'node':
            source_file_path = path.join(source_path, '%s.js' % service_name)
            if not path.exists(source_file_path):
                if init_jquery:
                    from pocketlab.methods.config import construct_init
                    source_text = retrieve_template('models/jquery.source.js.txt')
                    init_text = construct_init(module_type)
                    init_text = replace_text(init_text, replacement_map=replacement_map)
                    source_text = init_text + '\n' + source_text
                else:
                    source_text = retrieve_template('models/node.source.js.txt')
                with open(source_file_path, 'wt', encoding='utf-8') as f:
                    f.write(source_text)
                    f.close()
                _printer(source_file_path)

        # create package json
        if module_type == 'node':
            from pocketlab.methods.node import generate_package
            package_path = 'package.json'
            if init_jquery:
                package_text = retrieve_template('models/jquery.package.json')
                dependency_text = retrieve_template('models/jquery.global.dependencies.json')
            else:
                package_text = retrieve_template('models/node.package.json')
                dependency_text = retrieve_template('models/node.global.dependencies.json')
            generate_package(package_path, package_text, dependency_text, replacement_map, _printer)

        # create readme file
        readme_text = ''
        if not path.exists(readme_path):
            if module_type == 'node':
                readme_text = retrieve_template('models/node.readme.md.txt')
                readme_text = replace_text(readme_text, replacement_map=replacement_map)
            if module_type == 'python':
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

        # create other module folders
        module_folders = [ 'docs', test_folder, 'dev', '%s_dev' % test_folder ]
        for folder in module_folders:
            if not path.exists(folder):
                from os import makedirs
                makedirs(folder)
                _printer(folder, 'folder')

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
        if module_type == 'python':

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
            roadmap_list = [roadmap_docs, roadmap_temp]
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
                test_text = test_text.replace('pocketlab', service_name)
                with open(test_path, 'wt', encoding='utf-8') as f:
                    f.write(test_text)
                    f.close()
                _printer(test_path)

        # create other root files
        from pocketlab.methods.config import construct_changes, construct_setup
        manifest_text = retrieve_template('models/python.manifest.in.txt')
        mkdocs_text = retrieve_template('models/mkdocs.yaml.txt')
        module_files = {
            'CHANGES.rst': construct_changes(),
            'MANIFEST.in': replace_text(manifest_text, replacement_map=replacement_map),
            'mkdocs.yml': replace_text(mkdocs_text, replacement_map=replacement_map),
            'setup.py': construct_setup(service_name, replacement_map['<org-name>'])
        }
        if module_type == 'node':
            module_files = {
                'CHANGELOG.md': construct_changes(module_type),
                '.coveralls.yml': retrieve_template('models/coveralls.yml.txt'),
                '.babelrc': retrieve_template('models/babelrc.txt')
            }
            if init_jquery:
                webpack_text = retrieve_template('models/jquery.webpack.config.js.txt')
                module_files['karma.config.js'] = retrieve_template('models/karma.config.js.txt')
                module_files['webpack.config.js'] = replace_text(
                    webpack_text,
                    replacement_map=replacement_map
                )
        for key, value in module_files.items():
            if not path.exists(key):
                with open(key, 'wt', encoding='utf-8') as f:
                    f.write(value)
                    f.close()
                _printer(key)

        exit_msg = 'Framework for "%s" module setup in current directory.' % service_name

    # define project variables
    app_path = ''
    app_model = ''
    if init_express:
        init_webapp = True
        replacement_map['<service-description>'] = 'A Streamlined Express Webapp'
        app_path = 'main.mjs'
        app_model = 'models/main.mjs.txt'
    if init_flask:
        init_webapp = True
        replacement_map['<service-description>'] = 'A Slick Flask Webapp'
        app_path = 'main.py'
        app_model = 'models/main.py.txt'

    # add heroku configs
    if init_heroku:
        init_docker = True

    # add gae configurations
    if init_gae:

        # add .gcloudignore
        creating_ignores.append('gcloud')

        # add requirements and app configs
        from pocketlab.methods.config import retrieve_template
        gae_files = {
            'requirements.txt': 'models/gae.requirements.txt',
            'app.yaml': 'models/gae.app.yaml.txt'
        }
        for key, value in gae_files.items():
            if not path.exists(key):
                source_text = retrieve_template(value)
                with open(key, 'wt', encoding='utf-8') as f:
                    f.write(source_text)
                    f.close()
                _printer(key)

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
        license_type = license_type.lower()
        from pocketlab.methods.config import construct_license
        license_text = construct_license(license_type, replacement_map)
        if not path.exists(license_path):
            with open(license_path, 'wt', encoding='utf-8') as f:
                f.write(license_text)
                f.close()
            _printer(license_path)

    # add project folders
    if init_webapp:

        # add gitignore to projects with no vcs specified
        if not vcs_service and not existing_vcs:
            creating_ignores.append('git')

        # add project folders
        project_folders = [ 'data', 'keys', 'scripts', 'styles', 'public' ]
        for folder in project_folders:
            if not path.exists(folder):
                makedirs(folder)
                _printer(folder, 'folder')

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

        # add framework specific project folders
        other_folders = ['src', 'views']
        if init_flask:
            other_folders = ['methods', 'html']
        for folder in other_folders:
            if not path.exists(folder):
                makedirs(folder)
                _printer(folder, 'folder')

        # add ninja/nunjucks templates to html or views
        html_path = 'html'
        if init_express:
            html_path = 'views'
        ninja_files = [ 'wrapper.html', 'header.html', 'landing.html', 'content.html', 'footer.html' ]
        for file in ninja_files:
            template_path = path.join(html_path, file)
            if not path.exists(template_path):
                from pocketlab.methods.config import retrieve_template
                model_path = path.join('models', file)
                template_text = retrieve_template(model_path)
                with open(template_path, 'wt', encoding='utf-8') as f:
                    f.write(template_text)
                    f.close()
                _printer(template_path)

        # add public folders
        public_folders = ['fonts', 'images', 'styles', 'scripts']
        for folder in public_folders:
            public_folder = path.join('public', folder)
            if not path.exists(public_folder):
                makedirs(public_folder)
                _printer(public_folder, 'folder')

        # add files to public folder
        manifest_path = path.join('public', 'manifest.json')
        model_path = 'models/site.manifest.json'
        fields_map = {}
        from pocketlab.methods.node import generate_json
        generate_json(manifest_path, model_path, fields_map, replacement_map, _printer)

        # TODO add placeholder icons to public folder

        # add main file
        if app_path and not path.exists(app_path):
            from pocketlab.methods.config import retrieve_template, replace_text
            app_text = retrieve_template(app_model)
            app_text = replace_text(app_text, replacement_map=replacement_map)
            with open(app_path, 'wt', encoding='utf-8') as f:
                f.write(app_text)
                f.close()
            _printer(app_path)

        # add package.json and gulpfile.js to express
        if init_express:

            # create package.json
            from pocketlab.methods.node import generate_package
            from pocketlab.methods.config import retrieve_template
            package_path = 'package.json'
            package_text = retrieve_template('models/express.package.json')
            dependency_text = retrieve_template('models/webpack.global.dependencies.json')
            generate_package(package_path, package_text, dependency_text, replacement_map, _printer)

            # add gulpfile
            gulp_path = 'gulpfile.js'
            if not path.exists(gulp_path):
                from pocketlab.methods.config import retrieve_template
                gulp_text = retrieve_template('models/express.gulpfile.js.txt')
                with open(gulp_path, 'wt', encoding='utf-8') as f:
                    f.write(gulp_text)
                    f.close()
                _printer(gulp_path)

        # add readme file
        readme_path = 'README.md'
        if not path.exists(readme_path):
            from pocketlab.methods.config import retrieve_template, replace_text
            readme_text = retrieve_template('models/webapp.readme.md.txt')
            if vcs_service == 'mercurial' or 'mercurial' in existing_ignores:
                replacement_map['.gitignore'] = '.hgignore'
            readme_text = replace_text(readme_text, replacement_map=replacement_map)
            with open(readme_path, 'wt', encoding='utf-8') as f:
                f.write(readme_text)
                f.close()
            _printer(readme_path)

        exit_msg = 'Framework for "%s" service setup in current directory.' % service_name

    # create webpack controller files
    if init_webpack:

        # define webpack variables
        source_paths = [ 'scripts', 'styles' ]
        replacement_map['<service-description>'] = 'A Seamless Client-Side Controller Compiled By Webpack'

        # create source and public folders
        for folder in source_paths:
            if not path.exists(folder):
                from os import makedirs
                makedirs(folder)
                _printer(folder, 'folder')
            public_path = path.join('public', folder)
            if not path.exists(public_path):
                from os import makedirs
                makedirs(public_path)
                _printer(public_path, 'folder')

        # create app script file
        from pocketlab.methods.config import replace_text, retrieve_template
        source_file_path = path.join('scripts', 'app.js')
        if not path.exists(source_file_path):
            source_text = retrieve_template('models/webpack.app.js.txt')
            source_text = replace_text(source_text, replacement_map=replacement_map)
            with open(source_file_path, 'wt', encoding='utf-8') as f:
                f.write(source_text)
                f.close()
            _printer(source_file_path)

        # create app style file
        source_file_path = path.join('styles', 'app.scss')
        if not path.exists(source_file_path):
            source_text = retrieve_template('models/webpack.app.scss.txt')
            with open(source_file_path, 'wt', encoding='utf-8') as f:
                f.write(source_text)
                f.close()
            _printer(source_file_path)

        # create package.json
        from pocketlab.methods.node import generate_package
        package_path = 'package.json'
        package_text = retrieve_template('models/webpack.package.json')
        dependency_text = retrieve_template('models/webpack.global.dependencies.json')
        generate_package(package_path, package_text, dependency_text, replacement_map, _printer)

        # create other jquery files
        webpack_text = retrieve_template('models/webpack.config.js.txt')
        jquery_files = {
            '.babelrc': retrieve_template('models/babelrc.txt'),
            'gulpfile.js': retrieve_template('models/webpack.gulpfile.js.txt'),
            'webpack.config.js': replace_text(
                webpack_text,
                replacement_map=replacement_map
            )
        }
        for key, value in jquery_files.items():
            if not path.exists(key):
                with open(key, 'wt', encoding='utf-8') as f:
                    f.write(value)
                    f.close()
                _printer(key)

        if not init_webapp:
            exit_msg = 'Framework for "%s" client-side controller setup in current directory.' % service_name

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

        # # add docker ignore file
        # creating_ignores.append('docker')

        # add dockerfile file
        # TODO determine dockerfile based upon project language
        dockerfile_path = 'Dockerfile'
        if not path.exists(dockerfile_path):
            from pocketlab.methods.config import retrieve_template, replace_text
            dockerfile_text = retrieve_template('models/flask.dockerfile.txt')
            dockerfile_text = replace_text(dockerfile_text, replacement_map=replacement_map)
            with open(dockerfile_path, 'wt') as f:
                f.write(dockerfile_text)
                f.close()
            _printer(dockerfile_path)

        # add docker documentation to README.md
        if path.exists('README.md'):
            import re
            docker_pattern = re.compile('\n##\sDockerfiles')
            readme_text = open('README.md').read()
            if not docker_pattern.findall(readme_text):
                from pocketlab.methods.config import retrieve_template
                docker_text = retrieve_template('models/docker.readme.md.txt')
                with open('README.md', 'a') as f:
                    f.write(docker_text)
                    f.close()

    # add ignore files
    if creating_ignores:
        from pocketlab.methods.vcs import load_ignore
        from pocketlab.methods.config import replace_text
        for key, value in ignore_map.items():
            if key in creating_ignores:
                if not path.exists(value['path']):
                    file_text = load_ignore(**value['kwargs'])
                    if 'substitutions' in value.keys():
                        file_text = replace_text(file_text, substitution_map=value['substitutions'])
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
