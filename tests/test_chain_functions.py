import numpy as np
from ..src.extraction.chain_functions import use_strong_connections, use_alternative_connections, \
    create_chains, centres_from_chain
from .test_connection_functions import create_discs_set


def create_connections_set():
    return [(2, 3), (1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (9, 8), (11, 12)]


def test_use_strong_connections():
    connections = create_connections_set()
    chains = use_strong_connections(connections)
    assert len(chains) == 4


def test_use_alternative_connections():
    connections = create_connections_set()
    chains = use_strong_connections(connections)
    alternatives = [(5, 2, 1), (6, 9, 8)]
    with_alt = use_alternative_connections(chains, alternatives)
    assert len(with_alt) == 4
    assert ([1, 2, 5, 6, 9, 8, 7] in with_alt) or ([7, 8, 9, 6, 5, 2, 1] in with_alt)


def test_create_connections():
    connections = create_connections_set()
    alternatives = [(5, 2, 1), (6, 9, 8)]
    chains = create_chains(connections, alternatives)
    assert len(chains) == 3


def test_centres_from_chain():
    discs = create_discs_set()
    centres = centres_from_chain(discs, [0, 1, 2])
    assert len(centres) == 3
    assert all(centres[0] == np.array([2, 3]))


def test_alternative_and_cycle():
    chains = [[0, 1, 2, 3], [4, 5, 6]]
    alternatives = [(4, 0, 3)]
    with_alt = use_alternative_connections(chains, alternatives)
    assert with_alt[1] == [6, 5, 4, 3, 2, 1, 0]
