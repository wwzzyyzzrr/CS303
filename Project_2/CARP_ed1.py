# -*- coding: UTF-8 -*-
import copy

import numpy  as np
import  time
import sys
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

def floyed(matrix):
    n = len(matrix)
    for i in range(0,n):
        for j in range(0,n):
            for k in range(0, n):
                if matrix[i,j] != max_value and matrix[i,k] != max_value:
                    matrix[k,j] = min(matrix[k,j],matrix[i,k]+matrix[i,j])
                    matrix[j,k] = matrix[k,j]
    return matrix

def doScanning(matrixC, arcs, matrixD, CAPACITY, DEPOT, type):
    car_NO = 1
    cap =CAPACITY
    NowPot = DEPOT
    Node = NowPot
    edge = (NowPot,NowPot)
    output1 = ('s 0,')
    cost = 0
    flag = 0
    route= [[]]
    while len(arcs)>0:
        min = max_value
        flagValue = 0
        for i in arcs:
            if matrixD[i[0], i[1]] <= cap :
                if type == 0:
                    flagValue,min,Node,edge,flag = maxDemSC(DEPOT, Node, edge, flag, min, NowPot, flagValue, i, i[0], matrixC, matrixD, 1)
                    flagValue,min,Node,edge,flag = maxDemSC(DEPOT, Node, edge, flag, min, NowPot, flagValue, i, i[1], matrixC, matrixD, 0)
                elif type ==1:
                    flagValue,min,Node,edge,flag = minDemSC(DEPOT, Node, edge, flag, min, NowPot, flagValue, i, i[0], matrixC, matrixD, 1)
                    flagValue,min,Node,edge,flag = minDemSC(DEPOT, Node, edge, flag, min, NowPot, flagValue, i, i[1], matrixC, matrixD, 0)
                elif type ==2:
                    flagValue,min,Node,edge,flag = maxDisNode(DEPOT, Node, edge, flag, min, NowPot, flagValue, i, i[0], matrixC, matrixD, 1)
                    flagValue,min,Node,edge,flag = maxDisNode(DEPOT, Node, edge, flag, min, NowPot, flagValue, i, i[1], matrixC, matrixD, 0)
                elif type ==3:
                    flagValue,min,Node,edge,flag = minDisNode(DEPOT, Node, edge, flag, min, NowPot, flagValue, i, i[0], matrixC, matrixD, 1)
                    flagValue,min,Node,edge,flag = minDisNode(DEPOT, Node, edge, flag, min, NowPot, flagValue, i, i[1], matrixC, matrixD, 0)
        if min != max_value:
            min = max_value
            cap -= matrixD[edge[0],edge[1]]
            arcs.remove(edge)
            cost += matrixC[NowPot,Node]
            a = Node
            NowPot = edge[flag]
            cost += edge[2]
            b = edge[flag]
            route[car_NO-1].append((a,b))
            output1 += '(' + str(a + 1) + ',' + str(b + 1) + '),'
        else:
            route.append([])
            b = DEPOT
            output1 += '0,0,'
            cost += matrixC[NowPot,DEPOT]
            NowPot = DEPOT
            cap = CAPACITY
            car_NO += 1
    output1 +='0'
    cost += matrixC[NowPot, 0]
    return route, output1, cost

def minDisNode(DEPOT, Node, edge, flag, min, NowPot, flagValue, i, point, matrixC, matrixD, theOtherNodeIndex):
    if  min > matrixC[NowPot, point]:
        min = matrixC[NowPot, point]
        flagValue = matrixC[DEPOT,point]
        Node = point
        flag = theOtherNodeIndex
        edge = i
    elif min == matrixC[NowPot, point]:
        if flagValue > matrixC[DEPOT, point]:
            flagValue = matrixC[DEPOT, point]
            Node = point
            flag = theOtherNodeIndex
            edge = i
    return flagValue, min, Node, edge, flag

