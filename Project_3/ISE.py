import sys, copy, time, random
import numpy as np

def build_map(way):
    a = open(way)
    parameter = a.readline().split(' ')
    nodes = int(parameter[0])+1
    edges = int(parameter[1])
    next_node = []
    for i in range(0, nodes):
        next_node.append([])
    for i in range(0,edges):
        edge = a.readline().split(' ')
        next_node[int(edge[0])].append((int(edge[1]), float(edge[2])))
    return nodes, edges, next_node

def add_seed(way, nodes):
    a = open(way)
    unactive_set = []
    active_set = []
    list_temp = a.readlines()
    for i in list_temp:
        active_set.append(int(i))
    for i in range(0, nodes):
        if i not in active_set:
            unactive_set.append(i)
    return active_set, unactive_set

def IC(next_node, active_set, unactive_set):
    active_set_new = []
    for i in active_set:
        for j in next_node[i]:
            if random.random() <= j[1] and j[0] in unactive_set:
                active_set_new.append(j[0])
                unactive_set.remove(j[0])
    return active_set_new

def LT(next_node, active_set, unactive_set,threshold):
    active_set_new = []
    for i in active_set:
        for j in next_node[i] :
            if j[0] in unactive_set:
                threshold[j[0]] -= j[1]
                if threshold[j[0]]<=0:
                    active_set_new.append(j[0])
                    unactive_set.remove(j[0])
    return active_set_new, unactive_set

def do_IC(next_node, active_set,unactive_set):
    length = len(active_set)
    while len(active_set)>0:
        active_set = IC(next_node, active_set, unactive_set)
        length += len(active_set)
    return length

def do_LT(nodes, next_node, active_set, unactive_set):
    length = len(active_set)
    threshold = []
    for i in range(0,nodes):
        threshold.append(random.random())    
    while len(active_set)>0:
        active_set, unactve_set = LT(next_node, active_set, unactive_set,threshold)
        length += len(active_set)
    return length

def main(network,seed,model,timeout):
    begin_time=time.time()
    nodes, edges, next_node = build_map(network)
    active_set, unactive_set = add_seed(seed, nodes)
    length = 0
    times_cal = 0
    if model == 'LT':
        while time.time() - begin_time < timeout-0.5:
            times_cal+=1
            length += do_LT(nodes, next_node, copy.deepcopy(active_set), copy.deepcopy(unactive_set))
            if times_cal > 1000:
                break
    else:
        while time.time() - begin_time < timeout-0.5:
            times_cal+=1
            length += do_IC(next_node, copy.deepcopy(active_set), copy.deepcopy(unactive_set))
            if times_cal > 10:
                break           
    print('{0:.2f}'.format(length/times_cal))
    print(time.time()-begin_time)
arguments = sys.argv
network = arguments[2]
seed = arguments[4]
model = arguments[6]
timeout = float(arguments[8])
main(network,seed,model,timeout)