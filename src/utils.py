# src/utils.py
from datetime import datetime, timedelta
import numpy as np

def arredondar_500(valor):
    """Arredonda valor para o múltiplo de 500 mais próximo."""
    return round(valor / 500) * 500

def parse_date(date_string):
    """Converte string para datetime de forma segura."""
    if isinstance(date_string, datetime):
        return date_string
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except (ValueError, TypeError):
        return datetime.now()

def calcular_dias_entre_datas(data_inicio, data_fim):
    """Calcula diferença em dias entre duas datas."""
    inicio = parse_date(data_inicio)
    fim = parse_date(data_fim)
    return (fim - inicio).days

def validar_configuracao_quadrantes(config):
    """Valida a configuração de quadrantes."""
    required_keys = ['x_points', 'y_plan', 'dias_por_quadrante', 'data_inicio_padrao']
    
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Configuração inválida: falta chave '{key}'")
    
    if len(config['x_points']) != len(config['y_plan']):
        raise ValueError("x_points e y_plan devem ter o mesmo tamanho")
    
    if len(config['dias_por_quadrante']) != 15:
        raise ValueError("dias_por_quadrante deve ter 15 elementos")
    
    return True