__author__ = 'rcj1492'
__created__ = '2016.03'

'''
a method to determine absolute path from relative
'''

from os import path
from labMgmt.exceptions.lab_exception import LabException

def absolutePath(file_path, root_path, title=''):

    if path.isabs(file_path):
        if not path.exists(file_path):
            raise LabException('%s "%s" is not a valid absolute path.' % (title, file_path),  error='invalid_path')
        absolute_path = file_path
    else:
        absolute_path = path.abspath(file_path)
        if not path.exists(absolute_path):
            absolute_path = path.join(root_path, file_path)
            if not path.exists(absolute_path):
                raise LabException('%s "%s" is not a valid path from component root.' % (title, file_path), error='invalid_path')

    return absolute_path