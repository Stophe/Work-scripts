#!/usr/bin/env python
from os import getcwd, system
from os.path import isdir
import sys
from csv import writer, QUOTE_MINIMAL
#import cProfile

from vasp.find import Find
from vasp.outcar import Outcar
from vasp.oszicar import Oszicar
from vasp.poscar import Poscar
from vasp.contcar import Contcar
from vasp.kpoints import Kpoints
from vasp.doscar import Doscar


def outcar_is_needed():
    """Checks if information from the OUTCAR is needed. Returns True if it is,
    no otherwise.
    """
    possible_settings = ['total_cpu_time', 'volume', 'dos_per_atom', 'encut',
                         'kpoints', 'total_kpoints', 'nodes', 'total_nr_of_ions', 'ic_piezoelectric_tensor', 'e33']
    if len(set(possible_settings).intersection(set(sys.argv))) > 0:
        return True
    else:
        return False


def oszicar_is_needed():
    """Checks if information from the OSZICAR is needed. Returns True if it is,
    no otherwise.
    """
    possible_settings = ['total_energy', 'all_energies', 'magmom', 'c33']
    if len(set(possible_settings).intersection(set(sys.argv))) > 0:
        return True
    else:
        return False


def poscar_is_needed():
    """Checks if information from the POSCAR is needed. Returns True if it is,
    no otherwise.
    """
    possible_settings = ['old_title', 'old_formula_unit', 'old_surface_area',
                         'old_lattice_constant', 'old_all_energies', 'old_adatom_pos', 'adatom_pos']
    if len(set(possible_settings).intersection(set(sys.argv))) > 0:
        return True
    else:
        return False


def contcar_is_needed():
    """Checks if information from the POSCAR is needed. Returns True if it is,
    no otherwise.
    """
    possible_settings = ['title', 'formula_unit', 'surface_area',
                         'lattice_constant', 'alat', 'coa', 'all_energies',
                         'dos_per_atom', 'adatom_pos', 'average_u', 'e33', 'c33']
    if len(set(possible_settings).intersection(set(sys.argv))) > 0:
        return True
    else:
        return False


def kpoints_is_needed():
    """Checks if information from the KPOINTS is needed. Returns True if it is,
    no otherwise.
    """
    possible_settings = ['kpoint_type']
    if set(possible_settings).intersection(set(sys.argv)):
        return True
    else:
        return False


