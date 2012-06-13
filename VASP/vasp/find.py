'''
Created on Feb 27, 2012

@author: Christopher Tholander
'''

from os import listdir
from os.path import isdir


def Find(path, file_name, paths=[]):
    for item in listdir(path):
        if item == file_name:
            paths.append(path)
        elif isdir("%s/%s" % (path, item)):
            paths = Find("%s/%s" % (path, item), file_name, paths)
    return paths

if __name__ == "__main__":
    print "Looking for dirs containing 'OUTCAR' starting from '.':"
    print Find(".", "OUTCAR")
    print "Looking for dirs containing 'INCARS' starting from '.':"
    print Find(".", "INCAR")
