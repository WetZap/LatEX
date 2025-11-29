import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# DATOS EXPERIMENTALES - HIDRÓGENO
# ============================================================================
lambdas_exp = [656.2852, 486.135, 434.0472, 410.1734, 397.0075, 
               388.9064, 383.5397, 379.7909, 377.0633, 375.0151, 
               373.4369, 372.1946, 371.1978]

R_H = 1.0973731568160e7  # Constante de Rydberg (m⁻¹)

def energia_nivel(n):
    """Energía del nivel n del hidrógeno (eV)"""
    return -13.6 / (n**2)

# Identificar nivel superior de cada transición
n_inf = 2  # Serie de Balmer
niveles_sup = []

print("=" * 60)
print("IDENTIFICACIÓN DE TRANSICIONES - SERIE DE BALMER")
print("=" * 60)

for i, lam in enumerate(lambdas_exp):
    lam_m = lam * 1e-9  # nm a metros
    inv_lambda = 1.0 / lam_m  # m⁻¹
    
    inv_n_sup_sq = (1.0 / (n_inf**2)) - (inv_lambda / R_H)
    n_sup_sq = 1.0 / inv_n_sup_sq
    n_sup = int(round(np.sqrt(n_sup_sq)))
    
    niveles_sup.append(n_sup)
    
    nombres = ['Hα', 'Hβ', 'Hγ', 'Hδ', 'Hε', 'H8', 'H9', 
               'H10', 'H11', 'H12', 'H13', 'H14', 'H15']
    nombre = nombres[i] if i < len(nombres) else f'H{n_sup}'
    
    print(f"{nombre:4s}: n={n_sup:2d} → n=2,  λ = {lam:.2f} nm")

print("=" * 60)
print(f"Niveles observados: n = {min(niveles_sup)} hasta n = {max(niveles_sup)}")
print("=" * 60)

# ============================================================================
# CREAR DIAGRAMA DE GROTRIAN
# ============================================================================

fig, ax = plt.subplots(figsize=(16, 12))

n_maximo = max(niveles_sup)
todos_los_niveles = list(range(1, n_maximo + 1))

print(f"\nDibujando {len(todos_los_niveles)} niveles: n=1 hasta n={n_maximo}")

x_pos = 2.5

# ============ DIBUJAR TODOS LOS NIVELES ============
for n in todos_los_niveles:
    E = energia_nivel(n)
    
    if n == 1:
        color, lw, label_color = 'red', 4.0, 'red'
        label_x, label_ha = x_pos - 0.7, 'right'
    elif n == 2:
        color, lw, label_color = 'blue', 4.0, 'blue'
        label_x, label_ha = x_pos - 0.7, 'right'
    elif n <= 6:
        color, lw, label_color = 'black', 2.5, 'black'
        label_x, label_ha = x_pos + 0.7, 'left'
    else:
        color, lw, label_color = 'gray', 2.0, 'gray'
        label_x, label_ha = x_pos + 0.7, 'left'
    
    ax.plot([x_pos - 0.6, x_pos + 0.6], [E, E], 
           color=color, linewidth=lw, solid_capstyle='butt', zorder=5)
    
    fontsize = 13 if n <= 2 else (11 if n <= 8 else 9)
    fontweight = 'bold' if n <= 2 else 'normal'
    label_text = f'n={n}' if n <= 2 else (f'n={n}' if n <= 8 else f'{n}')
    
    ax.text(label_x, E, label_text, fontsize=fontsize, ha=label_ha, 
           va='center', color=label_color, fontweight=fontweight)

# ============ DIBUJAR TRANSICIONES ============
nombres_lineas = ['Hα', 'Hβ', 'Hγ', 'Hδ', 'Hε']

for idx, (lam, n_s) in enumerate(zip(lambdas_exp, niveles_sup)):
    E_superior = energia_nivel(n_s)
    E_inferior = energia_nivel(n_inf)
    
    # Color según λ
    if lam > 620:
        trans_color, alpha, lw_arrow = '#DC143C', 0.85, 2.8
    elif lam > 480:
        trans_color, alpha, lw_arrow = '#4169E1', 0.80, 2.5
    elif lam > 430:
        trans_color, alpha, lw_arrow = '#000080', 0.75, 2.2
    elif lam > 405:
        trans_color, alpha, lw_arrow = '#8B00FF', 0.70, 2.0
    else:
        trans_color, alpha, lw_arrow = '#9370DB', 0.65, 1.7
    
    offset_x = (idx % 6 - 2.5) * 0.06
    
    # Flecha
    ax.annotate('', 
                xy=(x_pos - offset_x, E_inferior), 
                xytext=(x_pos + offset_x, E_superior),
                arrowprops=dict(arrowstyle='->', color=trans_color, 
                              alpha=alpha, lw=lw_arrow,
                              connectionstyle=f"arc3,rad={0.1*offset_x}"),
                zorder=3)

