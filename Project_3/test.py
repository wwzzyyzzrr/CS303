from multiprocessing import Pool
import os, random, time

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    i = 0
    while time.time()-start<20:
        i += 1
    end = time.time()
    print('Task %s runs %d times' %(name, i))

print('The main processing pid %d'%os.getpid())
p = Pool(2)
for i in range(2):
    p.apply_async(long_time_task, args=(i,))
print('Waiting for all subprocesses done...')
p.close()
p.join()
print('All subprocesses done.')