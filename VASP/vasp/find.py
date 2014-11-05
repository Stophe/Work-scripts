'''
Created on Feb 27, 2012

@author: Christopher Tholander
'''

import os


def Find(path, filenames):
    paths = []
    for path, _, items in os.walk(path):
        for filename in filenames:
            if filename in items:
                paths.append(path)
    return paths


if __name__ == "__main__":
    print "Looking for dirs containing 'OUTCAR' starting from '.':"
    print Find(".", "OUTCAR")
    print "Looking for dirs containing 'INCARS' starting from '.':"
    print Find(".", "INCAR")
