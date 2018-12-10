import sys, copy, time, random, multiprocessing
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
    unactive_set = set()
    active_set = set()
    list_temp = a.readlines()
    for i in list_temp:
        active_set.add(int(i))
    for i in range(0, nodes):
        if i not in active_set:
            unactive_set.add(i)
    return active_set, unactive_set

def do_IC(next_node, active_set):
    active_set_new = (active_set).copy()
    while active_set_new:
        active_set_temp = set()
        for i in active_set_new:
            for j in next_node[i]:
                if random.random() < j[1]:
                    if j[0] not in active_set:
                        active_set_temp.add(j[0])
                        active_set.add(j[0])
        active_set_new = active_set_temp.copy()
    return len(active_set)

def do_LT(nodes, next_node, active_set):
    threshold = []
    for i in range(0,nodes):
        threshold.append(random.random())   
    active_set_new = (active_set).copy()    
    while active_set_new:
        active_set_temp = set()
        for i in active_set_new:
            for j in next_node[i] :
                if j[0] not in active_set:
                    threshold[j[0]] -= j[1]
                    if threshold[j[0]]<=0:
                        active_set_temp.add(j[0])
                        active_set.add(j[0])
        active_set_new = active_set_temp.copy()    
    length = len(active_set)
    return length

def cal(queue_temp, begin_time, nodes, next_node, active_set, unactive_set, P_num):
    times_cal = 0
    if model == 'LT':
        while time.time() - begin_time < timeout-1:
            times_cal+=1
            queue_temp.put(do_LT(nodes, next_node, active_set.copy()))
            if times_cal > 2000/P_num:
                break
    else:
        while time.time() - begin_time < timeout-1:
            times_cal+=1
            queue_temp.put(do_IC(next_node, active_set.copy()))
            if times_cal > 2000/P_num:
                break

def main(network,seed,model,timeout):
    begin_time=time.time()
    nodes, edges, next_node = build_map(network)
    active_set, unactive_set = add_seed(seed, nodes)
    length = 0
    times_cal = 0
    P_num = 4
    p = multiprocessing.Pool(P_num)
    influence = 0
    queue_temp = multiprocessing.Manager().Queue()
    for i in range(P_num-1):
        p.apply_async(cal, args=(queue_temp, begin_time, nodes, next_node, active_set, unactive_set, P_num,))
    cal(queue_temp, begin_time, nodes, next_node, active_set, unactive_set, P_num*2)
    while not queue_temp.empty():
        times_cal+=1
        length+=queue_temp.get()
    p.close()
    p.join()
    while not queue_temp.empty():
        times_cal+=1
        length+=queue_temp.get()
    print('{0:.2f}'.format(length/times_cal))
    print(times_cal)
    print(time.time()-begin_time)
arguments = sys.argv
network = arguments[2]
seed = arguments[4]
model = arguments[6]
timeout = float(arguments[8])
main(network,seed,model,timeout)