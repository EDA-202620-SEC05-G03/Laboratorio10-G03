from DataStructures.Graph import dijsktra_structure as ds
from DataStructures.Graph import digraph as G
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Priority_queue import priority_queue as pq   
from DataStructures.Stack import stack as st

inf = float('inf')
            
def dijkstra(my_graph, source):
    
    estructura = ds.new_dijsktra_structure(source, G.order(my_graph))
    visitados = estructura['visited']
    cola = estructura['pq']
    
    vertices = G.vertices(my_graph)
    for i in range(al.size(vertices)):
        v = al.get_element(vertices, i)
        mp.put(visitados, v, {'marked': False,
                              'edge_from': None,
                              'dist_to': inf})
        
    mp.get(visitados, source)['dist_to'] = 0
    pq.insert(cola, 0, source)
    
    while not pq.is_empty(cola):
        u = pq.remove(cola)
        info_u = mp.get(visitados, u)
        
        if info_u['marked']:
            continue
        info_u['marked'] = True
        
        arcos = G.edges_vertex(my_graph, u)
        for i in range(al.size(arcos)):
            arco = al.get_element(arcos, i)
            v = arco['to']
            peso = arco['weight']
            info_V = mp.get(visitados, v)
            
            nueva_dist = info_u['dist_to'] + peso
            if nueva_dist < info_V['dist_to']:
                info_V['dist_to'] = nueva_dist
                info_V['edge_from'] = u
                pq.insert(cola, nueva_dist, v)
                
    return estructura
        
def dist_to(key_v, aux_structure):
    info = mp.get(aux_structure['visited'], key_v)
    if info is None:
        return inf
    return info['dist_to']

def has_path_to(key_v, aux_structure):
    return dist_to(key_v, aux_structure) != inf

def path_to(key_v, aux_structure):
    if not has_path_to(key_v, aux_structure):
        return None
    camino = st.new_stack()
    actual = key_v
    while actual is not None:
        st.push(camino, actual)
        actual = mp.get(aux_structure['visited'], actual)['edge_from']
    
    return camino
    