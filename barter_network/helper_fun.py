"""Helper functions to be used in views.py/routes file"""

import networkx as nx
import matplotlib
matplotlib.use('Agg')

# for basic network visualizing
import matplotlib.pyplot as plt
# createdb -E UTF8 -T template0 --locale=en_US.utf8 barternet

# specifying system path for module import
import sys
sys.path.append('..')


def add_node(Z, u_id, name):
    """Adding nodes to a graph object in networkx"""

    Z.add_node(u_id,{'name':name})



def add_edges(skill_to, skill_from):
    """Adding edges to a graph object in networkx"""

    for x, name_s in skill_from:
        Z.add_edges_from([(x.user_id, y.user_id, {'name': name_s})for y in skill_to if x.skill_id == y.skill_id])