def doscar_is_needed():
    """Checks if information from the INCAR is needed. Returns true if it is,
    no otherwise.
    """
    possible_settings = ['dos', 'dos_per_atom', 'bandgap']
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
        sys.argv = sys.argv + ['kpoints', 'kpoint_type', 'total_kpoints',
                               'title', 'formula_unit',
                               'total_energy', 'all_energies',
                               'total_cpu_time', 'encut', 'surface_area',
                               'print', 'dos']
    elif isdir(sys.argv[1]):
        current_path = sys.argv[1]
    rf = open('%s/results.csv' % current_path, 'wb')
    result_csv_file = writer(rf, delimiter=',', quotechar='|',
                             quoting=QUOTE_MINIMAL)

    written_header = False

    paths = Find(current_path, 'OUTCAR')
    for path in paths:
        if outcar_is_needed(): outcar = Outcar(path)
        if oszicar_is_needed(): oszicar = Oszicar(path)
        if poscar_is_needed(): poscar = Poscar(path)
        if contcar_is_needed(): contcar = Contcar(path)
        if kpoints_is_needed(): kpoints = Kpoints(path, extract=True)
        if doscar_is_needed(): doscar = Doscar(path)
        
        results = []
        col_titles = []
        
        for argument in sys.argv:
            if argument == 'title':
                if 'Title' not in col_titles:
                    col_titles.append('Title')
                results.append(contcar.title)
            
            elif argument == 'lattice_constant' or argument =='alat':
                if 'a0 [Ang]' not in col_titles:
                    col_titles.append('a0 [Ang]')
                results.append(contcar.supercell.a0)
            
            elif argument == 'coa':
                if 'c/a' not in col_titles:
                    col_titles.append('c/a')
                try:
                    results.append(contcar.coa)
                except:
                    print contcar.path
                    
            elif argument == 'average_u':
                if '<u>' not in col_titles:
                    col_titles.append('<u>')
                results.append(contcar.calculate_average_u())
            
            elif argument == 'surface_area':
                if 'Surface Area [Ang^2]' not in col_titles:
                    col_titles.append('Surface Area [Ang^2]')
                results.append(contcar.surface_area)
            
            elif argument == 'formula_unit':
                if 'Formula unit' not in col_titles:
                    col_titles.append('Formula unit')
                results.append(contcar.formula_unit)
            
            elif argument == 'adatom_pos':
                found = False
                if 'adatom_pos' not in col_titles:
                    col_titles += ['adatom x', 'adatom y', 'adatom z']
                try:
                    contcar.find_adatoms()
                    for atom in contcar.supercell.atoms:
                        if atom.adatom:
                            if 'real' in sys.argv:
                                results += list(contcar.supercell.convert_to_real(atom.position))
                            else:
                                results += list(atom.position)
                            found = True
                            break
                except:
                    print "Error: No CONTCAR found, trying POSCAR instead!"
                if not found:
                    try:
                        poscar.find_adatoms()
                        for atom in poscar.supercell.atoms:
                            if atom.adatom:
                                if 'real' in sys.argv:
                                    results += list(poscar.supercell.convert_to_real(atom.position))
                                else:
                                    results += list(atom.position)
                                break
                    except:
                        print "Error: No POSCAR found either!"

            elif argument == 'old_adatom_pos':
                if 'old_adatom_pos' not in col_titles:
                    col_titles += ['old-adatom x', 'old-adatom y', 'old-adatom z']
                poscar.find_adatoms()
                for atom in poscar.supercell.atoms:
                    if atom.adatom:
                        if 'real' in sys.argv:
                            results += list(poscar.supercell.convert_to_real(atom.position))
                        else:
                            results += list(atom.position)
                        break
            
            elif argument == 'total_energy':
                if 'Total Energy [eV]' not in col_titles:
                    col_titles.append('Total Energy [eV]')
                results.append(oszicar.total_energy)
                
            elif argument == 'magmom':
                if 'Magmom' not in col_titles:
                    col_titles.append('Magmom')
                results.append(oszicar.magmom)
            
            elif argument == 'all_energies':
                f = open('%s/all_energies.csv' % current_path, 'wb')
                energy_csv_file = writer(f, delimiter=',', quotechar='|',
                                 quoting=QUOTE_MINIMAL)
                energy_csv_file.writerow([contcar.title] + oszicar.all_energies)
                f.close()
            
            elif argument == 'nodes':
                if 'Nodes' not in col_titles:
                    col_titles.append('Nodes')
                results.append(outcar.nodes)
                
            elif argument == 'total_cpu_time':
                if 'Total CPU time' not in col_titles:
                    col_titles.append('Total CPU time')
                results.append(outcar.total_cpu_time)
            
            elif argument == 'volume':
                if 'Volume [Ang^3]' not in col_titles:
                    col_titles.append('Volume [Ang^3]')
                results.append(outcar.volume)
            
            elif argument == 'total_nr_of_ions':
                if 'Nr of ions' not in col_titles:
                    col_titles.append('Nr of ions')
                results.append(outcar.total_nr_of_ions)
            
            elif argument == 'kpoints':
                if 'K-points' not in col_titles:
                    col_titles.append('K-points')
                results.append("%ix%ix%i" % outcar.kpoints)
            
            elif argument == 'total_kpoints':
                if 'Total K-points' not in col_titles:
                    col_titles.append('Total K-points')
                results.append(outcar.total_kpoints)

            elif argument == 'nkpts':
                if 'Total K-points' not in col_titles:
                    col_titles.append('NKPTS')
                results.append(outcar.nkpts)

            elif argument == 'kpoint_type':
                if 'K-mesh type' not in col_titles:
                    col_titles.append('K-mesh type')
                results.append(kpoints.mesh_type)

            elif argument == 'encut':
                if 'ENCUT' not in col_titles:
                    col_titles.append('ENCUT')
                results.append(outcar.encut)
            
            elif argument == 'bandgap':
                if 'Bandgap [eV]' not in col_titles:
                    col_titles.append('Bandgap [eV]')
                results.append(doscar.bandgap)
            
            elif argument == 'dos':
                f = open('%s/dos.csv' % current_path, 'w')
                f.write("Fermi level,Bandgap\n")
                f.write("%f,%f\n" % (doscar.fermi_level, doscar.bandgap))
                f.write("Energy,DOS,Integrated DOS\n")
                for line in doscar.dos:
                    f.write("%s,%s,%s\n" % (line[0], line[1], line[2]))
                f.close()
            
            elif argument == 'dos_per_atom':
                i = 0
                line = 0
                for count in contcar.counts:
                    int_dos = [[0] * 3] * doscar.steps
                    f = open('%s/dos%s.csv' % (current_path, outcar.atom_symbols[i]), 'w')
                    dos_csv_file = writer(f, delimiter=',', quotechar='|',
                                 quoting=QUOTE_MINIMAL)
                    dos_csv_file.writerow(['Symbol', 'Count'])
                    dos_csv_file.writerow([outcar.atom_symbols[i], count])
                    for atom in range(line, line + count):
                        for energy in range(0, doscar.steps):
                            int_dos[energy] = [doscar.dos_per_atom[atom][energy][0],
                                               int_dos[energy][1] + doscar.dos_per_atom[atom][energy][4],
                                               int_dos[energy][2] + doscar.dos_per_atom[atom][energy][5]]
                    dos_csv_file.writerow(['Energy', 'DOS', 'Integrated DOS'])
                    for row in int_dos:
                        dos_csv_file.writerow(row)
                    f.close()
                    line += count
                    i += 1  # Choose correct symbol
                
            elif argument == 'e33':
                pass
            elif argument == 'c33':
                pass
            elif argument == 'ic_piezoelectric_tensor':
                f = open('%s/ic_pieoelectric_tensor.csv' % current_path, 'w')
                f.write('Ion-clamped Piezoelectric tensor [C/m^2]\n')
                pt = outcar.ic_piezo_tensor()
                f.write('XX,YY,ZZ,XY,YZ,ZX\n')
                for item in pt[0]:
                    f.write(str(item) + ',')
                f.write('\n')
                for item in pt[1]:
                    f.write(str(item) + ',')
                f.write('\n')
                for item in pt[2]:
                    f.write(str(item) + ',')
                f.write('\n')
                f.close()

        if not written_header:
            result_csv_file.writerow(col_titles)
            written_header = True
        result_csv_file.writerow(results)
    rf.close()

    
    if 'print' in sys.argv: 
        system('/bin/cat "%s/results.csv"' % current_path)

if __name__ == '__main__':
#    if 'time_test' in sys.argv:
#        loc = locals()
#        glob = globals()
#        cProfile.runctx('main()', glob, loc, 'profiledata.txt')
#    else:
    main()
