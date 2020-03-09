import numpy as np
import random
import pylab
import os
import errno

class Percolation:
    def __init__(self):
        self.density = 0.7
        self.dimstart = 50
        self.dimfinal = 500
        self.diminc = 30
        self.test = 70
        self.successes = 0
        self.visualisation_output = '/Users/DanLenton/Downloads/PHYS379/Pictures/PercolationScaling'  # Change to route where you want the pictures to be saved
        self.evennextcoordinates = [[1, 0], [-1, 0], [0, 1], [-1, 1], [0, -1], [-1, -1]]
        self.oddnextcoordinates = [[1, 0], [-1, 0], [1, 1], [0, 1], [1, -1], [0, -1]]

    def distribution(self, dim, testnumber):
        self.testnumber = testnumber
        self.lattice = np.zeros((dim, dim), dtype=int)
        self.totalsites = int((dim ** 2) * self.density)
        for site in range(self.totalsites):
            randomi = random.randint(0, dim - 1)
            randomj = random.randint(0, dim - 1)
            self.lattice[randomi,randomj] = 1
        self.clusters(dim)

    def clusters(self,dim):

        self.cluster = []
        neighbour = 0
        counter = 0
        for i in range(dim):   # Iterating over every site in the lattice
            for j in range(dim):
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
Dimno = (P.dimfinal - P.dimstart)/P.diminc
Ratio = []
dimlist = []
inversedimlist =[]
for dim in np.arange(P.dimstart,P.dimfinal,P.diminc):
    dimlist.append(dim)
    inversedimlist.append(float(1/dim))
    P = Percolation()
    for testnumber in range(P.test - 1):
        P.distribution(dim,testnumber)
    rate = P.successes/P.test
    Ratio.append(rate)
    print(dim)
print(Ratio)


fig = pylab.figure()
for i in range(len(Ratio)):
    pylab.plot([dimlist[i]], [Ratio[i]], 'x', color='r')    # Occupied sites are blue circles

    axes = pylab.gca()
    pylab.title('PercolationScaling')
    pylab.show
    P.check_path_exists(P.visualisation_output)
    fig.savefig(P.visualisation_output + '/' + 'picture.png')   # Saves picture

fig = pylab.figure()
for i in range(len(Ratio)):
    pylab.plot([inversedimlist[i]], [Ratio[i]], 'x', color='r')    # Occupied sites are blue circles

    axes = pylab.gca()
    pylab.title('PercolationScalingInverse')
    pylab.show
    P.check_path_exists(P.visualisation_output)
    fig.savefig(P.visualisation_output + '/' + 'inversepicture.png')   # Saves picture
