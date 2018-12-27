import numpy as np
import random

class SMO:
    def __init__(self,x, y, C, maxIter,toler, minmove):
        self.x = x# Training data, num*dimension
        self.y = y# Label data
        self.a = np.random.uniform(size = np.shape(self.x)[1],)
        self.c = C
        self.e = np.zeros((len(self.x),2))
        self.b = 0
        self.maxIter = maxIter
        self.toler = toler #Means the range of the size of the mistake 
        self.minmove = minmove #means that the min distance the alpha move each time 

    def g(self, i):
        g = self.b
        for j in range(len(self.x)):
            g += self.a[j]*self.a[j]*np.dot(self.x[i], self.x[j])
        return g

    def E(self, i):
        E = self.g(i)-self.y[i]

    def updateE(self, index):
        e = self.E(index)
        self.e[index] = [1,e]

    def select_aj(self,i,Ei):
        maxj = 0
        index = 0
        self.e[i] = [1,Ei]
        validE = np.nonzero(self.e[:,0].A)[0]
        if len(validE>1):
            for n in validE:
                if n != i:
                    delta = abs(Ei - self.E(n))#The difference of two E of i and n
                    if delta > maxj:
                        index = n
                        maxj = delta
        else:
            index = random.randint(0, len(self.x)-1)
            while(index == i):
                index = random.randint(0, len(self.x)-1)
        return index,self.E(index)

    def get_aj(self,aj, H, L):# Make sure that a not out of range
        if aj>H:
            aj = H
        elif aj<L:
            aj = L
        return aj

    def update_aj(self, i, j):
        inta = np.dot(self.x[i], self.x[i]) + np.dot(self.x[j], self.x[j]) - 2*np.dot(self.x[i], self.x[j])
        if inta >= 0:
            return False
        self.a[j] = self.a[j] + y[i]*(self.e[i,1] - self.e[j,1])/inta
        self.updateE(j)
        return True

    def update_ai(self, i, j, aj_old):
        self.a[i] = self.a[i] + self.y[i]*self.y[j]*(aj_old - self.a[j])
        self.updateE(i)

    def cal_b1(self, i, j):
        return self.b - self.e[i,1] - self.y[i]*np.dot(self.x[i], self.x[i]) - self.y[j]*np.dot(self.x[j], self.x[i])

    def cal_b2(self, i, j):
        return self.b - self.e[j,1] - self.y[i]*np.dot(self.x[i], self.x[j]) - self.y[j]*np.dot(self.x[j], self.x[j])

    def update_b(self, i, j):
        if (self.a[i]>0) and (self.a[i]<self.c):
            self.b = self.cal_b1(i,j)
        elif(self.a[j]>0) and (self.a[j]<self.c):
            self.b = self.cal_b2(i, j)
        else:
            self.b = (self.cal_b1(i, j) + self.cal_b2(i, j)) / 2

    def changeaijPair(self, i):
        Ei = self.E(i)
        if ((self.y[i]*Ei< - self.toler) and (self.a[i]<self.c)) or ((self.y[i]*Ei>self.toler) and (self.a[i]>0)):
            j, Ej = self.select_aj(i, Ei)
            ai_old = self.a[i].copy()
            aj_old = self.a[j].copy()
            if (self.y[i]==self.y[j]):
                L = max(0, self.a[i]+self.a[j]-self.c)
                H = min(self.c, self.a[i]+self.a[j])
            else:
                L = max(0, self.a[j] - self.a[i])
                H = min(self.c, self.c+self.a[j]-self.a[i])
            if L >= H:
                return 0
            flag = self.update_aj(i, j)
            if flag == False:
                return 0
            if (abs(self.a[j]-aj_old)<self.minmove):
                return 0
            self.update_ai(i,j,aj_old)
            self.update_b(i, j)
            return 1
        else:
            return 0           

    def select_ai(self, needRepeat):
        aChanged = 0
        if needRepeat:
            for i in range(len(self.x)):
                aChanged += self.changeaijPair(i)
        else:
            nonBounds = np.nonzero((self.a.A>0)*(self.a.A<self.c))[0]
            for i in nonBounds:
                aChanged += self.changeaijPair(i)
        return aChanged

    def train(self):
        iters = 0
        needRepeat = True
        aChanged = 0
        while(iters < self.maxIter and (needRepeat or aChanged>0)):
            aChanged = self.select_ai(needRepeat)
            iters += 1
            if needRepeat:
                needRepeat = False
            elif(aChanged == 0):
                needRepeat = True

def cal_w(x, a, y):
    m, n = np.shape(x)
    w = np.zeros(n,1)
    for i in range(m):
        w += np.multiply(np.dot(a[i],y[i]),x[i,:].T)
    return w

def main():
    a = open("train_data.txt")
    b = a.readlines()
    matrix = []
    value = []
    d = 0.8
    for i in range(0, int(len(b)*d)):
        temp = b[i].split(' ')
        matrix.append(list(map(float,temp[0:len(temp)-1])))
        value.append(float(temp[len(temp)-1]))
    smo = SMO(np.array(matrix), np.array(value), 200, 2000, 0.001, 0.000001)
    smo.train()
    w = cal_w(smo.x, smo.a, smo.y)
    print(len(w))

main()