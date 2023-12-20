import numpy as np
from sklearn.neighbors import KDTree

from ..common.numerical import euc_dist, pcos, f2
from ..config import R_M


class Disc:
    """The single disc, that is a circle inscribed in the letter foreground

    :param array[int] centre: Coordinates of the disc center (in the skeleton)
    :param array[int] point1: Coordinates of the 1st tangent point (letter edge and the circle)
    :param array[int] point2: Coordinates of the 2nd tangent point (letter edge and the circle)
    """

    def __init__(self, centre, point1, point2):
        self.centre = centre
        self.point1 = point1
        self.point2 = point2

        self.radius = (euc_dist(centre, point1) + euc_dist(centre, point2)) * 0.5
        self.cos_al = pcos(point1, centre, point2)

    def __repr__(self):
        return f'C=({self.centre[0]}, {self.centre[1]}) r={f2(self.radius)}'

    def quality(self, expected):
        """Calculate the quality of the disc. An ideal disc should have:

        * the radius length equal to half of the expected stroke width
        * the angle between vectors from a center to tangent points equal to 180 degrees

        :param float expected: Expected radius
        :return: Quality measure in range (0, 1]
        :rtype: float
        """
        return self.cos_al * min(self.radius, expected) / max(self.radius, expected)

    def get_directional_vector(self):
        """Get the vector that is perpendicular to the vector connecting tangent points.
        This vector shows the direction where the neighbor disc should exist
        """
        vec_points = self.point1 - self.point2
        return np.array([vec_points[1], -vec_points[0]])


def create_discs(edge_pixels, skel_pixels, avg_width):
    """Transform a set of pixels into a set of discs

    :param np.ndarray edge_pixels: Egde pixels, each of them might be a tangent point
    :param np.ndarray skel_pixels: Skeleton pixels, each of them might be a disc center
    :param float avg_width: Expected radius
    :return: List of created and selected discs
    :rtype: list[Disc]
    """

    # Use KD-tree to optimize search
    tree = KDTree(edge_pixels, leaf_size=10)
    distances, nearest_ids = tree.query(skel_pixels)

    # Create all possible discs
    discs = []
    for i in range(len(skel_pixels)):

        centre = skel_pixels[i]
        p1 = edge_pixels[nearest_ids[i][0]]
        distance = distances[i][0]

        p2_ideal = (2 * centre) - p1
        max_error = max(1.5, distance)

        p2_dist, p2_id = tree.query([p2_ideal])

        if p2_dist[0][0] < max_error:
            p2 = edge_pixels[p2_id[0][0]]
            discs.append(Disc(centre, p1, p2))

    # Sort discs by quality
    discs.sort(key=lambda x: x.quality(avg_width), reverse=True)

    # Select discs using the greedy algorithm
    selected_discs = []
    while len(discs) > 0:
        best_disc = discs[0]
        selected_discs.append(best_disc)
        cb = best_disc.centre
        cr = best_disc.radius * R_M
        discs = list(filter(lambda x: euc_dist(x.centre, cb) > cr, discs))

    return selected_discs
