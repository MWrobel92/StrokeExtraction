import numpy as np

from ..src.extraction.stroke import Stroke
from ..src.extraction.chain_functions import centres_from_chain
from .test_connection_functions import create_discs_set


def create_example_stroke():
    discs = create_discs_set()
    chain = [2, 1, 3, 4]
    return Stroke(centres_from_chain(discs, chain))


def test_init():
    stroke = create_example_stroke()
    assert len(stroke.points) == 4


def test_str():
    stroke = Stroke(centres_from_chain(create_discs_set(), [0, 1, 2]))
    assert str(stroke) == '(2, 3)->(4, 6)->(4, 9)'


def test_length_tab():
    stroke = create_example_stroke()
    tab = stroke.length_tab()
    assert len(tab) == 4
    assert np.isclose(tab[0],  0.0)
    assert np.isclose(tab[1],  3.0)
    assert np.isclose(tab[-1], 8.656854)


def test_approximate():
    stroke = create_example_stroke()
    poly_x, poly_y = stroke.approximate()
    assert len(poly_x) == len(poly_y) == 4
    assert not all(poly_x == poly_y)


def test_approximate_short():
    stroke = Stroke(centres_from_chain(create_discs_set(), [0, 1, 2]))
    poly_x, poly_y = stroke.approximate()
    assert len(poly_x) == len(poly_y) == 4
    assert not all(poly_x == poly_y)
    assert np.isclose(poly_x[0], 0.0) and np.isclose(poly_y[0], 0.0)


def test_is_good():
    stroke = create_example_stroke()
    poly_x, poly_y = stroke.approximate()
    assert stroke.is_good()


def test_is_good_false():
    stroke = Stroke(centres_from_chain(create_discs_set(), [0, 1, 2, 3, 4]))
    assert not stroke.is_good()


def test_divide_using_error():
    stroke = Stroke(centres_from_chain(create_discs_set(), [0, 1, 2, 3, 4]))
    divided = stroke.divide_using_error()
    assert len(divided) == 1
    assert type(divided[0]) is Stroke


def test_vector_of_features():
    stroke = create_example_stroke()
    vec = stroke.vector_of_features()
    assert len(vec) == 8


def test_distinctness():
    s1 = Stroke(centres_from_chain(create_discs_set(), [1, 2, 3, 4]))
    s2 = Stroke(centres_from_chain(create_discs_set(), [0, 1, 2]))
    distinctness_12, distinctness_21 = s1.distinctness(s2)
    distinctness_1a, distinctness_1b = s1.distinctness(s1)
    assert np.isclose(distinctness_1a, 0.0)
    assert np.isclose(distinctness_1b, 0.0)
    assert np.isclose(distinctness_12, 0.5)
    assert np.isclose(distinctness_21, 0.333333)
