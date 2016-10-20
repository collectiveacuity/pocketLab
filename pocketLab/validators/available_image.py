__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketlab.exceptions.lab_exception import labException

def availableImage(image_name, image_tag, image_list, kwargs):

# construct error dictionary with keywords
    error = {
        'kwargs': kwargs,
        'error_value': image_name,
        'failed_test': 'available_resource'
    }

# check list of images for image name and tag values
    header_list = [ 'REPOSITORY', 'TAG', 'VIRTUAL SIZE' ]
    available_images = {}
    curated_images = []
    for image in image_list:
        if not '<none>' in image['REPOSITORY']:
            curated_images.append(image)
            available_images[image['REPOSITORY']] = image['TAG']
    if not image_tag:
        if not image_name in available_images.keys():
            error['message'] = 'Image "%s" not found. Try first running: "docker pull %s"' % (image_name, image_name)
            error['tprint'] = { 'headers': header_list, 'rows': curated_images }
            raise labException(**error)
    else:
        for key, value in available_images.items():
            if key == image_name:
                if value != image_tag:
                    error['message'] = 'Tag "%s" for image "%s" not found. Try using "latest" or leaving tag value blank.' % (image_tag, image_name)
                    error['tprint'] = { 'headers': header_list, 'rows': curated_images }
                    error['error_value'] = '%s:%s' % (image_tag, image_name)
                    raise labException(**error)
                else:
                    return True
        error['message'] = 'Image "%s:%s" not found. Try first running: "docker pull %s:%s"' % (image_name, image_tag, image_name, image_tag)
        error['tprint'] = { 'headers': header_list, 'rows': curated_images }
        error['error_value'] = '%s:%s' % (image_name, image_tag)
        raise labException(**error)

    return True