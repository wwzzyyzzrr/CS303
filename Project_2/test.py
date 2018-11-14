import threading

def test(a):
    while 1:
        a  = a+1

T = []
t1 = threading.Thread(target=test,args=(1))
t1.start
t2= threading.Thread(target=test,args=(1))
t2.start
t3 = threading.Thread(target=test,args=(1))
t3.start
while t1.is_alive:
    c = 0