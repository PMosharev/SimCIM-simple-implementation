import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import copy


def GraphFromFile(FileName):
    g = nx.Graph()
    with open(FileName) as fil:
        n, m = [int(j) for j in fil.readline().split()]
        print(n, m)
        for k in range(m):
            vert1, vert2, weight = [int(j) for j in fil.readline().split()]
            g.add_edge(vert1, vert2)
    return g

def AdjMatrixFromFile(FileName):
    with open(FileName) as fil:
        n, m = [int(j) for j in fil.readline().split()]
        J = [[0 for i in range(n)] for j in range(n)]

        for k in range(m):
            vert1, vert2, weight = [int(j) for j in fil.readline().split()]
            J[vert1 - 1][vert2 - 1] = weight
            J[vert2 - 1][vert1 - 1] = weight
    return J


def ImageGraph(G, Colors, FileName):
    nx.draw(G, node_color = Colors, with_labels=True)
    plt.savefig(FileName)
    plt.clf()



def PrintMatrix(Matrix):
    for i in Matrix:
        for j in i:
            print(j, end = '')
        print()


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

def CutValue(x, J, n):
    Cut = 0.0
    for i in range(n):
        for j in range(i):
           Cut += J[i][j] * (1 - x[i] * x[j])
    Cut = Cut * 0.5
    return Cut


def CreateTexFile(Zita, NSteps, Noize, NumberOfFiles, FileNames, OutTexFileName):
    with open(OutTexFileName, 'w') as OutTex:

        with open('TexTemplate.txt') as tmp:
            for s in tmp:
                OutTex.write(s)
        OutTex.write('Parameters: ' + r'\\' + '\n')
        OutTex.write('$\zeta = ' + str(Zita) + '$, ' + r'\\' + ' \n')
        OutTex.write('Number of steps =  $' + str(NSteps) + '$, ' + r'\\' + ' \n')
        OutTex.write('Noize Parameter = $ ' + str(Noize) + '$, ' + r'\\' + ' \n')

        for i in range(NumberOfFiles):
            OutTex.write(r'\newpage' + '\n')
            OutTex.write('FileName: ' + FileNames[i] + r'\\' + '\n')
            OutTex.write('Source Graph: '+ r'\\' + '\n')
            OutTex.write(r'\f' + 'box{\includegraphics[scale = 0.8]{Source' + str(i+1) +'.png}} \n \n')
            OutTex.write('Result Graph: '+ r'\\' + '\n')
            OutTex.write(r'\f' + 'box{\includegraphics[scale = 0.8]{Result' + str(i+1) +'.png}} \n \n')
        

        OutTex.write('\end{document}')

    return 0


