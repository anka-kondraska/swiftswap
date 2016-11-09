import networkx as nx
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
# createdb -E UTF8 -T template0 --locale=en_US.utf8 barternet



from model import db, User, Skill, UserSkill

Z = nx.DiGraph()
Z.clear



def add_node(u_id, name):
    Z.add_node(u_id,{'name':name})



def add_edges(skill_to, skill_from):
    for x, name_s in skill_from:
        Z.add_edges_from([(x.user_id, y.user_id, {'name': name_s})for y in skill_to if x.skill_id == y.skill_id])
    # print Z.edges(data=True)
    # return Z

# add_edges(skill_to, skill_from)