import numpy as np
import pylab
import errno
import os

class Automata:
    def __init__(self):
        self.dim = 20
        self.lattice = np.zeros((self.dim, self.dim), dtype=np.float64)
        self.visualisation_output = '/Users/DanLenton/Downloads/PHYS379/Pictures'
        self.Totaltime = 10
        self.time = 0


    def lattice_input(self):
        for i in range(self.dim):
            for j in range(self.dim):
                if (i < 15) and (i > 5) and (j < 15) and (j > 5):
                    self.lattice[i,j] = 1
        self.generate_lattice()

    def evolution(self):
        for i in range(self.dim):
            for j in range(self.dim):
                neighbourcount = 0
                self.nearestneighbourcoordinates = [[i,j+1],[i,j-1],[i+1,j+1],[i+1,j-1],[i+1,j],[i-1,j+1],[i-1,j-1],[i-1,j]]
                for coordinate in self.nearestneighbourcoordinates:
                    if (coordinate[0]>=0) and (coordinate[1]>=0) and (coordinate[0]<self.dim) and (coordinate[1]<self.dim):
                        neighbourcount += self.lattice[coordinate[0],coordinate[1]]
                if neighbourcount == 2:
                    self.lattice[i,j] = 1
                elif neighbourcount <= 1:
                    self.lattice[i,j] = 0
        self.time += 1
        if self.time <= 10:
            self.generate_lattice()

    def generate_lattice(self):

        fig = pylab.figure()
        for i in range(self.dim):
            for j in range(self.dim):
                a = self.lattice[i,j]
                if a == 1:
                    pylab.plot([i], [j], '.', color='c')
                if a == 0:
                    pylab.plot([i], [j], 'x', color='r')

        axes = pylab.gca()
        axes.set_xlim([-5, 25])
        axes.set_ylim([-5, 25])
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)
        pylab.title('Filler Title')
        pylab.show
        self.check_path_exists(self.visualisation_output)
        fig.savefig(self.visualisation_output + '/' + str(self.time) + 'picture.png')
        self.evolution()

    def check_path_exists(self, path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

A = Automata()
A.lattice_input()