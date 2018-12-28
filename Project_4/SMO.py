import numpy as np
import random,time, multiprocessing

class SMO:
    def __init__(self,x, y, C, maxIter,toler, minmove):
        self.x = x# Training data, num*dimension
        self.y = y# Label data
        self.m = np.shape(self.x)[0]
        self.a = np.random.uniform(0,C,self.m,)
        self.c = C
        self.e = []
        self.b = 0
        self.maxIter = maxIter
        self.toler = toler #Means the range of the size of the mistake 
        self.minmove = minmove #means that the min distance the alpha move each time
        self.K = np.array(np.zeros((self.m,self.m)))
        p_num = 8
        que = multiprocessing.Manager().Queue()
        p = multiprocessing.Pool(p_num-1)
        part_length = self.m//8
        for i in range(p_num-1):
            p.apply_async(self.calculateK, args=(i*part_length,(i+1)*part_length,que))
        self.calculateK((p_num-1)*part_length, self.m, que)
        while not que.empty():
            temp = que.get()
            index = temp[0]
            for j in range(1, len(temp)):
                self.K[index,j-1]=temp[j]
        p.close()
        p.join()
        while not que.empty():
            temp = que.get()
            index = temp[0]
            for j in range(1, len(temp)):
                self.K[index,j-1]=temp[j]
        for i in range(self.m):
            self.e.append(self.E(i))

    def calculateK(self, start, end, que):
        for i in range(start, end):
            v = [i]
            for j in range(self.m):
                v.append(self.k(i,j))
            que.put(v.copy())


    def k(self,i,j):
        return np.dot(self.x[i], self.x[j].T)

    def g(self, i):
        g = self.b+np.dot(np.multiply(self.a, self.y).T, self.K[i,:])
        return g

    def E(self, i):
        E = self.g(i)-self.y[i]
        return(E)

    def updateE(self, index):
        e = self.E(index)
        self.e[index] = e

    def select_aj(self,i,Ei):
        ''''''
        max = 0
        index = -1
        self.e[i] = Ei
        '''
        for j in range(self.m):
            temp = abs(self.e[j]-Ei)
            if temp>max:
                max = temp
                index = j
        '''
        if index == -1:
            index = random.randint(0, len(self.x)-1)
            while(index == i):
                index = random.randint(0, len(self.x)-1)
        return index,self.e[index]

    def get_aj(self,aj, H, L):# Make sure that a not out of range
        if aj>H:
            aj = H
        elif aj<L:
            aj = L
        return aj

    def update_aj(self, i, j, Ei, Ej, H, L):
        inta = self.K[i,i]+self.K[j,j]-2*self.K[i,j]
        print(inta)
        if inta <= 0:
            return False
        self.a[j] += self.y[i]*(Ei - Ej)/inta
        self.a[j] = self.get_aj(self.a[j], H, L)
        self.updateE(j)
        return True

    def update_ai(self, i, j, aj_old):
        self.a[i] += self.y[i]*self.y[j]*(aj_old - self.a[j])
        self.updateE(i)

    def cal_b1(self, i, j):
        return self.b - self.e[i] - self.y[i]*np.dot(self.x[i], self.x[i].T) - self.y[j]*np.dot(self.x[j], self.x[i].T)

    def cal_b2(self, i, j):
        return self.b - self.e[j] - self.y[i]*np.dot(self.x[i], self.x[j].T) - self.y[j]*np.dot(self.x[j], self.x[j].T)

    def update_b(self, i, j):
        if (self.a[i]>0) and (self.a[i]<self.c):
            self.b = self.cal_b1(i,j)
        elif(self.a[j]>0) and (self.a[j]<self.c):
            self.b = self.cal_b2(i, j)
        else:
            self.b = (self.cal_b1(i, j) + self.cal_b2(i, j)) / 2.0

    def changeaijPair(self, i):
        Ei = self.e[i]
        if ((self.y[i]*Ei< - self.toler) and (self.a[i]<self.c)) or ((self.y[i]*Ei>self.toler) and (self.a[i]>0)):
            j, Ej = self.select_aj(i, Ei)
            aj_old = self.a[j].copy()
            if (self.y[i]==self.y[j]):
                L = max(0, self.a[i]+self.a[j]-self.c)
                H = min(self.c, self.a[i]+self.a[j])
            else:
                L = max(0, self.a[j] - self.a[i])
                H = min(self.c, self.c+self.a[j]-self.a[i])
            if L == H:
                return 0
            flag = self.update_aj(i, j, Ei, Ej, H, L)
            if flag == False:
                return 0
            #if (abs(self.a[j]-aj_old)<self.minmove):
             #   return 0
            self.update_ai(i,j,aj_old)
            self.update_b(i, j)
            return 1
        else:
            return 0

    def train(self):
        iters = 0
        notupdate = 0
        last_index = set()
        while(iters < self.maxIter):
            index = set()
            for i in range(len(self.a)):
                if(self.a[i]>0 and self.a[i]<self.c):
                    temp = abs(self.y[i]*self.g(i)-1)
                if 0 < temp and i not in last_index:
                    index.add(i)
            if len(index)==0:
                for i in range(len(self.a)):
                    if(self.a[i]==0):
                        temp = 1-self.y[i]*self.g(i)
                    else:
                        temp = self.y[i]*self.g(i) - 1
                    if 0 < temp and i not in last_index:
                        index.add(i)
            while len(index)>0:
                i = index.pop()
                flag =self.changeaijPair(i)
                if flag==0:
                    notupdate += 1
                    if len(last_index) > 10:
                        last_index.pop()
                        last_index.add(i)
                    else:
                        last_index.add(i)
                else:
                    notupdate = 0
                    iters += 1
                if notupdate > 5000:
                    break
            else:
                break

def cal_w(x, a, y):
    m,n = np.shape(x)
    w = np.zeros((n,1))
    for i in range(m):
        w += a[i]*y[i]*x[i].T
    return w

def predict(w, x):
    return np.sign(np.dot(w,x))

def main():
    a = open("test1.txt")
    b = a.readlines()
    matrix = []
    value = []
    d = 1
    for i in range(len(b)):
        temp = b[i].split(' ')
        matrix.append(list(map(float,temp[0:len(temp)-1])))
        value.append(float(temp[len(temp)-1]))
    smo = SMO(np.mat(matrix), np.array(value), 20, 30000, 0.00001, 0)
    smo.train()
    w = cal_w(smo.x, smo.a, smo.y)
    print(w.T)
    #return 0
    a = open("test2.txt")
    b = a.readlines()
    test = []
    value = []
    for i in range(len(b)):
        temp = b[i].split(' ')
        test.append(list(map(float,temp[0:len(temp)-1])))
        value.append(float(temp[len(temp)-1]))
    mm = list(predict(np.array(test), w))
    wrong = 0
    for i in range(0,len(mm)):
        if mm[i] != value[i]:
            wrong+=1
    print(wrong/len(b))


time_begin = time.time()
main()
print(time.time() - time_begin)