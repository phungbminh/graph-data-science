import os

import networkx as nx
import utils.biokg2df as utl
from ogb.linkproppred import LinkPropPredDataset

def createBioKG():
    rootPwd = os.getcwd() + '/dataset/'
    dataset = LinkPropPredDataset(name="ogbl-biokg", root= rootPwd)
    graph = dataset[0]
    G = utl.bioKGEdgeList(graph)
    return nx.from_pandas_edgelist(G, 'Origin', 'Destination', create_using=nx.DiGraph())