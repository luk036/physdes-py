from numpy import isscalar


def overlap(lhs, rhs) -> bool:
    """[summary]

    Args:
        lhs ([type]): [description]
        rhs ([type]): [description]

    Returns:
        bool: [description]
    """
    if not isscalar(lhs):
        return lhs.overlaps(rhs)
    elif not isscalar(rhs):
        return rhs.overlaps(lhs)
    else:
        return lhs == rhs


def contain(lhs, rhs) -> bool:
    """[summary]

    Args:
        lhs ([type]): [description]
        rhs ([type]): [description]

    Returns:
        bool: [description]
    """
    if not isscalar(lhs):
        return lhs.contains(rhs)
    elif not isscalar(rhs):
        return False
    else:
        return lhs == rhs


def intersection(lhs, rhs):
    """[summary]

    Args:
        lhs ([type]): [description]
        rhs ([type]): [description]

    Returns:
        [type]: [description]
    """
    if not isscalar(lhs):
        return lhs.intersection_with(rhs)
    elif not isscalar(rhs):
        return rhs.intersection_with(lhs)
    else:
        assert lhs == rhs
        return lhs


def min_dist(lhs, rhs):
    """[summary]

    Args:
        lhs ([type]): [description]
        rhs ([type]): [description]

    Returns:
        [type]: [description]
    """
    if not isscalar(lhs):
        return lhs.min_dist_with(rhs)
    elif not isscalar(rhs):
        return rhs.min_dist_with(lhs)
    else:
        return abs(lhs - rhs)


def min_dist_change(lhs, rhs):
    """[summary]

    Args:
        lhs ([type]): [description]
        rhs ([type]): [description]

    Returns:
        [type]: [description]
    """
    if not isscalar(lhs):
        return lhs.min_dist_change_with(rhs)
    elif not isscalar(rhs):
        return rhs.min_dist_change_with(lhs)
    else:
        return abs(lhs - rhs)
