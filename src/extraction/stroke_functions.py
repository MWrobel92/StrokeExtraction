from .stroke import Stroke
from .chain_functions import centres_from_chain
from ..config import D_MIN


def recursive_stroke_analyze(stroke):
    """Check if the stroke should be partitioned into smaller pieces. If yes, cut it
    and recursively check both new parts

    :param Stroke stroke: Input stroke
    :returns: The list of output strokes
    """
    if stroke.is_good():
        result = [stroke]
    else:
        parts = stroke.divide_using_error()
        result = []
        for part in parts:
            divided = recursive_stroke_analyze(part)
            result.extend(divided)
    return result


def chains_to_strokes(discs, chains):
    """Transform the set of chains into a set of Stroke objects. This stage contains:

    * creation of stroke objects,
    * partitioning of the strokes with too high curvature,
    * removing stroke with too low distinctness (covered by another one).

    :param list discs: List of discs in such order that the index stored in a chain means
        the position of the disc within this list
    :param list chains: List of chains where each cain is the list of indices

    :return: List of strokes
    :rtype: List[Stroke]
    """
    strokes = []

    # Creation of stroke objects and partitioning of the ones with too high curvature
    for chain in chains:
        centres = centres_from_chain(discs, chain)
        new_stroke = Stroke(centres)
        for stroke in new_stroke.divide_by_angles():
            strokes.extend(recursive_stroke_analyze(stroke))

    # Selecting strokes with too low distinctness
    to_drop = set()
    for i in range(len(strokes)):
        for j in range(i + 1, len(strokes)):
            d1, d2 = strokes[i].distinctness(strokes[j])
            if d1 < d2:
                if d1 < D_MIN:
                    to_drop.add(i)
            else:
                if d2 < D_MIN:
                    to_drop.add(j)

    # Removing selected ones
    for i in sorted(to_drop, reverse=True):
        del strokes[i]

    return strokes
