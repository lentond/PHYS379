import numpy as np
import pylab
import errno
import os
import random

class Automata:               # Decided to use a class so that variables defined in one function can be accessed from all others without having to pass them.
    def __init__(self):
        self.dim = 20         # Dimension of a square lattice
        self.lattice = np.zeros((self.dim, self.dim), dtype=int)     # Defines an empty square lattice
        self.newsites = np.zeros((self.dim, self.dim), dtype=int)    # Introduced so changes can be made, but earlier changes in each time step do not affect the others.
        self.velocitylattice = np.zeros((self.dim, self.dim), dtype=list)
        self.newvelocities = np.zeros((self.dim, self.dim), dtype=list)
        for i in range(self.dim):
            for j in range(self.dim):
                self.newvelocities[i,j] = []
                self.velocitylattice[i, j] = []
        self.visualisation_output = '/Users/Jack/Documents/Code'   # Change to route where you want the pictures to be saved
        self.Totaltime = 20     # Change to time that lattice is run for
        self.time = 0
        self.evennextcoordinates = [[0, 0], [1, 0], [-1, 0], [0, 1], [-1, 1], [0, -1], [-1, -1]]
        self.oddnextcoordinates = [[0, 0], [1, 0], [-1, 0], [1, 1], [0, 1], [1, -1], [0, -1]]


    def lattice_input(self):        # Function sets up the initial configuration of the lattice
        for i in range(self.dim):       # Iterating over each lattice site
            for j in range(self.dim):
                if (i < 15) and (i >= 5) and (j < 15) and (j >= 5):  # For a central square block
                #if (i % 2 == 1) and (j % 2 == 1):                      # For an alternating grid
                #if i == 10:                                            # For a line
                    self.lattice[i,j] = 1
                    self.newsites[i,j] = 1
                    velgenerator = random.randint(0,8)
                    self.velocitylattice[i,j].append(velgenerator)
                    self.newvelocities[i,j].append(velgenerator)
        self.generate_lattice()

    def evolution(self):                        # Defines how lattice evolves at each time step
        self.newsites = np.copy(self.lattice)
        for i in range(self.dim):               # Iterating over each site in the lattice
            for j in range(self.dim):
                if self.lattice[i,j] >= 1:
                    next = [0,0,0,0]
                    inew = [0,0,0,0]
                    jnew = [0,0,0,0]
                    velnew = [0,0,0,0]
                    vel = self.velocitylattice[i,j]
                    counter = 0
                    while counter < len(vel):
                        vel[counter] = self.velocitylattice[i, j][counter]
                        velnew[counter] = self.rule(vel)[counter]
                        if j % 2 == 0:
                            next[counter] = self.evennextcoordinates[velnew[counter]]
                        if j % 2 == 1:
                            next[counter] = self.oddnextcoordinates[velnew[counter]]
                        next[counter] = self.nextcoordinates[velnew[counter]]
                        inew[counter] = (i+next[counter][0]) % (self.dim)
                        jnew[counter] = (j+next[counter][1]) % (self.dim)
                        #print(jnew)
                        self.newsites[inew[counter],jnew[counter]] += 1
                        #print(self.newvelocities[i,j])
                        del self.newvelocities[i,j][counter]
                        #print(self.newvelocities[i, j])
                        self.newvelocities[inew[counter], jnew[counter]].append(velnew[counter])
                        #print(self.newvelocities[inew[counter], jnew[counter]])
                        counter += 1
                        self.newsites[i, j] -= 1

        #print(self.lattice)
        self.time += 1
        self.lattice = np.copy(self.newsites)
        self.velocitylattice = np.copy(self.newvelocities)
        if self.time <= self.Totaltime: # Stops evolving once time limit is reached
            self.generate_lattice()

    def generate_lattice(self): # Produces a picture of the lattice using matplotlib.pyplot

        fig = pylab.figure()
        for i in range(self.dim):   # Iterating over every site in the lattice
            for j in range(self.dim):
                a = self.lattice[i,j]
                if a >= 1:
                    if j % 2 == 0:
                        pylab.plot([i], [j], '.', color='c')    # Occupied sites are blue circles
                    if j % 2 == 1:
                        pylab.plot([i+1/2], [j], '.', color='c')
                if a == 0:
                    if j % 2 == 0:
                        pylab.plot([i], [j], 'x', color='r')  # Occupied sites are red crosses
                    if j % 2 == 1:
                        pylab.plot([i + 1 / 2], [j], 'x', color='r')


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

    def rule(self, vel):     # Here define the rule for velocities after collisions.
        if len(vel) == 1:
            return vel
        if len(vel) == 2:
            return(vel)
        else:
            return(vel)


    def check_path_exists(self, path):  # Function that checks the save path exists and if not, creates it
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

A = Automata()
A.lattice_input()
