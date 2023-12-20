import numpy as np


def vlen(vec):
    """Return the vector length

    :rtype: float"""
    return np.sqrt((vec ** 2).sum())


def euc_dist(v1, v2):
    """Return the Euclidean distance between the two vectors

    :rtype: float"""
    return np.sqrt(((v1 - v2) ** 2).sum())


def f2(float_number):
    """Format the float number to 2 digits after the comma

    :rtype: string
    """
    return '{:.2f}'.format(float_number)


def vcos(v1, v2):
    """Get the cosine of the angle between the two vectors

    :rtype: float"""
    return np.dot(v1, v2) / (vlen(v1) * vlen(v2))


def pcos(a, b, c):
    """Get the cosine of the angle between vectors AB and BC.
    Parameters: the coordinates of points A, B, and C

    :rtype: float"""
    return vcos(b - a, c - b)


def pseudo_gaussian(real, ideal, rho):
    """Returns a similarity of two values. For equal values, returns 1. For very different values,
    tends to 0. It is based on the Gaussian curve

    :param float ideal: The tested value
    :param float real: The value for which the function should return 1
    :param float rho: Controls the width of the bell curve

    :rtype: float
    """

    temp = -(((ideal - real) / ideal) ** 2)
    return np.exp(temp / rho)
