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


import sys
import threading
from App import logic
from DataStructures.List import array_list as lt

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


servicefile = 'bus_routes_14000.csv'
stopsfile = 'bus_stops.csv'
initialStation = None

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def print_menu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Cargar información de buses de singapur") # Clase 1: Implementar digraph básico
    print("2- Encontrar las paradas más concurridas") # Casa 1: Implementar digraph completo
    print("3- Encontrar una ruta entre dos paradas (DFS)") # Casa 1: Implementar funcionalidad dfs
    print("4- Encontrar una ruta entre dos paradas (BFS)") # Clase 2: Implementar funcionalidad bfs
    print("5- Encontrar la ruta mínima entre dos paradas") # Casa 2: Implementar dijkstra
    print("6- Mostrar en un mapa la ruta mínima entre dos paradas") # Trabajo Complementario: Mostrar ruta con folium
    print("0- Salir")
    print("*******************************************")


def option_one(cont):
    print("\nCargando información de transporte de singapur ....")
    logic.load_services(cont, servicefile, stopsfile)
    numedges = logic.total_connections(cont)
    numvertex = logic.total_stops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))

def option_two(cont):
    top = logic.get_most_concurrent_stops(cont)
    print('\n------- OPCIÓN 2 --------')
    print('Las paradas más concurridas son: ')
    for i in range(lt.size(top)):
        llave, grado = lt.get_element(top, i)
        print(f"{i + 1}. '{llave}': {grado} conexiones")
        
def print_route(route):
    bus_actual = None
    for i in range(lt.size(route)):
        vertice = lt.get_element(route, i)

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

        if bus != bus_actual:
            if bus_actual is None:
                print(f"\n--- Tomar bus '{bus}' desde '{vertice}' ---")
            else:
                print(f"\n--- Cambiar a bus '{bus}' en la parada '{parada}' ---")
            bus_actual = bus

        print(parada, end=" -> ")
    print()

def option_three(cont):
    stop1 = input("Parada inicial: ")
    stop2 = input("Parada destino: ")
    
    print(f"\n------- OPCIÓN 3 --------")
    print(f"Parada inicial: {stop1}")
    print(f"Parada destino: {stop2}")
    
    route = logic.get_route_between_stops_dfs(cont, stop1, stop2)
    
    if route is None:
        print(f"\nNo existe una ruta entre {stop1} y {stop2}")
    else:
        print_route(route)
    

def option_four(cont):
    stop1 = input("Parada inicial: ")
    stop2 = input("Parada destino: ")
        
    print(f"\n------- OPCIÓN 4 --------")
    print(f"Parada inicial: {stop1}")
    print(f"Parada destino: {stop2}")
        
    route = logic.get_route_between_stops_bfs(cont, stop1, stop2)
        
    if route is None:
        print(f"\nNo existe una ruta entre {stop1} y {stop2}")
    else:
        print_route(route)

def option_five(cont):
    stop1 = input('Parada inicial: ')
    stop2 = input('Parada destino: ')
    
    print(f"\n------- OPCIÓN 5 --------")
    print(f"Parada inicial: {stop1}")
    print(f"Parada destino: {stop2}")
    
    route, distance = logic.get_shortest_route_between_stops(cont, stop1, stop2)
    
    if route is None:
        print(f"\nNo existe una ruta entre {stop1} y {stop2}")
    else:
        print_route(route)
        print(f"\nDistancia total: {distance:.3f} km")

def option_six(cont):
    if cont['paths'] is None:
        print(f"\nPrimero ejecuta la opción 5 para calcular la ruta minima.")
        return
    
    origen = cont['paths']['source']
    destino = input(f"Parada destino (origen {origen}): ")
    
    print(f"----- OPCION 6 ------")
    archivo = logic.show_calculated_shortest_route(cont, destino)
    
    if archivo is None:
        print(f"\nNo existe una ruta entre {origen} y {destino}")
    else:
        print(f"Mapa guardado en {archivo}. Abralo desde su navegador")


"""
Menu principal
"""


def main():
    working = True
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n>')

        if int(inputs[0]) == 1:
            print("\nInicializando....")
            cont = logic.new_analyzer()
            option_one(cont)
        elif int(inputs[0]) == 2:
            option_two(cont)
        elif int(inputs[0]) == 3:
            option_three(cont)
        elif int(inputs[0]) == 4:
            option_four(cont)
        elif int(inputs[0]) == 5:
            option_five(cont)
        elif int(inputs[0]) == 6:
            option_six(cont)
        else:
            working = False
            print("Saliendo...")
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=main)
    thread.start()
