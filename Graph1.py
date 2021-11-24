import numpy as np
import math
import random
from GraphOperations import *


def phi(xi, Deltaxi):
    if xi + Deltaxi < 1 and xi + Deltaxi > -1:
        return xi + Deltaxi
    elif xi + Deltaxi >= 1:
        return 1
    else:
        return -1

def nu(t, n):
    return 0.5*math.tanh(t / n * 6 - 3)

def DeltaXi(x, i, nu, Zita, J, f):
    Displacement = 0
    for j in range(len(x)):
        Displacement += J[i][j]*x[j]
    return nu * x[i] + Zita * Displacement + f

def Algor(x, J, NSteps, Zita, Noize):
    for t in range(NSteps):
        Nu = nu(t, NSteps)

        for i in range(len(x)):
            f = Noize*np.random.normal()
            Deltaxi = DeltaXi(x, i, Nu, Zita, J, f)
            x[i] = phi(x[i], Deltaxi)
    return x

def CutValue(x, J, n):
    Cut = 0.0
    for i in range(n):
        for j in range(i):
           Cut += J[i][j] * (1 - x[i] * x[j])
    Cut = Cut * (- 0.5)
    return Cut


Zita = - 0.05
NSteps = 1000
Noize = 0.00001

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
    J = AdjMatrixFromFile(FileName)

    with open(FileName) as fil:
        n = int(fil.readline().split()[0])
    x = [0 for j in range(n)]
    x = Algor(x, J, NSteps, Zita, Noize)
    RandX = [random.choice([-1, 1]) for j in range(n)]
    Jnew = ModifyMatrix(J,x)
    Cut = CutValue(x, J, n)
    RandomCut = CutValue(RandX, J, n)
    print('Source file: ', FileName)
    #print(x)
    print('Cut Value =', Cut)
    print('Cut Value for random cut = ', RandomCut)
    print()
##    SourceImageName = './Out/Source' + str(i+1) + '.png'
##    ResultImageName = './Out/Result' + str(i+1) + '.png'
##    ImageGraph(nx.DiGraph(np.matrix(J)), SetColors(x), SourceImageName)
##    ImageGraph(nx.DiGraph(np.matrix(Jnew)), SetColors(x), ResultImageName)
        

OutTexFileName = './Out/OutTexFile.tex'

#CreateTexFile(Zita, NSteps, Noize, NumberOfFiles, FileNames, OutTexFileName)

