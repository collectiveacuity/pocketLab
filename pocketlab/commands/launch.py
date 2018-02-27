__author__ = 'rcj1492'
__created__ = '2018.02'
__license__ = 'MIT'

_init_details = {
    'title': 'Launch',
    'description': 'Launches an instance or an auto-scaling group on a remote platform. Launch is currently only available for the ec2 platform. To create an configuration file to launch an ec2 instance, run ```lab init --ec2``` and adjust the settings appropriately.',
    'help': 'starts instances on remote platform',
    'benefit': 'Launch creates one or more remote instances to host services.'
}

from pocketlab.init import fields_model

def launch(platform_name, verbose=True, overwrite=False):
    
    exit_msg = ''
    
    title = 'launch'
    
    return exit_msg