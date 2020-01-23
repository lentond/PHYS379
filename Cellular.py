import numpy as np
import pylab
import errno
import os
import random

class Automata:               # Decided to use a class so that variables defined in one function can be accessed from all others without having to pass them.
    def __init__(self):
        self.dim = 20         # Dimension of a square lattice
        self.lattice = np.zeros((self.dim, self.dim), dtype=np.float64)     # Defines an empty square lattice
        self.newsites = np.zeros((self.dim, self.dim), dtype=np.float64)    # Introduced so changes can be made, but earlier changes in each time step do not affect the others.
        self.visualisation_output = '/Users/DanLenton/Downloads/PHYS379/Pictures'   # Change to route where you want the pictures to be saved
        self.Totaltime = 20     # Change to time that lattice is run for
        self.time = 0
        self.nearestneighbourcoordinates = [[0,1],[0,-1],[1,0],[-1,0],[1,-1],[-1,1],[1,1],[-1,-1]]  #Defines the locations relative to each site that affect each site


    def lattice_input(self):        # Function sets up the initial configuration of the lattice
        for i in range(self.dim):       # Iterating over each lattice site
            for j in range(self.dim):
                if (i < 15) and (i >= 5) and (j < 15) and (j >= 5):  # For a central square block
                #if (i % 2 == 1) and (j % 2 == 1):                      # For an alternating grid
                #if i == 10:                                            # For a line
                    self.lattice[i,j] = 1
                    self.newsites[i,j] = 1
        self.generate_lattice()

    def evolution(self):                        # Defines how lattice evolves at each time step
        self.newsites = np.copy(self.lattice)
        newfilled = []                          # List to record which sites become occupied upon evolution so they are not 'double occupied'
        for i in range(self.dim):               # Iterating over each site in the lattice
            for j in range(self.dim):
                neighbourcount = 0      # A simple model could depend on just the number of occupied neighbours
                belowcount = 0          # Other models may depend on the j coordinate of the neighbours
                levelcount = 0
                abovecount = 0
                straightbelowcount = 0
                straightabovecount = 0
                emptyneighbourlist = []     # A list in which to put the relative coordinates of all the empty sites surrounding a filled site
                counter = 0
                for element in self.nearestneighbourcoordinates:
                    a = self.lattice[(i + element[0]) % self.dim, (j + element[1]) % self.dim]  # Modulo self dim there to create periodic boundary conditions
                    neighbourcount += a     # Sums the number of filled sites around a site
                    if a == 0 and self.lattice[i,j] == 1:
                        emptyneighbourlist.append(element)  # Sums the number of empty sites around a filled site
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
                    randcoordinate = random.randint(0,len(emptyneighbourlist) - 1)  # Used to randomly select an empty site surrounding a filled site
                    if [(i + emptyneighbourlist[randcoordinate][0]) % self.dim, (j + emptyneighbourlist[randcoordinate][1]) % self.dim] not in newfilled:   # Used to ensure that sites are not double filled
                        self.newsites[i, j] = 0     # Emptying the filled site
                        self.newsites[(i + emptyneighbourlist[randcoordinate][0]) % self.dim, (j + emptyneighbourlist[randcoordinate][1]) % self.dim] = 1   # Occupying the empty site
                        newfilled.append([(i + emptyneighbourlist[randcoordinate][0]) % self.dim, (j + emptyneighbourlist[randcoordinate][1]) % self.dim])
                #if straightabovecount == 1 and straightbelowcount == 0:
                    #self.newsites[i,j] = 1
                #if straightbelowcount == 1 and straightabovecount == 0:
                    #self.newsites[i,j] = 0
        self.time += 1
        self.lattice = np.copy(self.newsites)
        if self.time <= self.Totaltime: # Stops evolving once time limit is reached
            self.generate_lattice()

    def generate_lattice(self): # Produces a picture of the lattice using matplotlib.pyplot

        fig = pylab.figure()
        for i in range(self.dim):   # Iterating over every site in the lattice
            for j in range(self.dim):
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
        fig.savefig(self.visualisation_output + '/' + str(self.time) + 'picture.png')   # Saves picture
        self.evolution()

    def check_path_exists(self, path):  # Function that checks the save path exists and if not, creates it
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

A = Automata()
A.lattice_input()