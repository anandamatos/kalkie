from datetime import datetime, timedelta
import numpy as np

def arredondar_500(valor):
    """Arredonda valor para o múltiplo de 500 mais próximo."""
    return round(valor / 500) * 500

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

def parse_date(date_input):
    """
    Converte input para datetime de forma segura.
    Aceita: datetime, string no formato YYYY-MM-DD, ou string no formato DD/MM/YYYY
    """
    if isinstance(date_input, datetime):
        return date_input
    
    if isinstance(date_input, str):
        # Tentar formato YYYY-MM-DD (padrão ISO)
        try:
            return datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            pass
        
        # Tentar formato DD/MM/YYYY
        try:
            return datetime.strptime(date_input, "%d/%m/%Y")
        except ValueError:
            pass
        
        # Tentar formato DD/MM/YY
        try:
            return datetime.strptime(date_input, "%d/%m/%y")
        except ValueError:
            pass
    
    raise ValueError(f"Formato de data não suportado: {date_input}")

def format_date(date_obj, format_type="iso"):
    """
    Formata datetime para string.
    format_type: "iso" (YYYY-MM-DD), "display" (DD/MM/YYYY), "short" (DD/MM/YY)
    """
    if not isinstance(date_obj, datetime):
        date_obj = parse_date(date_obj)
    
    if format_type == "iso":
        return date_obj.strftime("%Y-%m-%d")
    elif format_type == "display":
        return date_obj.strftime("%d/%m/%Y")
    elif format_type == "short":
        return date_obj.strftime("%d/%m/%y")
    else:
        raise ValueError("Tipo de formato inválido")

def calcular_data_inicio_quadrante(data_inicio, quadrante, dias_por_quadrante):
    """
    Calcula a data de início correta para cada quadrante.
    """
    data_inicio = parse_date(data_inicio)
    
    # Calcular dias acumulados até o início do quadrante
    dias_acumulados = sum(dias_por_quadrante[1:quadrante])
    return data_inicio + timedelta(days=dias_acumulados)

def gerar_datas_periodo(data_inicio, dias):
    """
    Gera lista de datas para um período.
    Retorna lista de datetime objects.
    """
    data_inicio = parse_date(data_inicio)
    return [data_inicio + timedelta(days=i) for i in range(dias)]

def obter_dia_semana_ptbr(data_obj):
    """
    Retorna o dia da semana em português.
    """
    if not isinstance(data_obj, datetime):
        data_obj = parse_date(data_obj)
    
    dias_semana = {
        0: "segunda", 1: "terça", 2: "quarta", 
        3: "quinta", 4: "sexta", 5: "sábado", 6: "domingo"
    }
    return dias_semana[data_obj.weekday()]

def data_hoje():
    """Retorna a data atual como datetime."""
    return datetime.now()

def diferenca_dias(data1, data2):
    """Calcula diferença em dias entre duas datas."""
    data1 = parse_date(data1)
    data2 = parse_date(data2)
    return (data2 - data1).days
