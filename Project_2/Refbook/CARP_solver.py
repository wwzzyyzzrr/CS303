import random
import numpy as np
import time
import sys

start = time.time()
# used in Ulusoy
def get_permutation(solution):
    # put solution into JUST SORTED TASKS!!!
    # the solution is made by path-scanning
    tasks = []
    length = len(solution)
    for i in range(length):
        now_route = solution[i]
        route_len = len(now_route)
        for j in range(route_len):
            tasks.append(now_route[j])

    return tasks

#use Ulusoy to split to improve the solution
def Ulusoy(solution,graph,dis,depot,capacity):

    inf = float("inf")
    tasks = get_permutation(solution)
    # get how many tasks:
    length = len(tasks)  # number of tasks

# v is the cost
    v = []
# p is the predecessor
    p = []

    for i in range(0, length + 1):
      p.append(0)

    v.append(0)
    for i in range(length):
        v.append(inf)

    for i in range(1, length + 1):  # index of Task is from 1 to t
        load = cost = 0
        j = i

        while j <= length and load <= capacity:
            load += graph[tasks[j - 1][0]][tasks[j - 1][1]]['demand']
            if j == i:
                cost = dis[depot][tasks[i - 1][0]] + graph[tasks[i - 1][0]][tasks[i - 1][1]]['cost'] + dis[tasks[i - 1][1]][
                    depot]
            else:
                cost = cost - dis[tasks[j - 2][1]][depot] + dis[tasks[j - 2][1]][tasks[j - 1][0]] + \
                       graph[tasks[j - 1][0]][tasks[j - 1][1]]['cost'] + dis[tasks[j - 1][1]][depot]

            if load <= capacity:
                if v[i - 1] + cost < v[j]:
                    v[j] = v[i - 1] + cost
                    p[j] = i - 1  # last node of the shortest path from node to j is node i - 1, must -1 when mapped to Task
                j += 1

    total_cost = v[length]
    routes = []
    # the end of each route
    end = length
    while True:
        route = []
        for i in range(p[end] + 1, end + 1):
            route.append(tasks[i - 1])
        routes.append(route)
        if p[end] == 0:
            break
        else:
            end = p[end]

    return total_cost,routes

# merge: parameter solution:
def merge(solution,p):
    #p is the number of chosen routes of the initial solution:
    #routes is used to store all the routes, and then randomly choose p of them
    # already get all routes, now we randomly choose p of them:

    selected_routes = []

    p_ = p

    # RECORD THE number of SELECTED ROUTES, we should embed the routes to original solution !!!
    random_num_tabu = []

    while(p_ > 0):
        random_num = random.randint(0,len(solution) - 1)
        if(random_num not in random_num_tabu):
            random_num_tabu.append(random_num)
            selected_routes.append(solution[random_num])
            p_ -= 1

    # now MERGE all the tasks of the selected routes to form a unordered list!
    tasks = []
    for i in range(len(selected_routes)):
        temp_route = selected_routes[i]
        length = len(temp_route)
        for j in range(length):
                temp = temp_route[j]
                tasks.append(temp)

    # the END of merge!
    return tasks,selected_routes


