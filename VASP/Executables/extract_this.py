#!/usr/bin/env python
from data_extraction import find_data
from data_extraction import Outcar
from data_extraction import Oszicar
from data_extraction import Poscar
from data_extraction import Kpoints
from os import getcwd
from os import system
from os.path import isdir
from sys import argv
from csv import writer
from csv import QUOTE_MINIMAL

# Checks if information from the OUTCAR is wanted
def outcar_is_wanted():
    if 'total_cpu_time' in argv:
        return True
    else:
        return False

# Checks if information from the OSZICAR is wanted
def oszicar_is_wanted():
    if 'total_energy' or 'all_energies' in argv:
        return True
    else:
        return False

# Checks if information from the POSCAR is wanted
def poscar_is_wanted():
    if 'title' or 'formula_unit' in argv:
        return True
    else:
        return False
    
def kpoints_is_wanted():
    possible_settings =['kpoints','kpoint_type','total_kpoints']
    if len(set(possible_settings).intersection(set(argv))) > 0:
        return True
    else:
        return False

# Extracts the data specified in the input arguments
def main(current_path):
    result_csv_file = writer(open('%s/results.csv' % current_path,'wb'),
                             delimiter=',',quotechar='|',quoting=QUOTE_MINIMAL)
    if 'all_energies' in argv:
        energy_csv_file = writer(open('%s/all_energies.csv' % current_path,'wb'),
                                 delimiter=',',quotechar='|',quoting=QUOTE_MINIMAL)
    data_paths =[] 
    find_data(current_path,data_paths)
    for path in data_paths:
        if outcar_is_wanted(): outcar = Outcar(path)
        if oszicar_is_wanted(): oszicar = Oszicar(path)
        if poscar_is_wanted(): poscar = Poscar(path)
        if kpoints_is_wanted(): kpoints = Kpoints(path)
        results=[]
        for argument in argv:
            if argument == 'title':
                results.append(poscar.title)
            elif argument == 'total_energy':
                results.append(oszicar.total_energy)
            elif argument == 'all_energies':
                energy_csv_file.writerow([poscar.title]+oszicar.all_energies)
            elif argument == 'formula_unit':
                results.append(poscar.formula_unit)
            elif argument == 'total_cpu_time':
                results.append(outcar.total_cpu_time)
            elif argument == 'kpoints':
                results.append(kpoints)
            elif argument == 'total_kpoints':
                results.append(kpoints.total_kpoints)
            elif argument == 'kpoint_type':
                results.append(kpoints.type)
        result_csv_file.writerow(results)

if __name__ == '__main__':
    current_path = getcwd()
    if len(argv) == 1:
        argv = argv + [current_path,'title','total_energy','formula_unit','total_cpu_time','all_energies',
                       'kpoints','total_kpoints','kpoint_type']
        main(current_path)
    elif isdir(argv[1]):
        main(argv[1])
    else:
        main(current_path)
    if 'print' in argv: system('cat results.csv')