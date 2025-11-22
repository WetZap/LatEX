import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Lectura de datos para el informe de Cuántica P4
def calculo_extremos(cs):
    inflexion = []
    maximos = []
    minimos = []
    xs = cs.x        # nodos
    coef = cs.c      # coeficientes (4, n-1): [a3, a2, a1, a0]
    for i in range(len(xs) - 1):
        d, c, b, a = coef[:, i]
        extremo_pos = (-((2*c)/(3*d)) + np.sqrt(((2*c)/(3*d))**2-(4*b/(3*d))))/2
        extremo_neg = (-((2*c)/(3*d)) - np.sqrt(((2*c)/(3*d))**2-(4*b/(3*d))))/2
        signo_pos = 2*c + 6*d*extremo_pos
        signo_neg = 2*c + 6*d*extremo_neg
        if signo_pos == 0:
            inflexion.append(extremo_pos)
        elif signo_pos > 0:
            minimos.append(extremo_pos)
        else:
            maximos.append(extremo_pos)
        if signo_neg == 0:
            inflexion.append(extremo_neg)
        elif signo_neg > 0:
            minimos.append(extremo_neg)
        else:
            maximos.append(extremo_neg)
    print("Inflexiones:", inflexion)
    print("Minimos:", minimos)
    print("Maximos:", maximos)




def calcular_funcion_analitica(datos):

    for conjunto in datos:
        eje_x = np.array([fila[0] for fila in conjunto])
        eje_y = np.array([fila[1] for fila in conjunto])
        
        cs = CubicSpline(eje_x, eje_y, bc_type="natural")
        funcion_analitica = lambda x: cs(x)
        V0_1 = lambda nu: cs(nu)

    # ======================================================
    # 4. Graficar datos originales + spline suave
    # ======================================================
        x_fino = np.linspace(eje_x.min(), eje_x.max(), 1000)

        plt.figure(figsize=(8, 4))
        plt.plot(eje_x, eje_y, "o", label="Datos 1")
        plt.plot(x_fino, V0_1(x_fino), "-", label="Spline Datos 1")

        plt.xlabel("ν (Hz)")
        plt.ylabel("V0 (V)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
        
        # ======================================================
        # 5. (Opcional) Imprimir las fórmulas por tramos
        # ======================================================

        calculo_extremos(cs)

    return 










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
contador = 1
ruta = "Datos/Medidas_B_5/"
rutas_archivos = extraer_rutas(ruta)
datos, valores_constantes = leer_datos(rutas_archivos)
fig=plt.figure(figsize=[18,12])
ax=fig.gca()
for i in datos:
    eje_x = [fila[0] for fila in i]
    eje_y = [fila[1] for fila in i]
    if contador ==1:
        maximos = calcular_funcion_analitica([i])
        print(maximos)
    plt.plot(eje_x, eje_y, linewidth=2,label=f'Datos {datos.index(i)+1}')

    contador += 1
plt.xlabel(r'$I nA$',fontsize=25)
plt.ylabel(r'$V_0 V$',fontsize=25)
plt.legend(loc='best',fontsize=25)
plt.grid()

        # Este comando permite modificar el grosor de los ejes:
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(4)

        # Con estas líneas podemos dar formato a los "ticks" de los ejes:
plt.tick_params(axis="x", labelsize=25, labelrotation=0, labelcolor="black")
plt.tick_params(axis="y", labelsize=25, labelrotation=0, labelcolor="black")
        # Aquí dibuja el gráfico que hemos definido.
plt.show()









