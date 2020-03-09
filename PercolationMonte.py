import numpy as np
import random
import pylab
import os
import errno

class Percolation:
    def __init__(self):
        self.dim = 300
        self.densitystart = 0.68
        self.densityfinal = 0.71
        self.densityinc = 0.001
        self.test = 50
        self.successes = 0
        self.visualisation_output = '/Users/DanLenton/Downloads/PHYS379/Pictures/PercolationMonte'  # Change to route where you want the pictures to be saved
        self.evennextcoordinates = [[1, 0], [-1, 0], [0, 1], [-1, 1], [0, -1], [-1, -1]]
        self.oddnextcoordinates = [[1, 0], [-1, 0], [1, 1], [0, 1], [1, -1], [0, -1]]

    def distribution(self,density,testnumber):
        self.testnumber = testnumber
        self.density = density
        self.lattice = np.zeros((self.dim, self.dim), dtype=int)
        self.totalsites = int((self.dim ** 2) * self.density)
        for site in range(self.totalsites):
            randomi = random.randint(0,self.dim - 1)
            randomj = random.randint(0, self.dim - 1)
            self.lattice[randomi,randomj] = 1
        self.clusters()

    def clusters(self):

        self.cluster = []
        neighbour = 0
        counter = 0
        for i in range(self.dim):   # Iterating over every site in the lattice
            for j in range(self.dim):
                if self.lattice[i,j] == 1:
                    self.cluster.append([[i,j]])
                    self.lattice[i,j] -= 1
                    newsites = []
                    if j % 2 == 0:
                        for neighbour in self.evennextcoordinates:
                            inew = (i + neighbour[0])
                            jnew = (j + neighbour[1])
                            if (0 <= inew <= 19) and (0 <= jnew <= 19):
                                if self.lattice[inew,jnew] == 1:
                                    self.cluster[counter].append([inew,jnew])
                                    newsites.append([inew,jnew])
                                    self.lattice[inew, jnew] -= 1
                    elif j % 2 == 1:
                        for neighbour in self.oddnextcoordinates:
                            inew = (i + neighbour[0])
                            jnew = (j + neighbour[1])
                            if (0 <= inew <= 19) and (0 <= jnew <= 19):
                                if self.lattice[inew,jnew] == 1:
                                    self.cluster[counter].append([inew,jnew])
                                    newsites.append([inew,jnew])
                                    self.lattice[inew, jnew] -= 1

                    while len(newsites) >= 1:
                        newsitescopy = []
                        for newsite in newsites:
                            if newsite[1] % 2 == 0:
                                for neighbour in self.evennextcoordinates:
                                    inew = (newsite[0] + neighbour[0])
                                    jnew = (newsite[1] + neighbour[1])
                                    if (0 <= inew <= 19) and (0 <= jnew <= 19):
                                        if self.lattice[inew, jnew] == 1:
                                            self.cluster[counter].append([inew, jnew])
                                            newsitescopy.append([inew, jnew])
                                            self.lattice[inew, jnew] -= 1
                            elif newsite[1] % 2 == 1:
                                for neighbour in self.oddnextcoordinates:
                                    inew = (newsite[0] + neighbour[0])
                                    jnew = (newsite[1] + neighbour[1])
                                    if (0 <= inew <= 19) and (0 <= jnew <= 19):
                                        if self.lattice[inew, jnew] == 1:
                                            self.cluster[counter].append([inew, jnew])
                                            newsitescopy.append([inew, jnew])
                                            self.lattice[inew, jnew] -= 1
                        newsites = newsitescopy
                    counter += 1
        #print(self.cluster)
        self.generate_clusters()

    def generate_clusters(self): # Produces a picture of the lattice using matplotlib.pyplot

        for cluster in self.cluster:
            clusterspan = []
            Leftedge = False
            Rightedge =False
            Bottomedge =False
            Topedge =False
            for point in cluster:
                if point[0] == 0:
                    Leftedge = True
                elif point[0] == 19:
                    Rightedge = True
                if point[1] == 0:
                    Bottomedge = True
                elif point[1] == 19:
                    Topedge = True
            if (Rightedge == True and Leftedge == True) or (Bottomedge == True and Topedge == True):
                self.span = cluster
                #print('There is a spanning cluster for density = ' + str(self.density) + ' test ' + str(self.testnumber))
                self.successes += 1


    def check_path_exists(self, path):  # Function that checks the save path exists and if not, creates it
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

P = Percolation()
Densityno = (P.densityfinal - P.densitystart)/P.densityinc
Ratio = []
densitylist =[]
for density in np.arange(P.densitystart,P.densityfinal,P.densityinc):
    densitylist.append(density)
    P = Percolation()
    for testnumber in range(P.test - 1):
        P.distribution(density,testnumber)
    rate = P.successes/P.test
    Ratio.append(rate)
print(Ratio)


fig = pylab.figure()
for i in range(len(Ratio)):
    pylab.plot([density[i]], [Ratio[i]], 'x', color='r')    # Occupied sites are blue circles

    axes = pylab.gca()
    axes.set_xlim([-5, 20])
    axes.set_ylim([-0.05, 1.3])
    pylab.title('PercolationMonte')
    pylab.show
    P.check_path_exists(P.visualisation_output)
    fig.savefig(P.visualisation_output + '/' + 'picture.png')   # Saves picture
