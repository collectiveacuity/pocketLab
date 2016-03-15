__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.exceptions.lab_exception import labException

def removableImage(image_name, image_settings, busy_images, kwargs):

# determine image id set from image settings
    image_id = image_settings['Id']
    id_set = set(image_id)
    if image_settings['RepoTags']:
        image_segments = image_settings['RepoTags'][0].split(':')
        seg_name = image_segments[0]
        seg_tag = image_segments[1]
        if seg_tag != 'latest':
            seg_name += ':%s' % seg_tag
        id_set.add(seg_name)

# check to see if any container is using image
    for key, value in busy_images.items():
        if value in id_set:
            error = {
                'kwargs': kwargs,
                'message': 'Image "%s" is linked to container "%s". Try first running: lab stop "%s"' % (image_name, key, key),
                'error_value': image_name,
                'failed_test': 'available_resource'
            }
            raise labException(**error)

    return image_id