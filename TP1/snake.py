import terminal
import random

CABEZA = 0
ARRIBA = 'w'
ABAJO = 's'
DERECHA = 'd'
IZQUIERDA = 'a'
FILAS = 10
COLUMNAS = 10
TIEMPO_MAX = 0.5
PUNTOS_MAX = 100

def crear_tablero(filas, columnas):
	'''Recibe por parámetro una cantidad de filas y columnas para crear una "matriz" (lista de listas) y que sea el tablero.
	Devuelve el tablero creado.'''
	tablero = []
	for i in range(filas):
		tablero.append([])
		for j in range(columnas):
			tablero[i].append(".")
	return tablero

def crear_fruta(filas, columnas, serpiente):
	'''Recibe por por parametro el número de filas y columnas del tablero, y la serpiente. Devuelve una posición random de la fruta
	mientras que esta nunca coincida con la de la serpiente.'''

	while True:
		x = random.randint(0, filas - 1)
		y = random.randint(0, columnas - 1)
		fruta = (x, y)
		if not fruta == serpiente[CABEZA]:
			return fruta

def crear_serpiente():
	'''Crea la serpiente en su posición inicial (inicio del tablero) y la devuelve.'''
	serpiente = [(0, 0)]
	return serpiente

def imprimir_jugada(tablero):
	'''Recibe por parametro el tablero creado y lo imprime.'''
	terminal.clear_terminal()
	for fila in tablero:
		print()
		for columna in fila:
			print(columna, end=" ")

def mover_serpiente(movimiento, serpiente):
	'''Recibe por parámetro el movimiento ingresado por el usuario y la serpiente. Muta la serpiente con las nuevas
	posiciones a lo largo de la partida. '''
	if ARRIBA in movimiento:
		nueva_posicion_cabeza = (serpiente[CABEZA][0] - 1, serpiente[CABEZA][1])
	elif ABAJO in movimiento:
		nueva_posicion_cabeza = (serpiente[CABEZA][0] + 1, serpiente[CABEZA][1])
	elif DERECHA in movimiento:
		nueva_posicion_cabeza = (serpiente[CABEZA][0], serpiente[CABEZA][1] + 1)
	elif IZQUIERDA in movimiento:
		nueva_posicion_cabeza = (serpiente[CABEZA][0], serpiente[CABEZA][1] - 1)
	

	serpiente.pop(-1)
	serpiente.insert(0, nueva_posicion_cabeza)
	
def pedir_movimiento(movimiento_anterior, tiempo_max):
	'''Recibe por parámetro el movieminto anterior y el tiempo máximo para ingresar una tecla. Cuando el usuario
	ingresa una tecla, se valida si es válida o no. La función devuelve el movimiento válido actual o el movimiento
	anterior.'''
	movimiento = terminal.timed_input(tiempo_max).lower()

	if es_movimiento_valido(movimiento):
		return obtener_movimiento_valido(movimiento)
	return movimiento_anterior

def es_movimiento_valido(movimiento):
	'''Recibe por parámetro el movimiento ingresado por el usuario y devuelve True si es uno de los movimientos
	válidos para el juego, si no lo es, devuelve False.'''
	for c in movimiento[::-1]:
		if (c == ARRIBA) or (c == ABAJO) or (c == IZQUIERDA) or (c == DERECHA):
			return True
	return False

def obtener_movimiento_valido(movimiento):
	'''Recibe por parámetro el movimiento válido ingresado por el usuario y devuelve la última entrada válida ingresada
	por el usuario.'''
	for c in movimiento[::-1]:
		if (c == ARRIBA) or (c == ABAJO) or (c == IZQUIERDA) or (c == DERECHA):
			return c

def comer_fruta(fruta, serpiente):
	'''La función recibe por parámetro la fruta y la serpiente. Si la posición de la cabeza de la serpiente es la misma
	que la de la fruta, la función devuelve True. '''
	return serpiente[CABEZA] ==	fruta

def perder(serpiente, copia_serpiente_vieja):
	'''Recibe por parámetro la serpiente. Devuleve True si la posición de la cabeza de la serpiente es la misma que
	los del algún borde del tablero o de alguna posición del cuerpo. '''
	if ((serpiente[CABEZA][0] < 0) or (serpiente[CABEZA][0] >= FILAS)) or ((serpiente[CABEZA][1] < 0) or \
		(serpiente[CABEZA][1] >= COLUMNAS)):
		return True
	else:
		return serpiente[0] in copia_serpiente_vieja
	return False

def ganar(puntos):
	'''Recibe por parámetro los puntos acumulados y si coinciden con el puntaje máximo disponible, devuelve True. '''
	return puntos == PUNTOS_MAX

def mostrar_jugada(serpiente, fruta, filas, columnas, puntos):
	'''Recibe por parámetro la serpiente, fruta, filas y columnas del tablero. Crea el tablero en dónde se mueve la 
	serpiente y lo muta agregando la serpiente y la fruta. Imprime el tablero.'''
	tablero = crear_tablero(filas, columnas)
	for parte_cuerpo in serpiente:
		tablero[parte_cuerpo[0]][parte_cuerpo[1]] = "■"
	tablero[fruta[0]][fruta[1]] = "♦"
	imprimir_jugada(tablero)
	print()
	print(f"¡Tenés {puntos} puntos!")

def main():
	serpiente = crear_serpiente()
	fruta = crear_fruta(FILAS, COLUMNAS, serpiente)

	puntos = 0
	movimiento_anterior = ABAJO
	mostrar_jugada(serpiente, fruta, FILAS, COLUMNAS, puntos)

	while True:
		copia_serpiente_vieja = serpiente[:]
		movimiento = (pedir_movimiento(movimiento_anterior, TIEMPO_MAX))
		mover_serpiente(movimiento, serpiente)
		movimiento_anterior = movimiento
			
		if perder(serpiente, copia_serpiente_vieja):
			print(f"¡Perdiste! Obtuviste {puntos} puntos en esta partida.")
			return

		if comer_fruta(fruta, serpiente):
			fruta = crear_fruta(FILAS, COLUMNAS, serpiente)
			serpiente.append(serpiente[-1])
			puntos += 10

		if ganar(puntos):
			print(f"¡Felicitaciones! Ganaste, obtuviste {puntos} puntos.")
			return
	
		mostrar_jugada(serpiente, fruta, FILAS, COLUMNAS, puntos)
main()


