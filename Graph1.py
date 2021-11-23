import numpy as np
import math
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

def Algor(x, n, Zita, Noize):
    for t in range(n):
        Nu = nu(t, n)

        for i in range(len(x)):
            f = Noize*np.random.normal()
            Deltaxi = DeltaXi(x, i, Nu, Zita, J, f)
            x[i] = phi(x[i], Deltaxi)
    return x

J = [[0,1,1,0,0,0],[1,0,1,0,0,0],[1,1,0,1,0,0],[0,0,1,0,1,1],[0,0,0,1,0,1],[0,0,0,1,1,0]]
#J = [[0,1,1,0,0],[1,0,1,1,0],[1,1,0,0,1],[0,1,0,0,1],[0,0,1,1,0]]
#J = [[0,1],[1,0]]
#J = [[0,2,2],[2,0,1],[2,1,0]]
#J = [[0,1,1,1,1,1],[1,0,0,0,0,0],[1,0,0,0,0,0],[1,0,0,0,0,0],[1,0,0,0,0,0],[1,0,0,0,0,0]]




x = [0, 0, 0, 0, 0, 0]
#x = [0, 0, 0, 0, 0]
#x = [0, 0]
#x = [0,0,0]
#x = [0,0,0,0,0,0]

Zita = - 0.05
n = 200
Noize = 0.00001

xnew = Algor(x, n, Zita, Noize)

    
print(xnew)

Jnew = ModifyMatrix(J,xnew)

FileOutName = '1.png'
MatrixG = nx.DiGraph(np.matrix(J))
ImageGraph(MatrixG, SetColors(x), FileOutName)

FileOutName = '2.png'
MatrixGnew = nx.DiGraph(np.matrix(Jnew))
ImageGraph(MatrixGnew, SetColors(x), FileOutName)
