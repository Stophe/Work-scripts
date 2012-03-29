'''
Created on Feb 27, 2012

@author: Christopher Tholander
'''


class Incar(object):
    '''
    Class for creating and extracting data from INCAR files
    '''

    def __init__(self, path, system=None, encut=None, npar=None, ismear=None,
                 sigma=None, prec=None, nelmin=None, ediff=None, ediffg=None,
                 nsw=None, ibrion=None, isif=None, ispin=None, magmom=None,
                 lwave=None, lcharge=None, lorbit=None, nbands=None):
        '''
        Constructor
        '''
        self.path = path
        self.system = system
        self.encut = encut
        self.npar = npar  # How VASP parallelize the calculation
        self.ismear = ismear
        self.sigma = sigma
        self.prec = prec
        self.nelmin = nelmin
        self.ediff = ediff
        self.ediffg = ediffg
        self.nsw = nsw  # Number of ionic relaxation steps
        self.ibrion = ibrion
        self.isif = isif
        self.ispin = ispin
        self.magmom = magmom
        self.lwave = lwave
        self.lcharge = lcharge
        self.lorbit = lorbit
        if system == None:
            self._extract_data()

    def _extract_data(self):
        # Extracts data from the INCAR file
        f = open("%s/INCAR" % self.path, 'r')
        for line in f:
            if 'ENCUT' in line and '#ENCUT' not in line:
                self.encut = line.split('=')[1][:-1]

    def create_file(self):
        f = open("%s/INCAR" % self.path, 'w')
        for attribute in self.__dict__:
            if self.__dict__[attribute] != None and attribute != 'path':
                f.write("%s=%s\n" % (attribute.upper(),
                                    self.__dict__[attribute]))
        f.close()

if __name__ == '__main__':
    path = '/Users/chtho/Desktop'
    system = "Test"
    incar = Incar(path, system)
    incar.create_file()
