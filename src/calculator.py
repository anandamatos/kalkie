import numpy as np
from src.data_manager import carregar_dados_reais
from src.quadrant_config import y_plan

def arredondar_500(valor):
    return round(valor / 500) * 500

def calcular_desvio_acumulado(quadrante_atual):
    """Calcula o desvio acumulado com base nos dados reais."""
    try:
        dados = carregar_dados_reais()
        dados_reais = dados["dados_reais"]
        
        # Calcular perda real acumulada
        perda_real_acumulada = sum(dados_reais)
        
        # Calcular perda planejada acumulada até o quadrante atual
        # Garantir que o slice está dentro dos limites
        end_index = min(quadrante_atual + 1, len(y_plan))
        perda_planejada_acumulada = np.sum(y_plan[1:end_index])
        
        # Calcular desvio (diferença entre planejado e realizado)
        desvio = perda_planejada_acumulada - perda_real_acumulada
        return desvio
        
    except Exception as e:
        print(f"Erro ao calcular desvio: {e}")
        return 0  # Retorna 0 em caso de erro

def calcular_meta_proximo_quadrante(quadrante_atual):
    """Calcula a meta necessária para o próximo quadrante."""
    # Calcular desvio acumulado
    desvio = calcular_desvio_acumulado(quadrante_atual)
    
    # Converter explicitamente para float
    desvio = float(desvio) if desvio is not None else 0.0
    
    # Meta planejada para o próximo quadrante
    if quadrante_atual + 1 < len(y_plan):
        meta_planejada = float(y_plan[quadrante_atual + 1])
    else:
        meta_planejada = float(y_plan[-1])
    
    # Meta ajustada = planejada + desvio acumulado
    meta_ajustada = meta_planejada + desvio
    
    return max(0.1, meta_ajustada)