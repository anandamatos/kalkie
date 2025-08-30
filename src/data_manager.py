import json
from datetime import datetime

def carregar_dados_reais():
    """Carrega dados reais do arquivo JSON."""
    dados_padrao = {
        "peso_inicial": 112.4,
        "dados_reais": [0, 1.7, -1.3, 2, -1.1, 2.8, -0.7],
        "quadrante_atual": 6,
        "data_inicio": "2025-07-20"
    }
    
    try:
        with open('../data/dados_reais.json', 'r') as f:
            dados = json.load(f)
            if len(dados["dados_reais"]) < 7:
                dados["dados_reais"] = dados_padrao["dados_reais"]
            return dados
    except FileNotFoundError:
        return dados_padrao