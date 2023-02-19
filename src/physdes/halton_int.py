from typing import List, Tuple


def vdc(k: int, base: int = 2, scale: int = 10) -> int:
    """[summary]

    Arguments:
        k (int): number

    Keyword Arguments:
        base (int): [description] (default: {2})

    Returns:
        int: [description]
    """
    vdc: int = 0
    factor: int = base**scale
    while k != 0:
        factor //= base
        remainder: int = k % base
        k //= base
        vdc += remainder * factor
    return vdc


class vdcorput:
    def __init__(self, base: int = 2, scale: int = 10):
        """[summary]

        Args:
            base (int, optional): [description]. Defaults to 2.
        """
        self._base: int = base
        self._scale: int = scale
        self._count: int = 0

    def __call__(self) -> int:
        """[summary]

        Returns:
            float: [description]
        """
        self._count += 1
        return vdc(self._count, self._base, self._scale)

    def reseed(self, seed: int):
        self._count = seed


class halton:
    """Generate Halton sequence"""

    def __init__(self, base: List[int], scale: List[int]):
        """[summary]

        Args:
            base (List[int]): [description]
            scale (List[int]): [description]
        """
        self._vdc0 = vdcorput(base[0], scale[0])
        self._vdc1 = vdcorput(base[1], scale[1])

    def __call__(self) -> Tuple[int, int]:
        """Get the next item

        Returns:
            list(float):  the next item
        """
        return (self._vdc0(), self._vdc1())

    def reseed(self, seed: int):
        """[summary]

        Args:
            seed (int): [description]
        """
        self._vdc0.reseed(seed)
        self._vdc1.reseed(seed)


if __name__ == "__main__":
    halgen = halton([2, 3], [11, 7])
    for _ in range(20):
        print(halgen())
