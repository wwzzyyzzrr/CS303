import sys, copy, time, random, queue, multiprocessing
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

def cal_degree(next_node):
    length = len(next_node)
    node_degree = []
    for i in range(0, length):
        node_degree.append(len(next_node[i]))
    return node_degree

def main(network,size,model,timeout):
    begin_time = time.time()
    nodes, edges, next_node = build_map(network)













arguments = sys.argv
network = arguments[2]
size = int(arguments[4])
model = arguments[6]
timeout = float(arguments[8])
main(network,size,model,timeout)
        