'''
Created on Feb 27, 2012

@author: chtho
'''
from os.path import isfile
import gzip
import bz2

class Outcar(object):
    '''
    Class for extracting data from OUTCAR files
    '''

    def __init__(self, path):
        '''
        Constructor
        '''
        self.path = path
        self.nodes = 0
        self.atom_symbols = []
        self.total_nr_of_ions = 0
        self.total_nr_of_electrons = 0
        self.total_cpu_time = 0
        self.volume = 0
        self.encut = 0
        self.kpoints = (0, 0, 0)
        self.nkpts = 0
        self.polarization = [[],[]]
        self.born_charge_33_average = 0
        self.ci_e33
        self._extract_data()
        self.total_kpoints = sum(self.kpoints)
    
    def _float_list(self, lst):
        new_lst = []
        for item in lst:
            new_lst.append(float(item))
        return new_lst
    
    def _extract_data(self):
        #: Extracts the data from the OUTCAR file
        if isfile("%s/OUTCAR.gz" % (self.path)):
            f = gzip.open("%s/OUTCAR.gz" % (self.path), 'rb')
        elif isfile("%s/OUTCAR.bz2" % (self.path)):
            f = bz2.BZ2File("%s/OUTCAR.bz2" % (self.path), 'rb')
        else:
            f = open("%s/OUTCAR" % (self.path), 'r')
        for line in f:
            if 'running on' in line and 'image' not in line:
                self.nodes = int(float(line.split()[2]))
            elif 'VRHFIN' in line:
                line = line.split()[1]
                self.atom_symbols.append(line[1:-1])
            elif 'NIONS' in line:
                line = line.split()
                self.total_nr_of_ions = int(float(line[11]))
            elif 'NELECT' in line:
                self.total_nr_of_electrons = int(float(line.split()[2]))
            elif 'ENCUT' in line:
                self.encut = line.split()[2]
            elif 'KPOINTS' in line:
                ln = line.split()[1].replace('x', ' ').split()
                self.kpoints = (int(ln[0]), int(ln[1]), int(ln[2]))
            elif 'NKPTS' in line:
                self.nkpts = int(line.split()[3])
            elif 'Ionic dipole moment: p[ion]=(' in line:
                l = self._float_list(line.split()[4:7])
                self.polarization[0] = l
            elif 'Total electronic dipole moment: p[elc]=(' in line:
                l = self._float_list(line.split()[5:8])
                self.polarization[1] = l
            elif 'PIEZOELECTRIC TENSOR  for field in x, y, z        (C/m^2)' in line:
                for i in range(4): f.next()
                l = f.next().split()
                self.ci_e33 = l[3]
            elif 'BORN EFFECTIVE CHARGES' in line:
                bec = []
                for i in range(2): f.next()
                for i in range(self.total_nr_of_ions):
                    l = f.next().next().next().split()
                    bec.append(l[3])
                    f.next()
                self.born_charge_33_average = sum(abs(bec))/len(bec)
        
        
        try:
            f.seek(-500000, 2)
        except:
            print self.path

        for line in f:
            if 'volume of cell' in line:
                self.volume = float(line.split()[4])
            elif 'Total CPU time' in line:
                self.total_cpu_time = line.split()[5]
        f.close()

    
    def ic_piezo_tensor(self):
        ic_piezo_tensor = [[],[],[]] # E-field in x, y, z, respectively
        
        f = open("%s/OUTCAR" % (self.path), 'r')
        for line in f:
            if ' PIEZOELECTRIC TENSOR (including local field effects) (C/m^2)' in line:
                for i in range(2): f.next()
                l = self._float_list(f.next().split()[1:7])
                ic_piezo_tensor[0] = l 
                l = self._float_list(f.next().split()[1:7])
                ic_piezo_tensor[1] = l
                l = self._float_list(f.next().split()[1:7])
                ic_piezo_tensor[2] = l 
                break
            elif 'PIEZOELECTRIC TENSOR  for field in x, y, z        (C/m^2)' in line:
                for i in range(2): f.next()
                l = self._float_list(f.next().split()[1:7])
                ic_piezo_tensor[0] = l 
                l = self._float_list(f.next().split()[1:7])
                ic_piezo_tensor[1] = l
                l = self._float_list(f.next().split()[1:7])
                ic_piezo_tensor[2] = l 
                break
                
        f.close()
        return ic_piezo_tensor
                
