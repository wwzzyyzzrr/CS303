# -*- coding: UTF-8 -*-
import random

import numpy  as np
import  time
import  copy
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
            a = Node
            NowPot = edge[flag]
            b = edge[flag]
            route[car_NO-1].append((a,b))
            if b == DEPOT:
                route.append([])
                NowPot = DEPOT
                cap = CAPACITY
                car_NO += 1
        else:
            route.append([])
            b = DEPOT
            NowPot = DEPOT
            cap = CAPACITY
            car_NO += 1
    return route

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

def localSearch(route, matrixC, matrixD, CAPACITY, DEPOT, VEHICLES):
    rr = []
    localSearchSplit(route, matrixC, matrixD, 0, 0, CAPACITY, [], DEPOT, 1, VEHICLES, rr)
    node = []
    cost_node = max_value
    for i in rr:
        if i[0] < cost_node:
            cost_node = i[0]
            node = i[1]
    routeFinal = []
    node = [-1] + node + [len(route) - 1]
    for i in range(0, len(node) - 1):
        routeFinal.append(route[node[i] + 1:node[i + 1] + 1])
    return routeFinal

def getOutputCost(route, matrixC, arcs):
    output1 = 's 0,'
    cost = 0
    for i in range(0, len(route)):
        NowPot = DEPOT
        for j in route[i]:
            cost += matrixC[NowPot, j[0]]
            output1 += '(' + str(j[0] + 1) + ',' + str(j[1] + 1) + '),'
            NowPot = j[1]
        cost += matrixC[DEPOT, NowPot]
        if i < len(route) - 1:
            output1 += '0,0,'
    output1 += '0'
    arcCost = 0
    for i in arcs:
        arcCost += i[2]
    return output1, arcCost + cost

def localSearchSplit(trip, matrixC, matrixD, index, cost, CAPACITY, route, DEPOT, carNum, VEHICLES, rr):
    cap = 0
    for i in range(index,len(trip)):
        cap = cap + matrixD[trip[i][0],trip[i][1]]
        if cap > CAPACITY//2:
            if cap <= CAPACITY:
                if i == len(trip)-1:
                    rr.append((cost,route))
                    break
                if carNum < VEHICLES:
                    route_temp = copy.deepcopy(route)
                    route_temp.append(i)
                    cost_temp = cost + matrixC[DEPOT,trip[i][1]]+matrixC[DEPOT,trip[i+1][0]]-matrixC[trip[i][1],trip[i+1][0]]
                    localSearchSplit(trip, matrixC, matrixD, i+1, cost_temp, CAPACITY, route_temp, DEPOT, carNum+1, VEHICLES, rr)
    return rr

def MS(route_in, matrixC, matrixD, CAPACITY, DEPOT, arcs, output_ini, cost_ini):
    routeTwoDimension = copy.deepcopy(route_in)
    tripChoice = []
    for i in range(0, 2*len(routeTwoDimension)//3):
        p = random.randint(0, len(routeTwoDimension)-1)
        tripChoice.append(routeTwoDimension[p])
        del routeTwoDimension[p]
    task = []
    for i in tripChoice:
        task = task+i
    arcs_tempPart = set(task)
    output=''
    cost=max_value
    route_out = []
    for type in range(0, 4):
        route_PS = doScanning(matrixC, copy.deepcopy(arcs_tempPart), matrixD, CAPACITY, DEPOT, type)
        route = []
        for i in route_PS:
            route = route + i
        routeFinal = localSearch(route, matrixC, matrixD, CAPACITY, DEPOT, len(tripChoice)+1)
        routeFinal += routeTwoDimension
        output_temp,cost_temp = getOutputCost(routeFinal, matrixC, arcs)
        if cost_temp<=cost:
            cost = cost_temp
            output = output_temp
            route_out = routeFinal
    if cost <= cost_ini:
        return route_out, output, cost
    else:
        return route_in, output_ini, cost_ini

begin_time = time.time()
#arguments = sys.argv
#way = arguments[1]
#max_time = int(arguments[3])
#seed = float(arguments[5])
way = 'C:/Users/Metaron/PyCharmProject/CS303/Project_2/Proj2_Carp/Proj2_Carp/CARP_samples/val7A.dat'
matrixC, matrixD, VERTICES, DEPOT, REdges, NREdges, VEHICLES, CAPACITY, TCORequired, arcs= BuildMap(way)
output1 = ''
cost =max_value
IniRoute = []
for type in range(0,4):
    routeTwoDimension = doScanning(matrixC, copy.deepcopy(arcs), matrixD, CAPACITY, DEPOT,type)
    route = []
    for i in routeTwoDimension:
        route = route+i
    routeFinal = localSearch(route, matrixC, matrixD, CAPACITY, DEPOT, len(routeTwoDimension))
    output, cost_temp = getOutputCost(routeFinal,matrixC,arcs)
    if cost > cost_temp:
        output1 = output
        cost = cost_temp
        IniRoute = routeFinal
first_time = time.time()-begin_time
print(first_time)
while time.time() - begin_time < 30 -first_time:
    IniRoute,output1,cost = MS(IniRoute, matrixC, matrixD, CAPACITY, DEPOT, arcs, output1, cost)

print(output1)
print('q %d'%cost)
print(time.time()-begin_time)