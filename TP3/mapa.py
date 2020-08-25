class Coord:
    """
    Representa las coordenadas de una celda en una grilla 2D, representada
    como filas y columnas. Las coordendas ``fila = 0, columna = 0`` corresponden
    a la celda de arriba a la izquierda.

    Las instancias de Coord son inmutables.
    """

    def __init__(self, fila=0, columna=0):
        """Constructor.

        Argumentos:
            fila, columna (int): Coordenadas de la celda
        """
        self.fila, self.columna = (fila, columna)

    def trasladar(self, df, dc):
        """Trasladar una celda.

        Devuelve una nueva instancia de Coord, correspondiente a las coordenadas
        de la celda que se encuentra ``df`` filas y ``dc`` columnas de distancia.

        Argumentos:
            df (int): Cantidad de filas a trasladar
            dc (int): Cantidad de columnas a trasladar

        Devuelve:
            Coord: Las coordenadas de la celda trasladada
        """
        return Coord(self.fila + df, self.columna + dc)

    def distancia(self, otra):
        """Distancia entre dos celdas.

        Argumentos:
            otra (Coord)

        Devuelve:
            int|float: La distancia entre las dos celdas (no negativo)
        """
        diferencia_filas = otra.fila - self.fila
        diferencia_columnas = otra.columna - self.columna

        distancia = (diferencia_filas**2 + diferencia_columnas**2) ** 1/2

        if distancia < 0:
            distancia = distancia * (-1)

        return distancia


    def __eq__(self, otra):
        """Determina si dos coordenadas son iguales"""

        return self.fila == otra.fila and self.columna == otra.columna

    def __iter__(self):
        """Iterar las componentes de la coordenada.

        Devuelve un iterador de forma tal que:
        >>> coord = Coord(3, 5)
        >>> f, c = coord
        >>> assert f == 3
        >>> assert c == 5
        """
        lista_coord = [self.fila, self.columna]
        return iter(lista_coord)

    def __hash__(self):
        """Código "hash" de la instancia inmutable."""
        # Este método es llamado por la función de Python hash(objeto), y debe devolver
        # un número entero.
        # Más información (y un ejemplo de cómo implementar la funcion) en:
        # https://docs.python.org/3/reference/datamodel.html#object.__hash__
        return hash((self.fila, self.columna))

    def __repr__(self):
        """Representación de la coordenada como cadena de texto"""
        return f"({self.fila}, {self.columna})"

class Mapa:
    """
    Representa el mapa de un laberinto en una grilla 2D con:

    * un tamaño determinado (filas y columnas)
    * una celda origen
    * una celda destino
    * 0 o más celdas "bloqueadas", que representan las paredes del laberinto

    Las instancias de Mapa son mutables.
    """
    def __init__(self, filas, columnas):
        """Constructor.

        El mapa creado tiene todas las celdas desbloqueadas, el origen en la celda
        de arriba a la izquierda y el destino en el extremo opuesto.

        Argumentos:
            filas, columnas (int): Tamaño del mapa
        """

        self.filas = filas
        self.columnas = columnas
        self.celda_origen = Coord(0, 0)
        self.celda_destino = Coord(filas - 1, columnas - 1)
        self.bloqueadas = set()

    def dimension(self):
        """Dimensiones del mapa (filas y columnas).

        Devuelve:
            (int, int): Cantidad de filas y columnas
        """
        return self.filas, self.columnas

    def origen(self):
        """Celda origen.

        Devuelve:
            Coord: Las coordenadas de la celda origen
        """
        return self.celda_origen

    def destino(self):
        """Celda destino.

        Devuelve:
            Coord: Las coordenadas de la celda destino
            """
        return self.celda_destino        

    def asignar_origen(self, coord):
        """Asignar la celda origen.

        Argumentos:
            coord (Coord): Coordenadas de la celda origen
        """
        self.celda_origen = coord

    def asignar_destino(self, coord):
        """Asignar la celda destino.

        Argumentos:
            coord (Coord): Coordenadas de la celda destino
        """
        self.celda_destino = coord

    def celda_bloqueada(self, coord):
        """¿La celda está bloqueada?

        Argumentos:
            coord (Coord): Coordenadas de la celda

        Devuelve:
            bool: True si la celda está bloqueada
        """
        return coord in self.bloqueadas

    def bloquear(self, coord):
        """Bloquear una celda.

        Si la celda estaba previamente bloqueada, no hace nada.

        Argumentos:
            coord (Coord): Coordenadas de la celda a bloquear
        """
        if self.celda_bloqueada(coord):
            return

        self.bloqueadas.add(coord)

    def desbloquear(self, coord):
        """Desbloquear una celda.

        Si la celda estaba previamente desbloqueada, no hace nada.

        Argumentos:
            coord (Coord): Coordenadas de la celda a desbloquear
        """
        if not self.celda_bloqueada(coord):
            return

        self.bloqueadas.remove(coord)

    def alternar_bloque(self, coord):
        """Alternar entre celda bloqueada y desbloqueada.

        Si la celda estaba previamente desbloqueada, la bloquea, y viceversa.

        Argumentos:
            coord (Coord): Coordenadas de la celda a alternar
        """
        if coord in self.bloqueadas:
            self.desbloquear(coord)
            return
        self.bloquear(coord)

    def es_coord_valida(self, coord):
        """¿Las coordenadas están dentro del mapa?

        Argumentos:
            coord (Coord): Coordenadas de una celda

        Devuelve:
            bool: True si las coordenadas corresponden a una celda dentro del mapa
        """
        return (coord.fila < self.filas and coord.fila >= 0) and (coord.columna < self.columnas and coord.columna >= 0)

    def trasladar_coord(self, coord, df, dc):
        """Trasladar una coordenada, si es posible.

        Argumentos:
            coord: La coordenada de una celda en el mapa
            df, dc: La traslación a realizar

        Devuelve:
            Coord: La coordenada trasladada si queda dentro del mapa. En caso
                   contrario, devuelve la coordenada recibida.
        """
        coord_transladada = coord.trasladar(df, dc)

        if self.es_coord_valida(coord_transladada):
            return coord_transladada
        return coord
        
    def __iter__(self):
        """Iterar por las coordenadas de todas las celdas del mapa.

        Se debe garantizar que la iteración cubre todas las celdas del mapa, en
        cualquier orden.

        Ejemplo:
            >>> mapa = Mapa(10, 10)
            >>> for coord in mapa:
            >>>     print(coord, mapa.celda_bloqueada(coord))
        """
        self.lista_cordenadas = []
        for x in range(self.filas):
            for y in range (self.columnas):
                self.lista_cordenadas.append(Coord(x, y))

        return iter(self.lista_cordenadas)

def coordenadas_vecinas(coord, mapa):
    '''Recibe por parámetro una coordenada y el mapa del laberinto, devuelve un alista
    donde se encuentran sus celdas vecinas.'''
    vecinas = []
    vecinas.append(mapa.trasladar_coord(coord, 1, 0))
    vecinas.append(mapa.trasladar_coord(coord, 0, 1))
    vecinas.append(mapa.trasladar_coord(coord, 0, -1))
    vecinas.append(mapa.trasladar_coord(coord, -1, 0))
    
    for vecina in vecinas:
        if vecina == coord:
            vecinas.remove(vecina)
    return vecinas