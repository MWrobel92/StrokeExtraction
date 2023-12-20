import numpy as np

from ..src.common.numerical import vlen, euc_dist, f2, vcos, pcos, pseudo_gaussian


def test_vlen():
    length = vlen(np.array([-4, 3]))
    assert np.isclose(length, 5.0)


def test_euc_dist():
    dist = euc_dist(np.array([5, 5]), np.array([8, 9]))
    assert np.isclose(dist, 5.0)


def test_f2():
    assert f2(0.37875) == '0.38'


def test_vcos_0_deg():
    cosine = vcos(np.array([2, 3]), np.array([4, 6]))
    assert np.isclose(cosine, 1.0)


def test_vcos_60_deg():
    cosine = vcos(np.array([2, 0]), np.array([2, 2 * np.sqrt(3.0)]))
    assert np.isclose(cosine, 0.5)


def test_vcos_90_deg():
    cosine = vcos(np.array([2, 3]), np.array([-3, 2]))
    assert np.isclose(cosine, 0.0)


def test_pcos_45_deg():
    cosine = pcos(np.array([6, 2]), np.array([4, 4]), np.array([1, 4]))
    assert np.isclose(cosine, 0.7071)


def test_pcos_0_deg():
    cosine = pcos(np.array([6, 2]), np.array([4, 4]), np.array([2, 6]))
    assert np.isclose(cosine, 1.0)


def test_pseudo_gaussian_ideal():
    assert np.isclose(pseudo_gaussian(5, 5, 5), 1.0)
    assert np.isclose(pseudo_gaussian(3, 3, 2), 1.0)


def test_pseudo_gaussian_equal():
    var1 = pseudo_gaussian(2.5, 5, 2)
    var2 = pseudo_gaussian(7.5, 5, 2)
    assert var1 > 0.0
    assert var1 < 1.0
    assert np.isclose(var1, var2)


def test_pseudo_gaussian_diff():
    var1 = pseudo_gaussian(2.5, 5, 2)
    var2 = pseudo_gaussian(3.5, 5, 2)
    var3 = pseudo_gaussian(2.5, 5, 5)
    assert var2 > var1
    assert var3 > var1
