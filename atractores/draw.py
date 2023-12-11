import math
import random
from matplotlib import pyplot
from time import time

def dibujar(parametros):
    # Desempaquetar los parámetros
    x, y, a = parametros

    # Listas para almacenar todo el camino
    x_lista = [x]
    y_lista = [y]

    # Iterativamente pasar (x, y) al mapa cuadrático
    for i in range(10000):

        # Calcular el siguiente punto (usando el mapa cuadrático)
        xnew = a[0] + a[1]*x + a[2]*x*x + a[3]*y + a[4]*y*y + a[5]*x*y
        ynew = a[6] + a[7]*x + a[8]*x*x + a[9]*y + a[10]*y*y + a[11]*x*y

        # Actualizar x y
        x = xnew
        y = ynew

        # Almacenar xy en la lista de caminos
        x_lista.append(x)
        y_lista.append(y)

    # Limpiar la figura
    pyplot.clf()

    # Diseño del gráfico
    pyplot.style.use("dark_background")
    pyplot.axis("off")

    # Crear el gráfico
    pyplot.scatter(x_lista[100:], y_lista[100:], s=0.1, c="white", linewidths=0)
    
    # Guardar la figura
    nombre = str(time()) 
    pyplot.savefig(nombre + ".png", dpi=1000)

parametros = (0.30020209069255444, 0.02621433695142117, [-0.6245023904369602, 0.5015579715351031, 1.1570876912931487, -1.3023042380219523, 0.578739911204667, -1.0004329487913655, 0.12531861098541608, -1.448429580959672, -1.0939155854873217, 1.0713759197091623, -1.8478075373747869, 1.6183331995471462])

dibujar(parametros)
