# src/quadrant_config.py
import numpy as np

def validar_configuracao_quadrantes(config):
    """Valida a configuração de quadrantes (movida para evitar ciclo de imports)."""
    required_keys = ['x_points', 'y_plan', 'dias_por_quadrante', 'data_inicio_padrao']
    
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Configuração inválida: falta chave '{key}'")
    
    if len(config['x_points']) != len(config['y_plan']):
        raise ValueError("x_points e y_plan devem ter o mesmo tamanho")
    
    if len(config['dias_por_quadrante']) != 15:
        raise ValueError("dias_por_quadrante deve ter 15 elementos")
    
    return True

def configurar_quadrantes():
    """Configura dias e metas por quadrante."""
    def f(x):
        return 0.6 * (10 ** (x / 14))
    
    x_points = np.arange(0, 15, 1)
    y_plan = f(x_points)
    
    # Ajustar soma total para ~43kg
    target_total = 43
    scale_factor = target_total / np.sum(y_plan[1:15])
    y_plan *= scale_factor
    y_plan[0] = 0  # Quadrante 0 = 0kg
    
    # Dias por quadrante (Q0 a Q14)
    dias_por_quadrante = [0]  # Q0
    for _ in range(1, 4): dias_por_quadrante.append(5)    # Q1-Q3: verde
    for _ in range(4, 8): dias_por_quadrante.append(7)    # Q4-Q7: azul
    for _ in range(8, 15): dias_por_quadrante.append(10)  # Q8-Q14: roxo
    
    return x_points, y_plan, dias_por_quadrante

def get_quadrant_config():
    """Retorna configuração unificada de quadrantes."""
    x_points, y_plan, dias_por_quadrante = configurar_quadrantes()
    
    config = {
        'x_points': x_points,
        'y_plan': y_plan,
        'dias_por_quadrante': dias_por_quadrante,
        'data_inicio_padrao': "2025-07-20"
    }
    
    # Validar configuração
    validar_configuracao_quadrantes(config)
    
    return config

# Manter compatibilidade com imports existentes
config = get_quadrant_config()
x_points = config['x_points']
y_plan = config['y_plan']
dias_por_quadrante = config['dias_por_quadrante']
data_inicio_padrao = config['data_inicio_padrao']