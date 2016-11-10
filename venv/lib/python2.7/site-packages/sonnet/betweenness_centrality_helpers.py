import heapq

"""
Adapted from NetworkX
Betweenness centrality measures.
https://github.com/networkx/networkx/blob/master/
            networkx/algorithms/centrality/betweenness.py
"""
#    Copyright (C) 2004-2011 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
__author__ = """Aric Hagberg (hagberg@lanl.gov)"""


def _single_source_shortest_path_basic(G,s):
    S=[]
    P={}
    for v in G:
        P[v]=[]
    sigma=dict.fromkeys(G,0.0)    # sigma[v]=0 for v in G
    D={}
    sigma[s]=1.0
    D[s]=0
    Q=[s]
    while Q:   # use BFS to find shortest paths
        v=Q.pop(0)
        S.append(v)
        Dv=D[v]
        sigmav=sigma[v]
        for w in G[v]:
            if w not in D:
                Q.append(w)
                D[w]=Dv+1
            if D[w]==Dv+1:   # this is a shortest path, count paths
                sigma[w] += sigmav
                P[w].append(v) # predecessors 
    return S,P,sigma


def _single_source_dijkstra_path_basic(G,s,weight='weight'):
    # modified from Eppstein
    S=[]
    P={}
    for v in G:
        P[v]=[]
    sigma=dict.fromkeys(G,0.0)    # sigma[v]=0 for v in G
    D={}
    sigma[s]=1.0
    push=heapq.heappush
    pop=heapq.heappop
    seen = {s:0}
    Q=[]   # use Q as heap with (distance,node id) tuples
    push(Q,(0,s,s))
    while Q:
        (dist,pred,v)=pop(Q)
        if v in D:
            continue # already searched this node.
        sigma[v] += sigma[pred] # count paths
        S.append(v)
        D[v] = dist
        for w,edgedata in G[v].items():
            vw_dist = dist + edgedata.get(weight,1)
            if w not in D and (w not in seen or vw_dist < seen[w]):
                seen[w] = vw_dist
                push(Q,(vw_dist,v,w))
                sigma[w]=0.0
                P[w]=[v]
            elif vw_dist==seen[w]:  # handle equal paths
                sigma[w] += sigma[v]
                P[w].append(v)
    return S,P,sigma

def _accumulate_basic(betweenness,S,P,sigma,s):
    delta=dict.fromkeys(S,0)
    while S:
        w=S.pop()
        coeff=(1.0+delta[w])/sigma[w]
        for v in P[w]:
            delta[v] += sigma[v]*coeff
        if w != s:
            betweenness[w]['betweenness_centrality']+=delta[w]
    return betweenness

def _accumulate_endpoints(betweenness,S,P,sigma,s):
    betweenness[s]['betweenness_centrality'] += len(S)-1
    delta=dict.fromkeys(S,0)
    while S:
        w=S.pop()
        coeff=(1.0+delta[w])/sigma[w]
        for v in P[w]:
            delta[v] += sigma[v]*coeff
        if w != s:
            betweenness[w]['betweenness_centrality'] += delta[w]+1
    return betweenness

def _rescale(betweenness,n,normalized,directed=False,k=None):
    if normalized is True:
        if n <=2:
            scale=None  # no normalization b=0 for all nodes
        else:
            scale=1.0/((n-1)*(n-2))
    else: # rescale by 2 for undirected graphs
        if not directed:
            scale=1.0/2.0
        else:
            scale=None
    if scale is not None:
        if k is not None:
            scale=scale*n/k
        for v in betweenness.graph.nodes():
            betweenness[v]['betweenness_centrality'] *= scale
    return betweenness