# ============ ETIQUETAS DE LAS PRINCIPALES LÍNEAS (MEJORADAS) ============
# Definir posiciones Y personalizadas para cada etiqueta
posiciones_etiquetas = [
    (0, -2.8),   # Hα: abajo del punto medio
    (1, -1.5),   # Hβ: arriba del punto medio
    (2, -1.0),   # Hγ: arriba
    (3, -0.6),   # Hδ: arriba
    (4, -0.35),  # Hε: arriba
]

for idx_etiq, y_offset in posiciones_etiquetas:
    if idx_etiq < len(lambdas_exp):
        lam = lambdas_exp[idx_etiq]
        n_s = niveles_sup[idx_etiq]
        E_superior = energia_nivel(n_s)
        E_inferior = energia_nivel(n_inf)
        
        # Posición Y de la etiqueta (ajustada manualmente)
        y_label = (E_superior + E_inferior) / 2 + y_offset
        
        # Color de la línea
        if lam > 620:
            trans_color = '#DC143C'
        elif lam > 480:
            trans_color = '#4169E1'
        elif lam > 430:
            trans_color = '#000080'
        elif lam > 405:
            trans_color = '#8B00FF'
        else:
            trans_color = '#9370DB'
        
        ax.text(x_pos + 1.3, y_label, 
               f'{nombres_lineas[idx_etiq]}\n{lam:.1f} nm', 
               fontsize=9, ha='left', va='center',
               bbox=dict(boxstyle='round,pad=0.4', 
                       facecolor='white', 
                       edgecolor=trans_color, 
                       linewidth=2, 
                       alpha=0.95),
               zorder=10)

# ============ DECORACIONES ============
ax.axhline(y=0, color='black', linestyle='--', linewidth=2.5, alpha=0.8, zorder=4)
ax.text(5.5, 0.2, 'Ionización (E = 0 eV)', fontsize=13, 
       fontweight='bold', style='italic', ha='right')

info = f'Niveles observados: n = {min(niveles_sup)} a {n_maximo}\n'
info += f'Total de transiciones: {len(lambdas_exp)}\n'
info += f'Rango λ: {min(lambdas_exp):.1f} - {max(lambdas_exp):.1f} nm'
ax.text(0.02, 0.98, info, transform=ax.transAxes, fontsize=10, 
       va='top', ha='left',
       bbox=dict(boxstyle='round,pad=0.6', 
               facecolor='wheat', 
               alpha=0.6, 
               edgecolor='black'))

ax.text(4.8, -13.0, 'Estado fundamental\n(n=1)', fontsize=12, ha='center',
       bbox=dict(boxstyle='round,pad=0.6', 
               facecolor='#FFB6C1', 
               alpha=0.5, 
               edgecolor='red', 
               linewidth=1.5))

ax.text(4.8, -3.0, 'Serie de Balmer\n(transiciones a n=2)', 
       fontsize=12, ha='center',
       bbox=dict(boxstyle='round,pad=0.6', 
               facecolor='#ADD8E6', 
               alpha=0.5, 
               edgecolor='blue', 
               linewidth=1.5))

# ============ CONFIGURACIÓN ============
ax.set_xlim(0.5, 6.5)
ax.set_ylim(-14.5, 1.0)
ax.set_ylabel('Energía (eV)', fontsize=16, fontweight='bold')
ax.set_title('Diagrama de Grotrian - Hidrógeno (H)\nSerie de Balmer (n→2)\nPráctica 5: Espectrometría Atómica', 
            fontsize=18, fontweight='bold', pad=25)

ax.grid(True, alpha=0.3, axis='y', linestyle=':', linewidth=1.2)
ax.set_xticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_linewidth(2)

plt.tight_layout()
plt.savefig('grotrian_hidrogeno_completo.png', dpi=300, bbox_inches='tight')
plt.savefig('grotrian_hidrogeno_completo.pdf', bbox_inches='tight')

print(f"\n{'='*60}")
print(f"✓ Diagrama guardado")
print(f"✓ Niveles: n=1 hasta n={n_maximo} ({len(todos_los_niveles)} niveles)")
print(f"✓ Transiciones: {len(lambdas_exp)}")
print(f"{'='*60}\n")

plt.show()
