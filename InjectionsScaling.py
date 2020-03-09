import numpy as np
import pylab
import errno
import os
import random
import math


class Automata:

    def __init__(self):
        self.Totaltime = 20
        self.dimstart = 10
        self.dimfinal = 60
        self.diminc = 10
        self.test = 10
        self.flowspeed = 0.5
        self.scale = 4
        self.bdensitystart = 0
        self.bdensityfinal = 1
        self.bdensityinc = 0.1
        self.test = 10

        self.visualisation_output = '/Users/DanLenton/Downloads/PHYS379/Pictures/InjectionsScaling'
        self.time = 0
        self.evennextcoordinates = [[0, 0], [1, 0], [-1, 0], [0, 1], [-1, 1], [0, -1], [-1, -1]]
        self.oddnextcoordinates = [[0, 0], [1, 0], [-1, 0], [1, 1], [0, 1], [1, -1], [0, -1]]


    def lattice_input(self,density,dim):
        self.dim = dim
        self.totalsites = int((self.dim ** 2))
        self.lattice = np.zeros((self.dim, self.dim, self.Totaltime), dtype=int)
        self.velocitylattice = np.zeros((self.dim, self.dim, self.Totaltime), dtype=list)
        self.vxtotal = np.zeros((self.Totaltime), dtype=int)
        self.injectedmomentum = np.zeros((self.Totaltime), dtype=int)
        for i in range(self.dim):
            for j in range(self.dim):
                for k in range(self.Totaltime):
                    self.velocitylattice[i, j, k] = []
        self.barrierdensity = density
        self.fluidparticledensity = (1-self.barrierdensity)/2
        self.fluidparticlenumber = int(self.fluidparticledensity * self.totalsites)
        self.barriersites = int(self.barrierdensity * self.totalsites)
        self.porosity = (self.totalsites - self.barriersites) / self.totalsites
        for site in range(self.barriersites):
            randomi = random.randint(0,self.dim - 1)
            randomj = random.randint(0, self.dim - 1)
            for k in range(self.Totaltime):
                self.lattice[randomi, randomj, k] = -10

        counter = 0
        while counter < self.fluidparticlenumber:
            i = random.randint(0, self.dim - 1)
            j = random.randint(0, self.dim - 1)
            if self.lattice[i, j, 0] == 0:
                self.lattice[i,j,0] = 1
                velgenerator = random.randint(0,6)
                self.velocitylattice[i, j, 0] = [velgenerator]
                #self.velocitylattice[i, j, 0] = [1]
                counter += 1

        self.evolution()

    def evolution(self):
        while self.time < self.Totaltime - 1:
            for i in range(self.dim):
                for j in range(self.dim):

                    if self.lattice[i,j,self.time] != 0:
                        next = [0,0,0,0,0,0,0]
                        inew = [0,0,0,0,0,0,0]
                        jnew = [0,0,0,0,0,0,0]
                        velnew = [0,0,0,0,0,0,0]
                        vel = self.velocitylattice[i,j,self.time]
                        counter = 0
                        while counter < len(vel):
                            if self.lattice[i, j, self.time] >= 0:
                                velnew[counter] = self.rule(vel)[counter]

                                if j % 2 == 0:
                                    next[counter] = self.evennextcoordinates[velnew[counter]]
                                if j % 2 == 1:
                                    next[counter] = self.oddnextcoordinates[velnew[counter]]
                                inew[counter] = (i+next[counter][0]) % (self.dim)
                                jnew[counter] = (j+next[counter][1]) % (self.dim)
                                self.lattice[inew[counter],jnew[counter], self.time + 1] += 1
                                self.velocitylattice[inew[counter], jnew[counter], (self.time + 1)].append(velnew[counter])
                            elif 0 > self.lattice[i, j, self.time] > -10:
                                velnew[counter] = self.barrier(vel)[counter]

                                if j % 2 == 0:
                                    next[counter] = self.evennextcoordinates[velnew[counter]]
                                if j % 2 == 1:
                                    next[counter] = self.oddnextcoordinates[velnew[counter]]
                                inew[counter] = (i + next[counter][0]) % (self.dim)
                                jnew[counter] = (j + next[counter][1]) % (self.dim)
                                self.lattice[inew[counter], jnew[counter], self.time + 1] += 1
                                self.velocitylattice[inew[counter], jnew[counter], (self.time + 1)].append(velnew[counter])
                            counter += 1

            injections = int(((self.flowspeed*self.totalsites) - self.vxtotal[self.time])/self.scale)
            for injection in range(injections):
                randomi = random.randint(0, self.dim - 1)
                randomj = random.randint(0, self.dim - 1)
                if self.lattice[randomi, randomj, self.time + 1] >= 1:
                    if (2 in self.velocitylattice[randomi,randomj, self.time + 1]) & (1 not in self.velocitylattice[randomi,randomj, self.time + 1]):
                        self.velocitylattice[randomi, randomj, self.time + 1].remove(2)
                        self.velocitylattice[randomi, randomj, self.time + 1].append(1)
                        self.injectedmomentum[self.time + 1] += 2
                    if (4 in self.velocitylattice[randomi, randomj, self.time + 1]) & (3 not in self.velocitylattice[randomi, randomj, self.time + 1]):
                        self.velocitylattice[randomi, randomj, self.time + 1].remove(4)
                        self.velocitylattice[randomi, randomj, self.time + 1].append(3)
                        self.injectedmomentum[self.time + 1] += 2
                    if (6 in self.velocitylattice[randomi, randomj, self.time + 1]) & (5 not in self.velocitylattice[randomi, randomj, self.time + 1]):
                        self.velocitylattice[randomi, randomj, self.time + 1].remove(6)
                        self.velocitylattice[randomi, randomj, self.time + 1].append(5)
                        self.injectedmomentum[self.time + 1] += 2
                    if (0 in self.velocitylattice[randomi,randomj, self.time + 1]) & (1 not in self.velocitylattice[randomi,randomj, self.time + 1]):
                        self.velocitylattice[randomi, randomj, self.time + 1].remove(0)
                        self.velocitylattice[randomi, randomj, self.time + 1].append(1)
                        self.injectedmomentum[self.time + 1] += 1

            self.time += 1
        if self.time == self.Totaltime - 1:
            self.quantitycalculator()

    def quantitycalculator(self):
        for k in range(self.Totaltime):
            for i in range(self.dim):
                for j in range(self.dim):
                    if 1 in self.velocitylattice[i, j, k]:
                        if self.lattice[i,j,k] >= 0:        #Only contributions from the pore space
                            self.vxtotal[k] += 1
                    if 3 in self.velocitylattice[i, j, k]:
                        if self.lattice[i, j, k] >= 0:
                            self.vxtotal[k] += 1
                    if 5 in self.velocitylattice[i, j, k]:
                        if self.lattice[i, j, k] >= 0:
                            self.vxtotal[k] += 1
                    if 2 in self.velocitylattice[i, j, k]:
                        if self.lattice[i, j, k] >= 0:
                            self.vxtotal[k] -= 1
                    if 4 in self.velocitylattice[i, j, k]:
                        if self.lattice[i, j, k] >= 0:
                            self.vxtotal[k] -= 1
                    if 6 in self.velocitylattice[i, j, k]:
                        if self.lattice[i, j, k] >= 0:
                            self.vxtotal[k] -= 1
        #print(self.vxtotal)
        print(self.barrierdensity)
        self.vxtotalavg = sum(self.vxtotal)/self.Totaltime
        print('The time averaged horizontal velocity is ' + str(self.vxtotalavg))
        self.momentumavg = sum(self.injectedmomentum)/(self.Totaltime - 1)
        #print(self.injectedmomentum)
        print('The time averaged injected momentum is ' + str(self.momentumavg))
        self.permeability = self.porosity*self.vxtotalavg/self.momentumavg
        print('The permeability is ' + str(self.permeability))
        self.coordinates = [(1-self.barrierdensity), self.permeability]

    def rule(self, vel):
        collisiondict = {'0100000': '0100000', '0010000': '0010000', '0001000': '0001000', '0000100': '0000100',
                         '0000010': '0000010', '0000001': '0000001',
                         '0110000': '0001001', '0101000': '0101000', '0100100': '1001000', '0100010': '0100010',
                         '0100001': '1000010', '0011000': '1000100', '0010100': '0010100', '0010010': '1000001',
                         '0010001': '0010001', '0001100': '0001100', '0001010': '1100000', '0001001': '0000110',
                         '0000110': '0110000', '0000101': '1010000', '0000011': '0000011', '0111000': '0001110',
                         '0110100': '0001101', '0110010': '0001011', '0110001': '0000111', '0101100': '0101100',
                         '0101010': '0101010', '0101001': '0100110', '0100110': '0101001', '0100101': '0011010',
                         '0100011': '0100011', '0011100': '0011100', '0011010': '0100101', '0011001': '0010110',
                         '0010110': '0011001', '0010101': '0010101', '0010011': '0010011', '0001110': '0111000',
                         '0001101': '0110100', '0001011': '0110010', '0000111': '0110001', '0111100': '0111100',
                         '0111010': '0111010', '0111001': '0110110', '0110110': '0001111', '0110101': '0110101',
                         '0110011': '0110011', '0101110': '0101110', '0101101': '0101101', '0101011': '0101011',
                         '0100111': '0100111', '0011110': '0011110', '0011101': '0011101', '0011011': '0011011',
                         '0010111': '0010111', '0001111': '0111001', '0111110': '1101101', '0111101': '1011110',
                         '0111011': '1100111', '0110111': '1011011', '0101111': '1111010', '0011111': '1110101',
                         '0111111': '0111111', '0000000': '0000000'}

        dualcollisiondict = {}
        for key in collisiondict:
            keylist = self.split(key)
            entrylist = self.split(collisiondict[key])
            for element in range(len(keylist)):
                keylist[element] += 1
                keylist[element] = keylist[element] % 2
            for element in range(len(entrylist)):
                entrylist[element] += 1
                entrylist[element] = entrylist[element] % 2
            key = self.join(keylist)
            item = self.join(entrylist)
            dualcollisiondict.update({key: item})

        if (len(vel) <= 1):
            return (vel)
        else:
            vel.sort()
            stringvel = self.veltobinary(vel)
            if vel[0] == 0:
                newstringvel = dualcollisiondict[stringvel]
            else:
                newstringvel = collisiondict[stringvel]
            newvel = self.binarytovel(newstringvel)
            return (newvel)

    def barrier(self, vel):


        newvel = []
        for vel in vel:
            if vel == 1:
                newvel.append(2)
            if vel == 2:
                newvel.append(1)
            if vel == 3:
                newvel.append(6)
            if vel == 4:
                newvel.append(5)
            if vel == 5:
                newvel.append(4)
            if vel == 6:
                newvel.append(3)
        return(newvel)


    def split(self, word):
        return [int(char) for char in word]

    def join(self, list):
        word = ''
        for number in list:
            word += str(number)
        return (word)

    def veltobinary(self, vel):
        binary = ''
        count = 0
        while count < 7:
            if count in vel:
                binary += '1'
            else:
                binary += '0'
            count += 1
        return(binary)

    def binarytovel(self, binary):
        vel = []
        splitbinary = self.split(binary)
        counter = 0
        for number in splitbinary:
            if number == 1:
                vel.append(counter)
            counter += 1
        return (vel)


    def check_path_exists(self, path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

A = Automata()
Coordinates = []
dimlist = []
counter = 0
for dim in np.arange(A.dimstart, A.dimfinal, A.diminc):
    dimlist.append(dim)
    for bdensity in np.arange(A.bdensitystart,A.bdensityfinal,A.bdensityinc):
        Coordinates.append([])
        samedensitycoords = []
        for test in range(A.test):
            A = Automata()
            A.lattice_input(bdensity,dim)
            samedensitycoords.append(A.coordinates)
        sum1 = 0
        sum2 = 0
        for i in range(len(samedensitycoords)):
            sum1 += samedensitycoords[i][0]
            sum2 += samedensitycoords[i][1]
        avg1 = sum1/len(samedensitycoords)
        avg2 = sum2/len(samedensitycoords)
        Coordinates[counter].append([avg1,avg2])
    counter+=1

fig = pylab.figure()
colourcounter = 0
colourlist = ['b','g','r','c','m','y','k','w']
for list in Coordinates:
    for i in range(len(list)):
        if i == 0:
            pylab.plot([math.log(list[i][0])], [math.log(list[i][1])], 'x', color=colourlist[colourcounter%7], label=dimlist[colourcounter])
        else:
            pylab.plot([math.log(list[i][0])], [math.log(list[i][1])], 'x', color=colourlist[colourcounter % 7])
    colourcounter += 1
pylab.legend(loc=0, fontsize=10.5, handletextpad=0.1)
axes = pylab.gca()
pylab.title('log-log plot')
pylab.show
A.check_path_exists(A.visualisation_output)
fig.savefig(A.visualisation_output + '/' + 'logpicture.png')

fig = pylab.figure()
colourcounter = 0
for list in Coordinates:
    for i in range(len(list)):
        if i == 0:
            pylab.plot([list[i][0]], [list[i][1]], 'x', color=colourlist[colourcounter%7], label=dimlist[colourcounter])
        else:
            pylab.plot([list[i][0]], [list[i][1]], 'x', color=colourlist[colourcounter % 7])
    colourcounter += 1
pylab.legend(loc=0, fontsize=10.5, handletextpad=0.1)
axes = pylab.gca()
pylab.title('Normal Plot')
pylab.show
A.check_path_exists(A.visualisation_output)
fig.savefig(A.visualisation_output + '/' + 'normalpicture.png')

