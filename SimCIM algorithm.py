import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math
import random

import time
import copy

# implementation of SimCIM algorithm from article https://arxiv.org/pdf/1901.08927.pdf (by Tiunov et. al)


            
def UploadGraph(FileName, WeightedVertices = False):
    with open(FileName) as fil:
        n, m = [int(j) for j in fil.readline().split()]

        G = nx.Graph(FileName = FileName)

        for i in range(n):
            G.add_node(i)
            
        for i in range(m):
            vert1, vert2, weight = [int(j) for j in fil.readline().split()]
            G.add_edge(vert1 - 1,vert2 - 1, weight = weight)
            

        if WeightedVertices:
            for i in range(n):
                _, G.nodes[i]['weight'] = [int(j) for j in fil.readline().split()]
        else:
            for i in range(n):
                G.nodes[i]["weight"] = 1

    return n, G


def OutputResults(G, n):

    Cut = 0.0    
    for i in G.edges():
        Cut += (1 - G.nodes[i[0]]["spin"] * G.nodes[i[1]]["spin"]) * G.edges[i]["weight"]
    Cut *= 0.5

    print('Cut Value =', Cut)

    
    PlusClusterPower = 0
    SumOfWeights = 0

    for i in G.nodes.data():
        SumOfWeights += i[1]["weight"]
        if i[1]["spin"] == 1:
            PlusClusterPower += i[1]["weight"]
    BalanceValue = PlusClusterPower/SumOfWeights                
        
    print('Balance value (0.5 corresponds to equal parts) ', round(BalanceValue, 2))

    print('\n \n')


    if n < 201: # Draw image for small graph
        
        NodeColors = []
        for i in G.nodes():
            if G.nodes[i]["spin"] == -1:
                NodeColors.append('red')
            elif G.nodes[i]["spin"] == 1:
                NodeColors.append('green')
            else:
                NodeColors.append('blue')

        EdgeColors = []

        for i in G.edges():
            if G.nodes[i[0]]["spin"] * G.nodes[i[1]]["spin"] == -1:
                EdgeColors.append('orange')
                G.edges[i]["weight"] = 0                
            else:
                EdgeColors.append('black')

        FileName = G.graph["FileName"]

        SourceImageName = './Images/' + FileName[7:-4] + '.png'
        
        plt.figure(figsize = (n // 3 + 5, n // 3 + 5))
        nx.draw(G, pos = nx.spring_layout(G), node_color = NodeColors, edge_color = EdgeColors, with_labels=True)
        plt.savefig(SourceImageName)
        plt.clf()              
        
        nx.write_gexf(G, './Results/' + FileName[7:-4] + '.gexf')   # save resulting graph with added spins of vertices and zero weights of cutted edges


def ListOfFiles():
    FileNames = []   

    # Uncomment this to try program on small graphs. (Set Noize = 0.000005 for better results in this case)
##    NumberOfFiles = 6
##    for i in range(NumberOfFiles):
##        FileNames.append('./Data/SimpleGraph' + str(i+1) + '.txt')


    ##FileNames.append('./Data/G1.txt')
    ##FileNames.append('./Data/G2.txt')
    ##FileNames.append('./Data/G7.txt')
    ##FileNames.append('./Data/G22.txt')
    ##FileNames.append('./Data/G39.txt')



    FileNames.append('./Data/SyntheticGraph1.txt')
    FileNames.append('./Data/SyntheticGraph2.txt')
    FileNames.append('./Data/SyntheticGraph3.txt')
    FileNames.append('./Data/SyntheticGraph4.txt')
    FileNames.append('./Data/SyntheticGraph5.txt')
    FileNames.append('./Data/SyntheticGraph6.txt')

    #FileNames.append('./Data/SimpleWeightedGraph.txt')

    return FileNames





def SimCIM(J,n, Params):

    NSteps = Params[0]
    Nu0 = Params[1]
    Zeta = Params[2]
    Noize = Params[3]

    
    x = np.zeros(n)

    for t in range(NSteps):

        Nu = Nu0*(1 - math.tanh(t / NSteps * 6 - 3))        # pump-loss factor, Fig2 (b) in the article
        fgen = (np.random.normal() for i in range(n))       # Generating vector of noize values for this iteration
        f = np.fromiter(fgen, float) * Noize
        
        x += Nu * x +  Zeta * np.dot(J.A, x) + f            # Equation (5) in Tiunov`s aritcle

        for i in range(n):              # Equation (6) in Tiunov`s article
            if x[i] > 1:
                x[i] = 1
            elif x[i] < -1:
                x[i] = -1

    for i in range(n):                  # After finish of algorithm, we define all positive spins to be 1 and negative to be -1
        if x[i] < 0:
            x[i] = -1
        else:
            x[i] = 1
    return x

    
def MaxCut(G, n, Params):    
    J = nx.adjacency_matrix(G)
    
    x = SimCIM(J, n, Params)
    
    for i in range(n):
        G.nodes[i]["spin"] = x[i]
        
    return G


def MinCut(G, n, Params):
    Ab = Params[4]
    J = nx.adjacency_matrix(G)
    V = np.array([i[1] for i in G.nodes(data = "weight")])
    
    x = SimCIM(- J + V * Ab / n , n, Params)                # Minimal Balanced Cut is the same Ising problem, but with different interaction matrix
    
    for i in range(n):
        G.nodes[i]["spin"] = x[i]

    return G



NSteps = 1000
Nu0 = -5
Zeta = -0.05
Noize = 0.005
Ab = 10

print('Number of steps = ', NSteps)
print('Zeta = ', Zeta)
print('Noize parameter = ', Noize)
print('Nu0 = ', Nu0)
print('Ab = ', Ab, '\n')


Params = [NSteps, Nu0, Zeta, Noize, Ab]





for FileName in ListOfFiles():
    print('Source file: ', FileName)

    
    n, G = UploadGraph(FileName)
    
    print('Number of vertices = ', n)

    time3 = time.time()
    
    G = MinCut(G,n, Params)

    time4 = time.time()

    print('Time spent: ', round(time4 - time3, 6), ' seconds \n')


    OutputResults(G, n)


    



    

    
        
        
        

        


        



