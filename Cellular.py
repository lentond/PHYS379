import numpy as np
import pylab
import errno
import os
import random

class Automata:
    def __init__(self):
        self.dim = 20
        self.lattice = np.zeros((self.dim, self.dim), dtype=np.float64)
        self.newsites = np.zeros((self.dim, self.dim), dtype=np.float64)
        self.visualisation_output = '/Users/DanLenton/Downloads/PHYS379/Pictures'
        self.Totaltime = 10
        self.time = 0
        self.nearestneighbourcoordinates = [[0,1],[0,-1],[1,0],[-1,0],[1,-1],[-1,1],[1,1],[-1,-1]]


    def lattice_input(self):
        for i in range(self.dim):
            for j in range(self.dim):
                if (i < 15) and (i >= 5) and (j < 15) and (j >= 5):  # For a central square block
                #if (i % 2 == 1) and (j % 2 == 1):                      # For an alternating grid
                #if i == 10:                                            # For a line
                    self.lattice[i,j] = 1
                    self.newsites[i,j] = 1
        self.generate_lattice()

    def evolution(self):
        self.newsites = np.copy(self.lattice)
        newfilled = []
        for i in range(self.dim):
            for j in range(self.dim):
                neighbourcount = 0      # A simple model could depend on just the number of occupied neighbours
                belowcount = 0          # Other models may depend on the j coordinate of the neighbours
                levelcount = 0
                abovecount = 0
                straightbelowcount = 0
                straightabovecount = 0
                emptyneighbourlist = []
                counter = 0
                for element in self.nearestneighbourcoordinates:
                    a = self.lattice[(i + element[0]) % self.dim, (j + element[1]) % self.dim]  # Modulo self dim there to create periodic boundary conditions
                    neighbourcount += a
                    if a == 0 and self.lattice[i,j] == 1:
                        emptyneighbourlist.append(element)
                    if element[1] == -1:
                        belowcount += a
                    elif element[1] == 0:
                        levelcount += a
                    elif element[1] == 1:
                        abovecount += a
                    if element[1] == -1 and element[0] == 0:
                        straightbelowcount += a
                    if element[1] == 1 and element[0] == 0:
                        straightabovecount += a
                if len(emptyneighbourlist) != 0:
                    randcoordinate = random.randint(0,len(emptyneighbourlist) - 1)
                    if [(i + emptyneighbourlist[randcoordinate][0]) % self.dim, (j + emptyneighbourlist[randcoordinate][1]) % self.dim] not in newfilled:
                        self.newsites[i, j] = 0
                        self.newsites[(i + emptyneighbourlist[randcoordinate][0]) % self.dim, (j + emptyneighbourlist[randcoordinate][1]) % self.dim] = 1
                        newfilled.append([(i + emptyneighbourlist[randcoordinate][0]) % self.dim, (j + emptyneighbourlist[randcoordinate][1]) % self.dim])
                #if straightabovecount == 1 and straightbelowcount == 0:
                    #self.newsites[i,j] = 1
                #if straightbelowcount == 1 and straightabovecount == 0:
                    #self.newsites[i,j] = 0
        self.time += 1
        self.lattice = np.copy(self.newsites)
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