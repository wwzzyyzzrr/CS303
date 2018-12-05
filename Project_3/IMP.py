import sys, copy, time, random, queue
import numpy as np

def build_map(way):
    a = open(way)
    parameter = a.readline().split(' ')
    nodes = int(parameter[0])
    edges = int(parameter[1])
    next_node = []
    for i in range(0, nodes):
        next_node.append([])
    matrixW = np.array([[0.00 for j in range(nodes)] for i in range(nodes)])
    for i in range(0,edges):
        edge = a.readline().split(' ')
        matrixW[int(edge[0])-1,int(edge[1])-1] = float(edge[2])
        next_node[int(edge[0])-1].append(int(edge[1])-1)
    return nodes, edges, matrixW,  next_node

def add_seed(way, nodes):
    a = open(way)
    unactive_set = []
    active_set = []
    list_temp = a.readlines()
    for i in list_temp:
        active_set.append(int(i)-1)
    for i in range(0, nodes):
        if i not in active_set:
            unactive_set.append(i)
    return active_set, unactive_set

def IC(next_node, matrixW, active_set, unactive_set):
    active_set_new = []
    for i in active_set:
        for j in next_node[i]:
            if random.random() <= matrixW[i,j] and j in unactive_set:
                active_set_new.append(j)
                unactive_set.remove(j)
    return active_set_new

def IC(next_node, matrixW, active_set, unactive_set):
    active_set_new = []
    for i in active_set:
        for j in next_node[i]:
            if random.random() <= matrixW[i,j] and j in unactive_set:
                active_set_new.append(j)
                unactive_set.remove(j)
    return active_set_new

def LT(next_node, matrixW, active_set, unactive_set,threshold):
    active_set_new = []
    for i in active_set:
        for j in next_node[i] :
            if j in unactive_set:
                threshold[j] -= matrixW[i,j]
                if threshold[j]<=0:
                    active_set_new.append(j)
                    unactive_set.remove(j)
    return active_set_new, unactive_set

def do_IC(next_node, matrixW, active_set,unactive_set):
    length = len(active_set)
    while len(active_set)>0:
        active_set = IC(next_node, matrixW, active_set, unactive_set)
        length += len(active_set)
    return length

def do_LT(nodes, next_node, matrixW, active_set, unactive_set):
    length = len(active_set)
    threshold = []
    for i in range(0,nodes):
        threshold.append(random.random())    
    while len(active_set)>0:
        active_set, unactve_set = LT(next_node, matrixW, active_set, unactive_set,threshold)
        length += len(active_set)
    return length

def Get_influence(nodes, next_node, matrixW, active_set, unactive_set, model):
    length = 0
    if model == 'LT':
        for i in range(0, 700):
            length += do_LT(nodes, next_node, matrixW, copy.deepcopy(active_set), copy.deepcopy(unactive_set))
    else:
        for i in range(0, 700):
            length += do_IC(next_node, matrixW, copy.deepcopy(active_set),  copy.deepcopy(unactive_set))
    return length/700

def main(network,size,model,timeout):
    nodes, edges, matrixW, next_node = build_map(network)
    active_set = set()
    unactive_set = set()
    for i in range(0,nodes):
        unactive_set.add(i)
    que = queue.PriorityQueue()
    for i in range(size):
        for i in unactive_set:
            active_set.add(i)
            unactive_set.remove(i)
            temp = Get_influence(nodes, next_node, matrixW, list(active_set), list(unactive_set), model)
            que.put((-temp, i))
            unactive_set.add(i)
            active_set.remove(i)
        temp_tuple = que.get()
        active_set.add(temp_tuple[1])
        unactive_set.remove(temp_tuple[1])
        influence = -temp_tuple[0]
    for i in active_set:
        print(i)

arguments = sys.argv
network = arguments[2]
size = int(arguments[4])
model = arguments[6]
timeout = float(arguments[8])
main(network,size,model,timeout)
        