from numpy import *
from numpy.linalg import inv
from numpy import identity,shape
from numpy.random.mtrand import rand
from random import *
import Distance

class KalmanFilter:
    def __init__(self, X, P, F, Q, Z, H, R):
        self.X = X
        self.P = P
        self.F = F
        self.Q = Q
        self.Z = Z
        self.H = H
        self.R = R

    def predict(self, X, P):
        X = self.F * X
        P = self.F * P * (self.F) + self.Q
        return (X, P)

    def update(self, X, P, Z):
        K = (P * self.H)/(self.H * P * self.H + self.R)
        X += K * (Z - self.H * X)
        P = (1 - K * self.H) * P
        return (X, P)

P = 1
F = 1
Q = 1e-5
X = -83
H = 1
R = 5
Y = {}
f = open("raw_rssi.txt", "r")
# k = open("rssi_output.txt.txt", "r")
k=0
for i in f:
    k = k+1
    # if i<25:
    #     Z = randint(1, 20) - 90
    # else:
    #     Z = randint(1, 20) - 40
    Z=int(i)
    if k==30:
        k=0
        P=1
    kalman = KalmanFilter(X, P, F, Q, Z, H, R)
    (X, P) = kalman.predict(X, P)
    (X, P) = kalman.update(X, P, Z)
    D = Distance.calculateDistance(-77,X)
    print(str(k)+"     "+str(Z) + "     " + str(X) + "     " + str(D))
    # k.write(str(Z) + "     " + str(X))
# k.close()
f.close()
    # print(X)