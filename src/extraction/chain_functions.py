def use_strong_connections(connections):
    """Transform the set of basic (strong) connections into a set of chains

    :param list connections: List of connections (basic ones only)
    """

    chains = []

    for i, j in connections:

        # Find strokes containing discs from the analyzed connection
        si = None
        sj = None
        for chain in chains:
            if (chain[0] == i) or (chain[-1] == i):
                si = chain
            if (chain[0] == j) or (chain[-1] == j):
                sj = chain

        if (si is None) and (sj is None):
            # Create a new stroke
            chains.append([i, j])

        elif (si is None) and (not (sj is None)):
            # Append disc i to the beginning or the end of stroke sj
            if sj[0] == j:
                sj.insert(0, i)
            else:
                sj.append(i)

        elif (not (si is None)) and (sj is None):
            # Append disc j to the beginning or the end of stroke si
            if si[0] == i:
                si.insert(0, j)
            else:
                si.append(j)

        elif si == sj:
            # This connection would complete the cycle. Drop it
            pass

        else:
            # Merge two strokes

            # Reverse if necessary
            if si[-1] != i:
                si.reverse()
            if sj[0] != j:
                sj.reverse()

            # Append sj to si
            si.extend(sj)

            # Remove sj from the list
            chains.remove(sj)

    return chains


def use_alternative_connections(chains, connections):
    """Modify the set of chains using alternative connections

    :param list chains: List of connections (basic ones only)
        (warning: this list might be modified within the function)
    :param list connections: List of alternative connections
    """
    for i, j, k in connections:
        # i - end of the stroke joined by an alternative connection
        # j - point inside the 2nd stroke
        # k - the next point within the 2nd stroke
        # after the merge, the new stoke should contain fragment i-j-k

        # Find strokes containing discs from the analyzed connection
        si = None
        sj = None
        for chain in chains:
            if (chain[0] == i) or (chain[-1] == i):
                si = chain
            if (j in chain) and (k in chain):
                sj = chain

        # Double-check if both stokes exist
        if (si is None) or (sj is None):
            continue

        # Check if this connection would not complete the cycle
        if si == sj:
            continue

        # Reverse si if necessary
        if si[-1] != i:
            si.reverse()

        # Append fragment of sj into si
        j_position = sj.index(j)
        k_position = sj.index(k)
        if abs(j_position - k_position) > 1:
            # The connection (j, k) has been already removed, because it would complete the cycle
            fragment = sj
            # TODO: An edge case; it might be good to rethink if it is better to append to j or k
            if k_position > 0:
                fragment.reverse()
        elif k_position > j_position:
            fragment = sj[j_position:]
        else:
            fragment = sj[:(j_position + 1)]
            fragment.reverse()

        si.extend(fragment)

    return chains


def create_chains(strong_connections, alternative_connections):
    """Transform the set of connections into a set of chains

    :param list strong_connections: List of basic (strong) connections
    :param list alternative_connections: List of alternative connections

    """

    # Create a set of chains
    tmp1 = use_strong_connections(strong_connections)
    tmp2 = use_alternative_connections(tmp1, alternative_connections)

    # Remove too short chains (with less than 3 points)
    chains = [ch for ch in tmp2 if len(ch) > 2]
    return chains


def centres_from_chain(discs, chain):
    """Transform the chain from the list of indices to the list of 2D points

    :param list discs: List of discs in such order that the index stored in a chain means
        the position of the disc within this list
    :param list chain: chain as the list of indices (created, for example, with
        :meth:`create_chains`)
    """

    return [discs[index].centre for index in chain]
