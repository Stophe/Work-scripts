'''
Created on Feb 27, 2012

@author: Christopher Tholander
'''

import os


def Find(path, file_name):
    paths = []
    for path, _, items in os.walk(path):
        if file_name in items:
            paths.append(path)
    return paths


if __name__ == "__main__":
    print "Looking for dirs containing 'OUTCAR' starting from '.':"
    print Find(".", "OUTCAR")
    print "Looking for dirs containing 'INCARS' starting from '.':"
    print Find(".", "INCAR")
