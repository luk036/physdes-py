# import numpy as np


def overlap1(lst: list) -> tuple[int, int] | None:
    num = len(lst)
    for idx in range(num - 1):
        for jdx in range(idx + 1, num):
            if lst[idx].overlaps(lst[jdx]):
                return idx, jdx
    return None
