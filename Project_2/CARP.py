# -*- coding: UTF-8 -*-
import numpy  as np
import  time
class node:
    def __init__(self):
        self.nextNode = []
    def addNextNode(self,node):
        self.nextNode.append(node)

    def addLastNode(self,node):
        self.lastNode.append(node)

max_value = 100000000

def getRouteTwoNode(firstnode, endnode, matrix,nodes):
    Node = firstnode
    route = []
    while firstnode!=endnode:
        min = max_value
        for i in nodes[firstnode].nextNode:
            if i == endnode:
                Node = endnode
                break
            if min > matrix[i, endnode]:
                min = matrix[i,endnode]
                Node = i
        route.append(Node)
        firstnode = Node
    return route

def floyed(matrix,n):
    for i in range(0,n):
        for j in range(0,n):
            for k in range(0, n):
                if matrix[i,j] != max_value and matrix[i,k] != max_value:
                    matrix[k,j] = min(matrix[k,j],matrix[i,k]+matrix[i,j])
                    matrix[j,k] = matrix[k,j]
    return matrix

def minDisNode(matrixC, arcs, matrixD, CAPACITY, DEPOT):
    car_NO = 1
    cap =CAPACITY
    NowPot = DEPOT
    Node = NowPot
    edge = (NowPot,NowPot)
    output1 = ('s 0,')
    cost = 0
    flag = 0
    while len(arcs)>0:
        min = max_value
        for i in arcs:
            if matrixD[i[0], i[1]] <= cap:
                if min > matrixC[NowPot, i[0]]:
                    min = matrixC[NowPot, i[0]]
                    Node = i[0]
                    flag = 1
                    edge = i
                if min > matrixC[NowPot, i[1]]:
                    min = matrixC[NowPot, i[1]]
                    Node = i[1]
                    flag = 0
                    edge = i
        if min != max_value:
            min = max_value
            cap -= matrixD[edge[0],edge[1]]
            arcs.remove(edge)
            cost += matrixC[NowPot,Node]
            a = Node
            NowPot = edge[flag]
            cost += matrixC[edge[0],edge[1]]
            b = edge[flag]
            output1 += '(' + str(a + 1) + ',' + str(b + 1) + '),'
        else:
            b = DEPOT
            output1 += '0,0,'
            cost += matrixC[NowPot,0]
            NowPot = 0
            cap = CAPACITY
            car_NO += 1
    output1 +='0'
    cost += matrixC[NowPot, 0]
    return car_NO, output1, cost

def minDemSC(matrixC, arcs, matrixD, CAPACITY, DEPOT):
    car_NO = 1
    cap = CAPACITY
    NowPot = DEPOT
    Node = NowPot
    edge = (NowPot, NowPot)
    output1 = ('s 0')
    cost = 0
    flag = 0

def BuildMap():
    a = open("/home/metaron/文件/CS303/Project_2/Proj2_Carp/Proj2_Carp/CARP_samples/egl-s1-A.dat")
    a.readline()
    VERTICES = int(a.readline().split(' ').pop())
    DEPOT = int(a.readline().split(' ').pop())-1
    REdges = int(a.readline().split(' ').pop())
    NREdges = int(a.readline().split(' ').pop())
    VEHICLES = int(a.readline().split(' ').pop())
    CAPACITY = int(a.readline().split(' ').pop())
    TCORequired = int(a.readline().split(' ').pop())
    a.readline()
    nodes = []
    arcs = set()
    line = a.readline()
    for i in range(0, VERTICES):
        nodes.append(node())
    matrixC = np.array([[max_value for j in range(VERTICES)] for i in range(VERTICES)])
    matrixD = np.array([[0 for j in range(VERTICES)] for i in range(VERTICES)])
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
        matrixC[prop[0],prop[1]] = prop[2]
        matrixC[prop[1],prop[0]] = prop[2]
        matrixD[prop[0],prop[1]] = prop[3]
        matrixD[prop[1],prop[0]] = prop[3]
        if prop[3]>0:
            arcs.add((prop[0],prop[1]))
        line = a.readline()
    #图建立完成
    for i in range(0, VERTICES):
        matrixC[i,i]=0
    matrixC = (floyed(matrixC,VERTICES))
    return matrixC, matrixD, VERTICES, DEPOT, REdges, NREdges, VEHICLES, CAPACITY, TCORequired, nodes, arcs

begin_time = time.time()
matrixC, matrixD, VERTICES, DEPOT, REdges, NREdges, VEHICLES, CAPACITY, TCORequired, nodes, arcs= BuildMap()
car_NO, output1, cost = minDisNode(matrixC, arcs, matrixD, CAPACITY, DEPOT)
NowPot = 0
print(car_NO)
print(output1)
print('q %d'%(cost))
print(time.time()-begin_time)
