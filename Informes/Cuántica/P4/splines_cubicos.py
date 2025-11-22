import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# ======================================================
# 1. Datos (Rellena aquí con tus valores reales)
# ======================================================
# Ejemplo de estructura: mismas x para las tres curvas
x = np.array([   # ν(Hz)
    0, 5, 10, 15, 20, 25, 30, 35,
    40, 45, 50, 55, 60, 65, 70, 75,
    80, 85, 90, 95, 100
], dtype=float)

# Sustituye estos ejemplos por tus 'Datos 1, 2, 3'
y1 = np.array([...], dtype=float)   # Datos 1  → V0(ν)
y2 = np.array([...], dtype=float)   # Datos 2
y3 = np.array([...], dtype=float)   # Datos 3

# ======================================================
# 2. Construir los splines cúbicos (naturales)
# ======================================================
cs1 = CubicSpline(x, y1, bc_type="natural")
cs2 = CubicSpline(x, y2, bc_type="natural")
cs3 = CubicSpline(x, y3, bc_type="natural")

# Definimos funciones "bonitas" para usarlas como V0(ν)
V0_1 = lambda nu: cs1(nu)
V0_2 = lambda nu: cs2(nu)
V0_3 = lambda nu: cs3(nu)

# ======================================================
# 3. Ejemplo de uso numérico
# ======================================================
nu_test = 62.9   # Hz, por ejemplo
print("V0_1(62.9 Hz) =", float(V0_1(nu_test)))
print("V0_2(62.9 Hz) =", float(V0_2(nu_test)))
print("V0_3(62.9 Hz) =", float(V0_3(nu_test)))

# ======================================================
# 4. Graficar datos originales + spline suave
# ======================================================
x_fino = np.linspace(x.min(), x.max(), 1000)

plt.figure(figsize=(8, 4))
plt.plot(x, y1, "o", label="Datos 1")
plt.plot(x, y2, "o", label="Datos 2")
plt.plot(x, y3, "o", label="Datos 3")

plt.plot(x_fino, V0_1(x_fino), "-", label="Spline Datos 1")
plt.plot(x_fino, V0_2(x_fino), "-", label="Spline Datos 2")
plt.plot(x_fino, V0_3(x_fino), "-", label="Spline Datos 3")

plt.xlabel("ν (Hz)")
plt.ylabel("V0 (V)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# ======================================================
# 5. (Opcional) Imprimir las fórmulas por tramos
# ======================================================
def imprimir_tramos(cs, nombre="S"):
    xs = cs.x        # nodos
    coef = cs.c      # coeficientes (4, n-1): [a3, a2, a1, a0]

    print(f"\nSpline cúbico {nombre}:")
    for i in range(len(xs) - 1):
        a3, a2, a1, a0 = coef[:, i]
        x_i = xs[i]
        print(f"Tramo {i}:   para {x_i} <= ν <= {xs[i+1]}")
        print(f"  {nombre}_i(ν) = {a3}*(ν-{x_i})**3 "
              f"+ {a2}*(ν-{x_i})**2 + {a1}*(ν-{x_i}) + {a0}\n")

# Llamar si quieres ver las expresiones
imprimir_tramos(cs1, "V0_1")
imprimir_tramos(cs2, "V0_2")
imprimir_tramos(cs3, "V0_3")
