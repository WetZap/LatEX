import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


nombre_archivo = 'datos_experimento.csv'

data = pd.read_csv(nombre_archivo, delimiter=',', header=0, names=['x', 'y', 'dx', 'dy'])