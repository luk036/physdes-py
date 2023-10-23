# import numpy as np


def overlap1(lst):
    n = len(lst)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if lst[i].overlaps(lst[j]):
                return i, j
    return None
