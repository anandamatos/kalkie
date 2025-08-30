import json
from src.utils import parse_date, format_date

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
            
            # Garantir que data_inicio está no formato correto usando função unificada
            if 'data_inicio' in dados:
                try:
                    # Validar e formatar corretamente a data
                    dados['data_inicio'] = format_date(parse_date(dados['data_inicio']), "iso")
                except ValueError:
                    # Se falhar, usar data padrão
                    dados['data_inicio'] = dados_padrao['data_inicio']
            else:
                dados['data_inicio'] = dados_padrao['data_inicio']
                
            return dados
    except FileNotFoundError:
        return dados_padrao
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return dados_padrao

def salvar_dados_reais(dados):
    """Salva dados reais no arquivo JSON."""
    try:
        # Garantir formato ISO antes de salvar usando função unificada
        if 'data_inicio' in dados:
            dados['data_inicio'] = format_date(dados['data_inicio'], "iso")
        
        with open('../data/dados_reais.json', 'w') as f:
            json.dump(dados, f, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")
        return False