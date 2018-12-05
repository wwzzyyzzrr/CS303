import queue

que=queue.PriorityQueue()
for i in range(5):
    que.put(i)
while not que.empty():
    print(que.get())