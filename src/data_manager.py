import json
from src.utils import parse_date, format_date  # ← ADICIONAR import

def carregar_dados_reais():
    """Carrega dados reais do arquivo JSON."""
    dados_padrao = {
        "peso_inicial": 112.4,
        "dados_reais": [0, 1.7, -1.3, 2, -1.1, 2.8, -0.7],
        "quadrante_atual": 6,
        "data_inicio": "2025-07-20"  # ← Manter como string ISO
    }
    
    try:
        with open('../data/dados_reais.json', 'r') as f:
            dados = json.load(f)
            if len(dados["dados_reais"]) < 7:
                dados["dados_reais"] = dados_padrao["dados_reais"]
            
            # Garantir que data_inicio está no formato correto
            if 'data_inicio' in dados:
                dados['data_inicio'] = format_date(dados['data_inicio'], "iso")
            else:
                dados['data_inicio'] = dados_padrao['data_inicio']
                
            return dados
    except FileNotFoundError:
        return dados_padrao

def salvar_dados_reais(dados):
    """Salva dados reais no arquivo JSON."""
    # Garantir formato ISO antes de salvar
    dados['data_inicio'] = format_date(dados['data_inicio'], "iso")
    
    with open('../data/dados_reais.json', 'w') as f:
        json.dump(dados, f, indent=2)