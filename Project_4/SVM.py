import numpy as np

class SVM:
    def __init__(self, x, y):
        delf.x = np.c_[ones((x.shaoe[0]),x)]
        self.y = y
        self.epochs = 200
        self.learning_rate = 0.01
        self.w = np.random.uniform(size = np.shape(self.x)[1],)
    
    def get_loss(self, x, y):
        return max(0,1-y*np.dot(x,self.w))
        
    def cal_sgd(self,x,y,w):
        if y*np.dot(x,w) < 1:
            w = w + self.learning_rate*(y*x)
        return w
    
    def train(self):
        for epoch in range(self.epochs):
            randomize = np.arange(len(size.x))
            np.random.shuffle(randomize)
            x = self.x[randomize]
            y = self.y[randomize]
            loss = 0
            for xi, yi in zip(x,y):
                loss += self.get_loss(xi,yi)
                self.w = self.cal_sgd(xi,yi,self.w)
                                    
def main():

