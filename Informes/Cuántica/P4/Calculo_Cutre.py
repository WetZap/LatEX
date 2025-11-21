import numpy as np
import matplotlib.pyplot as plt



def leer_datos(rutas_archivos):
    # Lee los datos de multilples archivos de texto y los devuelve como una lista de listas.
    datos = [[] for _ in range(len(rutas_archivos))]
    valores_constantes = [[] for _ in range(len(rutas_archivos))]
    for i, ruta_archivo in enumerate(rutas_archivos):
        
        with open(ruta_archivo, 'r') as archivo:
            conta = 0
            for linea in archivo:
                linea = linea.strip("\n")

                # Dividir la línea en valores separados por espacios y convertirlos a float
                # Nos saltamos las 3 primeras lineas de cada archivo
                if conta < 3:
                    conta += 1
                    continue
                else:
                    valores = [float(valor.replace(",", ".")) for valor in linea.split("\t")[0:2]]
                    datos[i].append(valores)
                    valores_constantes[i].append([float(valor.replace(",", ".")) for valor in linea.split("\t")[2:]])
    return datos, valores_constantes


def extraer_rutas(ruta_carpeta):

    """Extrae las rutas de los archivos de datos en una carpeta dada.
    """
    import os

    rutas_archivos = []
    for nombre_archivo in os.listdir(ruta_carpeta):
        if nombre_archivo.endswith('.txt'):
            rutas_archivos.append(os.path.join(ruta_carpeta, nombre_archivo))
    return rutas_archivos
ruta = "Datos/Medidas_B_5/"
rutas_archivos = extraer_rutas(ruta)
datos, valores_constantes = leer_datos(rutas_archivos)
fig=plt.figure(figsize=[18,12])
ax=fig.gca()
for i in datos:
    eje_x = [fila[0] for fila in i]
    eje_y = [fila[1] for fila in i]
    plt.plot(eje_x, eje_y, linewidth=2,label=f'Datos {datos.index(i)+1}')
    plt.show()









