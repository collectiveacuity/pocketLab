__author__ = 'rcj1492'
__created__ = '2016.03'

'''
a method to generate a valid path from the composition of multiple path references
'''

from re import compile
from os import path
from copy import deepcopy
from labMgmt.exceptions.lab_exception import LabException

def filePath(root_path, sub_path='', title=''):

    if not path.isdir(root_path):
        raise LabException('%s is not a valid %s path.' % (root_path, title), error='invalid_path')
    file_path = deepcopy(root_path)
    if sub_path:
        file_path = root_path + sub_path

    return file_path