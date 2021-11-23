import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import copy

def ImageGraph(G, Colors, FileName):
    nx.draw(G, node_color = Colors, with_labels=True)
    plt.savefig(FileName)
    plt.clf()

def GraphFromFile(FileName):
    g = nx.Graph()
    with open(FileName) as fil:
        n, m = [int(j) for j in fil.readline().split()]
        print(n, m)
        for k in range(m):
            vert1, vert2, weight = [int(j) for j in fil.readline().split()]
            g.add_edge(vert1, vert2)
    return g

def PrintMatrix(Matrix):
    for i in Matrix:
        for j in i:
            print(j, end = '')
        print()


def AdjMatrixFromFile(FileName):
    with open(FileName) as fil:
        n, m = [int(j) for j in fil.readline().split()]
        J = [[0 for i in range(n)] for j in range(n)]
        PrintMatrix(J)
        for k in range(m):
            vert1, vert2, weight = [int(j) for j in fil.readline().split()]
            J[vert1 - 1][vert2 - 1] = weight
            J[vert2 - 1][vert1 - 1] = weight
    return J

def ModifyMatrix(J, x):
    Jnew = copy.deepcopy(J)
    for i in range(len(x)):
        for j in range(i):
            if x[i] != x[j]:
                Jnew[i][j] = 0
                Jnew[j][i] = 0
    return Jnew

def SetColors(x):
    Colors = []
    for i in x:
        if i == -1:
            Colors.append('red')
        elif i == 1:
            Colors.append('green')
        else:
            Colors.append('blue')
    return Colors


##FileName = 'SimpleGraph1.txt'
##x = [1, -1]
##
##J = AdjMatrixFromFile(FileName)
##
##
##Jnew = ModifyMatrix(J, x)
##
##PrintMatrix(J)
##print('')
##PrintMatrix(Jnew)
##
##FileOutName = '1.png'
##MatrixG = nx.DiGraph(np.matrix(J))
##ImageGraph(MatrixG, FileOutName)
##
##FileOutName = '2.png'
##MatrixGnew = nx.DiGraph(np.matrix(Jnew))
##ImageGraph(MatrixGnew, FileOutName)


##for i in range(5):
##    FileName = 'SimpleGraph' + str(i+1) + '.txt'
##    FileOutName = 'GraphImage' + str(i+1) + '.png'
##    #PrintGraph(GraphFromFile(FileName), FileOutName)
##    J = AdjMatrixFromFile(FileName)
##    PrintMatrix(J)
##    MatrixG = nx.DiGraph(np.matrix(J))
##    ImageGraph(MatrixG, FileOutName)
##    print('')
    
        
##FileName = 'G1.txt'
##FileOutName = 'G1plot.png'
##PrintGraph(GraphFromFile(FileName), FileOutName)
  
#J = [[0,1,1,0,0,0],[1,0,1,0,0,0],[1,1,0,1,0,0],[0,0,1,0,1,1],[0,0,0,1,0,1],[0,0,0,1,1,0]]


