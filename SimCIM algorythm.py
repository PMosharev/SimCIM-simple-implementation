import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math
import random

import time
import copy

# implementation of SimCIM algorythm from article https://arxiv.org/pdf/1901.08927.pdf (by Tiunov et. al)

class MyGraph:
    def __init__(self, WeightedVertices = False):

        self.J = np.zeros(0)        
        
        self.V = np.zeros(0)
        self.x = np.zeros(0)
            
    def Upload(self, FileName, WeightedVertices = False):
        with open(FileName) as fil:
            n, m = [int(j) for j in fil.readline().split()]

            self.n = n
            self.m = m

            
            self.x = np.zeros(n)
            J = np.zeros(shape = (n,n), dtype = int)

            for i in range(m):
                vert1, vert2, weight = [int(j) for j in fil.readline().split()]
                J[vert1 - 1][vert2 - 1] = weight
                J[vert2 - 1][vert1 - 1] = weight

            self.J = J

            if WeightedVertices:
                for i in range(n):
                    _, self.V[i] = [int(j) for j in fil.readline().split()]
            else:
                self.V = np.ones(n)

                    
    def Draw(self, FileName, ):
        Colors = []
        for i in self.x:
            if i == -1:
                Colors.append('red')
            elif i == 1:
                Colors.append('green')
            else:
                Colors.append('blue')

        SourceImageName = './Images/' + FileName[7:-4] + '_Original' + '.png'
        GSource = nx.Graph(np.matrix(self.J))
        plt.figure(figsize = (self.n // 3 + 5, self.n // 3 + 5))
        nx.draw(GSource, pos = nx.circular_layout(GSource), with_labels=True)
        plt.savefig(SourceImageName)
        plt.clf()              
        

        
        ResultImageName = './Images/' + FileName[7:-4] + '_Result' + '.png'
        
        GResult = nx.Graph(np.matrix(Jnew))
        nx.draw(GResult, pos = nx.spring_layout(GResult), node_color = Colors, with_labels=True)
        plt.savefig(ResultImageName)
        plt.clf()

        nx.write_gexf(GSource, './Results/' + FileName[7:-4] + '_Original' + '.gexf')
        nx.write_gexf(GSource, './Results/' + FileName[7:-4] + '_Result' + '.gexf')
                    




def SimCIM(J, x, n, NSteps = 1000, Nu0 = -0.5, Zeta = -0.05, Noize = 0.005):

    print('Number of steps = ', NSteps)
    print('Zeta = ', Zeta)
    print('Noize parameter = ', Noize)
    print('Nu0 = ', Nu0, '\n')


    Res = open('./Results/Results.txt', 'a')
    Res.write('================================================================ \n')
    Res.write('Number of steps = ' + str(NSteps) + '\n')
    Res.write('Zeta = ' + str(Zeta) + '\n')
    Res.write('Noize parameter = ' + str(Noize) + '\n')
    Res.write('Nu0 = ' + str(Nu0) + '\n')
    Res.write('\n')
    Res.close()

    for t in range(NSteps):

        Nu = Nu0*(1 - math.tanh(t / NSteps * 6 - 3))     # pump-loss factor, Fig2 (b) in the article
        fgen = (np.random.normal() for i in range(n))
        f = np.fromiter(fgen, float) * Noize
        
        x += Nu * x +  Zeta * x.dot(J) + f

        for i in range(n):     # can I get rid of such direct elementwise checking?
            if x[i] > 1:
                x[i] = 1
            elif x[i] < -1:
                x[i] = -1


    for i in range(n):
        if x[i] < 0:
            x[i] = -1
        else:
            x[i] = 1
    return x

    
def MaxCut(G):
     return SimCIM(G.J, G.x, G.n)

def MinCut(G, Ab = 1):
    return SimCIM(-G.J + G.V * Ab , G.x, G.n)
    







Res = open('./Results/Results.txt', 'a')



FileNames = []   

# Uncomment this to try program on small graphs. (Set Noize = 0.000005 for better results in this case)
##
##NumberOfFiles = 6
##for i in range(NumberOfFiles):
##    FileNames.append('./Data/SimpleGraph' + str(i+1) + '.txt')


##FileNames.append('./Data/G1.txt')
##FileNames.append('./Data/G2.txt')
##FileNames.append('./Data/G7.txt')
##FileNames.append('./Data/G22.txt')
##FileNames.append('./Data/G39.txt')



FileNames.append('./Data/SyntheticGraph1.txt')
#FileNames.append('./Data/SyntheticGraph2.txt')
#FileNames.append('./Data/SyntheticGraph3.txt')


for FileName in FileNames:

    Gr = MyGraph()
    Gr.Upload(FileName)



    print('Source file: ', FileName)
    print('Number of vertices = ', Gr.n)
    print('Work started')
    Res.write('Source file: ' + FileName + '\n')
    Res.write('Number of vertices: ' + str(Gr.n) + '\n')
    


    time3 = time.time()
    
    x = MinCut(Gr)



    Jnew = copy.deepcopy(Gr.J)
    for i in range(len(x)):
        for j in range(i):
            if x[i] != x[j]:
                Jnew[i][j] = 0
                Jnew[j][i] = 0
    
    
    Cut = 0.0
    for i in range(Gr.n):
        for j in range(i):
           Cut += Gr.J[i][j] * (1 - x[i] * x[j])
    Cut = Cut * 0.5


    PlusClusterPower = 0
    for i in x:
        if i == 1:
            PlusClusterPower += 1
        
    
   

    time4 = time.time()

    
    print('Cut Value =', Cut)
    
    print('Balance value (0.5 is perfect) ', round(PlusClusterPower/Gr.n, 2))
    Res.write('Balance value (0.5 is perfect) ' + str(round(PlusClusterPower/Gr.n, 2)) + '\n')
    
    print('Time spent: ', round(time4 - time3, 6), ' seconds \n')


    Res.write('Cut Value =' + str(Cut) + '\n')
    
    Res.write('Time spent: ' + str(round(time4 - time3, 6)) + ' seconds' + '\n')
    Res.write('\n \n')
    


    if Gr.n < 201: # Draw images for small graph
        Gr.Draw(FileName)
        
        
        

        
Res.close()

        



