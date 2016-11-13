import random
import unittest
from math import trunc
import networkx as nx

from graphs import Sonnet


class SonnetTests(unittest.TestCase):

    def test_nodes(self):
        g = nx.gnp_random_graph(5, 0.1)
        sonnet = Sonnet(g)
        for node in sonnet.sonnet_nodes():
            self.assertTrue(type(node) == dict and 'id' in node)

    def test_add_atrr_and_sonnet_iterator(self):
        g = nx.gnp_random_graph(5, 0.1)
        sonnet = Sonnet(g)
        sonnet.add_attr('group', 1)
        for node in sonnet:
            self.assertTrue(
                'group' in sonnet[node] and sonnet[node]['group'] == 1
            )

    def test_sonnet_node_iter(self):
        g = nx.gnp_random_graph(5, 0.1)
        sonnet = Sonnet(g)
        for node in sonnet.sonnet_nodes_iter():
            self.assertTrue(type(node) == dict and 'id' in node)

    def test_node_rank(self):
        edges = [
            (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
            (1, 10), (1, 11), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8),
            (2, 9), (2, 10), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
            (4, 5), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (6, 7)
        ]
        g = nx.Graph()
        g.add_edges_from(edges)
        deg_seq = nx.degree(g).values()
        sonnet = Sonnet(g, max_node_size=10)
        sonnet.degree_centrality()
        sonnet.rank_nodes(rank_by='degree_centrality')
        rankings = sonnet.get_ranking(measure='degree_centrality').values()
        self.assertEqual(
            [int(deg) for deg in deg_seq],
            [int(rank) for rank in rankings]
        )
        sonnet2 = Sonnet(g, max_node_size=5)
        sonnet2.degree_centrality()
        sonnet2.rank_nodes(
            rank_by='degree_centrality',
            min_node_size=0.5
        )
        rankings2 = sonnet2.get_ranking(measure='degree_centrality').values()
        self.assertEqual(
            [trunc(rank * 10) for rank in rankings2],
            [50, 45, 40, 35, 30, 30, 30, 20, 15, 10, 5])

    def test_deg(self):
        g = nx.gnp_random_graph(20, 0.2)
        sonnet = Sonnet(g)
        nx_deg = nx.degree(g)
        sonnet_deg = sonnet.get_degree()
        self.assertEqual(nx_deg, sonnet_deg)

    def test_deg_centrality(self):
        g = nx.gnp_random_graph(20, 0.2)
        sonnet = Sonnet(g)
        nx_deg_centrality = nx.degree_centrality(g)
        sonnet_deg_centrality = sonnet.get_degree_centrality()
        self.assertEqual(nx_deg_centrality, sonnet_deg_centrality)

    def test_in_deg_centrality(self):
        g = nx.scale_free_graph(10)
        sonnet = Sonnet(g)
        nx_in_deg_centrality = nx.in_degree_centrality(g)
        sonnet_in_deg_centrality = sonnet.get_in_degree_centrality()
        self.assertEqual(nx_in_deg_centrality, sonnet_in_deg_centrality)

    def test_out_deg_centrality(self):
        g = nx.scale_free_graph(10)
        sonnet = Sonnet(g)
        nx_out_deg_centrality = nx.out_degree_centrality(g)
        sonnet_out_deg_centrality = sonnet.get_out_degree_centrality()
        self.assertEqual(nx_out_deg_centrality, sonnet_out_deg_centrality)

    def test_closeness_centrality(self):
        g = nx.gnp_random_graph(20, 0.2)
        sonnet = Sonnet(g)
        nx_close_centrality = nx.closeness_centrality(g)
        sonnet_closeness_centrality = sonnet.get_closeness_centrality()
        self.assertEqual(nx_close_centrality, sonnet_closeness_centrality)

    def test_betweenness_centrality(self):
        g = nx.gnp_random_graph(20, 0.2)
        nx_betwn_centrality = nx.betweenness_centrality(g)
        sonnet = Sonnet(g)
        sonnet_betwn_centrality = sonnet.get_betweenness_centrality()
        self.assertEqual(nx_betwn_centrality, sonnet_betwn_centrality)
        g2 = nx.gnp_random_graph(20, 0.2)
        for x in g2:
            g2.node[x]['weight'] = random.randint(1, 5)
        nx_betwn_centrality2 = nx.betweenness_centrality(g2, weight='weight')
        sonnet2 = Sonnet(g2)
        sonnet2.betweenness_centrality(weight='weight')
        sonnet_betwn_centrality2 = sonnet2.get_betweenness_centrality()
        self.assertEqual(nx_betwn_centrality2, sonnet_betwn_centrality2)
        g3 = nx.gnp_random_graph(20, 0.2)
        nx_betwn_centrality3 = nx.betweenness_centrality(g3, endpoints=True)
        sonnet3 = Sonnet(g3)
        sonnet3.betweenness_centrality(endpoints=True)
        sonnet_betwn_centrality3 = sonnet3.get_betweenness_centrality()
        self.assertEqual(nx_betwn_centrality3, sonnet_betwn_centrality3)

    def test_eigenvector_centrality(self):
        g = nx.gnp_random_graph(20, 0.2)
        try:
            nx_eigen_centrality = [
                trunc(
                    val*100
                ) for val in nx.eigenvector_centrality(g).values()
            ]
            sonnet = Sonnet(g)
            sonnet_eigen_centrality = [
                trunc(
                    val*100
                ) for val in sonnet.get_eigenvector_centrality().values()
            ]
            self.assertEqual(nx_eigen_centrality, sonnet_eigen_centrality)
        except nx.NetworkXError:
            self.assertEqual(1, 1)

    def test_communities(self):
        g = nx.gnp_random_graph(100, 0.1)
        sonnet = Sonnet(g)
        communities = sonnet.get_communities(min_com_size=4)
        self.assertTrue(type(communities) == dict)

    def test_jsonify(self):
        g = nx.gnp_random_graph(100, 0.1)
        sonnet = Sonnet(g)
        sonnet.betweenness_centrality()
        sonnet.rank_nodes(rank_by='betweenness_centrality')
        sonnet.find_communities()
        json_output = sonnet.jsonify()
        self.assertEqual(type(json_output), str)

    def test_degree_histogram(self):
        edges = [(1, 4), (2, 3), (2, 4), (3, 4)]
        g = nx.Graph()
        g.add_edges_from(edges)
        sonnet = Sonnet(g)
        x_vals, y_vals = sonnet.degree_histogram()
        self.assertEqual(x_vals, [1, 2, 3])
        self.assertEqual(y_vals, [0.25, 0.5, 0.25])


if __name__ == '__main__':
    unittest.main()