def better_rule(rule_num, free, szw1, dis, graph, load, capacity,depot):
    r = rule_num

    if (r == 1):
        longtao = szw1[0]
        maxdis = dis[longtao[0]][depot]
        chosen_tasks = []
        chosen_tasks.append(szw1[0])
        for i in range(1,len(szw1)):
            longtao = szw1[i]
            if (dis[longtao[0]][depot] > maxdis):
                maxdis = dis[longtao[0]][depot]
                chosen_tasks.clear()
                chosen_tasks.append(longtao)
            elif(dis[longtao[0]][depot] == maxdis):
                chosen_tasks.append(longtao)

        #print("chosen_tasks")
        #print(chosen_tasks)
        if(len(chosen_tasks) == 1):
            chosen_task = chosen_tasks[0]
        else:
            # randomly choose one !
            random_num = random.randint(0,len(chosen_tasks) - 1)
         #   print("randomnum")
          #  print(random_num)
            chosen_task = chosen_tasks[random_num]

        return chosen_task

    if (r == 2):
        longtao = szw1[0]
        mindis = dis[longtao[0]][depot]
        chosen_tasks = []
        for i in range(len(szw1)):
            longtao = szw1[i]
            if (dis[longtao[0]][depot] < mindis):
                mindis = dis[longtao[0]][depot]
                chosen_tasks.clear()
                chosen_tasks.append(longtao)
            elif(dis[longtao[0]][depot] == mindis):
                chosen_tasks.append(longtao)

        if (len(chosen_tasks) == 1):
            chosen_task = chosen_tasks[0]
        else:
            # randomly choose one !
            random_num = random.randint(0, len(chosen_tasks) - 1)
            chosen_task = chosen_tasks[random_num]

        return chosen_task

    if (r == 3):
        longtao = szw1[0]
        ratio = graph[longtao[0]][longtao[1]]['demand'] / graph[longtao[0]][longtao[1]]['cost']
        chosen_tasks = []
        for i in range(len(szw1)):
            longtao = szw1[i]
            temp_ratio = (graph[longtao[0]][longtao[1]]['demand'] / graph[longtao[0]][longtao[1]]['cost'])
            if (temp_ratio > ratio):
                ratio = temp_ratio
                chosen_tasks.clear()
                chosen_tasks.append(longtao)
            elif(temp_ratio == ratio):
                chosen_tasks.append(longtao)

        if (len(chosen_tasks) == 1):
            chosen_task = chosen_tasks[0]
        else:
            # randomly choose one !
            random_num = random.randint(0, len(chosen_tasks) - 1)
            chosen_task = chosen_tasks[random_num]

        return chosen_task

    if (r == 4):
        longtao = szw1[0]
        ratio = graph[longtao[0]][longtao[1]]['demand'] / graph[longtao[0]][longtao[1]]['cost']
        chosen_tasks = []
        for i in range(len(szw1)):
            longtao = szw1[i]
            temp_ratio = (graph[longtao[0]][longtao[1]]['demand'] / graph[longtao[0]][longtao[1]]['cost'])
            if (temp_ratio < ratio):
                ratio = temp_ratio
                chosen_tasks.clear()
                chosen_tasks.append(longtao)
            elif (temp_ratio == ratio):
                chosen_tasks.append(longtao)

        if (len(chosen_tasks) == 1):
            chosen_task = chosen_tasks[0]
        else:
            # randomly choose one !
            random_num = random.randint(0, len(chosen_tasks) - 1)
            chosen_task = chosen_tasks[random_num]

        return chosen_task

    if (r == 5):
        if (load < capacity / 2):
            # use rule1:
            return better_rule(1, free, szw1, dis, graph, load, capacity,depot)
        else:
            # use rule2:
            return better_rule(2, free, szw1, dis, graph, load, capacity,depot)


