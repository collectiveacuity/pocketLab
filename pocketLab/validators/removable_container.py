__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.exceptions.lab_exception import labException

def removableContainer(alias_name, container_list, kwargs):

# construct alias list and headers
    header_list = [ 'NAMES', 'STATUS', 'IMAGE', 'PORTS']
    alias_list = []
    for container in container_list:
        alias_list.append(container['NAMES'])

# check that container exists
    if not alias_name in alias_list:
        error = {
            'kwargs': kwargs,
            'message': 'Container "%s" does not exist. Containers currently active:' % alias_name,
            'tprint': { 'headers': header_list, 'rows': container_list },
            'error_value': alias_name,
            'failed_test': 'required_resource'
        }
        raise labException(**error)

    return True