#!/usr/bin/env python
from os import getcwd
from os import listdir
from os import system
from os.path import join
from os.path import isdir

def clean_files(path):
    for item in listdir(path):
        if isdir(join(path, item)):
             clean_files(join(path, item))
        elif item == "CHG":
            system("rm %s" % join(path, item))
        elif item == "CHGCAR":
            system("rm %s" % join(path, item))
        elif item == "DOSCAR":
            system("rm %s" % join(path, item))
        elif item == "IBZKPT":
            system("rm %s" % join(path, item))
        elif item == "PCDAT":
            system("rm %s" % join(path, item))
        elif item == "vasprun.xml":
            system("rm %s" % join(path, item))
        elif item == "WAVECAR":
            system("rm %s" % join(path, item))
        elif item == "XDATCAR":
            system("rm %s" % join(path, item))
        elif item == "EIGENVAL":
            system("rm %s" % join(path, item))
        elif item == "PROCAR":
            system("rm %s" % join(path, item))
        elif "slurm" in item:
            system("rm %s" % join(path, item))

if __name__ == "__main__":
    clean_files(getcwd())

