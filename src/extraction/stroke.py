import numpy as np

from ..common.numerical import euc_dist
from ..config import EPSILON, MAX_ANGLE


class Stroke:
    """Stroke as a sequence of 2D points. This class also allows the transformation of
    the stroke into a parametric form

    :param list chain: Chain of 2D points (centers of discs that make the stroke)
    """

    def __init__(self, chain):
        self.points = chain
        self.approximate()

    def __repr__(self):
        points_repr = [f'({p[0]}, {p[1]})' for p in self.points]
        return '->'.join(points_repr)

    def length_tab(self):
        """Get the table with distances from the beginning of the stroke to the given point
        """
        length_tab = [0.0]
        for i in range(1, len(self.points)):
            new_length = length_tab[-1] + euc_dist(self.points[i - 1], self.points[i])
            length_tab.append(new_length)
        return np.array(length_tab)

    def approximate(self):
        """Make an approximation of the stroke with 2 3rd-degree polynomials. It is a parametric
        form of functions x(t) and y(t) with t in the range [0, 1]. The result of this
        approximation is returned and also stored if fields poly_x and poly_y. The function
        calculates the error of approximation as well and saves it in the field appr_errors
        """
        length_tab = self.length_tab()
        self.length = length_tab[-1]
        t = length_tab / self.length

        x = np.array([point[0] for point in self.points], dtype='float')
        y = np.array([point[1] for point in self.points], dtype='float')

        if len(t) > 3:
            # Approximation with 3rd-degree polynomial
            self.poly_x = np.polyfit(t, x, 3)
            self.poly_y = np.polyfit(t, y, 3)
        else:
            # Approximation with 2nd-degree polynomial
            self.poly_x = np.concatenate(([0.0], np.polyfit(t, x, 2)))
            self.poly_y = np.concatenate(([0.0], np.polyfit(t, y, 2)))

        # Calculate the approximation error
        errors = []
        for i in range(len(t)):
            x_apr = np.polyval(self.poly_x, t[i])
            y_apr = np.polyval(self.poly_y, t[i])
            errors.append(euc_dist(self.points[i], (x_apr, y_apr)))
        self.appr_errors = np.array(errors)

        return self.poly_x, self.poly_y

    def is_good(self):
        """Check if the approximation error is below the threshold
        :rtype: Boolean
        """

        error = self.appr_errors.sum() / (len(self.appr_errors) * self.length)
        return error < EPSILON

    def divide_by_angles(self):
        """Analyze the stroke and cut it in points where the direction changes too rapidly

        :return: Listę kresek (obiektów typu :class:`Stroke`) po podziale
        """

        num = len(self.points)
        # Create a list of vectors using complex numbers
        points_cx = [complex(pt[1], pt[0]) for pt in self.points]
        vectors = [points_cx[i + 1] - points_cx[i] for i in range(num - 1)]
        # Rotate each vector by an angle of the previous one to get the direction change
        rotators = [complex(cx.real, -cx.imag) / abs(cx) for cx in vectors]
        rotated_by_prev = [vectors[i + 1] * rotators[i] for i in range(num - 2)]
        # Get the list of angles between vectors
        angles = np.angle(np.array(rotated_by_prev), deg=True)
        # Future work: consider using neighbor angles as well

        if max(abs(angles)) > MAX_ANGLE:
            breaking_points = np.flatnonzero(abs(angles) > MAX_ANGLE)
            breaking_points = np.append(breaking_points, [len(angles)])  # Add a guard
            previous = 0
            substrokes = []
            for bp in breaking_points:
                substroke = self.points[previous:(bp + 2)]
                if len(substroke) > 2:
                    substrokes.append(Stroke(substroke))
                previous = bp + 1
        else:
            substrokes = [self]

        return substrokes

    def divide_using_error(self):
        """Cut the stroke in such a point that the sum of approximation errors is similar in
        both parts. Do not consider strokes shorter than 3 points
        odrzucane.

        :return: List of at most 2 new strokes (:class:`Stroke` objects)
        """
        err = self.appr_errors

        best_partition = 0
        best_error_diff = err.sum()

        for i in range(1, len(err)):
            sub_error_1 = err[:i].sum()
            sub_error_2 = err[i:].sum()
            error_diff = abs(sub_error_1 - sub_error_2)
            if error_diff < best_error_diff:
                best_error_diff = error_diff
                best_partition = i

        substroke1 = self.points[:best_partition]
        substroke2 = self.points[best_partition:]

        divided = []
        if len(substroke1) > 2:
            divided.append(Stroke(substroke1))
        if len(substroke2) > 2:
            divided.append(Stroke(substroke2))

        return divided

    def vector_of_features(self):
        """Get the stroke as an 8-element vector of features. It contains coefficients of both
        polynomials: first x, then y, both from the highest power

        :rtype: np.array
        """

        return np.concatenate((self.poly_x, self.poly_y))

    def distinctness(self, another_stroke):
        """Get the distinctness measure of the stroke from the one given as an argument

        :param Stroke another_stroke: Stroke to be compared
        :return: Two values - distinctness of this stroke from another and vice versa
        """

        number_of_common = 0
        for p1 in self.points:
            for p2 in another_stroke.points:
                if all(p1 == p2):
                    number_of_common += 1

        d1 = 1.0 - (number_of_common / len(self.points))
        d2 = 1.0 - (number_of_common / len(another_stroke.points))

        return d1, d2

    def shape_string(self):
        """Get the coefficients of polynomials (excluding constant terms) with the precision
        of 5 digits, joined with a semicolon

        :rtype: string
        """
        strings_x = ['{:.5f}'.format(x) for x in self.poly_x]
        strings_y = ['{:.5f}'.format(x) for x in self.poly_y]
        strings_x.extend(strings_y)
        return ';'.join(strings_x)
