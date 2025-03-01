r"""
Generic Operations for Physical Design (src\physdes\generic.py)

This code defines a set of generic operations that are commonly used in physical design calculations. These operations are designed to work with different types of objects, including simple numbers (scalars) and more complex objects like intervals.

The code contains four main functions: overlap, contain, intersection, and min_dist. Each of these functions takes two inputs, typically referred to as 'lhs' (left-hand side) and 'rhs' (right-hand side), and performs a specific operation on them.

The 'overlap' function checks if two objects overlap or are equal. It returns True if they do overlap, and False otherwise. This function is useful for determining if two physical entities share some common space or value.

The 'contain' function checks if one object contains another. It returns True if the left-hand side object contains the right-hand side object, and False otherwise. This can be used to determine if one physical entity is completely within another.

The 'intersection' function finds the common part between two objects. If the objects are numbers, it returns the number if they're equal. For more complex objects, it returns the overlapping region. This is useful for finding where two physical entities meet or share space.

The 'min_dist' function calculates the minimum Manhattan distance between two objects. For numbers, it simply calculates the absolute difference. For more complex objects, it uses a special method to determine the closest points between the objects. This can be used to find how far apart two physical entities are.

Each of these functions is designed to work with both simple numbers and more complex objects. They do this by first checking if the input objects have special methods (like 'overlaps', 'contains', 'intersect_with', or 'min_dist_with'). If these methods exist, the functions use them. If not, they fall back to simpler calculations assuming the inputs are just numbers.

The code also includes many examples (in the form of doctests) to show how each function works with different types of inputs. These examples help illustrate the behavior of the functions and can be used to automatically test that the functions are working correctly.

Overall, this code provides a flexible set of tools for performing common operations in physical design calculations, capable of working with both simple numbers and more complex geometric objects.
"""


def overlap(lhs, rhs) -> bool:
    """
    The `overlap` function checks if two objects have an overlapping property or are equal.

    :param lhs: The `lhs` parameter represents the left-hand side object that we want to check for
        overlap with the `rhs` parameter

    :param rhs: The parameter `rhs` is the right-hand side of the comparison. It can be any object that
        supports the `overlaps` method or a scalar value

    :return: a boolean value.

    Examples:
        >>> overlap(1, 1)
        True
        >>> overlap(1, 3)
        False
        >>> from physdes.interval import Interval
        >>> overlap(Interval(1, 2), Interval(2, 3))
        True
        >>> overlap(Interval(1, 2), Interval(3, 4))
        False
        >>> overlap(Interval(1, 2), 2)
        True
        >>> overlap(Interval(1, 2), 4)
        False
        >>> overlap(2, Interval(2, 3))
        True
        >>> overlap(1, Interval(3, 4))
        False
        >>> overlap(1, Interval(1, 2))
        True
    """
    if hasattr(lhs, "overlaps"):
        return lhs.overlaps(rhs)
    elif hasattr(rhs, "overlaps"):
        return rhs.overlaps(lhs)
    else:  # assume scalar
        return lhs == rhs


def contain(lhs, rhs) -> bool:
    """
    The `contain` function checks if one object contains another object.

    :param lhs: The `lhs` parameter represents the left-hand side of the comparison, while the `rhs`
        parameter represents the right-hand side of the comparison

    :param rhs: The `rhs` parameter represents the right-hand side of the comparison. It can be any
        value or object that you want to check if it is contained within the `lhs` object

    :return: a boolean value.

    Examples:
        >>> contain(1, 1)
        True
        >>> contain(1, 3)
        False
        >>> from physdes.interval import Interval
        >>> contain(Interval(1, 4), Interval(2, 3))
        True
        >>> contain(Interval(1, 2), Interval(3, 4))
        False
        >>> contain(Interval(1, 2), 2)
        True
        >>> contain(Interval(1, 2), 4)
        False
        >>> contain(2, Interval(2, 3))
        False
        >>> contain(1, Interval(3, 4))
        False
    """
    if hasattr(lhs, "contains"):
        return lhs.contains(rhs)
    elif hasattr(rhs, "contains"):
        return False
    else:  # assume scalar
        return lhs == rhs


def intersection(lhs, rhs):
    """
    The `intersection` function returns the intersection of two objects if they have an
    `intersect_with` method, otherwise it returns the objects themselves if they are equal.

    :param lhs: The `lhs` parameter represents the left-hand side of the intersection operation, while
        the `rhs` parameter represents the right-hand side of the intersection operation

    :param rhs: The `rhs` parameter is the second input to the `intersection` function. It represents
        the right-hand side of the intersection operation

    :return: the intersection of `lhs` and `rhs`.

    Examples:
        >>> print(intersection(1, 1))
        1
        >>> from physdes.interval import Interval
        >>> print(intersection(Interval(1, 2), Interval(2, 3)))
        [2, 2]
        >>> print(intersection(Interval(1, 2), 2))
        [2, 2]
        >>> print(intersection(2, Interval(2, 3)))
        [2, 2]
        >>> print(intersection(1, Interval(1, 2)))
        [1, 1]
        >>> print(intersection(Interval(1, 2), Interval(1, 2)))
        [1, 2]
        >>> print(intersection(Interval(1, 2), Interval(2, 3)))
        [2, 2]
        >>> print(intersection(Interval(1, 2), 2))
        [2, 2]
    """
    if hasattr(lhs, "intersect_with"):
        return lhs.intersect_with(rhs)
    elif hasattr(rhs, "intersect_with"):
        return rhs.intersect_with(lhs)
    else:  # assume scalar
        assert lhs == rhs
        return lhs


