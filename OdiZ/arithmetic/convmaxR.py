from __future__ import division
import numpy as np

def convmaxR(u, v):
    m = len(u)
    n = len(v)
    
    ij1 = []
    maxij = np.zeros((m, n))
    ww = np.zeros((m, n))
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            maxij[i - 1, j - 1] = max(i - 1, j - 1)
            ww[i - 1, j - 1] = u[i - 1] * v[j - 1]

    temp = np.zeros((m, n, m))
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if maxij[i - 1, j - 1] == k - 1:
                    temp[i - 1, j - 1, k - 1] = ww[i - 1, j - 1]

    ss1 = []
    for k in range(n):
        ss1.append(sum(sum(temp[:, :, k])))

    return ss1        

if __name__ == "__main__":
    u = [1, 2, 3, 4, 5, 6]
    v = [4, 8, 12, 14, 16, 20]
    print(convmaxR(u, v))