import numpy as np
import random
import pylab
import os
import errno

class Percolation:
    def __init__(self):
        self.dim = 20
        self.density = 0.9
        self.lattice = np.zeros((self.dim, self.dim), dtype=int)
        self.totalsites = int((self.dim ** 2) * self.density)
        self.visualisation_output = '/Users/DanLenton/Downloads/PHYS379/Pictures/Percolation'  # Change to route where you want the pictures to be saved
        self.nearestneighbourlist = [[0,1],[0,-1],[1,0],[-1,0]]

    def distribution(self):
        for site in range(self.totalsites):
            randomi = random.randint(0,self.dim - 1)
            randomj = random.randint(0, self.dim - 1)
            self.lattice[randomi,randomj] = 1
        self.generate_lattice()

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
                    for neighbour in self.nearestneighbourlist:
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
                            for neighbour in self.nearestneighbourlist:
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
        pylab.title('Percolation')
        pylab.show
        self.check_path_exists(self.visualisation_output)
        fig.savefig(self.visualisation_output + '/' + 'picture.png')   # Saves picture
        self.clusters()

    def generate_clusters(self): # Produces a picture of the lattice using matplotlib.pyplot

        fig = pylab.figure()
        colourcounter = 0
        for cluster in self.cluster:   # Iterating over every site in the lattice
            print(cluster)
            colourlist = ['b', 'g', 'r', 'c', 'm', 'y']
            if len(cluster) > 8:
                for point in cluster:
                    pylab.plot(point[0], point[1], '.', color=colourlist[colourcounter])    # Occupied sites are blue circles
                    print(colourcounter)
                colourcounter += 1
            else:
                for point in cluster:
                    pylab.plot(point[0], point[1], '.', color='k')    # Occupied sites are blue circle


        axes = pylab.gca()
        axes.set_xlim([-5, 25])
        axes.set_ylim([-5, 25])
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)
        pylab.title('Percolation')
        pylab.show
        self.check_path_exists(self.visualisation_output)
        fig.savefig(self.visualisation_output + '/' +'clusterpicture.png')   # Saves picture

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
                self.spanningcluster()

    def spanningcluster(self):  # Produces a picture of the lattice using matplotlib.pyplot

        fig = pylab.figure()

        for point in self.span:
            pylab.plot(point[0], point[1], '.', color='r')

        axes = pylab.gca()
        axes.set_xlim([-5, 25])
        axes.set_ylim([-5, 25])
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)
        pylab.title('Percolation')
        pylab.show
        self.check_path_exists(self.visualisation_output)
        fig.savefig(self.visualisation_output + '/' + 'spanningpicture.png')

    def check_path_exists(self, path):  # Function that checks the save path exists and if not, creates it
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

P = Percolation()
P.distribution()