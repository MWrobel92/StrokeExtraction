from ..src.extraction.stroke_functions import recursive_stroke_analyze, chains_to_strokes
from ..src.extraction.stroke import Stroke
from ..src.extraction.chain_functions import centres_from_chain
from .test_connection_functions import create_discs_set


def test_recursive_stroke_analyze():
    discs = create_discs_set()
    stroke = Stroke(centres_from_chain(discs, [0, 1, 2, 3, 4]))
    strokes = recursive_stroke_analyze(stroke)
    assert len(strokes) == 1
    assert strokes[0].is_good()


def test_chains_to_strokes():
    discs = create_discs_set()
    chains = [[2, 1, 0], [0, 1, 2, 3, 4], [2, 1, 3, 4]]
    strokes = chains_to_strokes(discs, chains)
    assert len(strokes) == 2
    assert strokes[0].is_good()
    assert strokes[1].is_good()
