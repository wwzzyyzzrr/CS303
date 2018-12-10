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

def generate_g(nodes, next_node):
    g = []
    for i in range(nodes):
        g.append([]) 
    for i in range(0, nodes):
        for j in range(0, len(next_node[i]))):
            if random.random()>next_node[i][j][1]:
                g[i].append(next_node[i][j])
    return g 

def node_selection(nodes, R_set, size, S_k):
    for i in 
