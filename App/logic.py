"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

# ___________________________________________________
#  Importaciones
# ___________________________________________________

from DataStructures.List import single_linked_list as lt
from DataStructures.Map import map_linear_probing as m
from DataStructures.Graph import digraph as G
from DataStructures.List import array_list as al
from DataStructures.Graph import dfs
from DataStructures.Stack import stack as st
from DataStructures.Graph import bfs
from DataStructures.Graph import dijkstra as DJK

import csv
import time
import os
import folium

data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'


"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = new_analyzer()
    return analyzer


def new_analyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar la información de las paradas
   connections: Grafo para representar las rutas entre estaciones
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
            'stops': None,
            'connections': None,
            'paths': None
        }

        analyzer['stops'] = m.new_map(
            num_elements=8000, load_factor=0.7, prime=109345121)

        analyzer['connections'] = G.new_graph(order=20000)
        return analyzer
    except Exception as exp:
        return exp

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def load_services(analyzer, servicesfile, stopsfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    stopsfile = data_dir + stopsfile
    stops_input_file = csv.DictReader(open(stopsfile, encoding="utf-8"),
                                      delimiter=",")

    for stop in stops_input_file:
        add_stop(analyzer, stop)

    servicesfile = data_dir + servicesfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    lastservice = None
    for service in input_file:
        if not G.contains_vertex(analyzer['connections'], format_vertex(service)):
            add_stop_vertex(analyzer, format_vertex(service))
        add_route_stop(analyzer, service)

        if lastservice is not None:
            sameservice = lastservice['ServiceNo'] == service['ServiceNo']
            samedirection = lastservice['Direction'] == service['Direction']
            samebusStop = lastservice['BusStopCode'] == service['BusStopCode']
            if sameservice and samedirection and not samebusStop:
                add_stop_connection(analyzer, lastservice, service)

        add_same_stop_connections(analyzer, service)
        lastservice = service

    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def total_stops(analyzer):
    """
    Total de paradas de autobus en el grafo
    """
    return G.order(analyzer['connections'])


def total_connections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return G.size(analyzer['connections'])


# Funciones para la medición de tiempos

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


# Funciones para agregar informacion al grafo

def add_stop_connection(analyzer, lastservice, service):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    try:
        origin = format_vertex(lastservice)
        destination = format_vertex(service)
        clean_service_distance(lastservice, service)
        distance = float(service['Distance']) - float(lastservice['Distance'])
        distance = abs(distance)
        add_connection(analyzer, origin, destination, distance)
        return analyzer
    except Exception as exp:
        return exp


def add_stop(analyzer, stop):
    """
    Adiciona una parada (BusStopCode) en los stops del sistema de transporte
    """
    stop['services'] = lt.new_list()
    m.put(analyzer['stops'], stop['BusStopCode'], stop)
    return analyzer

def add_stop_vertex(analyzer, stopid):
    """
    Adiciona una estación como un vertice del grafo
    """

    G.insert_vertex(analyzer['connections'], stopid, stopid)
    return analyzer


def add_route_stop(analyzer, service):
    """
    Agrega a una estacion, una ruta que es servida en ese paradero
    """
    stop_info = m.get(analyzer['stops'], service['BusStopCode'])
    stop_services = stop_info['services']
    if lt.is_present(stop_services, service['ServiceNo'], lt.default_function) == -1:
        lt.add_last(stop_services, service['ServiceNo'])

    return analyzer


def add_connection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """

    G.add_edge(analyzer['connections'], origin, destination, distance)



def add_same_stop_connections(analyzer, service):
    stop_1 = format_vertex(service)
    stop_buses_lt = m.get(analyzer['stops'], service['BusStopCode'])['services']

    if lt.size(stop_buses_lt) > 1:
        pass

    node = stop_buses_lt['first']
    for _ in range(lt.size(stop_buses_lt)):
        stop_2 = format_vertex({'BusStopCode': service['BusStopCode'], 'ServiceNo': node['info']})
        if stop_1 != stop_2:
            add_connection(analyzer, stop_1, stop_2, 0)
        node = node['next']
    return analyzer


# ___________________________________________________
#  Funciones de resolución de requerimientos
# ___________________________________________________

def get_most_concurrent_stops(analyzer):
    """
    Obtiene las 5 paradas más concurridas
    """    
    grafo = analyzer['connections']
    llaves = G.vertices(grafo)
    
    paradas = al.new_list()
    for i in range(al.size(llaves)):
        llave = al.get_element(llaves, i)
        grado = G.degree(grafo, llave)
        al.add_last(paradas, (llave, grado))
    
    al.merge_sort(paradas, sort_crit_get_most_concurrent_stops)
    
    cantidad = 5
    if al.size(paradas) < cantidad:
        cantidad = al.size(paradas)
    
    top = al.sub_list(paradas, 0, cantidad)
    return top
        
def sort_crit_get_most_concurrent_stops(pareja_1, pareja_2):
    return pareja_1[1] > pareja_2[1]
    

def get_route_between_stops_dfs(analyzer, stop1, stop2):
    """
    Obtener la ruta entre dos parada usando dfs
    """
    graph = analyzer['connections']
    
    if not G.contains_vertex(graph, stop1) or not G.contains_vertex(graph, stop2):
        return None
    
    visited_map = dfs.dfs(graph, stop1)
    
    if not dfs.has_path_to(stop2, visited_map):
        return None
    
    path = dfs.path_to(stop2, visited_map)
    route = al.new_list()
    while not st.is_empty(path):
        al.add_last(route, st.pop(path))
        
    return route

def get_route_between_stops_bfs(analyzer, stop1, stop2):
    """
    Obtener la ruta entre dos parada usando bfs
    """
    graph = analyzer["connections"]

    if not G.contains_vertex(graph, stop1) or not G.contains_vertex(graph, stop2):
        return None

    visited_map = bfs.bfs(graph, stop1)

    if not bfs.has_path_to(stop2, visited_map):
        return None

    path = bfs.path_to(stop2, visited_map)
    route = al.new_list()
    while not st.is_empty(path):
        al.add_last(route, st.pop(path))
    return route

def get_shortest_route_between_stops(analyzer, stop1, stop2):
    """
    Obtener la ruta mínima entre dos paradas
    """
    graph = analyzer['connections']
    
    if not G.contains_vertex(graph, stop1) or not G.contains_vertex(graph, stop2):
        return None, None
    
    analyzer['paths'] = DJK.dijkstra(graph, stop1)
    
    camino = DJK.path_to(stop2, analyzer['paths'])
    
    if camino is None:
        return None, None
    
    ruta = al.new_list()
    while not st.is_empty(camino):
        al.add_last(ruta, st.pop(camino))
    
    distance = DJK.dist_to(stop2, analyzer['paths'])
    return ruta, distance
    

def show_calculated_shortest_route(analyzer, destination_stop):
    
    if analyzer['paths'] is None:
        return None
    
    camino = DJK.path_to(destination_stop, analyzer['paths'])
    if camino is None:
        return None

    mapa = folium.Map(
        location=(1.28143, 103.8499),
        zoom_start=12,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri"
    )
    puntos = []
    bus_actual = None
    
    while not st.is_empty(camino):
        vertice = st.pop(camino)
        
        parada = ""
        bus = ""
        
        paso_guion = False
        
        for letra in vertice:
            if letra == '-' and not paso_guion:
                paso_guion = True
            elif not paso_guion:
                parada = parada + letra
            else:
                bus = bus + letra
        
        info = m.get(analyzer['stops'], parada)
        punto = (float(info['Latitude']), float(info['Longitude']))
        puntos.append(punto)
        
        if bus_actual is None:
            folium.Marker(punto, tooltip=f"Inicio: {vertice}",
                          icon=folium.Icon("Green")).add_to(mapa)
        elif bus != bus_actual:
            folium.Marker(punto, tooltip=f"Cambiar a bus {bus} en {parada}",
                          icon=folium.Icon("blue")).add_to(mapa)
        else:
            folium.CircleMarker(punto, radius=3, tooltip=vertice).add_to(mapa)
        bus_actual = bus
        
    folium.Marker(puntos[-1], tooltip=f"Fin: {destination_stop}",
                  icon=folium.Icon("red")).add_to(mapa)
    folium.PolyLine(puntos).add_to(mapa)

    nombre_archivo = "ruta_minima.html"
    mapa.save(nombre_archivo)
    return nombre_archivo   


# ___________________________________________________
# Funciones Helper
# ___________________________________________________

def clean_service_distance(lastservice, service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['Distance'] == '':
        service['Distance'] = 0
    if lastservice['Distance'] == '':
        lastservice['Distance'] = 0


def format_vertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['BusStopCode'] + '-'
    name = name + service['ServiceNo']
    return name
