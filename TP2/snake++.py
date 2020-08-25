import terminal
import random
import csv

CABEZA = 0
ARRIBA = 'w'
ABAJO = 's'
DERECHA = 'd'
IZQUIERDA = 'a'

def crear_tablero(filas, columnas):
	'''Recibe por parámetro una cantidad de filas y columnas para crear una "matriz" (lista de listas) y que sea el tablero.
	Devuelve el tablero creado.'''
	tablero = []
	for i in range(filas):
		tablero.append([])
		for j in range(columnas):
			tablero[i].append(".")
	return tablero

def crear_fruta(filas, columnas, serpiente, obstaculos):
	'''Recibe por por parametro el número de filas y columnas del tablero, y la serpiente. Devuelve una posición random de la fruta
	mientras que esta nunca coincida con la de la serpiente.'''

	while True:
		x = random.randint(0, filas - 1)
		y = random.randint(0, columnas - 1)
		fruta = (x, y)
		if not fruta == serpiente[CABEZA] and not fruta in obstaculos:
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
	
def pedir_movimiento(movimiento_anterior, tiempo_max, teclas_especiales):
	'''Recibe por parámetro el movieminto anterior, el tiempo máximo para ingresar una tecla y las teclas necesarias para activar un especial. 
	Cuando el usuario ingresa una tecla, se valida si es válida o no. La función devuelve una secuencia con el movimiento válido actual o
	el movimiento anterior y con la tecla para activar el especial.'''
	movimiento = terminal.timed_input(tiempo_max).lower()

	movimiento_ingresado = obtener_movimiento_valido(movimiento, movimiento_anterior)
	especial_activado = obtener_especial_valido(movimiento, teclas_especiales)

	return movimiento_ingresado, especial_activado

def obtener_movimiento_valido(movimiento, movimiento_anterior):
	'''Recibe por parámetro las teclas ingresadas por el usuario y el mov anterior, si las teclas ingresadas son válidas para mover
	la serpiente devuelve el movimiento hecho y sino, devuelve el movimiento anterior.'''
	for c in movimiento[::-1]:
		if (c == ARRIBA) or (c == ABAJO) or (c == IZQUIERDA) or (c == DERECHA):
			return c
	return movimiento_anterior

def se_quiere_activar_especial(ingreso_usuario, teclas_especiales):
	'''Recibe como parámetro las teclas ingresadas por el usuario y un diccionario con las teclas para activar el especial; 
	dependiendo si las teclas son válidas para activar el especial devuelve un bool.'''
	for caract in ingreso_usuario[::-1]:
		if caract in teclas_especiales:
			return True
	return False

def obtener_especial_valido(ingreso_usuario, teclas_especiales):
	'''Recibe por parámetro las teclas ingresadas por el usuario y las teclas necesarias para activar algún especial, 
	devuelve la tecla válida para activar el especial. '''
	for caract in ingreso_usuario[::-1]:
		if caract in teclas_especiales:
			return caract
	return ""

def comer_fruta(fruta, serpiente):
	'''Recibe como parámetro la fruta y la serpiente. Si la posición de la cabeza de la serpiente es la misma
	que la de la fruta, la función devuelve True. '''
	return serpiente[CABEZA] ==	fruta

def perder(serpiente, copia_serpiente_vieja, filas, columnas, obstaculos):
	'''Recibe por parámetro la serpiente, filas, columnas y las posiciones de los obstaculos. Devuleve True si la posición
	de la cabeza de la serpiente es la misma que los del algún borde del tablero o de alguna posición del cuerpo. '''
	for obstaculo in obstaculos:
		if serpiente[CABEZA] == obstaculo:
			return True

	if ((serpiente[CABEZA][0] < 0) or (serpiente[CABEZA][0] >= filas)) or ((serpiente[CABEZA][1] < 0) or \
		(serpiente[CABEZA][1] >= columnas)):
		return True
	else:
		return serpiente[0] in copia_serpiente_vieja
	return False

def ganar(puntos, puntos_max):
	'''Recibe por parámetro los puntos acumulados y si coinciden con el puntaje máximo disponible, devuelve True. '''
	return puntos == puntos_max

