import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

# ============================================================================
# DATOS EXPERIMENTALES DE LONGITUDES DE ONDA (TUS VALORES)
# ============================================================================
lambdas_observadas = [388.90, 396.90, 403.10, 411.90, 439.20, 447.20, 471.10,
                      492.40, 501.30, 504.80, 587.40, 667.50, 706.60, 728.00]

# ============================================================================
# NIVELES DE ENERGÍA DEL HELIO (eV, relativos al fundamental)
# ============================================================================
niveles = {
    # Sistema S=1 (Singlete, multiplicidad = 1)
    '1s': {'E': 0.0, 'x': 2.5, 'S': 1},
    '2s': {'E': 20.616, 'x': 1.0, 'S': 1},
    '2p': {'E': 21.218, 'x': 2.0, 'S': 1},
    '3s': {'E': 22.920, 'x': 3.0, 'S': 1},
    '3p': {'E': 23.087, 'x': 4.0, 'S': 1},
    '3d': {'E': 23.074, 'x': 5.0, 'S': 1},
    '4s': {'E': 23.674, 'x': 6.0, 'S': 1},
    '4p': {'E': 23.742, 'x': 7.0, 'S': 1},
    '4d': {'E': 23.736, 'x': 8.0, 'S': 1},
    
    # Sistema S=3 (Triplete, multiplicidad = 3)
    '2s_t': {'E': 19.820, 'x': 1.0, 'S': 3},
    '2p_t': {'E': 20.964, 'x': 2.0, 'S': 3},
    '3s_t': {'E': 22.718, 'x': 3.0, 'S': 3},
    '3p_t': {'E': 22.920, 'x': 4.0, 'S': 3},
    '3d_t': {'E': 23.007, 'x': 5.0, 'S': 3},
    '4s_t': {'E': 23.597, 'x': 6.0, 'S': 3},
    '4p_t': {'E': 23.672, 'x': 7.0, 'S': 3},
    '4d_t': {'E': 23.706, 'x': 8.0, 'S': 3},
}

# Transiciones observadas (superior, inferior, lambda experimental)
transiciones = [
    ('3p_t', '2s_t', 388.90),   # S=3
    ('4p', '2s', 396.90),        # S=1
    ('4d_t', '2p_t', 403.10),    # S=3 (aprox)
    ('4s_t', '2p_t', 411.90),    # S=3 (aprox)
    ('4d', '2p', 439.20),        # S=1
    ('4d_t', '2p_t', 447.20),    # S=3
    ('4s_t', '2p_t', 471.10),    # S=3
    ('4d', '2p', 492.40),        # S=1
    ('3p', '2s', 501.30),        # S=1
    ('4s', '2p', 504.80),        # S=1
    ('3d_t', '2p_t', 587.40),    # S=3
    ('3d', '2p', 667.50),        # S=1
    ('3s_t', '2p_t', 706.60),    # S=3
    ('3s', '2p', 728.00),        # S=1
]

# ============================================================================
# CREAR DIAGRAMA DE GROTRIAN (ESTILO DE LA IMAGEN)
# ============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 10), sharey=True)

# Configurar subplots
for ax, S_val, color, title in [(ax1, 1, 'blue', 'S = 1'),
                                  (ax2, 3, 'red', 'S = 3')]:
    
    # Título del sistema
    ax.text(4.5, 24.2, title, fontsize=16, ha='center', 
           fontweight='bold', color=color,
           bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.3))
    
    # Dibujar niveles
    niveles_sistema = {k: v for k, v in niveles.items() if v['S'] == S_val}
    
    for nombre, datos in niveles_sistema.items():
        E = datos['E']
        x = datos['x']
        
        # Línea horizontal del nivel
        ax.plot([x-0.3, x+0.3], [E, E], color=color, linewidth=2.5)
        
        # Etiqueta del nivel
        label = nombre.replace('_t', '')
        
        # Posicionar etiqueta según si es s, p, o d
        if 's' in label:
            ax.text(x-0.5, E, label, fontsize=10, ha='right', va='center', fontweight='bold')
        else:
            ax.text(x+0.5, E, label, fontsize=10, ha='left', va='center', fontweight='bold')
    
    # Dibujar transiciones para este sistema
    for superior, inferior, wavelength in transiciones:
        if superior in niveles and inferior in niveles:
            if niveles[superior]['S'] == S_val:
                x_sup = niveles[superior]['x']
                x_inf = niveles[inferior]['x']
                E_sup = niveles[superior]['E']
                E_inf = niveles[inferior]['E']
                
                # Flecha de transición
                ax.annotate('', xy=(x_inf, E_inf), xytext=(x_sup, E_sup),
                           arrowprops=dict(arrowstyle='->', color=color, 
                                         alpha=0.6, lw=1.5))
                
                # Etiqueta de longitud de onda
                mid_x = (x_sup + x_inf) / 2
                mid_y = (E_sup + E_inf) / 2
                
                ax.text(mid_x, mid_y, f'{wavelength:.1f}nm', 
                       fontsize=7, ha='center', rotation=0,
                       bbox=dict(boxstyle='round,pad=0.2', 
                               facecolor='white', alpha=0.8, edgecolor='none'))
    
    # Configuración de ejes
    ax.set_xlim(0, 9)
    ax.set_ylim(-1, 24.5)
    ax.set_xlabel('', fontsize=12)
    ax.grid(True, alpha=0.2, axis='y')
    ax.set_xticks([])

# Etiqueta Y solo en el primer subplot
ax1.set_ylabel('Energy (eV)', fontsize=14, fontweight='bold')

# Título general
fig.suptitle('Diagrama de Grotrian - Helio (He I)\nPráctica 5: Espectrometría Atómica', 
            fontsize=16, fontweight='bold', y=0.98)

# Línea de ionización
for ax in [ax1, ax2]:
    ax.axhline(y=24.587, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax.text(8.5, 24.587, 'Ionización', fontsize=8, va='bottom', ha='right', style='italic')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('grotrian_helio_practica5.png', dpi=300, bbox_inches='tight')
plt.savefig('grotrian_helio_practica5.pdf', bbox_inches='tight')
print("\n✓ Diagrama de Grotrian guardado exitosamente")
print(f"✓ Transiciones graficadas: {len(transiciones)}")
print(f"✓ Longitudes de onda: {lambdas_observadas}")
plt.show()
