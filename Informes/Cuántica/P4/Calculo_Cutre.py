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
ruta = "Datos/Medidas_B_1/"
rutas_archivos = extraer_rutas(ruta)
datos, valores_constantes = leer_datos(rutas_archivos)
fig=plt.figure(figsize=[18,12])
ax=fig.gca()
for i in datos:
    eje_x = [fila[0] for fila in i]
    eje_y = [fila[1] for fila in i]
    fig=plt.figure(figsize=[18,12])
    ax=fig.gca()
    plt.plot(eje_x, eje_y, linewidth=2,label=fr'Datos para $U_2$= {valores_constantes[datos.index(i)][0][0]}, $U_3$= {valores_constantes[datos.index(i)][0][1]} y $U_H$= {valores_constantes[datos.index(i)][0][2]}')
    plt.ylabel(r'$I\ nA$',fontsize=25)
    plt.xlabel(r'$V_1\ V$',fontsize=25)
    plt.legend(loc='best',fontsize=25)
    plt.grid()
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(4)

        # Con estas líneas podemos dar formato a los "ticks" de los ejes:
    plt.tick_params(axis="x", labelsize=25, labelrotation=0, labelcolor="black")
    plt.tick_params(axis="y", labelsize=25, labelrotation=0, labelcolor="black")
        # Aquí dibuja el gráfico que hemos definido
    plt.show()









