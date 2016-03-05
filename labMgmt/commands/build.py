__author__ = 'rcj1492'
__created__ = '2016.03'

_cmd_details = {
    'command': 'build',
    'usage': 'build [options]',
    'description': 'builds an image from project components',
    'defaults': { 'service': 'aws' },
    'options': [
        {   'args': [ '-q', '--quiet' ],
            'kwargs': {
                'default': True,
                'dest': 'verbose',
                'help': 'turn off status messages from (default: %(default)s)',
                'action': 'store_false' }
        },
        {   'args': [ '-f', '--file' ],
            'kwargs': {
                'type': str,
                'default': 'lab-project.json',
                'metavar': 'FILE',
                'dest': 'projectFile',
                'help': 'path to project settings FILE (default: %(default)s)' }
        }
    ]
}

def run(**kwargs):

# import dependencies
    from labMgmt.importers import configFile
    from labMgmt.validators import projectModel, credModel
    from pprint import pprint

    verbose = kwargs['verbose']
    deploy_service = kwargs['service']

# ingest & validate project file
    project_file = kwargs['projectFile']
    project_details = configFile(project_file)
    project_details = projectModel(project_details)

# construct credentials dictionaries
    aws_credentials = {}
    for cred_file in project_details['credentials_files']:
        if cred_file['service'] == 'aws':
            credential_details = configFile(cred_file['file_path'])
            aws_credentials = credModel(credential_details, 'rules/aws-cred-model.json', 'aws')
    pprint(aws_credentials)
