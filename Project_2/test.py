import numpy  as np
a = open("/home/metaron/文件/CS303/Project_2/Proj2_Carp/Proj2_Carp/CARP_samples/egl-e1-A.dat")
a.readline()
VERTICES = int(a.readline().split(' ').pop())
DEPOT = int(a.readline().split(' ').pop())
REdges = int(a.readline().split(' ').pop())
NREdges = int(a.readline().split(' ').pop())
VEHICLES = int(a.readline().split(' ').pop())
CAPACITY = int(a.readline().split(' ').pop())
TCORequired = int(a.readline().split(' ').pop())
a.readline()
line = a.readline()
edge = []
while (line != ''):
    temp = (line.split(' '))
    prop = []
    for i in temp:
        if i!=None:
            prop.append()
    line = a.readline()
print(edge)