def path_scanning(tasks, capacity, graph, dis, rule_num,depot):
    # copy all the required tasks into free
    free = []
    for i in range(len(tasks)):
        free.append(tasks[i])
    #print(free)

    routes = []
    # totoally five rules, so there are five solution
    # record the total cost!!!!!!!!
    cost = 0

    totalload = 0

    totaldemand = 0
    length = len(free)
    for i in range(length):
        temp = free[i]
        totaldemand += graph[temp[0]][temp[1]]['demand']

    #print("totaldemand")
    #print(totaldemand)

    # outter loop to find the entire solution
    while ((totalload < totaldemand) or (len(free) != 0)):
        # reinitialize and find new routes
        load = 0
        route = []
        # set initial end node is 1 !
        current_end = 1

        #print("total_cost")
        #print(cost)
        while (load <= capacity):
            #print("-----------------------")
            # first find a task that don't violate the capacity constraints, otherwise end.
            remain = capacity - load
            #print("remain")
            #print(remain)
            #print("load")
            #print(load)
            temp_list = []
            for i in range(len(free)):
                now_task = free[i]
                # add all the eligible tasks to the temp_list
                if (graph[now_task[0]][now_task[1]]['demand'] <= remain):
                    temp_list.append(now_task)

            #print("temp_list")
            #print(temp_list)
            if len(temp_list) == 0:
                # no satisfy: END this route
                # directly to the depot and add the cost for shortest path
                cost = cost + dis[current_end][1]
                #print("cost from now to 1")
                #print(dis[current_end][1])
                if (len(route) != 0):
                    routes.append(route)
                    #print(route)
                # break the inner loop
                break

            else:
                #  tasks( >= 1) with reversed ones, added to the multiples[]
                multiples = []
                for i in range(len(temp_list)):
                    multiples.append(temp_list[i])
                    # reversed one should also be considered!!!!
                    multiples.append((temp_list[i][1], temp_list[i][0]))

                #print("multiples")
                #print(multiples)
                # find how many tasks that has the mininum dis to the current endpoint
                szw = multiples[0]
                mindis = dis[szw[0]][current_end]

                szw1 = []
                szw1.append(szw)

                #print("current_end")
                #print(current_end)

                for i in range(1,len(multiples)):
                    szw = multiples[i]
                    if (dis[szw[0]][current_end] < mindis):
                        mindis = dis[szw[0]][current_end]
                        szw1.clear()
                        szw1.append(szw)
                    elif (dis[szw[0]][current_end] == mindis):
                        szw1.append(szw)

                #print("szw1")
                #print(szw1)
                # if only one task has the minimum dis to current end
                if (len(szw1) == 1):
                    now_task = szw1[0]
                    route.append(now_task)
                    #print("now_task")
                    #print(now_task)

                    if now_task in free:
                        free.remove(now_task)
                    else:
                        # it's a reversed one
                        free.remove((now_task[1], now_task[0]))

                    load = load + graph[now_task[0]][now_task[1]]['demand']
                    totalload = totalload + graph[now_task[0]][now_task[1]]['demand']
                    cost += dis[now_task[0]][current_end]
                    cost += graph[now_task[0]][now_task[1]]['cost']
                    #update the current_end
                    current_end = now_task[1]
                    #print("cost1")
                    #print(cost)


                else:
                    #print("use rules---")
                    # multiple tasks that satisfy constraints and dis: use 5 rules to judge!!!

                    chosen_task = better_rule(rule_num, free, szw1, dis, graph, load, capacity,depot)
                    #print("chosen_task")
                    #print(chosen_task)
                    route.append(chosen_task)

                    if chosen_task in free:
                        free.remove(chosen_task)
                    else:
                        # it's a reversed one
                        free.remove((chosen_task[1], chosen_task[0]))

                    load = load + graph[chosen_task[0]][chosen_task[1]]['demand']
                    totalload = totalload + graph[chosen_task[0]][chosen_task[1]]['demand']
                    cost += dis[chosen_task[0]][current_end]
                    cost += graph[chosen_task[0]][chosen_task[1]]['cost']
                    current_end = chosen_task[1]
                    #print("cost2")
                    #print(cost)

    #print(cost)

    return cost, routes  # change the order



# calculate cost of single route
def calculate_cost(route, dis, graph, depot):

    cost = 0

    # cost of tasks
    length = len(route)
    for i in range(length):
        task = route[i]
        cost += graph[task[0]][task[1]]['cost']

    # tasks of from and to depot
    head = route[0][0]
    end = route[length-1][1]

    cost += dis[depot][head]
    cost += dis[end][depot]

    # tasks of bypassing path
    for i in range(length - 1):
        end = route[i][1]
        next_head = route[i+1][0]
        cost += dis[end][next_head]

    return cost

# reverse a single route with subroute of every length from 1 ---- total_length-1
def reverse(route,dis,graph,depot):
     initial_cost = calculate_cost(route,dis,graph,depot)
     length = len(route)
     # length of subroute
     for i in range(1,length):
         # j is the start index of reversed task
         for j in range(0, length - i + 1):

            new_route = []
            szw = 2 * j + i -1
            for s in range(j):
                new_route.append(route[s])
            for s in range(j,j + i):
                # because reverse the direction, so head and end should also be reversed!!!
                reversed = route[szw - s]
                new_route.append((reversed[1],reversed[0]))
            for s in range(j + i, length):
                new_route.append(route[s])

            new_cost = calculate_cost(new_route,dis,graph,depot)
            if(new_cost < initial_cost):
                return new_cost,new_route

     return initial_cost,route

def Reverse_operator(solution,dis,graph,depot):
    flag = 0
    while True:
        updated = False
        for i in range(len(solution)):
            route = solution[i]
            best_cost, best_route = reverse(route, dis, graph, depot)
            # it has been updated!!!
            if route != best_route:
                solution[i] = best_route
                updated = True
                flag = 1
                break
        if(updated == False):
            break

    return flag


