import numpy as np
import time

class SVM:
    def __init__(self, x, y):
        self.x = np.c_[np.ones((x.shape[0])),x]
        self.y = y
        self.epochs = 200
        self.learning_rate = 0.01
        self.w = np.random.uniform(size = np.shape(self.x)[1],)
    
    def get_loss(self, x, y):
        return max(0,1 - y * np.dot(x,self.w))
        
    def cal_sgd(self,x,y,w):
        if y*np.dot(x,w) < 1:
            w = w + self.learning_rate*(y*x)
        return w
    
    def train(self):
        l = 0
        randomize = np.arange(len(self.x))
        np.random.shuffle(randomize)
        x = self.x[randomize]
        y = self.y[randomize]
        for xi, yi in zip(x,y):
            l += self.get_loss(xi,yi)
        for epoch in range(self.epochs):
            randomize = np.arange(len(self.x))
            np.random.shuffle(randomize)
            x = self.x[randomize]
            y = self.y[randomize]
            loss = 0
            for xi, yi in zip(x,y):
                loss += self.get_loss(xi,yi)
                self.w = self.cal_sgd(xi,yi,self.w)
            if loss == 0:
                break
            elif(loss<(l//500)):
                self.learning_rate = 0.001
            elif(loss<(l//200)):
                self.learning_rate=0.005
            elif(loss<(l//100)):
                self.learning_rate=0.01
            elif(loss<(l//50)):
                self.learning_rate=0.05

def predict(x, w):
    test = np.c_[np.ones((x.shape[0])), x]
    return np.sign(np.dot(test, w))

def main():
    #path = "test.txt"
    path = input("Please input the path of training data: ") or "test.txt"
    a = open(path)
    b = a.readlines()
    matrix = []
    value = []
    d = 0.9
    for i in range(0, int(len(b)*d)):
        temp = b[i].split(' ')
        matrix.append(list(map(float,temp[0:len(temp)-1])))
        value.append(float(temp[len(temp)-1]))
    svm = SVM(np.array(matrix), np.array(value))
    #print(len(np.array(value)))
    svm.train()
    #print(svm.w)
    f = open('GDModel.txt','w') 
    l = ''
    for i in svm.w:
        l+=str(i)+' '
    print(l,end='',file=f)

begin=time.time()
main()
print(time.time()-begin)