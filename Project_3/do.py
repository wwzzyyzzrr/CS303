a = open('Amazon.txt')
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
    next_node[int(edge[0])].append(int(edge[1]))
    last_node[int(edge[1])].append(int(edge[0]))
b= open('network4.txt','w')
for i in range(0,len(next_node)):
    for j in next_node[i]:
        print('{0} {1} {2}'.format(i, j, 1/len(last_node[j])), file = b)
