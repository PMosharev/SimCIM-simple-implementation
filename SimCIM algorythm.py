import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math
import random

import time
import copy

# implementation of SimCIM algorythm from article https://arxiv.org/pdf/1901.08927.pdf (by Tiunov et. al)


            
def UploadGraph(FileName, WeightedVertices = False):
    with open(FileName) as fil:
        n, m = [int(j) for j in fil.readline().split()]

        G = nx.Graph()

        for i in range(n):
            G.add_node(i)
            
        for i in range(m):
            vert1, vert2, weight = [int(j) for j in fil.readline().split()]
            G.add_edge(vert1 - 1,vert2 - 1, weight = weight)
            

        if WeightedVertices:
            for i in range(n):
                _, G.nodes[i]['weight'] = [int(j) for j in fil.readline().split()]

    return n, G

                

                    

                    




def SimCIM(J,n, NSteps = 1000, Nu0 = -0.5, Zeta = -0.05, Noize = 0.005):

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

    x = np.zeros(n)

    for t in range(NSteps):

        Nu = Nu0*(1 - math.tanh(t / NSteps * 6 - 3))     # pump-loss factor, Fig2 (b) in the article
        fgen = (np.random.normal() for i in range(n))
        f = np.fromiter(fgen, float) * Noize
        
        x += Nu * x +  Zeta * np.dot(x, J.A) + f

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

    
def MaxCut(G, n):    
    J = nx.adjacency_matrix(G)    
    return SimCIM(J, n)

def MinCut(G, n, Ab = 3):
    J = nx.adjacency_matrix(G)
    V = np.array([i[1] for i in G.nodes(data = "weight")])
    
    print(V)
    return SimCIM(- J.T + V * Ab , n)
    







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



#FileNames.append('./Data/SyntheticGraph1.txt')
#FileNames.append('./Data/SyntheticGraph2.txt')
#FileNames.append('./Data/SyntheticGraph3.txt')

FileNames.append('./Data/SimpleWeightedGraph.txt')


for FileName in FileNames:

    
    n, G = UploadGraph(FileName, True)



    print('Source file: ', FileName)
    print('Number of vertices = ', n)
    print('Work started')
    Res.write('Source file: ' + FileName + '\n')
    Res.write('Number of vertices: ' + str(n) + '\n')
    


    time3 = time.time()
    
    x = MinCut(G,n)


    Cut = 0.0
    NewGraph = G.copy()
    for i in range(len(x)):
        for j in range(i):
            if x[i] != x[j] and (i, j) in NewGraph.edges:                
                NewGraph.remove_edge(j, i)
                Cut += 1

    PlusClusterPower = 0
    for i in x:
        if i == 1:
            PlusClusterPower += 1
        
    
   

    time4 = time.time()

    
    print('Cut Value =', Cut)
    
    print('Balance value (0.5 is perfect) ', round(PlusClusterPower/n, 2))
    Res.write('Balance value (0.5 is perfect) ' + str(round(PlusClusterPower/n, 2)) + '\n')
    
    print('Time spent: ', round(time4 - time3, 6), ' seconds \n')


    Res.write('Cut Value =' + str(Cut) + '\n')
    
    Res.write('Time spent: ' + str(round(time4 - time3, 6)) + ' seconds' + '\n')
    Res.write('\n \n')
    

    if n < 201: # Draw images for small graph
        
        Colors = []
        for i in x:
            if i == -1:
                Colors.append('red')
            elif i == 1:
                Colors.append('green')
            else:
                Colors.append('blue')

        SourceImageName = './Images/' + FileName[7:-4] + '_Original' + '.png'
        
        plt.figure(figsize = (n // 3 + 5, n // 3 + 5))
        nx.draw(G, pos = nx.circular_layout(G), with_labels=True)
        plt.savefig(SourceImageName)
        plt.clf()              
        

        
        ResultImageName = './Images/' + FileName[7:-4] + '_Result' + '.png'

        nx.draw(NewGraph, pos = nx.spring_layout(NewGraph), node_color = Colors, with_labels=True)
        plt.savefig(ResultImageName)
        plt.clf()

        nx.write_gexf(G, './Results/' + FileName[7:-4] + '_Original' + '.gexf')
        nx.write_gexf(NewGraph, './Results/' + FileName[7:-4] + '_Result' + '.gexf')
        
        
        

        
Res.close()

        



