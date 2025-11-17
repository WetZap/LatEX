# Lectura de datos para el informe de Cuántica P4



def leer_datos(ruta_archivo):
    """Lee los datos desde un archivo de texto y los devuelve como una lista de listas de floats.

    Args:
        ruta_archivo (str): La ruta al archivo de datos.

    Returns:
        list: Una lista de listas, donde cada sublista contiene los valores numéricos de una línea del archivo.
    """
    datos = []
    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            # Dividir la línea en valores separados por espacios y convertirlos a float
            valores = [float(valor) for valor in linea.split("\t")]
            datos.append(valores)
    return datos




