import networkx as nx
from barter_network.network import Z

from collections import defaultdict
from networkx.utils import *
from networkx.algorithms.traversal.edgedfs import helper_funcs, edge_dfs
from networkx.algorithms.cycles import *

def our_find_cycle(G, source=None, orientation='original'):
    """
    Returns the edges of a cycle found via a directed, depth-first traversal.

    Parameters
    ----------
    G : graph
        A directed/undirected graph/multigraph.

    source : node, list of nodes
        The node from which the traversal begins. If ``None``, then a source
        is chosen arbitrarily and repeatedly until all edges from each node in
        the graph are searched.

    orientation : 'original' | 'reverse' | 'ignore'
        For directed graphs and directed multigraphs, edge traversals need not
        respect the original orientation of the edges. When set to 'reverse',
        then every edge will be traversed in the reverse direction. When set to
        'ignore', then each directed edge is treated as a single undirected
        edge that can be traversed in either direction. For undirected graphs
        and undirected multigraphs, this parameter is meaningless and is not
        consulted by the algorithm.

    Returns
    -------
    edges : directed edges
        A list of directed edges indicating the path taken for the loop. If
        no cycle is found, then ``edges`` will be an empty list. For graphs, an
        edge is of the form (u, v) where ``u`` and ``v`` are the tail and head
        of the edge as determined by the traversal. For multigraphs, an edge is
        of the form (u, v, key), where ``key`` is the key of the edge. When the
        graph is directed, then ``u`` and ``v`` are always in the order of the
        actual directed edge. If orientation is 'ignore', then an edge takes
        the form (u, v, key, direction) where direction indicates if the edge
        was followed in the forward (tail to head) or reverse (head to tail)
        direction. When the direction is forward, the value of ``direction``
        is 'forward'. When the direction is reverse, the value of ``direction``
        is 'reverse'.

    Examples
    --------
    In this example, we construct a DAG and find, in the first call, that there
    are no directed cycles, and so an exception is raised. In the second call,
    we ignore edge orientations and find that there is an undirected cycle.
    Note that the second call finds a directed cycle while effectively
    traversing an undirected graph, and so, we found an "undirected cycle".
    This means that this DAG structure does not form a directed tree (which
    is also known as a polytree).

    >>> import networkx as nx
    >>> G = nx.DiGraph([(0,1), (0,2), (1,2)])
    >>> try:
    ...    find_cycle(G, orientation='original')
    ... except:
    ...    pass
    ...
    >>> list(find_cycle(G, orientation='ignore'))
    [(0, 1, 'forward'), (1, 2, 'forward'), (0, 2, 'reverse')]

    """
    out_edge, key, tailhead = helper_funcs(G, orientation)

    explored = set()
    cycle = []
    final_node = None
    for start_node in G.nbunch_iter(source):

        if start_node in explored:
            print "\tno loop possible :-("
            # No loop is possible.
            continue

        edges = []
        # All nodes seen in this iteration of edge_dfs
        seen = {start_node}

        # Nodes in active path.
        active_nodes = {start_node}

        previous_node = None
        for edge in edge_dfs(G, start_node, orientation):

            print 
            print "looking at", edge
            print "\tcycle", cycle
            print "\tedges", edges
            print "\texplored", explored
            print "\tfinal_node", final_node
            print "\tseen", seen
            print "\tactive_nodes", active_nodes
            print "\tprevious_node", previous_node

            # Determine if this edge is a continuation of the active path.
            tail, head = tailhead(edge)
            if previous_node is not None and tail != previous_node:
                print "\tpopping an edge"
                # This edge results from backtracking.
                # Pop until we get a node whose head equals the current tail.
                # So for example, we might have:
                #  (0,1), (1,2), (2,3), (1,4)
                # which must become:
                #  (0,1), (1,4)
                while True:
                    try:
                        popped_edge = edges.pop()
                        print "\tpopped", popped_edge, "from edges"
                    except IndexError:
                        print "\tresetting edges"
                        edges = []
                        active_nodes = {tail}
                        break
                    else:
                        popped_head = tailhead(popped_edge)[1]
                        active_nodes.remove(popped_head)
                        print "\tpopped", popped_head, "from active_nodes"

                    if edges:
                        print "\twe got edges"
                        last_head = tailhead(edges[-1])[1]
                        if tail == last_head:
                            print "tail equaled last head"
                            break

            edges.append(edge)

            if head == source:
                # We have a loop!
                print "\tfound a loop"
                cycle.extend(edges)
                final_node = head
                break
            elif head in explored:
                print "\thead in explored. No loop possible."
                # Then we've already explored it. No loop is possible.
                break
            else:
                print "\tadding the head of this edge to possible cycle"
                seen.add(head)
                active_nodes.add(head)
                previous_node = head

        if cycle:
            print "\twe found a cycle!"
            print "edges", edges
            break
        else:
            print "\tno cycle found. Adding to explored."
            explored.update(seen)

    else:
        assert(len(cycle) == 0)
        raise nx.exception.NetworkXNoCycle('No cycle found.')

    # We now have a list of edges which ends on a cycle.
    # So we need to remove from the beginning edges that are not relevant.

    for i, edge in enumerate(cycle):
        tail, head = tailhead(edge)
        if tail == final_node:
            break

    return cycle[i:]

oc = our_find_cycle(Z, source=1)
print "our cycle: ", oc

tc = nx.find_cycle(Z, source=1)
print "their cycle: ", tc