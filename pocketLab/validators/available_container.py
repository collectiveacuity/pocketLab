__author__ = 'rcj1492'
__created__ = '2016.03'

from re import compile
from pocketLab.exceptions.lab_exception import labException

def availableContainer(alias_name, container_list, kwargs):

# construct list of aliases and headers
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

# check that container is running
    for container in container_list:
        running_pattern = compile('^Up')
        if container['NAMES'] == alias_name:
            if not running_pattern.findall(container['STATUS']):
                error = {
                    'kwargs': kwargs,
                    'message': 'Container "%s" is not running. Containers currently active:' % alias_name,
                    'tprint': { 'headers': header_list, 'rows': container_list },
                    'error_value': alias_name,
                    'failed_test': 'available_resource'
                }
                raise labException(**error)

    return True
