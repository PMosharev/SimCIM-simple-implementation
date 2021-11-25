import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math
import random

import time
import copy

# implementation of SimCIM algorythm from article https://arxiv.org/pdf/1901.08927.pdf (by Tiunov et. al)


def Algor(x, J, n, NSteps, Zeta, Noize, Nu0):
    for t in range(NSteps):
        
        Nu = Nu0*math.tanh(t / n * 6 - 3)     # pump-loss factor, Fig2 (b) in the article

        for i in range(n):

            if x[i] != 1 and x[i] != -1:
                
                f = Noize*np.random.normal()
                
                Displacement = 0
                
                for j in range(n):
                    Displacement += J[i][j]*x[j]
                
                Deltaxi = Nu * x[i] + Zeta * Displacement + f     # Equation (5) in the article

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




Zeta = - 0.05
NSteps = 1000
Noize = 0.05
Nu0 = 0.5

print('Number of steps = ', NSteps)
print('Zeta = ', Zeta)
print('Noize parameter = ', Noize)
print('Nu0 = ', Nu0, '\n')


Res = open('Results.txt', 'a')
Res.write('================================================================ \n')
Res.write('Number of steps = ' + str(NSteps) + '\n')
Res.write('Zeta = ' + str(Zeta) + '\n')
Res.write('Noize parameter = ' + str(Noize) + '\n')
Res.write('Nu0 = ' + str(Nu0) + '\n')

Res.write('\n')


FileNames = []   

# Uncomment this to try program on small graphs. (Set Noise = 0.000005 for better results in this case)

##NumberOfFiles = 6
##for i in range(NumberOfFiles):
##    FileNames.append('./Data/SimpleGraph' + str(i+1) + '.txt')


FileNames.append('./Data/G1.txt')
#FileNames.append('./Data/G2.txt')
#FileNames.append('./Data/G7.txt')
FileNames.append('./Data/G22.txt')
#FileNames.append('./Data/G39.txt')




for FileName in FileNames:
    
    with open(FileName) as fil:
        n, m = [int(j) for j in fil.readline().split()]
        
        J = [[0 for i in range(n)] for j in range(n)]

        for k in range(m):
            vert1, vert2, weight = [int(j) for j in fil.readline().split()]
            J[vert1 - 1][vert2 - 1] = weight
            J[vert2 - 1][vert1 - 1] = weight
            
    x = [0 for j in range(n)]

    print('Source file: ', FileName)
    print('Number of vertices = ', n)
    print('Work started')
    Res.write('Source file: ' + FileName + '\n')
    Res.write('Number of vertices: ' + str(n) + '\n')
    


    time3 = time.time()
    
    x = Algor(x, J, n, NSteps, Zeta, Noize, Nu0)

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

    time4 = time.time()

    
    print('Cut Value =', Cut)    
    print('Time spent: ', round(time4 - time3, 6), ' seconds \n')


    Res.write('Cut Value =' + str(Cut) + '\n')
    Res.write('Time spent: ' + str(round(time4 - time3, 6)) + ' seconds' + '\n')
    Res.write('\n \n')
    


    if n < 50: # Draw images for small graph

        Colors = []
        for i in x:
            if i == -1:
                Colors.append('red')
            elif i == 1:
                Colors.append('green')
            else:
                Colors.append('blue')

        SourceImageName = './Images/' + FileName[7:-4] + '_Original' + '.png'
        nx.draw(nx.DiGraph(np.matrix(J)), node_color = Colors, with_labels=True)
        plt.savefig(SourceImageName)
        plt.clf()
        
        
        ResultImageName = './Images/' + FileName[7:-4] + '_Result' + '.png'
        nx.draw(nx.DiGraph(np.matrix(Jnew)), node_color = Colors, with_labels=True)
        plt.savefig(ResultImageName)
        plt.clf()

        
        

        
Res.close()

        