def mostrar_jugada(serpiente, fruta, filas, columnas, puntos, obstaculos, posicion_especial, especial):
	'''Recibe por parámetro la serpiente, fruta, filas y columnas del tablero. Crea el tablero en dónde se mueve la 
	serpiente y lo muta agregando la serpiente y la fruta. Imprime el tablero.'''
	tablero = crear_tablero(filas, columnas)
	tablero[posicion_especial[0]][posicion_especial[1]] = especial
	for parte_cuerpo in serpiente:
		tablero[parte_cuerpo[0]][parte_cuerpo[1]] = "■"
	tablero[fruta[0]][fruta[1]] = "♦"
	for obstaculo in obstaculos:
		tablero[obstaculo[0]][obstaculo[1]] = "∏"
	imprimir_jugada(tablero)
	print()
	print(f"¡Tenés {puntos} puntos!")

def cambiar_nivel(ruta_archivo):
	'''Recibe por parámetro la ruta del nivel a jugar. Devuelve una lista con los valores de los datos necesarios para
	jugar el nivel. '''
	especiales = {}
	with open(ruta_archivo) as nivel:
		puntos_max = int(nivel.readline().rstrip("\n"))
		tiempo_max = float(nivel.readline().rstrip("\n"))
		tamano = nivel.readline().rstrip("\n").split("x")
		filas = int(tamano[0])
		columnas = int(tamano[1])
		obs = nivel.readline().rstrip("\n").split(";")
		obstaculos = [tuple(map(int, numero.split(','))) for numero in obs]
		esp = nivel.readline().rstrip("\n").split(",")
		for especial in esp:
			especiales[especial] = especiales.get(especial, 0)
		return [puntos_max, tiempo_max, filas, columnas, obstaculos, especiales]

def crear_posicion_especial(especiales, serpiente, fruta, obstaculos, filas, columnas):
	'''Recibe por parámetro la mochila de los especiales, la serpiente, fruta, obstaculos, filas y columnas. Elige un 
	especial aleatorio y una posición aleatoria del mismo. Devuleve una lista con el especial y su posición.'''
	especiales_lista = list(especiales.keys())
	aleatorio = random.randint(0, len(especiales_lista) - 1)
	especial_aleatorio = especiales_lista[aleatorio]
	while True:
		x = random.randint(0, filas - 1)
		y = random.randint(0, columnas - 1)
		posicion_especial = (x, y)
		if posicion_especial != serpiente[CABEZA] and posicion_especial != fruta and posicion_especial not in obstaculos:
			return [especial_aleatorio, posicion_especial]

def recolectar_especial(serpiente, posicion_especial):
	'''Recibe por parámetro la serpiente y la posición del especial aleatorio ubicado en el tablero. Devuelve un booleano
	dependiendo si la posición de la cabeza de la serpiente es la misma que la del especial.'''
	if serpiente[CABEZA] == posicion_especial:
		return True
	return False

def recolectar_informacion_especiales(ruta_archivo):
	'''Recibe por parámetro una ruta de archivo, donde se encuentra la información de los especiales, y devuelve una lista con toda
	la información de dicho archivo.'''
	info_especiales = []
	with open(ruta_archivo) as archivo:
		csv_reader = csv.reader(archivo)
		for fila in csv_reader:
			info_especiales.append(fila)
		return info_especiales

def imprimir_mochila(mochila, info_especiales):
	'''Recibe como parámetro la mochila de especiales y la información de ellos. Imprime la cantidad de especiales en la mochila y 
	la descripción de los mismos. '''
	print()
	print("ESPECIAL", "|", "CANTIDAD", "|", "TECLA", "|", "DESCRIPCIÓN")
	for fila in info_especiales:
		print(fila[0], "       |      ", mochila.get(fila[0], 0), " |    ", fila[3], "|", fila[4])

def crear_dic_teclas_acciones_especiales(info_especiales):
	'''Recibe por parámetro una lista con toda la información de los especiales y devuelve una tupla con un diccionario con las teclas necesarias
	para activar el diccionario y otro con las acciones que realiza cada especial.'''
	teclas = {}
	acciones = {}
	for fila in info_especiales:
		teclas[fila[3]] = fila[0]
		acciones[fila[0]] = (fila[1], fila[2])
	return teclas, acciones


