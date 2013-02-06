'''
Created on Nov 15, 2012

@author: chtho
'''
from numpy import array
from numpy.linalg import norm
from random import shuffle

class Sqs():
    '''
    Class for generating SQS structures 
    '''


    def __init__(self, supercell, part1, part2):
        '''
        Constructor
        part1 is the first atom type to be mixed
        part2 is the second
        '''
        self.supercell = supercell
        self.part1 = part1
        self.part2 = part2
        
    def mix(self):
        mixing_atoms = []
        for atom in self.supercell.atoms:
            if atom.symbol == self.part1 or atom.symbol == self.part2:
                mixing_atoms.append(atom.symbol)
        
        shuffle(mixing_atoms)
        
        for atom in self.supercell.atoms:
            if atom.symbol == self.part1 or atom.symbol == self.part2:
                atom.symbol = mixing_atoms.pop()
        self.supercell.sort()
     
    def expand_refcell(self, ref_cell, times):
        for i in range(1, times):
            for atom in self.supercell.atoms:
                ref_cell.add(atom.symbol, atom.position + array([  i, 0.0, 0.0]))
                ref_cell.add(atom.symbol, atom.position + array([0.0,   i, 0.0]))
                ref_cell.add(atom.symbol, atom.position + array([0.0, 0.0,   i]))
                ref_cell.add(atom.symbol, atom.position + array([ -i, 0.0, 0.0]))
                ref_cell.add(atom.symbol, atom.position + array([0.0,  -i, 0.0]))
                ref_cell.add(atom.symbol, atom.position + array([0.0, 0.0,  -i]))
                
                ref_cell.add(atom.symbol, atom.position + array([  i,  i, 0.0]))
                ref_cell.add(atom.symbol, atom.position + array([ -i, -i, 0.0]))
                ref_cell.add(atom.symbol, atom.position + array([  i, -i, 0.0]))
                ref_cell.add(atom.symbol, atom.position + array([ -i,  i, 0.0]))
                ref_cell.add(atom.symbol, atom.position + array([0.0,  i,   i]))
                ref_cell.add(atom.symbol, atom.position + array([0.0, -i,  -i]))
                ref_cell.add(atom.symbol, atom.position + array([0.0,  i,  -i]))
                ref_cell.add(atom.symbol, atom.position + array([0.0, -i,   i]))
                ref_cell.add(atom.symbol, atom.position + array([ -i, 0.0, -i]))
                ref_cell.add(atom.symbol, atom.position + array([  i, 0.0, -i]))
                ref_cell.add(atom.symbol, atom.position + array([ -i, 0.0,  i]))
                ref_cell.add(atom.symbol, atom.position + array([  i, 0.0,  i]))                
                
                ref_cell.add(atom.symbol, atom.position + array([ i,  i,  i]))
                ref_cell.add(atom.symbol, atom.position + array([ i, -i,  i]))
                ref_cell.add(atom.symbol, atom.position + array([-i,  i,  i]))
                ref_cell.add(atom.symbol, atom.position + array([ i,  i, -i]))
                ref_cell.add(atom.symbol, atom.position + array([ i, -i, -i]))
                ref_cell.add(atom.symbol, atom.position + array([-i, -i,  i]))
                ref_cell.add(atom.symbol, atom.position + array([-i,  i, -i]))
                ref_cell.add(atom.symbol, atom.position + array([-i, -i, -i]))
        
    def calculate_sro(self):
        reference_supercell = self.supercell.copy()
        self.expand_refcell(reference_supercell, 2)
        total_sro = [0]*6
        for atom1 in self.supercell.atoms:
            distances = []
            for atom2 in reference_supercell.atoms:
                if atom2.symbol == self.part1 or atom2.symbol == self.part2:
                    distances.append((norm(atom2.position - atom1.position), atom2)) 
            distances.sort()
            neighbours =[]
            for distance in distances:
                if neighbours == []:
                    neighbours.append([distance])
                elif distance[0] != neighbours[-1][-1][0]:
                    neighbours.append([distance])
                else:
                    neighbours[-1].append(distance)            
            for i in range(0, 6):
                print len(neighbours[i])
            
            for i in range(1, 6):
                atom_sro = 1
                for neighbour in neighbours[i]:
                    if neighbour[1].symbol == atom1.symbol:
                        atom_sro = atom_sro * 1
                    else:
                        atom_sro = atom_sro * -1
                total_sro[i] = total_sro[i] + atom_sro / float(len(neighbours[i]))

        for i in range(1, len(total_sro)):
            total_sro[i] = total_sro[i] / (len(self.supercell.atoms) / 2.0)

        for i in range(1, len(total_sro)):
            print "%i\t%f" % (i, total_sro[i])  

                    
            
                
if __name__ == "__main__":
    pass
