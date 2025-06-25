import numpy as np
import math

def euclidean(l1, l2):
    n = min(len(l1), len(l2))
    return np.sqrt(np.sum((l1[:n] - l2[:n])**2))

def chiSquareDistance(l1, l2):
    n = min(len(l1), len(l2))
    return np.sum((l1[:n] - l2[:n])**2 / l2[:n])

# def bhatta(l1, l2):
#     n = min(len(l1), len(l2))
#     N_1, N_2 = np.sum(l1[:n])/n, np.sum(l2[:n])/n
#     score = np.sum(np.sqrt(l1[:n] * l2[:n]))
#     num = round(score, 2)
#     den = round(math.sqrt(N_1*N_2*n*n), 2)
#     return math.sqrt( 1 - num / den )

def bhatta(l1, l2):
    n = min(len(l1), len(l2))
    l1 = np.clip(l1[:n], 0, None)
    l2 = np.clip(l2[:n], 0, None)

    sum1 = np.sum(l1) + 1e-8
    sum2 = np.sum(l2) + 1e-8

    score = np.sum(np.sqrt(l1 * l2))
    num = round(score, 2)
    den = round(math.sqrt(sum1 * sum2), 2)

    if den == 0:
        return 1.0  # максимально несхожі

    return math.sqrt(max(0.0, 1 - num / den))