from __future__ import division
import numpy as np

def Rmax(A, As, B, Bs):

    Z1A, Z1As, Z2A, Z2As = A, As, B, Bs
    m1 = len(Z1As)
    m2 = len(Z2As)
    m3 = m1
    
    tmp32 = np.zeros((m1, m2))
    for i in range(m1):
        for j in range(m2):
            tmp32[i, j] = min(Z1A[i],Z2A[j])
    
    supp32 = np.zeros((m1, m2))
    for i in range(m1):
	    for j in range(m2):
		    supp32[i, j] = max(Z1As[i], Z2As[j])
				
    tmp3 = np.zeros((m1, m2, m3))
    supp3 = np.zeros((m1, m2, m3))
    
    for k in range(1, m3 + 1):
        for i in range(1, m1 + 1):
            for j in range(1, m2 + 1):
                if (max(i, j) == k):
                    tmp3[i - 1, j - 1, k - 1] = tmp32[i - 1, j - 1]
    
    out1 = []
    out2 = []
                
    for k in range(m3):
        tmp22 = tmp3[:, :, k]
        i,j = np.unravel_index(tmp22.argmax(), tmp22.shape)
        out1.append(tmp22[i,j])
        out2.append(supp32[i,j])

    return out1, out2

if __name__ == "__main__": 
    print(Rmax([1, 2, 3, 4], [0.2, 0.4, 0.1, 0.3], [5, 2, 3, 6], [0.1, 0.3, 0.5, 0.8]))
        