def maxDisNode(DEPOT, Node, edge, flag, min, NowPot, flagValue, i, point, matrixC, matrixD, theOtherNodeIndex):
    if  min > matrixC[NowPot, point]:
        min = matrixC[NowPot, point]
        flagValue = matrixC[DEPOT,point]
        Node = point
        flag = theOtherNodeIndex
        edge = i
    elif min == matrixC[NowPot, point]:
        if flagValue < matrixC[DEPOT, point]:
            flagValue = matrixC[DEPOT, point]
            Node = point
            flag = theOtherNodeIndex
            edge = i
    return flagValue, min, Node, edge, flag

def minDemSC(DEPOT, Node, edge, flag, min, NowPot, flagValue, i, point, matrixC, matrixD, theOtherNodeIndex):
    if  min > matrixC[NowPot, point]:
        min = matrixC[NowPot, point]
        if matrixC[NowPot, point] != 0:
            flagValue = matrixD[i[0], i[1]] / matrixC[NowPot, point]
        Node = point
        flag = theOtherNodeIndex
        edge = i
    elif min == matrixC[NowPot, point]:
        if matrixC[NowPot,point]!=0 and flagValue > matrixD[i[0],i[1]]/matrixC[NowPot,point]:
            flagValue = matrixD[i[0], i[1]] / matrixC[NowPot, point]
            Node = point
            flag = theOtherNodeIndex
            edge = i
    return flagValue, min, Node, edge, flag

def maxDemSC(DEPOT, Node, edge, flag, min, NowPot, flagValue, i, point, matrixC, matrixD, theOtherNodeIndex):
    if  min > matrixC[NowPot, point]:
        min = matrixC[NowPot, point]
        if matrixC[NowPot, point] != 0:
            flagValue = matrixD[i[0], i[1]] / matrixC[NowPot, point]
        Node = point
        flag = theOtherNodeIndex
        edge = i
    elif min == matrixC[NowPot, point]:
        if matrixC[NowPot,point]!=0 and flagValue < matrixD[i[0],i[1]]/matrixC[NowPot,point]:
            flagValue = matrixD[i[0], i[1]] / matrixC[NowPot, point]
            Node = point
            flag = theOtherNodeIndex
            edge = i
    return flagValue, min, Node, edge, flag


def BuildMap(way):
    a = open(way)
    a.readline()
    VERTICES = int(a.readline().split(' ').pop())
    DEPOT = int(a.readline().split(' ').pop())-1
    REdges = int(a.readline().split(' ').pop())
    NREdges = int(a.readline().split(' ').pop())
    VEHICLES = int(a.readline().split(' ').pop())
    CAPACITY = int(a.readline().split(' ').pop())
    TCORequired = int(a.readline().split(' ').pop())
    a.readline()
    arcs = set()
    line = a.readline()
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
        matrixC[prop[0],prop[1]] = prop[2]
        matrixC[prop[1],prop[0]] = prop[2]
        matrixD[prop[0],prop[1]] = prop[3]
        matrixD[prop[1],prop[0]] = prop[3]
        if prop[3]>0:
            arcs.add((prop[0],prop[1],prop[2]))
        line = a.readline()
    #图建立完成
    for i in range(0, VERTICES):
        matrixC[i,i]=0
    matrixC = (floyed(matrixC))
    return matrixC, matrixD, VERTICES, DEPOT, REdges, NREdges, VEHICLES, CAPACITY, TCORequired, arcs

begin_time = time.time()
#arguments = sys.argv
#way = arguments[1]
#max_time = int(arguments[3])
#seed = float(arguments[5])
way = 'C:/Users/Metaron/PyCharmProject/CS303/Project_2/Proj2_Carp/Proj2_Carp/CARP_samples/val7A.dat'
matrixC, matrixD, VERTICES, DEPOT, REdges, NREdges, VEHICLES, CAPACITY, TCORequired, arcs= BuildMap(way)
route = []
output = ''
cost = max_value
for type in range(0,4):
    route_temp, output_temp, cost_temp = doScanning(matrixC, copy.deepcopy(arcs), matrixD, CAPACITY, DEPOT,type)
    if cost_temp < cost:
        cost = cost_temp
        route = route_temp
        output = output_temp
NowPot = 0
for i in route:
    print(i)
print(output)
print('q %d'%(cost))
