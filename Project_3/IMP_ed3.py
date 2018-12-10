import sys, copy, time, random, queue, multiprocessing
import numpy as np

def build_map(way):
    a = open(way)
    parameter = a.readline().split(' ')
    nodes = int(parameter[0])+1
    edges = int(parameter[1])
    next_node = []
    last_node = []
    for i in range(0, nodes):
        next_node.append([])
        last_node.append([])
    for i in range(0,edges):
        edge = a.readline().split(' ')
        next_node[int(edge[0])].append((int(edge[1]), float(edge[2])))
        last_node[int(edge[1])].append((int(edge[0]), float(edge[2])))
    return nodes, edges, next_node, last_node

def cal_degree(next_node, nodes):
    node_degree = []
    for i in range(0, nodes):
        node_degree.append(len(next_node[i]))
    return node_degree

def get_max_degree(unactive_set, node_degree):
    node = unactive_set.pop()
    unactive_set.add(node)
    for i in unactive_set:
        if node_degree[i]>node_degree[node]:
            node = i
    return node

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

def Get_influence(nodes, next_node, active_set, model, times):
    length = 0
    if model == 'LT':
        for i in range(0, times):
            length += do_LT(nodes, next_node, active_set.copy())
    else:
        for i in range(0, times):
            length += do_IC(next_node, active_set.copy)
    return length/times

def do_Active(nodes, next_node, active_set, work_set, model,times,queue_temp, influence):
    for i in work_set:
        active_set.add(i)
        temp = Get_influence(nodes, next_node, active_set, model,times) - influence
        queue_temp.put((-temp, i))
        active_set.remove(i)

def main(network,size,model,timeout):
    begin_time = time.time()
    nodes, edges, next_node, last_node = build_map(network)
    node_degree = cal_degree(next_node,nodes)
    node_degree_use =(node_degree).copy()
    node_neighbor_num = []
    active_set = set()
    unactive_set = set()
    for i in range(nodes):
        unactive_set.add(i)
    if nodes>200:
        times = 100
        for i in range(nodes):
            node_neighbor_num.append(0)
        for i in range(0,min(nodes//70,size*20,nodes)):
            u = get_max_degree(unactive_set, node_degree_use)
            active_set.add(u)
            unactive_set.remove(u)
            for j in last_node[u]:
                v = j[0]
                node_neighbor_num[v] += 1
                node_degree_use[v] = node_degree[v] - 2*node_neighbor_num[v] - (node_degree[v] - node_neighbor_num[v])*node_neighbor_num[v]*j[1]
        node_select = (active_set).copy()
    else:
        times = 700
        node_select = (unactive_set).copy()
    
    active_set = set()
    unactive_set = set()
    for i in range(nodes):
        unactive_set.add(i)
    que = queue.PriorityQueue()
    P_num = 4
    p = multiprocessing.Pool(P_num)
    influence = 0
    queue_temp = multiprocessing.Manager().Queue()   
    temp_list = list(node_select)
    list_len = len(temp_list)
    part_len = list_len//P_num-1
    #print(len(node_select))
    for i in range(0,P_num):
        p.apply_async(do_Active, args=(nodes, next_node, (active_set).copy(), set(temp_list[i*part_len:(i+1)*part_len]), model,times,queue_temp, influence,))
    do_Active(nodes, next_node, (active_set).copy(), set(temp_list[(P_num)*part_len:list_len]), model,times,queue_temp, influence)
    p.close()
    while not queue_temp.empty():
        que.put(queue_temp.get())
    p.join()
    while not queue_temp.empty():
        que.put(queue_temp.get())
    temp_tuple = que.get()
    while temp_tuple[1] not in unactive_set:
            temp_tuple = que.get()
    active_set.add(temp_tuple[1])
    unactive_set.remove(temp_tuple[1])
    node_select.remove(temp_tuple[1])
    influence -= temp_tuple[0]
    for j in range(size-1):
        print(active_set)
        print(j+1)
        p = multiprocessing.Pool(P_num)
        B = que.get()
        while B[1] not in unactive_set:
            B = que.get()
        active_set.add(B[1])
        unactive_set.remove(B[1])
        temp = Get_influence(nodes, next_node, active_set, unactive_set, model,times) - influence
        C = que.get()
        if temp < -C[0]:
            unactive_set.add(B[1])
            active_set.remove(B[1])
            queue_temp = multiprocessing.Manager().Queue()        
            queue_temp = multiprocessing.Manager().Queue()   
            temp_list = list(node_select)
            list_len = len(temp_list)
            part_len = list_len//P_num
            for i in range(0,P_num):
                p.apply_async(do_Active, args=(nodes, next_node, (active_set).copy(), set(temp_list[i*part_len:(i+1)*part_len]), model,times,queue_temp, influence,))
            do_Active(nodes, next_node, (active_set).copy(), set(temp_list[(P_num)*part_len:list_len]), model,times,queue_temp, influence)
            p.close()
            while not queue_temp.empty():
                que.put(queue_temp.get())
            p.join()
            while not queue_temp.empty():
                que.put(queue_temp.get())
            temp_tuple = que.get()
            while temp_tuple[1] not in unactive_set:
                temp_tuple = que.get()
            active_set.add(temp_tuple[1])
            unactive_set.remove(temp_tuple[1])
            node_select.remove(temp_tuple[1])
            influence -= temp_tuple[0]
        else:
            que.put(C)
            node_select.remove(B[1])
            influence += temp
    for i in active_set:
        print(i)
    print(influence)
    print(time.time()-begin_time)


arguments = sys.argv
network = arguments[2]
size = int(arguments[4])
model = arguments[6]
timeout = float(arguments[8])
main(network,size,model,timeout)
        