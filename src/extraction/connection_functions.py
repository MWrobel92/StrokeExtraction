import numpy as np

from ..common.numerical import euc_dist, pseudo_gaussian, vcos
from ..config import RHO, Q_MIN, QR_MAX


def connection_quality_and_side(disc1, disc2):
    """Calculate the quality of the connection between two discs. The high-quality connection
    should fulfill the following conditions:

    * areas of both discs are similar,
    * the center of the 2nd disc is close to the bisector of an angle between vectors from
      the center of the 1st disc to its tangent points,
    * the disnance between disc centers is close to the radius of the 1st disc.

    Calculate also the information about the location of the 2nd disc regarding the 1st one.
    If discs B and C lay on the same side of disc A, the sign of this value for pairs (A, B)
    and (A, C) should be the same.

    :returns: 2-element tuple (see :meth:`connection_quality` i :meth:`connection_side`)
    """

    r1 = disc1.radius
    r2 = disc2.radius

    distance = euc_dist(disc1.centre, disc2.centre)
    q_dist = pseudo_gaussian(distance, r1, RHO)

    q_area = min(r1, r2) / max(r1, r2)

    direction = disc1.get_directional_vector()
    real = disc1.centre - disc2.centre
    cos_betha = vcos(direction, real)
    q_angle = vcos(direction, real) ** 2

    quality = q_dist * q_area * q_angle
    side = (cos_betha > 0.0)

    return quality, side


def connection_quality(d1, d2):
    """Get only the quality value from :meth:`connection_quality_and_side`

    :returns: ality measure in range (0, 1]
    :rtype: float
    """

    quality, _ = connection_quality_and_side(d1, d2)
    return quality


def connection_side(d1, d2):
    """Get only the information about the side from :meth:`connection_quality_and_side`

    :returns: The location of the 2nd disc regarding the 1st one (left/right)
    :rtype: Boolean
    """
    _, side = connection_quality_and_side(d1, d2)
    return side


def get_connection_matrixes(disc_list):
    """Create two matrices with information about connections between all possible pairs of discs.

    * The first one is a triangular matrix with the quality of each connection (this is
      the representation of a non-directed weighted graph).
    * The second one contains the information about the relative position of the discs.
      If the element (i, j) equals the element (i, k), it means that disc j lays on the same
      side of disc i as disc k, so the chain j-i-k does not make any sense.
    """

    num = len(disc_list)
    quality_matrix = np.zeros((num, num))
    side_matrix = np.full((num, num), False)
    for i in range(num):
        for j in range(i + 1, num):
            qij, sij = connection_quality_and_side(disc_list[i], disc_list[j])
            qji, sji = connection_quality_and_side(disc_list[j], disc_list[i])

            quality_matrix[i, j] = min(qij, qji)

            side_matrix[i, j] = sij
            side_matrix[j, i] = sji

    return quality_matrix, side_matrix


def copy_and_clean(quality_matrix):
    """Make a copy of the matrix with the quality of each connection. Replace
    poor-quality elements with zeros
    """

    num = len(quality_matrix)
    quality_copy = np.zeros((num, num))
    for i in range(num):
        for j in range(i + 1, num):
            quality = quality_matrix[i, j]
            if quality >= Q_MIN:
                quality_copy[i, j] = quality

    return quality_copy


def create_strong_connections(quality_matrix, side_matrix):
    """Make a selection of connections using a greedy algorithm

    :param np.array quality_matrix: Matrix with the quality of each connection,
        created with :meth:`get_connection_matrixes`
    :param np.array side_matrix: Matrix with the the relative position of discs within
        each connection, created with :meth:`get_connection_matrixes`
    :returns: List of connections as tuples (i,j)
    """
    quality_copy = copy_and_clean(quality_matrix)
    matrix_size = len(quality_copy)
    connections = []

    while np.count_nonzero(quality_copy) > 0:

        # Get coordinates of the best elements
        max1d = np.argmax(quality_copy)
        i = max1d // matrix_size
        j = max1d % matrix_size
        connections.append((i, j))

        # Assign zeros to elements that cannot exist together with the best one
        for k in range(matrix_size):
            if side_matrix[i, k] == side_matrix[i, j]:
                quality_copy[min(i, k), max(i, k)] = 0.0
            if side_matrix[j, k] == side_matrix[j, i]:
                quality_copy[min(j, k), max(j, k)] = 0.0

    return connections


def find_alt_connections(quality_matrix, side_matrix, strong_connections):
    """Look for alternative connections, that is the ones that connect the end of one stroke
    to the point within another stroke

    :param np.array quality_matrix: Matrix with the quality of each connection,
        created with :meth:`get_connection_matrixes`
    :param np.array side_matrix: Matrix with the the relative position of discs within
        each connection, created with :meth:`get_connection_matrixes`
    :param list strong_connections: List of connection created with
        :meth:`create_strong_connections`

    :returns: List of tuples (i, j, k) where (i, j) is an alternative connection and k is
        the next disc in the stroke with disc j
    """
    quality_copy = copy_and_clean(quality_matrix)
    number_of_discs = len(quality_copy)
    alt_connections = []

    # Prepare a table with indices of neighbor discs
    neighbors = {
        True: (np.zeros(number_of_discs, dtype='int') - 1),
        False: (np.zeros(number_of_discs, dtype='int') - 1)
    }

    for i, j in strong_connections:
        side_ij = side_matrix[i, j]
        neighbors[side_ij][i] = j
        side_ji = side_matrix[j, i]
        neighbors[side_ji][j] = i

    for i in range(number_of_discs):

        if (neighbors[True][i] < 0) == (neighbors[False][i] < 0):
            # It is not the end of the stroke, skip it
            continue

        empty_side = (neighbors[True][i] < 0)

        alternative = None
        alt_quality = 0.0

        # Check the connections from disc i...
        for j in range(number_of_discs):
            # ...from its free side...
            if side_matrix[i, j] != empty_side:
                continue
            # ...with acceptable quality...
            quality = quality_copy[min(i, j), max(i, j)]
            if quality < Q_MIN:
                continue
            # ...linking to the fragment of another stroke...
            side_ji = side_matrix[j, i]
            k = neighbors[not side_ji][j]
            if k < 0:
                continue
            # ...and not much worse from the existing connection within the stroke
            k2 = neighbors[side_ji][j]
            cmp_quality = quality_copy[min(k2, j), max(k2, j)]
            if (cmp_quality - quality) > QR_MAX:
                continue

            if cmp_quality > alt_quality:
                alternative = (i, j, k)
                alt_quality = cmp_quality

        if not (alternative is None):
            alt_connections.append(alternative)

    return alt_connections


def create_connections(discs):
    """Do the entire stage of creating connections (basic and alternative)

    :param list discs: List of discs
    """
    quality_matrix, side_matrix = get_connection_matrixes(discs)
    connections = create_strong_connections(quality_matrix, side_matrix)
    alt_connections = find_alt_connections(quality_matrix, side_matrix, connections)
    return connections, alt_connections
