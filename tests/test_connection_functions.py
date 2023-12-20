import numpy as np
from ..src.extraction.connection_functions import connection_quality, connection_side, \
    get_connection_matrixes, copy_and_clean, create_strong_connections, find_alt_connections, \
    create_connections
from ..src.extraction.disc import Disc


def create_disc(cx, cy, p1x, p1y, p2x, p2y):
    return Disc(np.array([cx, cy]), np.array([p1x, p1y]), np.array([p2x, p2y]))


def create_discs_set():
    """Create an example set of discs:

    The set contains 5 discs, as in the matrix below:
    - a number is the disc center,
    - an "x" is the tangent point

    0 1 2 3 4 5 6 7 8 9
    1 . . . . . . x . .
    2 . . x . . x . 5 .
    3 . 1 . . . . 4 . x
    4 x . . . . . . x .
    5 . . . . . . . . .
    6 . x - 2 - x . . .
    7 . . . . . . . . .
    8 . . . . . . . . .
    9 . x - 3 - x . . .
    """
    d1 = create_disc(2, 3, 3, 2, 1, 4)
    d2 = create_disc(4, 6, 2, 6, 6, 6)
    d3 = create_disc(4, 9, 2, 9, 6, 9)
    d4 = create_disc(7, 3, 6, 2, 8, 4)
    d5 = create_disc(8, 2, 9, 3, 7, 1)
    return d1, d2, d3, d4, d5


def test_connection_quality_ideal():
    d1, d2, d3, d4, d5 = create_discs_set()
    q45 = connection_quality(d4, d5)
    assert np.isclose(q45, 1.0)


def test_connection_quality_range():
    d1, d2, d3, d4, d5 = create_discs_set()
    q12 = connection_quality(d1, d2)
    q13 = connection_quality(d1, d3)
    q21 = connection_quality(d2, d1)
    assert min(q12, q13, q21) > 0.0
    assert max(q12, q13, q21) < 1.0


def test_connection_quality_relations():
    d1, d2, d3, d4, d5 = create_discs_set()
    q12 = connection_quality(d1, d2)
    q13 = connection_quality(d1, d3)
    q21 = connection_quality(d2, d1)
    assert q12 > q13
    assert q12 > q21


def test_connection_side():
    d1, d2, d3, d4, d5 = create_discs_set()
    s21 = connection_side(d2, d1)
    s24 = connection_side(d2, d4)
    s23 = connection_side(d2, d3)
    assert s21 == s24
    assert s21 != s23


def test_get_connection_matrixes_size():
    discs = create_discs_set()
    quality_matrix, side_matrix = get_connection_matrixes(discs)
    assert len(quality_matrix) == 5
    assert len(side_matrix) == 5
    assert len(quality_matrix[0]) == 5


def test_get_connection_matrixes_triangle():
    discs = create_discs_set()
    quality_matrix, side_matrix = get_connection_matrixes(discs)
    is_zero = []
    for i in range(5):
        for j in range(5):
            if i >= j:
                is_zero.append(np.isclose(0.0, quality_matrix[i, j]))
    assert all(is_zero)


def test_get_connection_matrixes_quality():
    discs = create_discs_set()
    quality_matrix, side_matrix = get_connection_matrixes(discs)
    assert np.isclose(quality_matrix[3, 4], 1.0)
    assert quality_matrix[0, 1] > quality_matrix[0, 2]


def test_get_connection_matrixes_side():
    discs = create_discs_set()
    quality_matrix, side_matrix = get_connection_matrixes(discs)
    assert side_matrix[1, 0] == side_matrix[1, 3]
    assert side_matrix[1, 3] != side_matrix[1, 2]


def test_copy_and_clean():
    d1, d2, d3, d4, d5 = create_discs_set()
    d6 = create_disc(10, 2, 11, 1, 9, 3)
    discs = [d2, d3, d4, d5, d6]
    quality_matrix, side_matrix = get_connection_matrixes(discs)
    cleaned = copy_and_clean(quality_matrix)
    assert cleaned[1, 4] < quality_matrix[1, 4]
    assert cleaned[0, 2] > 0.0
    assert np.isclose(cleaned[1, 4], 0.0)


def test_create_strong_connections():
    discs = create_discs_set()
    quality_matrix, side_matrix = get_connection_matrixes(discs)
    connections = create_strong_connections(quality_matrix, side_matrix)
    assert len(connections) == 3
    assert connections[0] == (3, 4)
    assert connections[1] == (1, 2)
    assert connections[2] == (0, 1)


def test_create_alt_connections():
    discs = create_discs_set()
    quality_matrix, side_matrix = get_connection_matrixes(discs)
    connections = create_strong_connections(quality_matrix, side_matrix)
    alt = find_alt_connections(quality_matrix, side_matrix, connections)
    assert len(alt) == 1
    assert alt[0] == (3, 1, 2)


def test_create_connections():
    discs = create_discs_set()
    connections, alt_connections = create_connections(discs)
    assert len(alt_connections) == 1
    assert len(connections) == 3
    assert connections[0] == (3, 4)
