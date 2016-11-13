# -*- coding: utf-8 -*-
import functools
import json
import random
import networkx as nx
try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("Matplotlib required for plot()")
from IPython.display import Image, SVG
from IPython.core.pylabtools import print_figure
from networkx.readwrite import json_graph
from betweenness_centrality_helpers import (
    _single_source_shortest_path_basic, _single_source_dijkstra_path_basic,
    _accumulate_endpoints, _accumulate_basic, _rescale
)
from nxfa2 import forceatlas2_layout


class SonnetException(Exception):
    pass


class Sonnet(object):

    def __init__(self, graph, name=None, max_node_size=6, min_node_size=1,
                 min_com_size=4, rank_by='degree_centrality',
                 color_by='community'):
        self.graph = graph.copy()
        self.name = name
        self.max_node_size = max_node_size
        self.min_node_size = min_node_size
        self.min_com_size = min_com_size
        self.rank_by = rank_by
        self.color_by = color_by

    def d3graph(self, **kwargs):
        return D3Graph(self.graph, **kwargs)

    def matplotgraph(self, **kwargs):
        return MatplotGraph(self.graph, **kwargs)

    def __getitem__(self, node):
        return self.graph.node[node]

    def __len__(self):
        return len(self.nodes())

    def __iter__(self):
        return iter(self.graph.node)

    def is_multigraph(self):
        return self.graph.is_multigraph()

    def nodes(self):
        return self.graph.nodes()

    def sonnet_nodes(self):
        node_list = [node for node in self.sonnet_nodes_iter()]
        return node_list

    def add_attr(self, attr, value):
        for node in self.nodes_iter():
            self[node][attr] = value

    def get_attr(self, attr):
        try:
            attr_dict = {
                node: a for (node, a) in self.attr_iter(attr)
            }
        except KeyError:
            raise SonnetException('Attr does not exist')
        return attr_dict

    def degree(self):
        for node, degree in self.graph.degree_iter():
            self[node]['degree'] = degree

    def degree_centrality(self):
        normal = 1.0 / (len(self) - 1.0)
        for node, degree in self.graph.degree_iter():
            self[node]['degree_centrality'] = degree * normal

    def in_degree_centrality(self):
        if not self.graph.is_directed():
            msg = "in_degree_centrality() not defined for undirected graphs."
            raise nx.NetworkXError(msg)
        normal = 1.0 / (len(self) - 1.0)
        for node, degree in self.graph.in_degree_iter():
            self[node]['in_degree_centrality'] = degree * normal

    def out_degree_centrality(self):
        if not self.graph.is_directed():
            msg = "out_degree_centrality() not defined for undirected graphs."
            raise nx.NetworkXError(msg)
        normal = 1.0 / (len(self) - 1.0)
        for node, degree in self.graph.out_degree_iter():
            self[node]['out_degree_centrality'] = degree * normal

    def closeness_centrality(self, distance=None, normalized=True):
        """
        Adapted from NetworkX closeness centrality measures.
        https://github.com/networkx/networkx/blob/master/
                networkx/algorithms/centrality/closeness.py
        """
        #    Copyright (C) 2004-2013 by
        #    Aric Hagberg <hagberg@lanl.gov>
        #    Dan Schult <dschult@colgate.edu>
        #    Pieter Swart <swart@lanl.gov>
        #    All rights reserved.
        #    BSD license.
        if distance is not None:
            # use Dijkstra's algorithm with specified attribute as edge weight
            path_length = functools.partial(
                nx.single_source_dijkstra_path_length, weight=distance
            )
        else:
            path_length = nx.single_source_shortest_path_length
        nodes = self.nodes()
        for n in nodes:
            sp = path_length(self.graph, n)
            totsp = sum(sp.values())
            if totsp > 0.0 and len(self) > 1:
                self[n]['closeness_centrality'] = (len(sp) - 1.0) / totsp
                # normalize to number of nodes-1 in connected part
                if normalized:
                    s = (len(sp) - 1.0) / (len(self) - 1.0)
                    self[n]['closeness_centrality'] *= s
            else:
                self[n]['closeness_centrality'] = 0.0

    def betweenness_centrality(self, k=None, normalized=True, weight=None,
                               endpoints=False, seed=None):
        """
        Adapted from NetworkX betweenness centrality measures.
        https://github.com/networkx/networkx/blob/master/
                networkx/algorithms/centrality/betweenness.py
        """
        #    Copyright (C) 2004-2011 by
        #    Aric Hagberg <hagberg@lanl.gov>
        #    Dan Schult <dschult@colgate.edu>
        #    Pieter Swart <swart@lanl.gov>
        #    All rights reserved.
        #    BSD license.
        self.add_attr('betweenness_centrality', 0.0)
        if k is None:
            nodes = self.graph
        else:
            random.seed(seed)
            nodes = random.sample(self.nodes(), k)
        for s in nodes:
            # single source shortest paths
            if weight is None:  # use BFS
                S, P, sigma = _single_source_shortest_path_basic(self.graph, s)
            else:  # use Dijkstra's algorithm
                S, P, sigma = _single_source_dijkstra_path_basic(
                    self.graph, s, weight=weight
                )
            # accumulation
            if endpoints:
                _accumulate_endpoints(self, S, P, sigma, s)
            else:
                _accumulate_basic(self, S, P, sigma, s)
        # rescaling
        _rescale(self, len(self), normalized=normalized,
                 directed=self.graph.is_directed(), k=k)

    def eigenvector_centrality(self, max_iter=100, tol=1.0e-6,
                               nstart=None, weight='weight'):
        """
        Adapted from NetworkX eigenvector centrality measures.
        https://github.com/networkx/networkx/blob/
            master/networkx/algorithms/centrality/eigenvector.py
        """
        #    Copyright (C) 2004-2011 by
        #    Aric Hagberg <hagberg@lanl.gov>
        #    Dan Schult <dschult@colgate.edu>
        #    Pieter Swart <swart@lanl.gov>
        #    All rights reserved.
        #    BSD license.
        from math import sqrt
        if self.is_multigraph() is True:
            raise nx.NetworkXException('Eigenvector centrality '
                                       'not defined for multigraphs.')

        if len(self) == 0:
            raise nx.NetworkXException("Empty graph.")

        if nstart is None:
            # choose starting vector with entries of 1/len(G)
            self.add_attr('eigenvector_centrality', 1.0/len(self))
            #x = dict([(n,1.0/len(G)) for n in G])
        else:
            self.add_attr('eigenvector_centrality', nstart)
            #x = nstart
        # normalize starting vector
        sx = 1.0/sum(self.get_eigenvector_centrality().values())
        for k in self.nodes_iter():
            self[k]['eigenvector_centrality'] *= sx
        nnodes = self.graph.number_of_nodes()
        # make up to max_iter iterations
        for i in range(max_iter):
            xlast = self.get_eigenvector_centrality()
            x = dict.fromkeys(xlast, 0)
            # do the multiplication y=Ax
            for n in x:
                for nbr in self.graph[n]:
                    self[n]['eigenvector_centrality'] += \
                        xlast[nbr]*self.graph[n][nbr].get(weight, 1)
            # normalize vector
            try:
                sx = 1.0/sqrt(
                    sum(v**2 for v in
                        self.get_eigenvector_centrality().values())
                )
            # this should never be zero?
            except ZeroDivisionError:
                sx = 1.0
            for n in x:
                self[n]['eigenvector_centrality'] *= sx
            # check convergence
            err = sum([
                abs(self[n]['eigenvector_centrality']-xlast[n]) for n in x
            ])
            if err < nnodes*tol:
                return None

        raise nx.NetworkXError("""eigenvector_centrality():
    power iteration failed to converge in %d iterations."%(i+1))""")

    def rank_nodes(self, rank_by=None, max_node_size=None, min_node_size=1):
        if rank_by is None:
            if self.rank_by:
                rank_by = self.rank_by
            else:
                msg = ('Please set rank_by to determine size distribution')
                raise SonnetException(msg)
        if max_node_size is None:
            if self.max_node_size:
                max_node_size = self.max_node_size
            else:
                raise SonnetException('Please enter max_node_size for nodes')
        if min_node_size is None:
            if self.min_node_size:
                min_node_size = self.min_node_size
            else:
                raise SonnetException('Please enter max_node_size for nodes')
        ranking = '{0}_ranking'.format(rank_by)
        data_dict = self.get_attr(rank_by)
        values = data_dict.values()
        max_value = max(values)
        min_value = min(values)
        value_range = float(max_value - min_value)
        for key, value in data_dict.items():
            value_difference = value - min_value
            if value_difference == 0:
                self[key][ranking] = min_node_size
            else:
                value_fraction = value_difference / value_range
                size_fraction = (max_node_size -
                                 min_node_size) * value_fraction
                self[key][ranking] = size_fraction + min_node_size

    def find_communities(self, min_com_size=4, default_value=''):
        if min_com_size is None:
            min_com_size = self.min_com_size
        try:
            communities = list(
                nx.k_clique_communities(self.graph, min_com_size)
            )
        except nx.NetworkXNotImplemented:
            graph = self.graph.to_undirected()
            communities = list(nx.k_clique_communities(graph, min_com_size))
        if communities:
            for group, community in enumerate(communities):
                group += 1
                for member in community:
                    self[member]['community'] = group
            for node in self.nodes():
                group = self[node].get('community', '')
                if not group:
                    self[node]['community'] = default_value
        else:
            raise SonnetException('No Communities')

    def degree_histogram(self):
        try:
            output = self._degree_histogram()
        except KeyError:
            self.degree()
            output = self._degree_histogram()
        return output

    def _degree_histogram(self):
        node_value = 1.0 / len(self)
        degree_seq = list(self.graph.degree().values())
        max_degree = max(degree_seq) + 1
        freq = max_degree * [0]
        for degree in degree_seq:
            freq[degree] += node_value
        xvals = []
        yvals = []
        for n, val in enumerate(freq):
            if freq[n] > 0:
                xvals.append(n)
                yvals.append(val)
        return xvals, yvals

    def get_degree(self):
        try:
            degree_dict = self._get_degree()
        except KeyError:
            self.degree()
            degree_dict = self._get_degree()
        return degree_dict

    def _get_degree(self):
        degree_dict = {
            node: d for (node, d) in self.degree_iter()
        }
        return degree_dict

    def get_degree_centrality(self):
        try:
            degree_cent_dict = self._get_degree_centrality()
        except KeyError:
            self.degree_centrality()
            degree_cent_dict = self._get_degree_centrality()
        return degree_cent_dict

    def _get_degree_centrality(self):
        degree_cent_dict = {
            node: dc for (node, dc) in self.degree_centrality_iter()
        }
        return degree_cent_dict

    def get_in_degree_centrality(self):
        try:
            in_degree_cent_dict = self._get_in_degree_centrality()
        except KeyError:
            self.in_degree_centrality()
            in_degree_cent_dict = {
                node: idc for (node, idc) in self.in_degree_centrality_iter()
            }
        return in_degree_cent_dict

    def _get_in_degree_centrality(self):
        in_degree_cent_dict = {
            node: idc for (node, idc) in self.in_degree_centrality_iter()
        }
        return in_degree_cent_dict

    def get_out_degree_centrality(self):
        try:
            out_degree_cent_dict = self._get_out_degree_centrality()
        except KeyError:
            self.out_degree_centrality()
            out_degree_cent_dict = self._get_out_degree_centrality()
        return out_degree_cent_dict

    def _get_out_degree_centrality(self):
        out_degree_cent_dict = {
            node: odc for (node, odc) in self.out_degree_centrality_iter()
        }
        return out_degree_cent_dict

    def get_closeness_centrality(self):
        try:
            closeness_cent_dict = self._get_closeness_centrality()
        except KeyError:
            self.closeness_centrality()
            closeness_cent_dict = self._get_closeness_centrality()
        return closeness_cent_dict

    def _get_closeness_centrality(self):
        closeness_cent_dict = {
            node: cdc for (node, cdc) in self.closeness_centrality_iter()
        }
        return closeness_cent_dict

    def get_betweenness_centrality(self):
        try:
            betweenness_cent_dict = self._get_betweenness_centrality()
        except KeyError:
            self.betweenness_centrality()
            betweenness_cent_dict = self._get_betweenness_centrality()
        return betweenness_cent_dict

    def _get_betweenness_centrality(self):
        betweenness_cent_dict = {
            node: bc for (node, bc) in self.betweenness_centrality_iter()
        }
        return betweenness_cent_dict

    def get_eigenvector_centrality(self):
        try:
            eigenvector_cent_dict = self._get_eigenvector_centrality()
        except KeyError:
            self.eigenvector_centrality()
            eigenvector_cent_dict = self._get_eigenvector_centrality()
        return eigenvector_cent_dict

    def _get_eigenvector_centrality(self):
        eigenvector_cent_dict = {
            node: ec for (node, ec) in self.eigenvector_centrality_iter()
        }
        return eigenvector_cent_dict

    def get_ranking(self, measure, max_node_size=None, min_node_size=None):
        if max_node_size is None:
            max_node_size = self.max_node_size
        if min_node_size is None:
            min_node_size = self.min_node_size
        try:
            ranking_dict = self._get_ranking(measure)
        except KeyError:
            self.rank_nodes(
                rank_by=measure,
                max_node_size=max_node_size,
                min_node_size=min_node_size
            )
            ranking_dict = self._get_ranking(measure)
        return ranking_dict

    def _get_ranking(self, measure):
        rank_string = '{0}_ranking'.format(measure)
        ranking_dict = {
            node: rank for (node, rank) in self.ranking_iter(rank_string)
        }
        return ranking_dict

    def get_communities(self, min_com_size=None, default_value=''):
        if min_com_size is None:
            min_com_size = self.min_com_size
        try:
            communities = self._get_communities()
        except KeyError:
            self.find_communities(
                min_com_size=min_com_size,
                default_value=default_value
            )
            communities = self._get_communities()
        return communities

    def _get_communities(self):
        community_dict = {
            node: c for (node, c) in self.community_iter()
        }
        return community_dict

    def get_communitiy_dict(self, min_com_size=4):
        try:
            communities = self._get_communities_dict()
        except KeyError:
            self.find_communities(min_com_size=min_com_size)
            communities = self._get_communities_dict()
        return communities

    def _get_communities_dict(self):
        communities = {}
        for node, community in self.community_iter():
            if community not in communities:
                communities[community] = [node]
            else:
                communities[community].append(node)
        return communities

    def nodes_iter(self):
        return iter(self.graph.node)

    def sonnet_nodes_iter(self):
        for node in self.nodes_iter():
            sonnet_node = {'id': node}
            sonnet_node.update(self[node])
            yield(sonnet_node)

    def attr_iter(self, attr):
        for node in self.nodes_iter():
            yield(node, self[node][attr])

    def degree_iter(self):
        for node in self.nodes_iter():
            yield(node, self[node]['degree'])

    def degree_centrality_iter(self):
        for node in self.nodes_iter():
            yield(node, self[node]['degree_centrality'])

    def in_degree_centrality_iter(self):
        if not self.graph.is_directed():
            msg = "in_degree_centrality() not defined for undirected graphs."
            raise nx.NetworkXError(msg)
        for node in self.nodes_iter():
            yield(node, self[node]['in_degree_centrality'])

    def out_degree_centrality_iter(self):
        if not self.graph.is_directed():
            msg = "out_degree_centrality() not defined for undirected graphs."
            raise nx.NetworkXError(msg)
        for node in self.nodes_iter():
            yield(node, self[node]['out_degree_centrality'])

    def closeness_centrality_iter(self):
        for node in self.nodes_iter():
            yield(node, self[node]['closeness_centrality'])

    def betweenness_centrality_iter(self):
        for node in self.nodes_iter():
            yield(node, self[node]['betweenness_centrality'])

    def eigenvector_centrality_iter(self):
        for node in self.nodes_iter():
            yield(node, self[node]['eigenvector_centrality'])

    def ranking_iter(self, measure):
        for node in self.nodes_iter():
            yield(node, self[node][measure])

    def community_iter(self):
        for node in self.nodes_iter():
            yield(node, self[node]['community'])

    def jsonify(self):
        graph_data = json_graph.node_link_data(self.graph)
        graph_data['name'] = self.name
        output = json.dumps(graph_data)
        return output


