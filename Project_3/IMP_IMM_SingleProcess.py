import sys, copy, time, random, queue, multiprocessing, math
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

def generate_g(nodes, next_node, last_node):
    g = []
    for i in range(0,nodes):
        g.append(set())
    for i in range(0, nodes):
        for j in range(0, len(next_node[i])):
            if random.random() < next_node[i][j][1]:
                g[j].add(i)
    return g

def get_RRset_lt(last_node, node):
    a = set([node])
    a_new = set([node])
    while a_new:
        a_temp = set()
        for i in a_new:
            if(len(last_node[i])>0):
                index = random.randint(0, len(last_node[i])-1)
                if last_node[i][index][0] not in a:
                    a.add(last_node[i][index][0])
                    a_temp.add(last_node[i][index][0])
        a_new = a_temp
    return a

def get_RRset(last_node, node):
    a = set([node])
    a_new = a.copy()
    while a_new:
        a_temp = set()
        for i in a_new:
            for j in last_node[i]:
                if random.random() < j[1]:
                    if j[0] not in a:
                        a_temp.add(j[0])
                        a.add(j[0])
        a_new = a_temp.copy()
    return a

def get_fraction(R_set, S):
    Cover = set()
    for i in S:
        for r_index in range(0,len(R_set)):
            if i in R_set[r_index]:
                Cover.add(r_index)
    frac = len(Cover)/len(R_set)
    return frac

def node_selection(nodes, R_set, size):
    Set_k = set()
    RDic = dict()
    num = []
    for i in range(0, nodes):
        num.append(0)
    for i in range(0, len(R_set)):
        for j in R_set[i]:
            num[j] += 1
            if j not in RDic.keys():
                RDic[j] = [i]
            else:
                RDic[j].append(i)
    while len(Set_k) < size:
        s = num.index(max(num))
        Set_k.add(s) 
        rr = list(RDic[s])
        for i in rr:
            for j in R_set[i]:
                num[j] -= 1
                RDic[j].remove(i)
    return Set_k

def add_RR(que, times, nodes, last_node, model):
    set_temp= []
    if model:
        for i in range(times):
            index = random.randint(0,nodes -1)
            set_temp.append(get_RRset_lt(last_node, index))
    else:
        for i in range(times):
            index = random.randint(0,nodes -1)
            set_temp.append(get_RRset(last_node, index))
    que.put(set_temp)

def sampling(nodes, next_node, last_node, size, epsilon, lota, p_num, model):
    R_set = []
    LB = 1
    C_n_k = math.factorial(nodes)/(math.factorial(size)*math.factorial(nodes-size))
    epsilon_a = math.sqrt(2) * epsilon #epsilon`
    alpha = math.sqrt(lota*math.log(nodes)+math.log(2))
    beta = math.sqrt((1-1/math.e)*(math.log(C_n_k) + lota*math.log(nodes) + math.log(2)))
    lambda_a = ((2+2/3*epsilon_a)*(math.log(C_n_k)+lota*math.log(nodes)+math.log(math.log2(nodes)))*nodes)/math.pow(epsilon_a, 2) #lambda`
    lambda_b = 2*nodes*math.pow((1-1/math.e)*alpha + beta, 2)*math.pow(epsilon, -2) #lambda*
    for i in range(1, int(math.log2(nodes))):
        x = nodes/(math.pow(2, i))
        theta_i = lambda_a/x
        if model:
            while len(R_set)<theta_i:
                index = random.randint(0,nodes -1)
                R_set.append(get_RRset_lt(last_node, index))
        else:
            while len(R_set)<theta_i:
                index = random.randint(0,nodes -1)
                R_set.append(get_RRset(last_node, index))
        S_i = node_selection(nodes, R_set, size)
        F_R_S = get_fraction(R_set, S_i)
        if nodes*F_R_S >= (1+epsilon_a)*x:
            LB = nodes*F_R_S/(1+epsilon_a)
            break
    theta = lambda_b/LB
    if model:
        while len(R_set)<theta:
            index = random.randint(0,nodes -1)
            R_set.append(get_RRset_lt(last_node, index))
    else:
        while len(R_set)<theta:
            index = random.randint(0,nodes -1)
            R_set.append(get_RRset(last_node, index))
    return R_set

def IMM(nodes, next_node, last_node, size, model):
    lota = 1
    epsilon = 0.2
    p_num = 7
    R_set = sampling(nodes, next_node, last_node, size, epsilon, lota, p_num, model)
    Set_k = node_selection(nodes, R_set, size)
    return Set_k

def main(network,size,model,timeout):
    nodes, edges, next_node, last_node = build_map(network)
    begin_time = time.time()
    Set = IMM(nodes, next_node, last_node, size, model)
    f = open('seeds.txt','w')
    for i in Set:
        print(i,file = f)
    print(time.time()-begin_time)


arguments = sys.argv
network = arguments[2]
size = int(arguments[4])
model = arguments[6]=='LT'
timeout = float(arguments[8])
main(network,size,model,timeout)
