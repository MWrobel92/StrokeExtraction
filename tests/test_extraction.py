import numpy as np
import skimage.io as io
import warnings

from ..src.extraction import preprocessing, stroke_extraction


def test_preprocessing():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        input_image = io.imread('data/tx.png', as_gray=True)
    binary = preprocessing(input_image)
    foreground_num = np.count_nonzero(binary)
    assert foreground_num > 500
    assert foreground_num < 1000


def test_extraction_stage():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        input_image = io.imread('data/tx.png', as_gray=True)
    strokes = stroke_extraction(input_image)
    assert len(strokes) == 4
