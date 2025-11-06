# Escribire un programa que junte una multitud de programas
# utiles a lo largo de la carrera, se hara en forma de menu

# Importamos todos los modulos necesarios
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
from scipy.optimize import curve_fit
from statistics import stdev
from statistics import mean
from scipy import odr




'''
Lista de numeros para los programas, debera cambiar el valor de opción para ejecutar un programa u otro
1 Ajuste lineal tipo y = ax con incertidumbre
2 Ajuste lineal tipo y = ax + b con incertidumbre
3 Ajuste lineal tipo y = ax² + bx + c con incertidumbre
4 Ajuste de dos conjuntos de datos y determinación de intersección



'''
opcion = ''

# Esta sera la ruta en la que se encuentran los datos, el archivo debe estar en .csv
file_name = "CuartRepre.csv"

# Ahora escribiremos el delimitador, si lo has separado con espacios, con comas, con tabuladores:
delimitador = '\t'

# Nombre de la gráfica que se guardara.
nombre_graf = ''


while opcion != '0':
    print('------------------------------------------------')
    print('Programa de ajustes lineales y análisis de datos')
    print('------------------------------------------------')
    print('Seleccione una opción:')
    print('1. Ajuste lineal tipo y = a * x')
    print('2. Ajuste lineal tipo y = a * x + b')
    print('3. Ajuste lineal tipo y = a * x² + b * x + c')
    print('4. Ajuste de dos conjuntos de datos y determinación de intersección')
    print('0. Salir')
    opcion = input('Ingrese el número de la opción deseada: ')

    if opcion not in ['0', '1', '2', '3', '4']:
        print('Opción no válida. Por favor, intente de nuevo.')
        
    if opcion == '1':
        print('------------------------------------------------')
        print('Escogió la opción 1, ajuste lineal tipo y = a * x: ')
        print('------------------------------------------------')

        print(f"El archivo de datos debe tener la siguiente estructura:\nx{delimitador}y{delimitador}dx{delimitador}dy{delimitador}")
        
        ### Función de ajuste

        def func(x, a):
            return a*x

        ### Lectura de datos

        data = pd.read_csv(file_name, delimiter=delimitador, header=0, names=['x', 'y','dx', 'dy'])
        print(data)

        ### Ajuste

        popt, pcov = curve_fit(func, data.x, data.y, sigma=data.dy, absolute_sigma=True,maxfev=10000)

        y_pred = func(data.x, *popt)

        r = data.y - y_pred
        chisq = sum((r / data.dy) ** 2)
        mediax = mean(data.x)
        mediay = mean(data.y)

        mediaxy = mean(data.x*data.y)
        sigmax = stdev(data.x)
        sigmay = stdev(data.y)
        coef_Pearson = len(data.x)*(mediaxy-mediax*mediay)/((len(data.x)-1)*sigmax*sigmay)

        ### Salida de resultados

        print(f'   a: {popt[0]} \u00B1 {np.sqrt(pcov.diagonal())[0]}')
        print('')
        print(f'chi\u00b2: {chisq}')
        print('')
        print(f'media x: {mediax}')
        print(f'media y: {mediay}')
        print(f'media xy: {mediaxy}')
        print(f'Sigma x: {sigmax}')
        print(f'Sigma y: {sigmay}')
        print(f'Coeficiente de Pearson: {coef_Pearson}')

        ### Gráfica
        # - figure crea la figura con el tamaño indicado (los valores son en pulgadas y el valor por defecto de número de puntos por pulgada es 100).
        # - errorbar muestra los datos data.x y data.y con sus errores (data.dx y data.dy).
        #     - el formato es puntos de color azul: format='b.'
        #     - label es la etiqueta que aparecerá en la leyenda
        #     - definimos el grosor de las líneas con linewidth
        # - plot lo usamos para mostrar la recta de regresión.
        #     - Aquí indicamos que el formato es una línea roja: format='r-'
        # - xlim e ylim definen los límites de los ejes x e y respectivamente.
        # - xlabel e ylabel definen la etiqueta de los ejes x e y respectivamente
        #     - Podemos definir una etiqueta en formato LaTex poniendo r antes de la cadena de texto y la exprexión LaTex entre simbolos $ (mira ylabel)
        # - legend muestra la leyenda.

        fig=plt.figure(figsize=[18,12])
        ax=fig.gca()
        plt.errorbar(data.x, data.y, xerr=data.dx, yerr=data.dy, fmt='b.', label='Datos', linewidth=3)
        plt.plot(data.x, y_pred, 'g-', label='Ajuste',linewidth=4.0)


        plt.xlabel(r'$\nu (Hz)$',fontsize=25)
        plt.ylabel(r'$V_0 (V)$',fontsize=25)
        plt.legend(loc='best',fontsize=25)
        plt.grid()

        # Este comando permite modificar el grosor de los ejes:
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(4)

        # Con estas líneas podemos dar formato a los "ticks" de los ejes:
        plt.tick_params(axis="x", labelsize=25, labelrotation=0, labelcolor="black")
        plt.tick_params(axis="y", labelsize=25, labelrotation=0, labelcolor="black")

        # Aquí dibuja el gráfico que hemos definido.
        plt.savefig(nombre_graf)
        plt.show()

    elif opcion == '2':
        print('----------------------------------------------------')
        print('Escogió opción 2, ajuste lineal tipo y = a * x + b: ')
        print('----------------------------------------------------')

        print(f"El archivo de datos debe tener la siguiente estructura:\nx{delimitador}y{delimitador}dx{delimitador}dy{delimitador}")

        ### Función de ajuste

        def func(x, a, b):
            return a*x + b

        ### Lectura de datos

        data = pd.read_csv(file_name, delimiter=delimitador, header=0, names=['x', 'y','dx', 'dy'])
        print(data)

        ### Ajuste

        popt, pcov = curve_fit(func, data.x, data.y, sigma=data.dy, absolute_sigma=True,maxfev=10000)

        y_pred = func(data.x, *popt)

        r = data.y - y_pred
        chisq = sum((r / data.dy) ** 2)
        mediax = mean(data.x)
        mediay = mean(data.y)

        mediaxy = mean(data.x*data.y)
        sigmax = stdev(data.x)
        sigmay = stdev(data.y)
        coef_Pearson = len(data.x)*(mediaxy-mediax*mediay)/((len(data.x)-1)*sigmax*sigmay)

        ### Salida de resultados

        print(f'   a: {popt[0]} \u00B1 {np.sqrt(pcov.diagonal())[0]}')
        if popt.size > 1:
            print(f'   b: {popt[1]} \u00B1 {np.sqrt(pcov.diagonal())[1]}')

        print('')
        print(f'chi\u00b2: {chisq}')
        print('')
        print(f'media x: {mediax}')
        print(f'media y: {mediay}')
        print(f'media xy: {mediaxy}')
        print(f'Sigma x: {sigmax}')
        print(f'Sigma y: {sigmay}')
        print(f'Coeficiente de Pearson: {coef_Pearson}')

        ### Gráfica
        # - figure crea la figura con el tamaño indicado (los valores son en pulgadas y el valor por defecto de número de puntos por pulgada es 100).
        # - errorbar muestra los datos data.x y data.y con sus errores (data.dx y data.dy).
        #     - el formato es puntos de color azul: format='b.'
        #     - label es la etiqueta que aparecerá en la leyenda
        #     - definimos el grosor de las líneas con linewidth
        # - plot lo usamos para mostrar la recta de regresión.
        #     - Aquí indicamos que el formato es una línea roja: format='r-'
        # - xlim e ylim definen los límites de los ejes x e y respectivamente.
        # - xlabel e ylabel definen la etiqueta de los ejes x e y respectivamente
        #     - Podemos definir una etiqueta en formato LaTex poniendo r antes de la cadena de texto y la exprexión LaTex entre simbolos $ (mira ylabel)
        # - legend muestra la leyenda.

        fig=plt.figure(figsize=[18,12])
        ax=fig.gca()
        plt.errorbar(data.x, data.y, xerr=data.dx, yerr=data.dy, fmt='b.', label='Datos', linewidth=3)
        plt.plot(data.x, y_pred, 'g-', label='Ajuste',linewidth=4.0)


        plt.xlabel(r'$\nu (Hz)$',fontsize=25)
        plt.ylabel(r'$V_0 (V)$',fontsize=25)
        plt.legend(loc='best',fontsize=25)
        plt.grid()

        # Este comando permite modificar el grosor de los ejes:
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(4)

        # Con estas líneas podemos dar formato a los "ticks" de los ejes:
        plt.tick_params(axis="x", labelsize=25, labelrotation=0, labelcolor="black")
        plt.tick_params(axis="y", labelsize=25, labelrotation=0, labelcolor="black")

        # Aquí dibuja el gráfico que hemos definido.
        plt.savefig(nombre_graf)
        plt.show()

    elif opcion == '3':
        print('-------------------------------------------------------------')
        print('Escogio opción 3, ajuste lineal tipo y = a * x² + b * x + c: ')
        print('-------------------------------------------------------------')

        print(f"El archivo de datos debe tener la siguiente estructura:\nx{delimitador}y{delimitador}dx{delimitador}dy{delimitador}")

        ### Función de ajuste

        def func(x, a, b,c):
            return (a*(x**2) + (b*x) + c)

        ### Lectura de datos

        data = pd.read_csv(file_name, delimiter=delimitador, header=0, names=['x', 'y','dx', 'dy'])
        print(data)

        ### Ajuste

        popt, pcov = curve_fit(func, data.x, data.y, sigma=data.dy, absolute_sigma=True,maxfev=10000)

        y_pred = func(data.x, *popt)

        r = data.y - y_pred
        chisq = sum((r / data.dy) ** 2)
        mediax = mean(data.x)
        mediay = mean(data.y)

        mediaxy = mean(data.x*data.y)
        sigmax = stdev(data.x)
        sigmay = stdev(data.y)
        coef_Pearson = len(data.x)*(mediaxy-mediax*mediay)/((len(data.x)-1)*sigmax*sigmay)

        ### Salida de resultados

        print(f'   a: {popt[0]} \u00B1 {np.sqrt(pcov.diagonal())[0]}')
        if popt.size > 1:
            print(f'   b: {popt[1]} \u00B1 {np.sqrt(pcov.diagonal())[1]}')
        if popt.size >= 2:
            print(f'   c: {popt[2]} \u00B1 {np.sqrt(pcov.diagonal())[2]}')

        print('')
        print(f'chi\u00b2: {chisq}')
        print('')
        print(f'media x: {mediax}')
        print(f'media y: {mediay}')
        print(f'media xy: {mediaxy}')
        print(f'Sigma x: {sigmax}')
        print(f'Sigma y: {sigmay}')
        print(f'Coeficiente de Pearson: {coef_Pearson}')

        ### Gráfica
        # - figure crea la figura con el tamaño indicado (los valores son en pulgadas y el valor por defecto de número de puntos por pulgada es 100).
        # - errorbar muestra los datos data.x y data.y con sus errores (data.dx y data.dy).
        #     - el formato es puntos de color azul: format='b.'
        #     - label es la etiqueta que aparecerá en la leyenda
        #     - definimos el grosor de las líneas con linewidth
        # - plot lo usamos para mostrar la recta de regresión.
        #     - Aquí indicamos que el formato es una línea roja: format='r-'
        # - xlim e ylim definen los límites de los ejes x e y respectivamente.
        # - xlabel e ylabel definen la etiqueta de los ejes x e y respectivamente
        #     - Podemos definir una etiqueta en formato LaTex poniendo r antes de la cadena de texto y la exprexión LaTex entre simbolos $ (mira ylabel)
        # - legend muestra la leyenda.

        fig=plt.figure(figsize=[18,12])
        ax=fig.gca()
        plt.errorbar(data.x, data.y, xerr=data.dx, yerr=data.dy, fmt='b.', label='Datos', linewidth=3)
        plt.plot(data.x, y_pred, 'g-', label='Ajuste',linewidth=4.0)


        plt.xlabel(r'$T (s)$',fontsize=25)
        plt.ylabel(r'$\theta (rad)$',fontsize=25)
        plt.legend(loc='best',fontsize=25)
        plt.grid()

        # Este comando permite modificar el grosor de los ejes:
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(4)

        # Con estas líneas podemos dar formato a los "ticks" de los ejes:
        plt.tick_params(axis="x", labelsize=25, labelrotation=0, labelcolor="black")
        plt.tick_params(axis="y", labelsize=25, labelrotation=0, labelcolor="black")

        # Aquí dibuja el gráfico que hemos definido.
        plt.savefig(nombre_graf)
        plt.show()

    elif opcion == '4':
        print('------------------------------------------------------------------------------------')
        print('Escogio opción 4, ajuste de dos conjuntos de datos y determinación de intersección: ')
        print('------------------------------------------------------------------------------------')

        print(f"El archivo de datos debe tener la siguiente estructura:\nx{delimitador}y{delimitador}dx{delimitador}dy{delimitador}")

        def weighted_linear_fit(data):
        ### Ajuste lineal con incertidumbres en x e y usando ODR.

            model = odr.Model(lambda p, x: p[0]*x + p[1])
            mydata = odr.RealData(data['x'], data['y'], sx=data['dx'], sy=data['dy'])
            odr_fit = odr.ODR(mydata, model, beta0=[1., 0.])
            return odr_fit.run()

        def calculate_intersection(fit1, fit2):
            ### Calcula intersección y su matriz de covarianza.

            # Parámetros y covarianzas
            a1, b1 = fit1.beta
            a2, b2 = fit2.beta
            cov1 = fit1.cov_beta
            cov2 = fit2.cov_beta

            # Cálculo analítico de la intersección
            denom = a1 - a2
            if abs(denom) < 1e-10:
                raise ValueError("Las rectas son paralelas (no hay intersección)")

            x_int = (b2 - b1) / denom
            y_int = a1 * x_int + b1

            # Propagación de errores (primer orden)
            da1 = (b1 - b2)/(denom**2)
            db1 = -1/denom
            da2 = -da1
            db2 = -db1

            grad = np.array([da1, db1, da2, db2])
            total_cov = np.block([[cov1, np.zeros((2,2))],[np.zeros((2,2)), cov2]])

            cov_intersection = grad.T @ total_cov @ grad
            return (x_int, y_int), cov_intersection

        def plot_results(set1, set2, fit1, fit2, intersection, cov):
            ### Genera la visualización con matplotlib.

            plt.figure(figsize=(10, 6))

            # Conjuntos de datos con barras de error
            plt.errorbar(set1['x'], set1['y'], xerr=set1['dx'], yerr=set1['dy'], fmt='o', color='blue', label='Conjunto 1', alpha=0.7)
            plt.errorbar(set2['x'], set2['y'], xerr=set2['dx'], yerr=set2['dy'], fmt='s', color='green', label='Conjunto 2', alpha=0.7)

            # Rectas ajustadas
            x_vals = np.array([min(set1['x'].min(), set2['x'].min()), max(set1['x'].max(), set2['x'].max())])

            plt.plot(x_vals, fit1.beta[0]*x_vals + fit1.beta[1], 'b-', label=f'Recta 1: $y = {fit1.beta[0]:.2f}x + {fit1.beta[1]:.2f}$')
            plt.plot(x_vals, fit2.beta[0]*x_vals + fit2.beta[1], 'g-', label=f'Recta 2: $y = {fit2.beta[0]:.2f}x + {fit2.beta[1]:.2f}$')

            # Punto de intersección con elipse de error
            x_int, y_int = intersection
            plot_uncertainty_ellipse(x_int, y_int, cov, plt.gca())

            plt.scatter(x_int, y_int, color='red', s=100, zorder=5, label=f'Intersección: ({x_int:.2f}, {y_int:.2f})')

            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Ajuste lineal e intersección con incertidumbres')
            plt.legend()
            plt.grid(True)
            plt.show()

        def plot_uncertainty_ellipse(x, y, cov, ax, n_std=2.0):
            ### Dibuja una elipse de incertidumbre alrededor del punto.


            pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
            ell_radius_x = np.sqrt(1 + pearson)
            ell_radius_y = np.sqrt(1 - pearson)

            ellipse = Ellipse((0, 0), width=ell_radius_x * 2 * n_std, height=ell_radius_y * 2 * n_std,facecolor='red', alpha=0.2, edgecolor='none')

            transf = transforms.Affine2D() \
                .rotate_deg(45) \
                .scale(np.sqrt(cov[0, 0]) * n_std, 
                        np.sqrt(cov[1, 1]) * n_std) \
                .translate(x, y)

            ellipse.set_transform(transf + ax.transData)
            ax.add_patch(ellipse)


            try:
                # Leer archivo CSV
                data = pd.read_csv(file_name, delimiter=delimitador, header=0, names=['x', 'y','dx', 'dy'])
                if not all(col in data.columns for col in ['x', 'y', 'dx', 'dy']):
                    raise ValueError("El archivo debe contener las columnas: x, y, dx, dy")
                
                # Separar conjuntos (asume que están ordenados secuencialmente)
                n = int(input("Número de puntos en el primer conjunto: "))
                set1 = data.iloc[:n]
                set2 = data.iloc[n:]
                
                # Realizar ajustes
                fit1 = weighted_linear_fit(set1)
                fit2 = weighted_linear_fit(set2)
                
                # Calcular intersección
                intersection, cov = calculate_intersection(fit1, fit2)
                x_int, y_int = intersection
                x_err, y_err = np.sqrt(np.diag(cov))
                
                # Resultados
                print("\n--- RESULTADOS ---")
                print(f"Recta 1: y = ({fit1.beta[0]:.4f} ± {fit1.sd_beta[0]:.4f})x + ({fit1.beta[1]:.4f} ± {fit1.sd_beta[1]:.4f})")
                print(f"Recta 2: y = ({fit2.beta[0]:.4f} ± {fit2.sd_beta[0]:.4f})x + ({fit2.beta[1]:.4f} ± {fit2.sd_beta[1]:.4f})")
                print("\nIntersección:")
                print(f"x = {x_int:.4f} ± {x_err:.4f}")
                print(f"y = {y_int:.4f} ± {y_err:.4f}")
                
                # Gráfico
                plot_results(set1, set2, fit1, fit2, intersection, cov)
                
            except Exception as e:
                print(f"Error: {str(e)}")

