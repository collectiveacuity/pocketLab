__author__ = 'rcj1492'
__created__ = '2016.03'

from labMgmt.importers import configFile
from labMgmt.validators import projectModel, credModel
from pprint import pprint

def start(**kwargs):
    print(kwargs)

def stop(**kwargs):
    print(kwargs)

def pause(**kwargs):
    print(kwargs)

def build(**kwargs):

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
            aws_credentials = credModel(credential_details, 'rules/aws-cred-model.json')
    pprint(aws_credentials)

