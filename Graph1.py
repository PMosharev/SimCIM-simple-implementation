import numpy as np
import math
import random
from GraphOperations import *
import time
import copy




def Algor(x, J, n, NSteps, Zita, Noize, Nu0):
    for t in range(NSteps):
        Nu = Nu0*math.tanh(t / n * 6 - 3)

        for i in range(n):

            if x[i] != 1 and x[i] != -1:
                f = Noize*np.random.normal()
                
                Displacement = 0
                
                for j in range(n):
                    Displacement += J[i][j]*x[j]
                
                Deltaxi = Nu * x[i] + Zita * Displacement + f

                if x[i] + Deltaxi >= 1:
                    x[i] = 1
                elif x[i] + Deltaxi <= -1:
                    x[i] = -1
                else:
                    x[i] += Deltaxi

    for i in range(n):
        if x[i] < 0:
            x[i] = -1
        else:
            x[i] = 1

    return x




Zita = - 0.05
NSteps = 1000
Noize = 0.05
Nu0 = 0.5

print('Number of steps = ', NSteps, '\n')


NumberOfFiles = 3
FileNames = []
##
##for i in range(NumberOfFiles):
##    FileNames.append('./Data/SimpleGraph' + str(i+1) + '.txt')

FileNames.append('./Data/G39.txt')
FileNames.append('./Data/G1.txt')
FileNames.append('./Data/G22.txt')

for FileName in FileNames:
    
    with open(FileName) as fil:
        n, m = [int(j) for j in fil.readline().split()]
        
        J = [[0 for i in range(n)] for j in range(n)]

        for k in range(m):
            vert1, vert2, weight = [int(j) for j in fil.readline().split()]
            J[vert1 - 1][vert2 - 1] = weight
            J[vert2 - 1][vert1 - 1] = weight
            
    x = [0 for j in range(n)]

    time3 = time.time()
    
    x = Algor(x, J, n, NSteps, Zita, Noize, Nu0)

    Jnew = copy.deepcopy(J)
    for i in range(len(x)):
        for j in range(i):
            if x[i] != x[j]:
                Jnew[i][j] = 0
                Jnew[j][i] = 0
    
    Cut = 0.0
    for i in range(n):
        for j in range(i):
           Cut += J[i][j] * (1 - x[i] * x[j])
    Cut = Cut * 0.5

    print('Source file: ', FileName)

    print('Cut Value =', Cut)

    time4 = time.time()
    print(time4 - time3)
    #print('Cut Value for random cut = ', RandomCut)
    print()
##    SourceImageName = './Out/Source' + str(i+1) + '.png'
##    ResultImageName = './Out/Result' + str(i+1) + '.png'
##    ImageGraph(nx.DiGraph(np.matrix(J)), SetColors(x), SourceImageName)
##    ImageGraph(nx.DiGraph(np.matrix(Jnew)), SetColors(x), ResultImageName)
        

#OutTexFileName = './Out/OutTexFile.tex'

#CreateTexFile(Zita, NSteps, Noize, NumberOfFiles, FileNames, OutTexFileName)

