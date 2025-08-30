import json
import logging
from src.utils import parse_date, format_date
from src.validation import validar_arquivo_json, validar_dados_completos

logger = logging.getLogger(__name__)

def carregar_dados_reais():
    """Carrega e valida dados reais do arquivo JSON."""
    try:
        dados = validar_arquivo_json('../data/dados_reais.json')
        
        # Garantir que data_inicio está no formato ISO
        if 'data_inicio' in dados:
            dados['data_inicio'] = format_date(dados['data_inicio'], "iso")
        
        logger.info("Dados carregados e validados com sucesso")
        return dados
        
    except Exception as e:
        logger.error(f"Erro crítico ao carregar dados: {e}")
        # Fallback para dados padrão validados
        return validar_dados_completos({})

def salvar_dados_reais(dados):
    """Salva dados reais no arquivo JSON com validação."""
    try:
        # Validar dados antes de salvar
        dados_validados = validar_dados_completos(dados)
        
        # Garantir formato ISO para data
        if 'data_inicio' in dados_validados:
            dados_validados['data_inicio'] = format_date(dados_validados['data_inicio'], "iso")
        
        with open('../data/dados_reais.json', 'w', encoding='utf-8') as f:
            json.dump(dados_validados, f, indent=2, ensure_ascii=False)
        
        logger.info("Dados salvos com sucesso")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao salvar dados: {e}")
        return False

def adicionar_registro_peso(peso: float, quadrante: int):
    """Adiciona um novo registro de peso ao histórico."""
    try:
        dados = carregar_dados_reais()
        
        # Inicializar histórico se não existir
        if 'historico_pesos' not in dados:
            dados['historico_pesos'] = []
        
        # Adicionar novo registro
        novo_registro = {
            'data': format_date(datetime.now(), "iso"),
            'peso': float(peso),
            'quadrante': int(quadrante)
        }
        
        # Validar o novo registro
        from src.validation import validar_objeto, HISTORICO_PESO_SCHEMA
        registro_validado = validar_objeto(novo_registro, HISTORICO_PESO_SCHEMA)
        
        dados['historico_pesos'].append(registro_validado)
        
        # Manter apenas os últimos 100 registros
        dados['historico_pesos'] = dados['historico_pesos'][-100:]
        
        return salvar_dados_reais(dados)
        
    except Exception as e:
        logger.error(f"Erro ao adicionar registro de peso: {e}")
        return False