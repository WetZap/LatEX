import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# NIVELES DE ENERGÍA DEL HELIO (COMPLETO)
# ============================================================================
niveles = {
    # Sistema S=1 (Singlete)
    '1s': {'E': 0.0, 'x': 2.5, 'S': 1},
    '2s': {'E': 20.616, 'x': 1.0, 'S': 1},
    '2p': {'E': 21.218, 'x': 2.0, 'S': 1},
    '3s': {'E': 22.920, 'x': 3.0, 'S': 1},
    '3p': {'E': 23.087, 'x': 4.0, 'S': 1},
    '3d': {'E': 23.074, 'x': 5.0, 'S': 1},
    '4s': {'E': 23.674, 'x': 6.0, 'S': 1},
    '4p': {'E': 23.742, 'x': 7.0, 'S': 1},
    '4d': {'E': 23.736, 'x': 8.0, 'S': 1},
    '5s': {'E': 23.977, 'x': 9.0, 'S': 1},   # AÑADIDO
    '5d': {'E': 23.977, 'x': 10.0, 'S': 1},  # AÑADIDO
    
    # Sistema S=3 (Triplete)
    '2s_t': {'E': 19.820, 'x': 1.0, 'S': 3},
    '2p_t': {'E': 20.964, 'x': 2.0, 'S': 3},
    '3s_t': {'E': 22.718, 'x': 3.0, 'S': 3},
    '3p_t': {'E': 22.920, 'x': 4.0, 'S': 3},
    '3d_t': {'E': 23.007, 'x': 5.0, 'S': 3},
    '4s_t': {'E': 23.597, 'x': 6.0, 'S': 3},
    '4p_t': {'E': 23.672, 'x': 7.0, 'S': 3},
    '4d_t': {'E': 23.706, 'x': 8.0, 'S': 3},
    '5s_t': {'E': 23.927, 'x': 9.0, 'S': 3},   # AÑADIDO
    '5d_t': {'E': 23.977, 'x': 10.0, 'S': 3},  # AÑADIDO
}

# Transiciones CORREGIDAS
transiciones = [
    ('3p_t', '2s_t', 388.90),   # S=3: 1s3p³P → 1s2s³S
    ('4p', '2s', 396.90),        # S=1: 1s4p¹P → 1s2s¹S
    ('5d_t', '2p_t', 403.10),    # S=3: 1s5d³D → 1s2p³P
    ('5s_t', '2p_t', 411.90),    # S=3: 1s5s³S → 1s2p³P
    ('5d', '2p', 439.20),        # S=1: 1s5d¹D → 1s2p¹P
    ('4d_t', '2p_t', 447.20),    # S=3: 1s4d³D → 1s2p³P
    ('4s_t', '2p_t', 471.10),    # S=3: 1s4s³S → 1s2p³P
    ('4d', '2p', 492.40),        # S=1: 1s4d¹D → 1s2p¹P
    ('3p', '2s', 501.30),        # S=1: 1s3p¹P → 1s2s¹S
    ('4s', '2p', 504.80),        # S=1: 1s4s¹S → 1s2p¹P
    ('3d_t', '2p_t', 587.40),    # S=3: 1s3d³D → 1s2p³P
    ('3d', '2p', 667.50),        # S=1: 1s3d¹D → 1s2p¹P
    ('3s_t', '2p_t', 706.60),    # S=3: 1s3s³S → 1s2p³P
    ('3s', '2p', 728.00),        # S=1: 1s3s¹S → 1s2p¹P
]

# ============================================================================
# CREAR DIAGRAMA DE GROTRIAN
# ============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 11), sharey=True)

for ax, S_val, color, title in [(ax1, 1, 'blue', 'S = 1 (Singlete)'),
                                  (ax2, 3, 'red', 'S = 3 (Triplete)')]:
    
    # Título
    ax.text(5.5, 24.3, title, fontsize=15, ha='center', 
           fontweight='bold', color=color,
           bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.3))
    
    # Dibujar niveles
    niveles_sistema = {k: v for k, v in niveles.items() if v['S'] == S_val}
    
    for nombre, datos in niveles_sistema.items():
        E = datos['E']
        x = datos['x']
        
        ax.plot([x-0.35, x+0.35], [E, E], color=color, linewidth=2.5)
        
        label = nombre.replace('_t', '')
        if 's' in label:
            ax.text(x-0.45, E, label, fontsize=9, ha='right', va='center', fontweight='bold')
        else:
            ax.text(x+0.45, E, label, fontsize=9, ha='left', va='center', fontweight='bold')
    
    # Dibujar transiciones
    for superior, inferior, wavelength in transiciones:
        if superior in niveles and inferior in niveles:
            if niveles[superior]['S'] == S_val:
                x_sup = niveles[superior]['x']
                x_inf = niveles[inferior]['x']
                E_sup = niveles[superior]['E']
                E_inf = niveles[inferior]['E']
                
                ax.annotate('', xy=(x_inf, E_inf), xytext=(x_sup, E_sup),
                           arrowprops=dict(arrowstyle='->', color=color, 
                                         alpha=0.6, lw=1.5))
                
                mid_x = (x_sup + x_inf) / 2
                mid_y = (E_sup + E_inf) / 2
                
                ax.text(mid_x, mid_y, f'{wavelength:.1f}', 
                       fontsize=7, ha='center',
                       bbox=dict(boxstyle='round,pad=0.2', 
                               facecolor='white', alpha=0.85, edgecolor='none'))
    
    ax.set_xlim(0, 11)
    ax.set_ylim(-1, 24.7)
    ax.grid(True, alpha=0.2, axis='y')
    ax.set_xticks([])
    ax.axhline(y=24.587, color='black', linestyle='--', linewidth=1, alpha=0.5)

ax1.set_ylabel('Energía (eV)', fontsize=14, fontweight='bold')
fig.suptitle('Diagrama de Grotrian - Helio (He I)\nPráctica 5: Espectrometría Atómica', 
            fontsize=16, fontweight='bold', y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('grotrian_helio_practica5.png', dpi=300, bbox_inches='tight')
plt.savefig('grotrian_helio_practica5.pdf', bbox_inches='tight')
print("\n✓ Diagrama corregido guardado")
print(f"✓ Total de transiciones: {len(transiciones)}")
plt.show()
# ============================================================================