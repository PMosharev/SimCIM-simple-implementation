import numpy as np
import os


Weighted = True

n = int(input('Введите число вершин графа ') or '200')

m1 = int(input('Введите минимальную степень вершины ') or '1')
m2 = int(input('Введите максимальную степень вершины ') or '5')

iGraph = 3

FileName = './Data/SyntheticGraphTmp' + str(iGraph) + '.txt'

GraphFile = open(FileName, 'w')

NumberOfEdges = 0



for i in range(1, n+1):
    k = np.random.randint(m1, m2)
    for j in range(k):
        k2 = np.random.randint(1,n)
        if k2 != i:
            if Weighted:
                GraphFile.write(str(i) + ' ' + str(k2) + ' ' + str(1) + '\n')
            else:
                GraphFile.write(str(i) + ' ' + str(k2) + ' 1\n')
            NumberOfEdges += 1

if Weighted:
    for i in range(n-1):
        GraphFile.write(str(i) + ' ' + str(1) + '\n')
    GraphFile.write(str(n-1) + ' ' + str(30) + '\n')
        
    
GraphFile.close()

if Weighted:
    ResultingFileName = './Data/WeightedSyntheticGraph' + str(iGraph) + '.txt'
else:
    ResultingFileName = './Data/5SyntheticGraph' + str(iGraph) + '.txt'

FileResult = open(ResultingFileName, 'w')
FileResult.write(str(n) + ' ' + str(NumberOfEdges) + '\n')

with open(FileName) as GraphFile:
    for i in GraphFile:
        FileResult.write(i)

FileResult.close()

with open(ResultingFileName) as FileResult:
    print(sum(1 for _ in FileResult))
        
os.remove(FileName)


print(NumberOfEdges)

