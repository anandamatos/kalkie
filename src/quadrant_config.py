import json
import os
import numpy as np  # ← ADICIONAR ESTA LINHA
from src.utils import validar_configuracao_quadrantes  # ← CORRIGIDO


def configurar_quadrantes(config_override=None, total_quadrants=15):
    """Configura dias e metas por quadrante.

    total_quadrants: número total de pontos (ex.: 15 -> Q0..Q14)
    """
    def f(x, denom):
        # denom = total_quadrants - 1 (ex.: 14 para 15 pontos)
        return 0.6 * (10 ** (x / denom))
    
    if total_quadrants < 2:
        total_quadrants = 15
    denom = max(1, total_quadrants - 1)
    x_points = np.arange(0, total_quadrants, 1)
    y_plan = f(x_points, denom)
    
    # Ajustar soma total para ~43kg
    target_total = 43
    scale_factor = target_total / np.sum(y_plan[1:total_quadrants])
    y_plan *= scale_factor
    y_plan[0] = 0  # Quadrante 0 = 0kg
    
    # Dias por quadrante (Q0 a Qn) - valores padrão
    dias_por_quadrante = [0]  # Q0
    # padrão: 3 fases (5,7,10) replicadas conforme necessário
    # preencher até total_quadrants
    i = 1
    # Q1-Q3: 5 dias
    while i < min(4, total_quadrants):
        dias_por_quadrante.append(5)
        i += 1
    # Q4-Q7: 7 dias
    while i < min(8, total_quadrants):
        dias_por_quadrante.append(7)
        i += 1
    # resto: 10 dias
    while i < total_quadrants:
        dias_por_quadrante.append(10)
        i += 1

    # Aplicar overrides se existirem
    if config_override:
        if 'dias_por_quadrante' in config_override:
            dias = config_override['dias_por_quadrante']
            # validar tamanho e converter se necessário
            if isinstance(dias, list) and len(dias) == total_quadrants:
                dias_por_quadrante = dias

        # permitir alterar target_total via override (aplicado na função chamadora)

    return x_points, y_plan, dias_por_quadrante

def _load_config_file():
    """Tenta carregar overrides a partir de data/config.json (relativo a src)."""
    root = os.path.dirname(os.path.dirname(__file__))
    cfg_path = os.path.join(root, 'data', 'config.json')
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    return None


def get_quadrant_config():
    """Retorna configuração unificada de quadrantes. Lê overrides de data/config.json quando existir."""
    cfg_overrides = _load_config_file()

    # determinar total_quadrants a partir de overrides (fallback 15)
    total_quadrants = 15
    if cfg_overrides and 'total_quadrants' in cfg_overrides:
        try:
            total_quadrants = int(cfg_overrides['total_quadrants'])
        except Exception:
            total_quadrants = 15

    x_points, y_plan, dias_por_quadrante = configurar_quadrantes(config_override=cfg_overrides, total_quadrants=total_quadrants)

    # Defaults
    data_inicio_padrao = "2025-07-20"
    target_total = 43

    # Aplicar overrides básicos
    if cfg_overrides:
        if 'data_inicio_padrao' in cfg_overrides:
            data_inicio_padrao = cfg_overrides['data_inicio_padrao']
        if 'target_total' in cfg_overrides:
            target_total = cfg_overrides['target_total']

    # Re-escala y_plan caso target_total tenha sido sobrescrito
    if target_total != 43:
        # recalcular scale_factor com o novo target_total
        scale_factor = target_total / np.sum(y_plan[1:len(y_plan)])
        y_plan = y_plan * scale_factor
        y_plan[0] = 0

    config = {
        'x_points': x_points,
        'y_plan': y_plan,
        'dias_por_quadrante': dias_por_quadrante,
        'data_inicio_padrao': data_inicio_padrao,
        'target_total': target_total
    }

    # Validar configuração
    validar_configuracao_quadrantes(config)

    return config


# Manter compatibilidade com imports existentes (módulos que importam nomes antigos)
config = get_quadrant_config()
x_points = config['x_points']
y_plan = config['y_plan']
dias_por_quadrante = config['dias_por_quadrante']
data_inicio_padrao = config['data_inicio_padrao']