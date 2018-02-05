__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

'''
remove services with non-existent roots from registry
remove broken/previous docker images from docker
remove exited status 1 containers from docker
'''

_clean_details = {
    'title': 'clean',
    'description': 'Removes broken resources from the registries.',
    'help': 'cleans registries of broken resources',
    'benefit': 'Frees up space by removing superfluous files.'
}

from pocketlab.init import fields_model

def clean(verbose=True, virtualbox='default'):

    '''
        a method to remove orphaned resources in lab repositories
        
    :param verbose: [optional] boolean to toggle process messages
    :param virtualbox: [optional] string with name of virtualbox image (win7/8)
    :return: string with exit message
    '''

    title = 'clean'

# validate inputs
    input_fields = {
        'verbose': verbose,
        'virtualbox': virtualbox
    }
    for key, value in input_fields.items():
        if value:
            object_title = '%s(%s=%s)' % (title, key, str(value))
            fields_model.validate(value, '.%s' % key, object_title)

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

# construct docker client
    from labpack.platforms.docker import dockerClient
    try:
        docker_client = dockerClient(virtualbox_name=virtualbox)
    except:
        docker_client = None

# remove docker containers with exit 1 status
    if docker_client:
        for container in docker_client.ps():
            if container['STATUS'].find('Exited (1)') > -1:
                try:
                    docker_client.rm(container['CONTAINER_ID'])
                    if verbose:
                        if container['NAMES']:
                            container_name = 'alias "%s"' % container['NAMES'].split(' ')[0]
                        else:
                            container_name = 'of image "%s"' % container['IMAGE']
                        print('Container %s with exit(1) status removed from docker.' % container_name)
                except:
                    pass

# remove docker images with <none> in name tag
    if docker_client:
        for image in docker_client.images():
            if image['TAG'] == '<none>':
                try:
                    docker_client.rmi(image['IMAGE ID'], override=True)
                    if verbose:
                        image_name = '"%s:%s"' % (image['REPOSITORY'], image['TAG'])
                        print('Image %s removed from docker.' % image_name)
                except:
                    pass

    exit_msg = 'Lab environment has been cleaned up.'

    return exit_msg