def MS_operator(capacity, graph, dis, depot, p, solution):
    # firstly merge, output an unordered list of tasks
    tasks, selected_routes = merge(solution, p)
    # calculate the total cost of selected routes!!!

    initial_cost = 0
    length = len(selected_routes)
    for i in range(length):
        now_route = selected_routes[i]
        initial_cost += calculate_cost(now_route, dis, graph, depot)

    mincosts = [1 << 30, 1 << 30, 1 << 30, 1 << 30, 1 << 30]
    mincost_solutions = [[], [], [], [], []]

    # because of the random, use iterations to find best one of each path-scanning!!!
    for i in range(10):
        # rule_num from 1---5
        for rule_num in range(1, 6):
            cost, routes = path_scanning(tasks, capacity, graph, dis, rule_num, depot)
            if (cost < mincosts[rule_num - 1]):
                mincosts[rule_num - 1] = cost
                mincost_solutions[rule_num - 1] = routes

    # use Ulusoy
    total_cost = [0, 0, 0, 0, 0]
    temp_solution = [[], [], [], [], []]
    for i in range(1, 6):
        total_cost[i - 1], temp_solution[i - 1] = Ulusoy(mincost_solutions[i - 1], graph, dis, depot, capacity)

    # choose the best one !!!
    mincost = total_cost[0]
    best = temp_solution[0]
    for i in range(5):
        if (total_cost[i] < mincost):
            mincost = total_cost[i]
            best = temp_solution[i]

    improved = False
    # check if the mincost is less than initial_cost. If so, we make progress and do the following. otherwise return NO IMPORVEMENT!!!
    if (mincost < initial_cost):
        # now we already get mincost routes, we need to delete old selected routes and insert now routes into initial solution
        # DELETE:
        for i in range(length):
            if (selected_routes[i] in solution):
                solution.remove(selected_routes[i])

        # INSERT:
        len1 = len(best)
        for i in range(len1):
            solution.append(best[i])

        improved = True

    return improved

def local_search(solution,capacity, graph, dis, depot,p):

    #if reverse never update the solution: e.g. trapped in local optima, we should use MS to search new solution:
    if(Reverse_operator(solution,dis,graph,depot) == 0):
        #print("fuck")
        # use MS operator
        improved = MS_operator(capacity,graph,dis,depot,p,solution)
        if(improved == True):
            # again use reverse_search to improve the new solution
            Reverse_operator(solution,dis,graph,depot)

    # solution is a list, it's iterative and it's directly changed within every function. So, no need to return it.
    #return newcost:
    cost = 0
    for i in range(len(solution)):
        now_route = solution[i]
        cost += calculate_cost(now_route,dis,graph,depot)

    return cost


def readfile(path):
  datas = []
  tasks = []

  node_num = 0

  szw = np.dtype([('cost', int), ('demand', int)])
  graph = np.zeros((1,1),dtype= szw)
  dis = np.zeros((1,1), dtype=int)
    
  f = open(path,'r')
  count = 0
  for line in f.readlines():
     if line.find('END') != -1:
         break
     #count is used to calculate row_num
     count += 1
     
     if ((count <= 8) and (count != 1)):
      temp = line[:-1].replace(' ','').split(':')
      data = int(temp[-1])
      if(count == 2):
         node_num = data
         datas.append(node_num)
      if count == 3:
         depot = data
         datas.append(depot)
      if count == 4:
         req_edges = data
         datas.append(req_edges)
      if count == 5:
         unreq_edges = data
         datas.append(unreq_edges)
      if count == 6:
         vehicle = data
         datas.append(vehicle)
      if count == 7:
         capacity = data
         datas.append(capacity)
      if count == 8:
         totalcost = data
         datas.append(totalcost)
     elif count == 9:
         # construct graph
         graph = np.zeros((node_num + 1,node_num + 1),dtype= szw)
         dis = np.zeros((node_num + 1, node_num + 1), dtype=int)
         for i in range(1,node_num + 1):
             for j in range(1,node_num + 1):
                 if(i == j):
                     dis[i][j] == 0
                 else:
                     # int !!!
                     dis[i][j] = 1 << 29

     elif(count >= 10):
         sb = line[:-1].split(' ')
         temp = []
         for i in range(len(sb)):
             if(sb[i] != ''):
                 temp.append(sb[i])

         node1 = int(temp[0])
         node2 = int(temp[1])
         cost = int(temp[2])
         demand = int(temp[3])
         graph[node1][node2] = graph[node2][node1] = (cost,demand)
         dis[node1][node2] = dis[node2][node1] = cost
         if(demand > 0):
             tasks.append((node1,node2))

  return datas,tasks,graph,dis

