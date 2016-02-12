from __future__ import division
import numpy as np
import scipy as sp
from scipy.optimize import minimize
from Rsub import Rsub
from convsubR import convsubR

def Zsub(Z1A, Z1As, Z1B, Z1Bs, Z2A, Z2As, Z2B, Z2Bs):
    
    m1 = len(Z1As)
    m2 = len(Z2As)
    n1 = len(Z1Bs)
    n2 = len(Z2Bs)
            
    e = 0.0001
    
    x01 = [1 for i in range(m1)]
    x02 = [1 for i in range(m2)]
    Aeq = tuple([(e, None) for i in range(m1)])
    
    global C1
    C1 = Z1A
    
    p1 = []
    for i in range(n1):
        global d1
        d1 = Z1Bs[i]
        fun1 = lambda x: (np.dot(C1, x) - d1) * (np.dot(C1, x) - d1)

        x = minimize(fun1, x01, method = 'SLSQP', bounds = Aeq,  constraints = ({'type': 'eq', 'fun': lambda x:  1 - sum(x)}))
        p1.append(x.x)
    p1 = np.array(p1).transpose()
    
    C2 = Z2A
    p2 = []
    for i in range(n2):
        global d2
        d2 = Z1Bs[i]
        fun2 = lambda x: (np.dot(C2, x) - d2) * (np.dot(C2, x) - d2)
        
        x = minimize(fun2, x02, method = 'SLSQP', bounds = Aeq,  constraints = ({'type': 'eq', 'fun': lambda x:  1 - sum(x)}))
        p2.append(x.x)    
    p2 = np.matrix(p2).transpose()
    
    
    Z3A, Z3As = Rsub(Z1A,Z1As,Z2A,Z2As)
    u = p1
    v = p2
    ZconvM = []
    for k1 in range(n1):
        for k2 in range(n2):
            ZconvM.append(convsubR(u[:, k1], v[:, k2]))

    p3 = np.array(ZconvM).transpose()
    
    Z1p=p1
    Z2p=p2
    Z3p=p3
      
    Z12B = np.zeros((n1, n2))
    for k1 in range(n1):
        for k2 in range(n2):
            Z12B[k1, k2] = min(Z1B[k1], Z2B[k2])

    Z3B = Z12B.max(axis = 0)
    Z12Bs = np.zeros((n1, n2))
    for k1 in range(n1):
        for k2 in range(n2):
            Z12Bs[k1, k2] = np.dot(Z3A, convsubR(u[:, k1], v[:, k2]))
       
    Z3Bs = Z12Bs.max(axis = 0)
    Z3Bs = np.unique(Z3Bs)

    return Z3A, Z3As, Z3B, Z3Bs, Z3p, Z1p, Z2p
    
if __name__ == "__main__":
  
    Z1As=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    Z1A=[0, 0, 0, 0, 0.2, 0.4, 0.6, 0.8, 1, 0.5, 0]

    Z1Bs=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    Z1B=[0, 0, 0, 0, 0.5, 1, 0.5, 0, 0, 0, 0]

    Z2As=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    Z2A=[0, 0, 0.5, 1, 0.5, 0, 0, 0, 0, 0, 0]

    Z2Bs=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    Z2B=[0, 0, 0, 0, 0, 0, 0, 0.5, 1, 0.5, 0]
    
    print(Zsub(Z1A, Z1As, Z1B, Z1Bs, Z2A, Z2As, Z2B, Z2Bs))