def min_dist(lhs, rhs):
    """
    The `min_dist` function calculates the minimum Manhattan distance between two objects, using their
    `min_dist_with` method if available, or by subtracting them if they are scalars.

    :param lhs: The `lhs` parameter represents the left-hand side value or object that we want to
        calculate the minimum Manhattan distance with

    :param rhs: The parameter `rhs` represents the right-hand side value or object that we want to
        compare with the left-hand side value or object `lhs`

    :return: the minimum Manhattan distance between `lhs` and `rhs`.

    Examples:
        >>> min_dist(1, 1)
        0
        >>> min_dist(1, 3)
        2
        >>> from physdes.interval import Interval
        >>> min_dist(Interval(1, 2), Interval(2, 3))
        0
        >>> min_dist(Interval(1, 2), Interval(3, 4))
        1
        >>> min_dist(Interval(1, 2), 2)
        0
        >>> min_dist(Interval(1, 2), 4)
        2
        >>> min_dist(2, Interval(2, 3))
        0
        >>> min_dist(1, Interval(3, 4))
        2
        >>> min_dist(1, Interval(1, 2))
        0
        >>> min_dist(Interval(1, 2), Interval(1, 2))
        0
        >>> min_dist(Interval(1, 2), Interval(2, 3))
        0
        >>> min_dist(Interval(1, 2), 2)
        0
        >>> min_dist(2, Interval(2, 3))
        0
    """
    if hasattr(lhs, "min_dist_with"):
        return lhs.min_dist_with(rhs)
    elif hasattr(rhs, "min_dist_with"):
        return rhs.min_dist_with(lhs)
    else:  # assume scalar
        return abs(lhs - rhs)


# def min_dist_change(lhs, rhs):
#     """
#     The `min_dist_change` function calculates the minimum Manhattan distance change between two objects.
#
#     :param lhs: The `lhs` parameter represents the left-hand side value or object that you want to
#     compare
#     :param rhs: The `rhs` parameter represents the right-hand side value or object that we want to
#     compare with the `lhs` parameter
#     :return: The function `min_dist_change` returns the minimum Manhattan distance change between `lhs` and `rhs`.
#
#     Examples:
#         >>> min_dist_change(1, 1)
#         0
#         >>> min_dist_change(1, 3)
#         2
#         >>> min_dist_change(Interval(1, 2), Interval(2, 3))
#         0
#         >>> min_dist_change(Interval(1, 2), Interval(3, 4))
#         1
#         >>> min_dist_change(Interval(1, 2), 2)
#         0
#         >>> min_dist_change(Interval(1, 2), 4)
#         2
#         >>> min_dist_change(2, Interval(2, 3))
#         0
#         >>> min_dist_change(1, Interval(3, 4))
#         2
#         >>> min_dist_change(1, Interval(1, 2))
#         0
#         >>> min_dist_change(Interval(1, 2), Interval(1, 2))
#         0
#         >>> min_dist_change(Interval(1, 2), Interval(2, 3))
#         0
#         >>> min_dist_change(Interval(1, 2), 2)
#         0
#     """
#     if hasattr(lhs, "min_dist_change_with"):
#         return lhs.min_dist_change_with(rhs)
#     elif hasattr(rhs, "min_dist_change_with"):
#         return rhs.min_dist_change_with(lhs)
#     else:  # assume scalar
#         return abs(lhs - rhs)


def displacement(lhs, rhs):
    """
    The `displacement` function calculates the displacement between two objects or scalars.

    :param lhs: The `lhs` parameter represents the left-hand side of the displacement operation. It can
        be either an object that has a `displace` method or a scalar value

    :param rhs: The `rhs` parameter represents the displacement value that needs to be subtracted from
        the `lhs` parameter

    :return: the displacement between `lhs` and `rhs`. If `lhs` has a `displace` method, it calls that
        method passing `rhs` as an argument. Otherwise, it assumes `lhs` is a scalar and returns the
        difference between `lhs` and `rhs`.

    Examples:
        >>> displacement(1, 1)
        0
        >>> displacement(1, 3)
        -2
        >>> from physdes.interval import Interval
        >>> print(displacement(Interval(1, 2), Interval(2, 3)))
        [-1, -1]
        >>> print(displacement(Interval(1, 2), Interval(3, 4)))
        [-2, -2]
    """
    if hasattr(lhs, "displace"):
        return lhs.displace(rhs)
    else:  # assume scalar
        return lhs - rhs


if __name__ == "__main__":
    import doctest

    doctest.testmod()
