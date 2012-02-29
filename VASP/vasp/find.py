'''
Created on Feb 27, 2012

@author: Christopher Tholander
'''

from os import listdir
from os.path import isdir


class Find(object):
    '''
    classdocs
    '''

    def __init__(self, path, file_name):
        '''
        Constructor
        '''
        self.paths = []
        self._find_paths(path, file_name)

    def _find_paths(self, path, file_name):
        """Finds the paths to the result files"""
        directory_list = listdir(path)
        for item in directory_list:
            if item == file_name:
                self.paths.append(path)
            elif isdir("%s/%s" % (path, item)):
                self._find_paths("%s/%s" % (path, item), file_name)
