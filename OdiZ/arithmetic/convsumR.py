from __future__ import division
import numpy as np

def convsumR(u, v):
    m = len(u)
    n = len(v)
    
    ij1 = []
    ww = np.zeros((m, n))
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            ij1.append((i - 1) + (j - 1))
            ww[i - 1, j - 1] = u[i - 1] * v[j - 1]

    temp = np.zeros((m, n, m))
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if (i + j >= 2 * k - 1) and (i + j <= 2 * k):
                    temp[i - 1, j - 1, k - 1] = ww[i - 1, j - 1]

    ss1 = []
    for k in range(n):
        ss1.append(sum(sum(temp[:, :, k])))

    return ss1        


if __name__ == "__main__":
    u = [1, 2, 3, 4, 5, 6]
    v = [4, 8, 12, 14, 16, 20]
    print(convsumR(u, v))

    u = [0.17618838, 0.17618838, 0.17618838, 0.176169962, 0.174514383, 0.120750517, 0, 0, 0, \
    0, 0]
    v = [0.184112698, 0.130102247, 0, 0, 0, 0, 0, 0.130102247, 0.184112698, 0.185775727, \
    0.185794383]
    print(convsumR(u, v))