def activar_especial(tecla_usuario, mochila_especiales, teclas_especiales):
	'''Recibe por parámetro la tecla ingresada por el usuario, la mochila de los especiales y un diccionario con las teclas necesarias
	para activar el especial. Devuelve un bool si se quieren activar el especial y se tiene la cantidad necesaria de ellos en la mochila. '''
	return se_quiere_activar_especial(tecla_usuario, teclas_especiales) and mochila_especiales[teclas_especiales[tecla_usuario]] > 0

def main():

	nivel = 0
	cant_niveles = 3

	while nivel <= cant_niveles:
		nivel += 1
		try:
			nivel_datos = cambiar_nivel(f"nivel_{nivel}.txt")
		except IOError:
			print("No pueden cargarse correctamente los niveles.")
			return
		
		puntos_max = nivel_datos[0] * 10
		tiempo_max = nivel_datos[1]
		filas = nivel_datos[2]
		columnas = nivel_datos[3]
		obstaculos = nivel_datos[4]
		mochila_especiales = nivel_datos[5]
		
		serpiente = crear_serpiente()
		fruta = crear_fruta(filas, columnas, serpiente, obstaculos)
		datos_especial_aleatorio = crear_posicion_especial(mochila_especiales, serpiente, fruta, obstaculos, filas, columnas)
		especial_aleatorio = datos_especial_aleatorio[0]
		posicion_especial = datos_especial_aleatorio[1]
		informacion_especiales = recolectar_informacion_especiales("especiales.csv")
		teclas_especiales = crear_dic_teclas_acciones_especiales(informacion_especiales)[0]
		acciones_especiales = crear_dic_teclas_acciones_especiales(informacion_especiales)[1]

		puntos = 0
		movimiento_anterior = ABAJO
		mostrar_jugada(serpiente, fruta, filas, columnas, puntos, obstaculos, posicion_especial, especial_aleatorio)
		imprimir_mochila(mochila_especiales, informacion_especiales)

		while True:
			
			copia_serpiente_vieja = serpiente[:]

			try:
				ingreso_usuario = pedir_movimiento(movimiento_anterior, tiempo_max, teclas_especiales)
			except UnicodeDecodeError:
				continue

			movimiento = ingreso_usuario[0]
			especial_activado = ingreso_usuario[1]

			mover_serpiente(movimiento, serpiente)
			movimiento_anterior = movimiento
				
			if perder(serpiente, copia_serpiente_vieja, filas, columnas, obstaculos):
				
				print(f"¡Perdiste! Obtuviste {puntos} puntos en este nivel.")
				return

			if comer_fruta(fruta, serpiente):
				
				fruta = crear_fruta(filas, columnas, serpiente, obstaculos)
				serpiente.append(serpiente[-1])
				puntos += 10

			
			if activar_especial(especial_activado, mochila_especiales, teclas_especiales):

				if acciones_especiales[teclas_especiales[especial_activado]][0] == "largo":
					if acciones_especiales[teclas_especiales[especial_activado]][1] == "+1":
						serpiente.append(serpiente[-1])
						puntos += 10

					if acciones_especiales[teclas_especiales[especial_activado]][1] == "-1":
						serpiente.pop(-1)
						puntos -= 10

				if acciones_especiales[teclas_especiales[especial_activado]][0] == "velocidad":
					if acciones_especiales[teclas_especiales[especial_activado]][1] == "+1":
						tiempo_max += 1

					if acciones_especiales[teclas_especiales[especial_activado]][1] == "-0.3":
						tiempo_max -= 0.3

				mochila_especiales[teclas_especiales[especial_activado]] = mochila_especiales[teclas_especiales[especial_activado]] - 1

			if recolectar_especial(serpiente, posicion_especial):
				mochila_especiales[especial_aleatorio] = mochila_especiales[especial_aleatorio] + 1
				especial_aleatorio = crear_posicion_especial(mochila_especiales, serpiente, fruta, obstaculos, filas, columnas)[0]
				posicion_especial = crear_posicion_especial(mochila_especiales, serpiente, fruta, obstaculos, filas, columnas)[1]

			if ganar(puntos, puntos_max):
				print(f"¡Felicitaciones! Ganaste, obtuviste {puntos} puntos en este nivel.")
				break

			mostrar_jugada(serpiente, fruta, filas, columnas, puntos, obstaculos, posicion_especial, especial_aleatorio)
			imprimir_mochila(mochila_especiales, informacion_especiales)
		
main()


