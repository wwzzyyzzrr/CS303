# -*- coding: UTF-8 -*-
import numpy  as np

class node:
    def __init__(self):
        self.nextNode = []
    def addNextNode(self,node):
        self.nextNode.append(node)

    def addLastNode(self,node):
        self.lastNode.append(node)

edge = {}#key 为(a,b), value 为[cost, demand]

max_value = 100000000

def floyed(matrix,n):
    for i in range(0,n):
        for j in range(0,n):
            for k in range(0, n):
                if matrix[i,j] != max_value and matrix[i,k] != max_value:
                    matrix[k,j] = min(matrix[k,j],matrix[i,k]+matrix[i,j])
    return matrix

if __name__ == '__main__':
    a = open("/home/metaron/文件/CS303/Project_2/Proj2_Carp/Proj2_Carp/CARP_samples/egl-e1-A.dat")
    a.readline()
    VERTICES = int(a.readline().split(' ').pop())
    DEPOT = int(a.readline().split(' ').pop())
    REdges = int(a.readline().split(' ').pop())
    NREdges = int(a.readline().split(' ').pop())
    VEHICLES = int(a.readline().split(' ').pop())
    CAPACITY = int(a.readline().split(' ').pop())
    TCORequired = int(a.readline().split(' ').pop())
    a.readline()
    line = a.readline()
    nodes = []
    for i in range(0, VERTICES):
        nodes.append(node())
    matrixA = np.array([[max_value for j in range(VERTICES)] for i in range(VERTICES)])
    while (line != 'END'):
        temp = (line.split(' '))
        prop = []
        for i in temp:
            if i!='':
                prop.append(int(i))
        prop[0] -= 1
        prop[1] -= 1
        nodes[prop[0]].addNextNode(prop[1])
        nodes[prop[1]].addNextNode(prop[0])
        edge[(prop[0],prop[1])]=(prop[2],prop[3])
        edge[(prop[1],prop[0])]=(prop[2],prop[3])
        matrixA[prop[0],prop[1]] = prop[2]
        matrixA[prop[1],prop[0]] = prop[2]
        line = a.readline()
    #图建立完成
    for i in range(0, VERTICES):
        matrixA[i,i]=0
    matrix = (floyed(matrixA,VERTICES))
    print(matrix)