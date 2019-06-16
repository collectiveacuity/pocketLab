__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

'''
update the .ignore file
update the docker-compose.yaml file
update the setup.py file
TODO: check dependencies and alert new versions
'''

_update_details = {
    'title': 'Update',
    'description': 'Updates the configuration files for a service. When a package and platform are specified, update adds (or updates) the service to the configuration files for the package on the platform. Otherwise, update only updates the local configuration files for a service with the latest pocketlab configurations.',
    'help': 'updates the config files for a service',
    'benefit': 'Keeps your services up-to-date with the latest configurations.'
}

from pocketlab.init import fields_model

def update(package_option, platform_option, service_option, environ_type='', region_name='', resource_tags='', print_terminal='', all_services=False, verbose=True):

    title = 'update'
    
    # ingest service option
    if isinstance(service_option, str):
        if service_option:
            service_option = [service_option]
    if isinstance(package_option, str):
        if package_option:
            package_option = [package_option]
    if isinstance(platform_option, str):
        if platform_option:
            platform_option = [platform_option]

    # validate inputs
    input_fields = {
        'package_option': package_option,
        'service_option': service_option,
        'platform_option': platform_option,
        'environ_type': environ_type,
        'region_name': region_name,
        'resource_tags': resource_tags
    }
    for key, value in input_fields.items():
        if value:
            object_title = '%s(%s=%s)' % (title, key, str(value))
            fields_model.validate(value, '.%s' % key, object_title)

    # validate package and platform
    local_update = False
    if package_option and not platform_option:
        raise ValueError('Update requires a platform if the package option is specified.')
    elif platform_option and not package_option:
        raise ValueError('Update requires a package if the platform option is specified.')
    elif not platform_option and not package_option:
        local_update = True

    # determine service name
    service_name = ''
    service_list = []
    if service_option:
        service_list = service_option
        service_name = service_option[0]
    platform_name = ''
    if platform_option:
        platform_name = platform_option[0]
    package_name = ''
    if package_option:
        package_name = package_option[0]

    # handle local configuration updates
    if local_update:

        # define test ignore
        def _test_ignore(text):
            import re
            lab_test = re.findall('\\?\.lab', text)
            node_test = re.findall('\nnode_modules/', text)
            if lab_test:
                return 'service'
            elif node_test:
                return 'node'
            return 'python'

        # define update process
        def _apply_update(root_path, service_name=''):
    
        # construct message
            from os import path
            msg_insert = 'local service'
            if service_name:
                msg_insert = 'service "%s"' % service_name
            setup_path = path.join(root_path, 'setup.py')
            if path.exists(setup_path):
                msg_insert = msg_insert.replace('service', 'module')
    
        # update vcs ignore
            import hashlib
            from pocketlab.methods.vcs import load_ignore
            from pocketlab.methods.vcs import merge_ignores
            vcs_files = {
                'git': {
                    'path': path.join(root_path, '.gitignore'),
                    'name': '.gitignore',
                    'vcs': 'git'
                },
                'mercurial': {
                    'path': path.join(root_path, '.hgignore'),
                    'name': '.hgignore',
                    'vcs': 'mercurial'
                },
                'npm': {
                    'path': path.join(root_path, '.npmignore'),
                    'name': '.npmignore',
                    'vcs': 'git'
                },
                'docker': {
                    'path': path.join(root_path, '.dockerignore'),
                    'name': '.dockerignore',
                    'vcs': 'docker'
                }
            }
            for key, value in vcs_files.items():
                if path.exists(value['path']):
                    old_text = open(value['path']).read()
                    old_hash = hashlib.sha1(old_text.encode('utf-8')).hexdigest()
                    ignore_type = _test_ignore(old_text)
                    template_text = load_ignore(vcs=value['vcs'], type=ignore_type)
                    new_text = merge_ignores(old_text, template_text)
                    new_hash = hashlib.sha1(new_text.encode('utf-8')).hexdigest()
                    if old_hash != new_hash:
                        with open(value['path'], 'wt') as f:
                            f.write(new_text)
                            f.close()
                        if verbose:
                            print('%s file for %s updated.' % (value['name'], msg_insert))
    
        # update setup.py
            setup_path = path.join(root_path, 'setup.py')
            if path.exists(setup_path):
                from pocketlab.methods.config import update_setup
                old_text = open(setup_path).read()
                old_hash = hashlib.sha1(old_text.encode('utf-8')).hexdigest()
                new_text = update_setup(old_text, root_path)
                new_hash = hashlib.sha1(new_text.encode('utf-8')).hexdigest()
                if old_hash != new_hash:
                    with open(setup_path, 'wt', encoding='utf-8') as f:
                        f.write(new_text)
                        f.close()
                    if verbose:
                        print('setup.py file for %s updated.' % msg_insert)

        # construct update list
        from pocketlab.methods.service import retrieve_services
        update_list, msg_insert = retrieve_services(service_list, all_services)

        # apply updates
        for service in update_list:
            update_kwargs = {
                'root_path': service['path'],
                'service_name': service['name']
            }
            _apply_update(**update_kwargs)

        # modify service to module
        if msg_insert.find('local service') > -1:
            from os import path
            if path.exists('./setup.py'):
                msg_insert = msg_insert.replace('local service', 'local module')

    # handle remote package configuration update
    else:

        # construct path to service root
        from pocketlab.methods.service import retrieve_service_root
        if service_name:
            service_insert = '"%s"' % service_name
            service_root = retrieve_service_root(service_name)
        else:
            service_insert = 'in working directory'
            service_root = './'

        # retrieve service configurations
        from pocketlab.methods.service import retrieve_service_config
        service_title = '%s %s %s' % (title, package_name, platform_name)
        service_config, service_name = retrieve_service_config(service_root, service_name, service_title)

        # TODO handle update sequence

        print(service_config)
        msg_insert = '%s on %s with service %s' % (package_name, platform_name, service_insert)

    # construct exit message
    exit_msg = 'Configurations for %s have been updated.' % msg_insert
        
    return exit_msg
