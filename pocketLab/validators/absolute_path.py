__author__ = 'rcj1492'
__created__ = '2016.03'

'''
a method to determine absolute path from relative
'''

from os import path
from pocketlab.exceptions.lab_exception import labException

def absolutePath(file_path, root_path, kwargs, title=''):

# construct error dictionary with keywords
    error = { 'kwargs': kwargs }

    if path.isabs(file_path):
        if not path.exists(file_path):
            error['message'] = '%s "%s" is not a valid absolute path.' % (title, file_path)
            error['failed_test'] = 'invalid_path'
            error['error_value'] = file_path
            raise labException(**error)
        absolute_path = file_path
    else:
        absolute_path = path.abspath(file_path)
        if not path.exists(absolute_path):
            absolute_path = path.join(root_path, file_path)
            if not path.exists(absolute_path):
                error['message'] = '%s "%s" is not a valid path from component root.' % (title, file_path)
                error['failed_test'] = 'invalid_path'
                error['error_value'] = file_path
                raise labException(**error)

    return absolute_path