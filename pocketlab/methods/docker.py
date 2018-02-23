__author__ = 'rcj1492'
__created__ = '2018.02'
__license__ = 'MIT'

def compile_run_kwargs(service_config, service_repo, service_alias, service_tag, service_path, system_envvar):

    from os import path

    run_kwargs = {
        'image_name': service_repo, 
        'container_alias': service_alias, 
        'image_tag': service_tag, 
        'environmental_variables': system_envvar,
        'mapped_ports': None, 
        'mounted_volumes': None, 
        'start_command': '', 
        'network_name': 'host'
    }

# add optional compose variables
    if 'environment' in service_config.keys():
        for key, value in service_config['environment'].items():
            if key.upper() not in run_kwargs['environmental_variables'].keys():
                run_kwargs['environmental_variables'][key] = value
    if 'ports' in service_config.keys():
        run_kwargs['mapped_ports'] = {}
        for port in service_config['ports']:
            port_split = port.split(':')
            sys_port = port_split[0]
            con_port = port_split[1]
            run_kwargs['mapped_ports'][sys_port] = con_port
    if 'volumes' in service_config.keys():
        run_kwargs['mounted_volumes'] = {}
        for volume in service_config['volumes']:
            if volume['type'] == 'bind':
                volume_path = path.join(service_path, volume['source'])
                run_kwargs['mounted_volumes'][volume_path] = volume['target']
    if 'command' in service_config.keys():
        run_kwargs['start_command'] = service_config['command']
    if 'networks' in service_config.keys():
        if service_config['networks']:
            run_kwargs['network_name'] = service_config['networks'][0]

    return run_kwargs

def compile_run_command(run_kwargs, root_path='./', os='Linux'):
    
# compose run command
    from os import path
    windows_path = ''
    if os in ('Windows'):
        windows_path = '/'
    sys_cmd = 'docker run --name %s' % run_kwargs['container_alias']
    for key, value in run_kwargs['environmental_variables'].items():
        sys_cmd += ' -e %s=%s' % (key.upper(), value)
    for key, value in run_kwargs['mapped_ports'].items():
        sys_cmd += ' -p %s:%s' % (key, value)
    for key, value in run_kwargs['mounted_volumes'].items():
        sys_cmd += ' -v %s"${pwd}/%s":%s' % (windows_path, path.relpath(key, start=root_path), value)
    if run_kwargs['network_name']:
        sys_cmd += ' --network %s' % run_kwargs['network_name']
    sys_cmd += ' -d %s' % run_kwargs['image_name']
    if run_kwargs['image_tag']:
        sys_cmd += ':%s' % run_kwargs['image_tag']
    if run_kwargs['start_command']:
        sys_cmd += ' %s' % run_kwargs['start_command'].strip()
    
    return sys_cmd