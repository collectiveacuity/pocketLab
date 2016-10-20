__author__ = 'rcj1492'
__created__ = '2016.03'

'''
possible objects to remove
-p PROJECT removes project from local registry
-i IMAGE removes image from local docker (possible removal of online repo??)
-c COMPONENT removes component from project file (possible removal of files??)

'''

_cmd_details_remove = {
    'command': 'remove',
    'usage': 'remove [options]',
    'description': 'removes an image or component from an environment',
    'brief': 'removes an image or component from an environment',
    'defaults': { },
    'options': [
        {   'args': [ '-i, --image' ],
            'kwargs': {
                'type': str,
                'default': '',
                'metavar': 'IMAGE',
                'dest': 'image',
                'help': 'name of a local docker IMAGE'
            }
        },
        {   'args': [ '-t, --tag' ],
            'kwargs': {
                'type': str,
                'default': '',
                'metavar': 'TAG',
                'dest': 'tag',
                'help': 'TAG associated with a docker image'
            }
        },
        {   'args': [ '--virtualbox' ],
            'kwargs': {
                'type': str,
                'default': 'default',
                'metavar': 'IMAGE',
                'dest': 'virtualbox',
                'help': 'name of docker virtualbox IMAGE (default: %(default)s)' }
        }
    ]
}

def remove(**kwargs):

# import dependencies
    from pocketlab.importers.config_file import configFile
    from pocketlab.clients.localhost_client import localhostClient
    from pocketlab.clients.docker_session import dockerSession
    from pocketlab.validators.config_model import configModel
    from pocketlab.validators.available_image import availableImage
    from pocketlab.validators.removable_image import removableImage

# determine system properties
    localhost = localhostClient()

# ingest & validate virtualbox property
    vbox_name = kwargs['virtualbox']
    if not localhost.os in ('Windows','Mac'):
        vbox_name = ''

# check for docker installation
    docker_session = dockerSession(kwargs, vbox_name)

# construct image name
    docker_image = kwargs['image']
    image_tag = kwargs['tag']
    image_name = docker_image
    if image_tag:
        image_name += ':%s' % image_tag

# validate the local availability of docker image
    image_list = docker_session.images()
    availableImage(docker_image, image_tag, image_list, kwargs)

# retrieve image id and construct image name
    image_settings = docker_session.inspect(docker_image=docker_image, image_tag=image_tag)

# retrieve dictionary of images linked to active containers
    container_list = docker_session.ps()
    busy_images = {}
    for container in container_list:
        container_settings = docker_session.inspect(container_alias=container['NAMES'])
        container_synopsis = docker_session.synopsis(container_settings)
        busy_images[container_synopsis['container_alias']] = container_synopsis['docker_image']

# validate the removability of image
    image_id = removableImage(image_name, image_settings, busy_images, kwargs)

# remove image
    end_command = docker_session.rmi(image_id)
    success_text = 'Sweet! Image "%s" removed.' % image_name
    print(success_text)

    return end_command