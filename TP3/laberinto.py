from mapa import coordenadas_vecinas
from mapa import Mapa
from mapa import Coord
from random import randint
from pilas_colas import Pila

def generar_laberinto(filas, columnas):
    """Generar un laberinto.

    Argumentos:
        filas, columnas (int): Tamaño del mapa

    Devuelve:
        Mapa: un mapa nuevo con celdas bloqueadas formando un laberinto
              aleatorio
    """
    mapa = Mapa(filas, columnas)

    for i in range(0, filas):
    	for j in range(0, columnas):
    		coordenada = Coord(i, j)
    		mapa.bloquear(coordenada)

    mapa.asignar_origen(Coord(1, 1))

    if columnas % 2 != 0 and filas % 2 != 0:
        mapa.asignar_destino(Coord(filas - 2, columnas - 2))
    else:
        if columnas % 2 != 0:
            mapa.asignar_destino(Coord(filas - 1, columnas - 2))
        if filas % 2 != 0:
            mapa.asignar_destino(Coord(filas - 2, columnas - 1))

    coord = mapa.origen()
    camino = Pila()
    camino.apilar(coord)

    visitadas = set()

    while not camino.esta_vacia():

        coord = camino.ver_tope()
        mapa.desbloquear(coord)
        visitadas.add(coord)

        celdas_vecinas = [mapa.trasladar_coord(coord, 2, 0), mapa.trasladar_coord(coord, -2, 0), mapa.trasladar_coord(coord, 0, 2), mapa.trasladar_coord(coord, 0, -2)]
        vecinas = celdas_vecinas[:]
        for vecina in vecinas:
            if vecina == coord:
                celdas_vecinas.remove(vecina)
            elif not mapa.celda_bloqueada(vecina):
                celdas_vecinas.remove(vecina)

        if (len(celdas_vecinas) == 0) or (coord == mapa.destino()):
            camino.desapilar()
            continue

        vecina_aleatoria = randint(0, len(celdas_vecinas) - 1)

        coord_vecina = celdas_vecinas[vecina_aleatoria]

        if coord_vecina in visitadas:
            continue

        desbloquear_celda_medio(mapa, coord, coord_vecina)
        camino.apilar(coord_vecina)
        

    return mapa


def desbloquear_celda_medio(mapa, coord1, coord2):
    '''Recibe por parámetro un mapa y dos coordenadas impares. Desbloquea del mapa la celda que se encuentra en el medio de ellas dos.'''
    if coord1.fila == coord2.fila:
        if coord2.columna > coord1.columna:
            coord = Coord(coord1.fila, coord2.columna - 1)
        else:
            coord = Coord(coord1.fila, coord2.columna + 1)

    if coord1.columna == coord2.columna:
        if coord2.fila > coord1.fila:
            coord = Coord(coord2.fila - 1, coord1.columna)
        else:
            coord = Coord(coord2.fila + 1, coord1.columna)

    mapa.desbloquear(coord)
        
