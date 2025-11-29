import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def encuentraPicos(datos):
    # ==== 1. Preparar datos ====
    x = [fila[0] for fila in datos]
    y = [fila[1] for fila in datos]

    # ==== 2. Encontrar picos ====
    # Ajusta 'prominence', 'height' o 'distance' según necesites
    peaks, props = find_peaks(y, prominence=0.05*max(y), height=0.1*max(y), distance=5)
    #peaks, props = find_peaks(y, prominence=0.05, height=1.3, distance=5)

    lambda_picos = [x[i] for i in peaks]
    cuentas_picos = [y[i] for i in peaks]

    print("Picos encontrados (lambda, cuentas):")
    for lam, val in zip(lambda_picos, cuentas_picos):
        print(f"{lam:.1f} nm  ->  {val:.3f}")

    # ==== 3. Graficar y marcar picos ====
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, label="Espectro")
    plt.plot(lambda_picos, cuentas_picos, "rx", label="Picos")
    plt.xlabel("λ (nm)")
    plt.ylabel("Cuentas")
    plt.legend()
    plt.tight_layout()
    plt.show()


# Lectura de datos para el informe de Cuántica P4

def leer_datos(rutas_archivos):
    # Lee los datos de multilples archivos de texto y los devuelve como una lista de listas.
    datos = [[] for _ in range(len(rutas_archivos))]
    for i, ruta_archivo in enumerate(rutas_archivos):
        with open(ruta_archivo, "r") as archivo:
            conta = 0
            for linea in archivo:
                linea = linea.strip("\n")

                # Dividir la línea en valores separados por espacios y convertirlos a float
                # Nos saltamos las 21 primeras lineas de cada archivo
                if conta < 21:
                    conta += 1
                    continue
                else:
                    valores = [float(valor) for valor in linea.split(",")]
                    datos[i].append(valores)
    return datos


def extraer_rutas(ruta_carpeta):
    """Extrae las rutas de los archivos de datos en una carpeta dada."""
    import os

    rutas_archivos = []
    for nombre_archivo in os.listdir(ruta_carpeta):
        if nombre_archivo.endswith(".csv"):
            rutas_archivos.append(os.path.join(ruta_carpeta, nombre_archivo))
    return rutas_archivos


contador = 1
ruta = "Datos/Krypton/"
rutas_archivos = extraer_rutas(ruta)
datos = leer_datos(rutas_archivos)
'''
fig = plt.figure(figsize=[18, 12])
ax = fig.gca()

for i in datos:
    eje_x = [fila[0] for fila in i]
    eje_y = [fila[1] for fila in i]
    fig=plt.figure(figsize=[18,12])
    ax=fig.gca()
    plt.plot(eje_x, eje_y, linewidth=2,label=fr'Datos {contador}º Medida')
    plt.ylabel(r'$\Delta$',fontsize=25)
    plt.xlabel(r'$\lambda$ (nm)',fontsize=25)
    plt.legend(loc='best',fontsize=25)
    plt.grid()
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(4)

        # Con estas líneas podemos dar formato a los "ticks" de los ejes:
    plt.tick_params(axis="x", labelsize=25, labelrotation=0, labelcolor="black")
    plt.tick_params(axis="y", labelsize=25, labelrotation=0, labelcolor="black")
        # Aquí dibuja el gráfico que hemos definido
    plt.show()
    contador += 1
'''
for j in datos:
    print('-'*70)
    encuentraPicos(j)