def Floyd(node_num,dis):
    for k in range(1,node_num + 1):
        for i in range(1,node_num + 1):
            for j in range(1,node_num + 1):
                dis[i][j] = min(dis[i][k] + dis[k][j],dis[i][j])
    print(dis)





arguments = sys.argv
path = arguments[1]
max_time = int(arguments[3])
seed = float(arguments[5])


datas,tasks,graph,dis = readfile(path)

Floyd(datas[0],dis)

# firstly use path-scanning to have a feasible solution:
capacity = datas[5]
depot = datas[1]
vehicle_num = datas[4]
# set q as half vehicle num
p = int(vehicle_num / 2)

test_begin = time.time()

init_cost = 1 << 30
init_solution = []

for i in range(1, 6):
    rule_num = i
    for j in range(10):
        cost, solution = path_scanning(tasks, capacity, graph, dis, rule_num, depot)
        if (cost < init_cost):
            init_solution.clear()
            init_cost = cost
            for i in range(len(solution)):
                init_solution.append(solution[i])


a = []
mmp = 0
for i in range(len(init_solution)):
    a.append(init_solution[i])
    mmp += calculate_cost(init_solution[i],dis,graph,depot)

it = 1
for szw in range(it):

    for i in range(100):
     cost = local_search(init_solution,capacity,graph,dis,depot,p)

    if (cost < mmp):
        mmp = cost
        a.clear()
        for i in range(len(init_solution)):
            a.append(init_solution[i])

    if(szw != it - 1):
     init_solution = []
     init_cost = 1 << 30
     for i in range(1, 6):
        rule_num = i
        for j in range(10): # here can be changed to 20 iterations ???
            cost, solution = path_scanning(tasks, capacity, graph, dis, rule_num, depot)
            if (cost < init_cost):
                init_solution.clear()
                init_cost = cost
                for i in range(len(solution)):
                    init_solution.append(solution[i])

test_end = time.time()
one_loop_time = test_end - test_begin
#print("one_loop")
#print(one_loop_time)
catious_one_loop_time = int(one_loop_time + 1.5)
#print("catious")
#print(catious_one_loop_time)
nowtime = time.time()
left_time = max_time - (nowtime - start)
#print("lefttime")
#print(left_time)
it = int(left_time / catious_one_loop_time)
#print("it")
#print(it)

max_run_loop_time = catious_one_loop_time


for szw in range(it):
    #print("max loop")
   # print(max_run_loop_time)
    emm = time.time()
    if(left_time - (time.time() - nowtime) <= max_run_loop_time):
        #print("fuck!")
        break

    for i in range(100):
     cost = local_search(init_solution,capacity,graph,dis,depot,p)

    if (cost < mmp):
        mmp = cost
        a.clear()
        for i in range(len(init_solution)):
            a.append(init_solution[i])

    if(szw != it - 1):
     init_solution = []
     init_cost = 1 << 30
     for i in range(1, 6):
        rule_num = i
        for j in range(10): # here can be changed to 20 iterations ???
            cost, solution = path_scanning(tasks, capacity, graph, dis, rule_num, depot)
            if (cost < init_cost):
                init_solution.clear()
                init_cost = cost
                for i in range(len(solution)):
                    init_solution.append(solution[i])

    emm1 = time.time()
    if(max_run_loop_time < emm1 - emm):
        max_run_loop_time = emm1 - emm

sb = "s "
for i in range(len(a)):
    sb += '0,'
    route = a[i]
    for j in range(len(route)):
        task = route[j]
        sb = sb + "(" + str(task[0]) + "," + str(task[1]) + ")" + ','

    sb += '0'
    if( i != len(a) - 1):
        sb += ","

print(sb)
fc = "q " + str(mmp)
print(fc)
#print("total time used")
#print(time.time() - start)