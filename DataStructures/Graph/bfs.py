from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al
from DataStructures.Stack import stack as st
from DataStructures.Graph import digraph as G
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Queue import queue as q

def bfs(my_graph, source):
    visited_map = mp.new_map(G.order(my_graph), 0.5)
    mp.put(visited_map, source, {'edge_from': None, 'dist_to': 0})
    bfs_vertex(my_graph, source, visited_map)
    return visited_map
    
def bfs_vertex(my_graph, source, visited_map):
    cola = q.new_queue()
    q.enqueue(cola, source)
    
    while not q.is_empty(cola):
        vertex = q.dequeue(cola)
        dist_vertex = mp.get(visited_map, vertex)['dist_to']

        adjacents = G.adjacents(my_graph, vertex)
        for i in range(al.size(adjacents)):
            w = al.get_element(adjacents, i)
            if not mp.contains(visited_map, w):
                mp.put(visited_map, w, {'edge_from': vertex,
                                        'dist_to': dist_vertex + 1})
                q.enqueue(cola, w)

    return visited_map


def has_path_to(key_v, visited_map):
    return mp.contains(visited_map, key_v)


def path_to(key_v, visited_map):
    if not has_path_to(key_v, visited_map):
        return None
    camino = st.new_stack()
    actual = key_v
    while actual is not None:
        st.push(camino, actual)
        actual = mp.get(visited_map, actual)['edge_from']
    return camino
                