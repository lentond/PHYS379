import numpy as np
import pylab
import errno
import os
import random

class Automata:               # Decided to use a class so that variables defined in one function can be accessed from all others without having to pass them.
    def __init__(self):
        self.dim = 20         # Dimension of a square lattice
        self.Totaltime = 20  # Change to time that lattice is run for
        self.lattice = np.zeros((self.dim, self.Totaltime), dtype=np.float64)     # Defines an empty square lattice
        self.visualisation_output = '/Users/DanLenton/Downloads/PHYS379/Pictures/OneDimension'   # Change to route where you want the pictures to be saved
        self.time = 0
        self.nearestneighbourcoordinates = [-1,1]


    def lattice_input(self):        # Function sets up the initial configuration of the lattice
        for i in range(self.dim):       # Iterating over each lattice site
                if (i==10):  # For a central square block
                #if (i % 2 == 1) and (j % 2 == 1):                      # For an alternating grid
                #if i == 10:                                            # For a line
                    self.lattice[i,0] = 1
        self.evolution()

    def evolution(self):                        # Defines how lattice evolves at each time step
        while self.time < self.Totaltime - 1:
            for i in range(self.dim):
                neighbourcount = 0      # A simple model could depend on just the number of occupied neighbours

                for element in self.nearestneighbourcoordinates:
                    a = self.lattice[(i + element) % self.dim, self.time]  # Modulo self dim there to create periodic boundary conditions
                    neighbourcount += a     # Sums the number of filled sites around a site

                if neighbourcount >= 1:
                    self.lattice[i, self.time + 1] = 1
                else:
                    self.lattice[i, self.time + 1] = 0
            self.time += 1

        self.generate_lattice()

    def generate_lattice(self): # Produces a picture of the lattice using matplotlib.pyplot

        fig = pylab.figure()
        for i in range(self.dim):   # Iterating over every site in the lattice
            for j in range(self.Totaltime):
                a = self.lattice[i,j]
                if a == 1:
                    pylab.plot([i], [j], '.', color='c')    # Occupied sites are blue circles
                if a == 0:
                    pylab.plot([i], [j], 'x', color='r')    # Unoccupied sites are blue circles

        axes = pylab.gca()
        axes.set_xlim([-5, 25])
        axes.set_ylim([-5, 25])
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)
        pylab.title('Filler Title')
        pylab.show
        self.check_path_exists(self.visualisation_output)
        fig.savefig(self.visualisation_output + '/' + 'picture.png')   # Saves picture

    def check_path_exists(self, path):  # Function that checks the save path exists and if not, creates it
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

A = Automata()
A.lattice_input()