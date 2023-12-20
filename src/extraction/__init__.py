"""Functions and classes related strictly to stroke extraction
"""

import numpy as np
from scipy.ndimage import label
from skimage.filters import threshold_otsu
from skimage.morphology import skeletonize, dilation, erosion

from .disc import create_discs
from .connection_functions import create_connections
from .chain_functions import create_chains
from .stroke_functions import chains_to_strokes


def preprocessing(grayscale_image):
    """Do a preprocessing. It contains:

    * binarization,
    * noise reduction,
    * bold (if necessary),
    * adding margin.

    :param np.array grayscale_image: Input image in grayscale

    :returns: Preprocessed binary image
    :rtype: np.array
    """

    # Thresholding
    threshold = threshold_otsu(grayscale_image)
    binary = (grayscale_image < threshold)

    # Skeletonization
    skeleton = skeletonize(binary)

    # Noise reduction (and bold)
    num_foreground = np.count_nonzero(binary)
    num_skeleton = np.count_nonzero(skeleton)
    avg_width = num_foreground / num_skeleton
    struct_element = np.array([[0.0, 0.0, 0.0], [0.0, 1.0, 1.0], [0.0, 1.0, 0.0]])
    binary = dilation(binary, struct_element)
    if avg_width > 3.0:
        binary = erosion(binary, struct_element)

    # Adding margin (1 pixel arround)
    binary = np.pad(binary, ((1, 1), (1, 1)), 'constant', constant_values=False)
    return binary


def stroke_extraction(input_image):
    """Do the entire stroke extraction. Transform a raster input image into a set
    of extracted strokes

    :param np.array input_image: Input image in grayscale (bright background)

    :returns: List of extracted :class:`Stroke` objects
    :rtype: list[Stroke]
    """
    # Preprocessing
    binary = preprocessing(input_image)

    # Segmentation
    labeled, number_of_areas = label(binary)
    extracted_strokes = []

    # TODO: Try to make it parallel
    for this_label in range(1, number_of_areas + 1):
        segment = (labeled == this_label)

        # Split the set of pixels into background, interior, and boundary
        enlarged = dilation(segment)
        skeleton = skeletonize(segment)
        edge = enlarged ^ segment

        skel_pixels = np.transpose(np.nonzero(skeleton))
        edge_pixels = np.transpose(np.nonzero(edge))

        # Estimate the average stroke width
        avg_width = np.count_nonzero(segment) / len(skel_pixels)

        # Create discs
        discs = create_discs(edge_pixels, skel_pixels, avg_width)

        # Create connections
        connections, alt_connections = create_connections(discs)

        # Create chains and, finally, strokes
        chains = create_chains(connections, alt_connections)
        segment_strokes = chains_to_strokes(discs, chains)

        extracted_strokes.extend(segment_strokes)

    return extracted_strokes