class D3Graph(Sonnet):

    def __init__(self, graph, min_node_size=1, max_node_size=6,
                 min_com_size=4, rank_by='degree_centrality',
                 color_by='community', height=800, width=1280, gravity=0.06,
                 charge=-150, link_distance=40):
        super(D3Graph, self).__init__(
            graph,
            name=None,
            min_node_size=min_node_size,
            max_node_size=max_node_size,
            min_com_size=min_com_size,
            rank_by=rank_by,
            color_by=color_by
        )
        self.height = height
        self.width = width
        self.gravity = gravity
        self.charge = charge
        self.link_distance = link_distance

    def jsonify(self):
        graph_data = json_graph.node_link_data(self.graph)
        graph_data['name'] = self.name
        graph_data['height'] = self.height
        graph_data['width'] = self.width
        graph_data['color_by'] = self.color_by
        graph_data['gravity'] = self.gravity
        graph_data['charge'] = self.charge
        graph_data['link_distance'] = self.link_distance
        self.graph = json.dumps(graph_data)
        return self.graph


class MatplotGraph(Sonnet):

    def __init__(self, graph, name=None, max_node_size=500,
                 min_node_size=100, rank_by='degree_centrality',
                 color_by='community', min_com_size=4, notebook=False):
        super(MatplotGraph, self).__init__(
            graph,
            name=name,
            max_node_size=max_node_size,
            min_node_size=min_node_size,
            rank_by=rank_by,
            color_by=color_by,
            min_com_size=min_com_size
        )
        self.notebook = notebook

    def plot_degree_histogram(self, notebook=False, format='svg',
                              title='Degree Distribution', savefig=None,
                              xlabel='Degree', ylabel='P(k)', xscale='linear',
                              low_xlim=None, up_xlim=None, low_ylim=None,
                              up_ylim=None, yscale='linear', grid=True,
                              grid_linestyle='-', grid_color='0.75',
                              title_fontsize=18, label_fontsize=16,
                              legend=False, size=80, color='b', label=None):
        if notebook is None:
            notebook = self.notebook
        xvals, yvals = self.degree_histogram()
        fig, ax = plt.subplots()
        ax.set_title(title, fontsize=title_fontsize)
        ax.set_xlabel(xlabel, fontsize=label_fontsize)
        ax.set_ylabel(ylabel, fontsize=label_fontsize)
        ax.set_xscale(xscale)
        ax.set_yscale(yscale)
        if low_xlim and up_xlim:
            ax.set_xlim(low_xlim, up_xlim)
        if low_ylim and up_ylim:
            ax.set_ylim(low_ylim, up_xlim)
        if grid:
            ax.grid(True, linestyle=grid_linestyle, color=grid_color)
        ax.scatter(xvals, yvals, label=label, s=size, color=color)
        if legend:
            ax.legend()
        if savefig:
            plt.savefig(savefig)
        if notebook:
            data = print_figure(fig, format)
            plt.close
            if format == 'svg':
                return SVG(data)
            else:
                return Image(data, embed=True)
        return plt.show()

    def plot(self, notebook=None, format='svg', title=None, savefig=None,
             title_fontsize=14, layout='spring', max_node_size=None,
             min_node_size=None, rank_by=None, min_com_size=None,
             color_by=None, with_labels=True, save_as=None, nodelist=None,
             node_shape='o', alpha=1.0, cmap='RdYlBu', node_color=None,
             vmin=None, vmax=None, norm=None, ax=None, linewidths=None,
             fontsize=12, fontweight='normal', **kwargs):
        if notebook is None:
            notebook = self.notebook
        if ax is None:
            fig, ax = plt.subplots()
        if max_node_size is None:
            max_node_size = self.max_node_size
        if min_node_size is None:
            min_node_size = self.min_node_size
        if rank_by is None:
            rank_by = self.rank_by
        if min_com_size is None:
            min_com_size = self.min_com_size
        if color_by is None:
            color_by = self.color_by
        if layout == 'force':
            pos = forceatlas2_layout(self.graph)
        elif layout == 'circular':
            pos = nx.drawing.circular_layout(self.graph)
        elif layout == 'random':
            pos = nx.drawing.random_layout(self.graph)
        elif layout == 'shell':
            pos = nx.drawing.shell_layout(self.graph)
        elif layout == 'spectral':
            pos = nx.drawing.spectral_layout(self.graph)
        else:
            pos = nx.drawing.spring_layout(self.graph)
        if rank_by is None:
            rank_by = self.rank_by
        if min_com_size is None:
            min_com_size = self.min_com_size
        if color_by is None:
            color_by = self.color_by
        if title is None:
            title = '{0}/{1}'.format(rank_by, color_by)
        ax.set_title(title, fontsize=title_fontsize)
        node_collection = self.draw_nodes(
            pos,
            max_node_size=max_node_size,
            min_node_size=min_node_size,
            rank_by=rank_by,
            min_com_size=min_com_size,
            color_by=color_by,
            nodelist=nodelist,
            node_shape=node_shape,
            alpha=alpha,
            cmap=cmap,
            node_color=node_color,
            vmin=vmin,
            vmax=vmax,
            ax=ax,
            linewidths=linewidths
        )
        edge_collection = nx.draw_networkx_edges(self.graph, pos, **kwargs)
        if with_labels:
                nx.draw_networkx_labels(
                    self.graph,
                    pos,
                    fontsize=fontsize,
                    fontweight=fontweight
                )
        plt.colorbar(node_collection)
        if savefig:
            plt.savefig(savefig)
        if notebook:
            data = print_figure(fig, format)
            plt.close(fig)
            if format == 'svg':
                return SVG(data)
            else:
                return Image(data, embed=True)
        else:
            return plt.show()

    def draw_nodes(self, pos, max_node_size=None, min_node_size=None,
                   rank_by=None, min_com_size=None, color_by=None,
                   nodelist=None, node_shape=None, alpha=None, cmap=None,
                   node_color=None, vmin=None, vmax=None, norm=True, ax=None,
                   linewidths=None, label=None):
        if nodelist is None:
            nodelist = self.nodes()
        if not nodelist or len(nodelist) == 0:  # empty nodelist, no drawing
            return None
        try:
            xy = np.asarray([pos[v] for v in nodelist])
        except KeyError as e:
            raise nx.NetworkXError('Node %s has no position.' % e)
        except ValueError:
            raise nx.NetworkXError('Bad value in node positions.')
        if cmap:
            cmap = plt.cm.get_cmap(cmap)
        if rank_by:
            node_size = self.get_ranking(
                measure=rank_by,
                max_node_size=max_node_size,
                min_node_size=min_node_size,
            ).values()
        else:
            node_size = max_node_size
        if color_by:
            if color_by == 'community':
                try:
                    node_color = self.get_communities(
                        min_com_size=min_com_size,
                        default_value=0
                    ).values()
                except SonnetException:
                    raise SonnetException(
                        'No communities, color_by other attribute'
                    )
            else:
                node_color = self.get_attr(color_by).values()
        else:
            node_color = node_color
        if norm:
            norm = plt.matplotlib.colors.Normalize()
        node_collection = ax.scatter(xy[:, 0], xy[:, 1],
                                     s=node_size,
                                     c=node_color,
                                     marker=node_shape,
                                     cmap=cmap,
                                     norm=norm,
                                     vmin=None,
                                     vmax=None,
                                     alpha=alpha,
                                     linewidths=linewidths,
                                     label=label)

        node_collection.set_zorder(2)
        return node_collection
