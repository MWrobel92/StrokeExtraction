import numpy as np
from ..src.extraction.disc import Disc, create_discs
from ..src.common.numerical import vcos


def get_disc_1():
    cc = np.array([5, 5])
    p1 = np.array([5, 1])
    p2 = np.array([8, 9])
    return Disc(cc, p1, p2)


def test_init():
    d = get_disc_1()
    assert all(d.centre == np.array([5, 5]))
    assert np.isclose(d.radius, 4.5)


def test_print():
    d = get_disc_1()
    assert str(d) == 'C=(5, 5) r=4.50'


def test_radius():
    d = get_disc_1()
    assert np.isclose(d.radius, 4.5)


def test_cos_alpha():
    d = get_disc_1()
    assert np.isclose(d.cos_al, 0.8)


def test_quality_1r():
    d = get_disc_1()
    assert np.isclose(d.quality(4.5), 0.8)


def test_quality_2r():
    d = get_disc_1()
    assert np.isclose(d.quality(9.0), 0.4)


def test_get_directional_vector():
    d = get_disc_1()
    vec = np.array([-3, -8])
    assert np.isclose(vcos(vec, d.get_directional_vector()), 0.0)


def test_create_discs():
    edge_pixels = np.array([[3, 1], [4, 5], [4, 1], [7, 1], [10, 2], [13, 3], [11, 5], [7, 5]])
    skel_pixels = np.array([[3, 3], [6, 3], [7, 3], [10, 4]])
    avg_width = 2.0
    discs = create_discs(edge_pixels, skel_pixels, avg_width)
    assert len(discs) == 3
    assert all(discs[0].centre == np.array([7, 3]))
    assert np.isclose(discs[0].radius, 2.0)
