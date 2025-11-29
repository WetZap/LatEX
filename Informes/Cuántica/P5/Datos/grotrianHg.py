import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# DATOS DEL MERCURIO - Práctica 5
# ============================================================================

# Configuración electrónica base: [Xe]4f¹⁴5d¹⁰ (simplificada como estado base)
# Estados relevantes para el espectro visible

# Niveles de energía del Hg (en eV, relativos al estado fundamental 6s²)
niveles = {
    # Estado fundamental
    '6s² ¹S₀': {'E': 0.0, 'x': 2.0, 'config': '6s²'},
    
    # Configuración 6s6p
    '6s6p ³P₀': {'E': 4.667, 'x': 1.0, 'config': '6s6p'},
    '6s6p ³P₁': {'E': 4.887, 'x': 2.0, 'config': '6s6p'},
    '6s6p ³P₂': {'E': 5.461, 'x': 3.0, 'config': '6s6p'},
    '6s6p ¹P₁': {'E': 6.704, 'x': 4.0, 'config': '6s6p'},
    
    # Configuración 6s7s
    '6s7s ³S₁': {'E': 7.731, 'x': 5.0, 'config': '6s7s'},
    '6s7s ¹S₀': {'E': 7.926, 'x': 6.0, 'config': '6s7s'},
    
    # Configuración 6s6d
    '6s6d ¹D₂': {'E': 8.844, 'x': 7.0, 'config': '6s6d'},
    '6s6d ³D₁': {'E': 8.845, 'x': 8.0, 'config': '6s6d'},
    '6s6d ³D₂': {'E': 8.852, 'x': 9.0, 'config': '6s6d'},
    '6s6d ³D₃': {'E': 8.856, 'x': 10.0, 'config': '6s6d'},
}

# Transiciones del visible (de la Tabla del manual)
transiciones = [
    ('6s6d ³D₃', '6s6p ³P₂', 365.016, 9000, 'violeta'),
    ('6s6d ³D₂', '6s6p ³P₂', 365.484, 3000, 'violeta'),
    ('6s6d ³D₁', '6s6p ³P₂', 366.289, 500, 'violeta'),
    ('6s7s ³S₁', '6s6p ³P₀', 404.656, 12000, 'violeta'),
    ('6s7s ¹S₀', '6s6p ³P₁', 407.783, 1000, 'violeta'),
    ('6s7s ³S₁', '6s6p ³P₁', 435.834, 12000, 'azul'),
    ('6s7s ³S₁', '6s6p ³P₂', 546.075, 6000, 'verde'),
    ('6s6d ³D₂', '6s6p ¹P₁', 576.961, 1000, 'amarillo'),
    ('6s6d ¹D₂', '6s6p ¹P₁', 579.067, 900, 'amarillo'),
]

# Colores para las transiciones
color_map = {
    'violeta': '#8B00FF',
    'azul': '#0000FF',
    'verde': '#00FF00',
    'amarillo': '#FFD700'
}

# ============================================================================
# CREAR DIAGRAMA DE GROTRIAN
# ============================================================================

fig, ax = plt.subplots(figsize=(16, 11))

# Dibujar niveles de energía
for nombre, datos in niveles.items():
    E = datos['E']
    x = datos['x']
    
    # Color según configuración
    if '6s²' in nombre:
        color = 'black'
        lw = 3
    elif '6s6p' in nombre:
        color = 'blue'
        lw = 2.5
    elif '6s7s' in nombre:
        color = 'red'
        lw = 2.5
    elif '6s6d' in nombre:
        color = 'green'
        lw = 2.5
    else:
        color = 'gray'
        lw = 2
    
    # Línea del nivel
    ax.plot([x-0.4, x+0.4], [E, E], color=color, linewidth=lw)
    
    # Etiqueta del nivel
    label = nombre.replace('6s6p ', '').replace('6s7s ', '').replace('6s6d ', '').replace('6s² ', '')
    ax.text(x+0.5, E, label, fontsize=9, va='center', fontweight='bold')

# Dibujar transiciones
for superior, inferior, wavelength, intensidad, color_trans in transiciones:
    if superior in niveles and inferior in niveles:
        x_sup = niveles[superior]['x']
        x_inf = niveles[inferior]['x']
        E_sup = niveles[superior]['E']
        E_inf = niveles[inferior]['E']
        
        # Grosor según intensidad
        alpha = min(0.8, 0.3 + (intensidad / 12000) * 0.5)
        lw = min(2.5, 0.8 + (intensidad / 12000) * 1.7)
        
        # Color de la transición según el color de la luz
        trans_color = color_map.get(color_trans, 'gray')
        
        # Dibujar flecha
        ax.annotate('', xy=(x_inf, E_inf), xytext=(x_sup, E_sup),
                   arrowprops=dict(arrowstyle='->', color=trans_color, 
                                 alpha=alpha, lw=lw))
        
        # Etiqueta de longitud de onda
        mid_x = (x_sup + x_inf) / 2
        mid_y = (E_sup + E_inf) / 2
        
        ax.text(mid_x-0.2, mid_y, f'{wavelength:.1f}', 
               fontsize=7, ha='center',
               bbox=dict(boxstyle='round,pad=0.2', 
                       facecolor='white', alpha=0.85, edgecolor='none'))

# Etiquetas de configuración
ax.text(2.0, -0.7, '6s²', fontsize=12, ha='center', fontweight='bold', color='black')
ax.text(2.5, 6.0, '6s6p', fontsize=12, ha='center', fontweight='bold', color='blue')
ax.text(5.5, 8.2, '6s7s', fontsize=12, ha='center', fontweight='bold', color='red')
ax.text(8.5, 9.2, '6s6d', fontsize=12, ha='center', fontweight='bold', color='green')

# Configuración del gráfico
ax.set_xlim(-0.5, 11)
ax.set_ylim(-1, 9.5)
ax.set_ylabel('Energía (eV)', fontsize=14, fontweight='bold')
ax.set_title('Diagrama de Grotrian - Mercurio (Hg)\nPráctica 5: Espectrometría Atómica', 
            fontsize=16, fontweight='bold', pad=20)

# Leyenda de colores
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=color_map['violeta'], label='Violeta (365-408 nm)'),
    Patch(facecolor=color_map['azul'], label='Azul (435.8 nm)'),
    Patch(facecolor=color_map['verde'], label='Verde (546.1 nm)'),
    Patch(facecolor=color_map['amarillo'], label='Amarillo (577-579 nm)')
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10)

# Grid
ax.grid(True, alpha=0.25, axis='y', linestyle=':')
ax.set_xticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)

plt.tight_layout()

for _, _, wl, _, color in transiciones:
    print(f"  {wl:.1f} nm ({color})")
plt.show()
# ============================================================================