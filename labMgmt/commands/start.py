__author__ = 'rcj1492'
__created__ = '2016.03'

_cmd_details = {
    'command': 'start',
    'usage': 'start [options]',
    'description': 'initiates a container with a project component',
    'brief': 'initiates a container with a project component',
    'defaults': {},
    'options': [
        {   'args': [ '-q', '--quiet' ],
            'kwargs': {
                'dest': 'verbose',
                'default': True,
                'help': 'turn off pipe of stdout from container',
                'action': 'store_false'
            }
        },
        {   'args': [ '-f', '--file' ],
            'kwargs': {
                'type': str,
                'default': 'lab-component.json',
                'metavar': 'FILE',
                'dest': 'componentFile',
                'help': 'path to component settings FILE (default: %(default)s)' }
        },
        {   'args': [ '-r', '--root' ],
            'kwargs': {
                'type': str,
                'default': '$(pwd)',
                'metavar': 'ROOT',
                'dest': 'componentRoot',
                'help': 'path to component ROOT directory (default: %(default)s)' }
        },
        {   'args': [ '-b', '--box' ],
            'kwargs': {
                'type': str,
                'default': 'default',
                'metavar': 'VBOX',
                'dest': 'virtualbox',
                'help': 'name of docker virtualbox (default: %(default)s)' }
        },
    ]
}

def run(**kwargs):

# import dependencies
    from os import path
    from re import compile
    from labMgmt.importers.config_file import configFile
    from labMgmt.importers.local_os import localOS
    from labMgmt.importers.docker_config import dockerConfig
    from labMgmt.validators.config_model import configModel
    from labMgmt.validators.file_path import filePath
    from labMgmt.exceptions.lab_exception import LabException
    from pprint import pprint

# ingest verbose options
    verbose = kwargs['verbose']

# determine system properties
    local_os = localOS()

# ingest & validate root path
    root_path = kwargs['componentRoot']
    if root_path == '$(pwd)':
        root_path = path.abspath('.')
    filePath(root_path)

# ingest & validate component file
    slash_pattern = compile('\\|/')
    component_file = kwargs['componentFile']
    if not slash_pattern.findall(component_file):
        component_file = '%s/%s' % (root_path, component_file)
    comp_details = configFile(component_file)
    comp_details = configModel(comp_details, 'rules/lab-component-model.json', 'component settings')

# validate path to mapped volumes
    for volume in comp_details['mapped_volumes']:
        volume_path = '%s/%s' % (root_path, volume)
        print(volume_path)
        if not path.isdir(volume_path):
            raise LabException('%s is not a valid volume path.' % volume_path, error='invalid_path')

# ingest & validate virtualbox property
    vbox_name = kwargs['virtualbox']
    if not local_os in ('Windows','Mac'):
        vbox_name = ''

# retrieve docker settings
    docker_config = dockerConfig(vbox_name)
    system_ip = docker_config.localhost()
    image_list = docker_config.images()

    print(local_os)
    print(root_path)
    print(component_file)
    print(system_ip)
    print(image_list)
    pprint(comp_details)