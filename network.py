import networkx as nx
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import matplotlib.pyplot as plt
# createdb -E UTF8 -T template0 --locale=en_US.utf8 barternet



from model import connect_to_db, db, User, Skill, UserSkill
from server import app
connect_to_db(app)


nodes = db.session.query(UserSkill.user_id,User.user_fname).join(User).all() # nodes_edges = db.session.query(UserSkill.user_id,UserSkill.skill_id,UserSkill.skill_direction).all()
skill_to = UserSkill.query.filter(UserSkill.skill_direction =='to').all()
# skill_from = UserSkill.query.filter(UserSkill.skill_direction =='from').all()
skill_from = db.session.query(UserSkill,Skill.skill_name).join(Skill).filter(UserSkill.skill_direction=='from').all()


Z = nx.DiGraph()
Z.clear

# 

def add_nodes(data):
    for a in data:
        Z.add_node(a[0],name=a[1])

    # Z.add_nodes_from(data)
    print Z.nodes(data=True)
    # return Z

add_nodes(nodes)

def add_edges(skill_to, skill_from):
    for x, name_s in skill_from:
        Z.add_edges_from([(x.user_id, y.user_id, {'name': name_s})for y in skill_to if x.skill_id == y.skill_id])
    print Z.edges(data=True)
    # return Z

add_edges(skill_to, skill_from)


def create_graph(graph=Z):
    pos = nx.spring_layout(Z)
    nx.draw(Z, pos, node_color="r",edge_color='blue', #with_labels=True,
        alpha=0.5, node_size=700, width=1, font_size=15, scale=30)
    node_labels = nx.get_node_attributes(Z, 'name')
    nx.draw_networkx_labels(Z, pos, labels=node_labels)
    edge_labels = nx.get_edge_attributes(Z, 'name')
    nx.draw_networkx_edge_labels(Z, pos, labels=edge_labels)
    plt.savefig('graph.png')

create_graph()





# def add_node(nodes_edges):
#     for node,skill,direction in nodes_edges:
#         Z.add_node(node, {direction: skill})
#         print "NODE ADDED", Z.nodes(data=True)
#     return Z.nodes(data=True)

  

# edge_node=add_node(nodes_edges)


# def add_edge(data):
#     for node_r, attributes in Z.nodes(data=True):
#         attr_fro = attributes['from']
#         Z.add_edges_from([(node_r, node) for node, attributes in Z.nodes(data=True)
#                       if attr_fro==attributes['to']])

#     return Z

# add_edge(edge_node)

