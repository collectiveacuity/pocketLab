__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

'''
remove services with non-existent roots from registry
TODO: remove broken/previous docker images from docker
TODO: remove exited status 1 containers from docker
'''

_clean_details = {
    'title': 'clean',
    'description': 'Removes broken resources from the registries.',
    'help': 'cleans registries of broken resources',
    'benefit': 'Frees up space by removing superfluous files.'
}

def clean(verbose=True):

# construct registry client
    from pocketlab import __module__
    from labpack.storage.appdata import appdataClient
    registry_client = appdataClient(collection_name='Registry Data', prod_name=__module__)

# remove each file in registry without a valid path
    from os import path
    from labpack.records.settings import load_settings, remove_settings
    for file_path in registry_client.localhost.walk(registry_client.collection_folder):
        remove_file = False
        try:
            details = load_settings(file_path)
            service_name = details['service_name']
            service_root = details['service_root']
            if not path.exists(service_root):
                remove_file = True
        except:
            remove_file = True
        if remove_file:
            if verbose:
                file_root, file_ext = path.splitext(file_path)
                file_dir, file_name = path.split(file_root)
                print('Broken service "%s" removed from lab registry.' % file_name)
            remove_settings(file_path)

# TODO remove docker containers with exit 1 status

# TODO remove docker images with ^none name

    exit_msg = 'Lab environment has been cleaned up.'

    return exit_msg

