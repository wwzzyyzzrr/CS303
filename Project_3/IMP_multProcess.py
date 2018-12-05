import sys, copy, time, random, queue, multiprocessing
import numpy as np

def build_map(way):
    a = open(way)
    parameter = a.readline().split(' ')
    nodes = int(parameter[0])
    edges = int(parameter[1])
    next_node = []
    for i in range(0, nodes):
        next_node.append([])
    for i in range(0,edges):
        edge = a.readline().split(' ')
        next_node[int(edge[0])-1].append((int(edge[1])-1, float(edge[2])))
    return nodes, edges, next_node

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

def Get_influence(nodes, next_node, active_set, unactive_set, model, times):
    length = 0
    if model == 'LT':
        for i in range(0, times):
            length += do_LT(nodes, next_node, list(active_set), list(unactive_set))
    else:
        for i in range(0, times):
            length += do_IC(next_node, list(active_set),  list(unactive_set))
    return length/times

def do_Active(nodes, next_node, active_set, unactive_set, work_set, model,times,queue_temp, influence):
    for i in work_set:
        active_set.add(i)
        unactive_set.remove(i)
        temp = Get_influence(nodes, next_node, active_set, unactive_set, model,times) - influence
        queue_temp.put((-temp, i))
        unactive_set.add(i)
        active_set.remove(i)

def main(network,size,model,timeout):
    begin_time = time.time()
    nodes, edges, next_node = build_map(network)
    active_set = set()
    unactive_set = set()
    for i in range(0,nodes):
        unactive_set.add(i)
    que = queue.PriorityQueue()
    p = multiprocessing.Pool(8)
    influence = 0
    times = 10000
    queue_temp = multiprocessing.Manager().Queue()        
    temp_list = list(unactive_set)
    list_len = len(temp_list)
    part_len = list_len//8
    for i in range(0,7):
        p.apply_async(do_Active, args=(nodes, next_node, copy.deepcopy(active_set), copy.deepcopy(unactive_set), set(temp_list[i*part_len:(i+1)*part_len]), model,times,queue_temp, influence,))
    p.apply_async(do_Active, args=(nodes, next_node, copy.deepcopy(active_set), copy.deepcopy(unactive_set), set(temp_list[7*part_len:list_len]), model,times,queue_temp, influence,))
    p.close()
    p.join()
    while not queue_temp.empty():
        que.put(queue_temp.get())
    temp_tuple = que.get()
    active_set.add(temp_tuple[1])
    unactive_set.remove(temp_tuple[1])
    influence -= temp_tuple[0]
    for j in range(size-1):
        p = multiprocessing.Pool(8)
        B = que.get()[1]
        active_set.add(B)
        unactive_set.remove(B)
        temp = Get_influence(nodes, next_node, active_set, unactive_set, model,times) - influence
        C = que.get()
        if temp < -C[0]:
            unactive_set.add(B)
            active_set.remove(B)
            que.queue.clear()
            queue_temp = multiprocessing.Manager().Queue()        
            temp_list = list(unactive_set)
            list_len = len(temp_list)
            part_len = list_len//8
            for i in range(0,7):
                p.apply_async(do_Active, args=(nodes, next_node, copy.deepcopy(active_set), copy.deepcopy(unactive_set), set(temp_list[i*part_len:(i+1)*part_len]), model,times,queue_temp, influence,))
            p.apply_async(do_Active, args=(nodes, next_node, copy.deepcopy(active_set), copy.deepcopy(unactive_set), set(temp_list[7*part_len:list_len]), model,times,queue_temp, influence,))
            p.close()
            p.join()
            while not queue_temp.empty():
                que.put(queue_temp.get())
            temp_tuple = que.get()
            active_set.add(temp_tuple[1])
            unactive_set.remove(temp_tuple[1])
            influence -= temp_tuple[0]
        else:
            que.put(C)
            influence += temp
    for i in active_set:
        print(i+1)
    print(influence)
    print(time.time()-begin_time)
arguments = sys.argv
network = arguments[2]
size = int(arguments[4])
model = arguments[6]
timeout = float(arguments[8])
main(network,size,model,timeout)
        