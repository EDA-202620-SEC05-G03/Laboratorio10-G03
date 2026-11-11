from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import vertex as V

def new_graph(order):
    grafo = {'vertices': mp.new_map(order, 0.5),
             'num_edges':0}
    return grafo

def insert_vertex(my_graph, key_u, info_u):
    vertice = V.new_vertex(key_u, info_u)
    mp.put(my_graph['vertices'], key_u, vertice)
    return my_graph

def contains_vertex(my_graph, key_u):
    return mp.contains(my_graph['vertices'], key_u)

def order(my_graph):
    return mp.size(my_graph['vertices'])

def size(my_graph):
    return my_graph['num_edges']

def add_edge(my_graph, key_u, key_v, weight=1.0):
    vertice_u = mp.get(my_graph['vertices'], key_u)
    if vertice_u is None:
        raise Exception("El vertice u no existe")

    if not mp.contains(my_graph['vertices'], key_v):
        raise Exception("El vertice v no existe")

    arco_existente = V.get_edge(vertice_u, key_v)
    V.add_adjacent(vertice_u, key_v, weight)

    if arco_existente is None:
        my_graph['num_edges'] += 1

    return my_graph
    
    


