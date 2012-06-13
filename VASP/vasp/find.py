'''
Created on Feb 27, 2012

@author: Christopher Tholander
'''

from os import listdir
from os.path import isdir


def Find(path, file_name):
    paths = []
    directory_list = listdir(path)
    for item in listdir(path):
        if item == file_name:
            paths.append(path)
        elif isdir("%s/%s" % (path, item)):
            Find("%s/%s" % (path, item), file_name)
    return paths

