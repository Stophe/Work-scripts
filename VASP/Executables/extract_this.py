#!/usr/bin/env python
from os import getcwd, system
from os.path import isdir
import sys
from csv import writer,QUOTE_MINIMAL
from vasp.find import Find
from vasp.outcar import Outcar
from vasp.oszicar import Oszicar
from vasp.poscar import Poscar
from vasp.kpoints import Kpoints
from vasp.incar import Incar

def outcar_is_needed():
    """Checks if information from the OUTCAR is needed. Returns True if it is, no otherwise."""
    possible_settings = ['total_cpu_time']
    if len(set(possible_settings).intersection(set(sys.argv))) > 0:
        return True
    else:
        return False

def oszicar_is_needed():
    """Checks if information from the OSZICAR is needed. Returns True if it is, no otherwise."""
    possible_settings = ['total_energy', 'all_energies']
    if len(set(possible_settings).intersection(set(sys.argv))) > 0:
        return True
    else:
        return False

def poscar_is_needed():
    """Checks if information from the POSCAR is needed. Returns True if it is, no otherwise."""
    possible_settings = ['title', 'formula_unit', 'surface_area', 'lattice_constant']
    if len(set(possible_settings).intersection(set(sys.argv))) > 0:
        return True
    else:
        return False
    
def kpoints_is_needed():
    """Checks if information from the KPOINTS is needed. Returns True if it is, no otherwise."""
    possible_settings =['kpoints', 'kpoint_type', 'total_kpoints']
    if set(possible_settings).intersection(set(sys.argv)):
        return True
    else:
        return False


def incar_is_needed():
    """Checks if information from the INCAR is needed. Returns true if it is, no otherwise."""
    possible_settings = ['encut']
    if set(possible_settings).intersection(set(sys.argv)):
        return True
    else:
        return False


def main():
    """
    The main function. Extracts the data specified in the input arguments.
    
    If no argument is given the default is to get all data.
    If a path is given, that will be used as the current directory.
    """
    current_path = getcwd()
    if len(sys.argv) == 1:
        sys.argv = sys.argv + ['kpoints', 'kpoint_type', 'total_kpoints', 'title', 'formula_unit',
                               'total_energy', 'all_energies','total_cpu_time', 'encut', 'surface_area', 'print']
    elif isdir(sys.argv[1]):
        current_path = sys.argv[1]
    rf = open('%s/results.csv' % current_path, 'wb')
    result_csv_file = writer(rf, delimiter=',', quotechar='|', quoting = QUOTE_MINIMAL)
    if 'all_energies' in sys.argv:
        ef = open('%s/all_energies.csv' % current_path, 'wb')
        energy_csv_file = writer(ef, delimiter=',', quotechar='|', quoting = QUOTE_MINIMAL)
    find = Find(current_path, 'OUTCAR') 
    for path in find.paths:
        if outcar_is_needed(): outcar = Outcar(path)
        if oszicar_is_needed(): oszicar = Oszicar(path)
        if poscar_is_needed(): poscar = Poscar(path)
        if kpoints_is_needed(): kpoints = Kpoints(path)
        if incar_is_needed(): incar = Incar(path)
        results = []
        
        for argument in sys.argv:
            if argument == 'title':
                results.append(poscar.title)
            elif argument == 'lattice_constant':
                results.append(poscar.a0)
            elif argument == 'surface_area':
                results.append(poscar.surface_area)
            elif argument == 'formula_unit':
                results.append(poscar.formula_unit)
            elif argument == 'total_energy':
                results.append(oszicar.total_energy)
            elif argument == 'all_energies':
                energy_csv_file.writerow([poscar.title] + oszicar.all_energies)
            elif argument == 'total_cpu_time':
                results.append(outcar.total_cpu_time)
            elif argument == 'kpoints':
                results.append(kpoints)
            elif argument == 'total_kpoints':
                results.append(kpoints.total_kpoints)
            elif argument == 'kpoint_type':
                results.append(kpoints.mesh_type)
            elif argument == 'encut':
                results.append(incar.encut)
        result_csv_file.writerow(results)
    rf.close()
    try: ef.close()
    except: pass
    
    if 'print' in sys.argv: 
        system('/bin/cat "%s/results.csv"' % current_path)

if __name__ == '__main__':
    main()
