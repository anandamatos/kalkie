import json
import logging
import os
from datetime import datetime
from src.utils import parse_date, format_date
from src.validation import validar_arquivo_json, validar_dados_completos

logger = logging.getLogger(__name__)

# Caminhos absolutos relativos ao projeto (evita problemas com caminhos relativos a src)
ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(ROOT, 'data', 'dados_reais.json')


def carregar_dados_reais():
    """Carrega e valida dados reais do arquivo JSON."""
    try:
        dados = validar_arquivo_json(DATA_PATH)

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

        # Garantir diretório existe
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

        with open(DATA_PATH, 'w', encoding='utf-8') as f:
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


def limpar_dados_reais():
    """Limpa os dados de evolução mantendo apenas a configuração básica.
    Usado após setup para reiniciar do Q0."""
    try:
        dados = carregar_dados_reais()
        dados_antigos = dados.copy()
        
        # Criar backup se as datas mudaram (novo período)
        if (dados.get('data_inicio') != dados_antigos.get('data_inicio') or 
            dados.get('data_fim') != dados_antigos.get('data_fim')):
            
            # Criar nome do backup com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = os.path.join(ROOT, 'data', 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            # Salvar dados antigos como backup
            backup_path = os.path.join(backup_dir, f'{timestamp}_dados_reais.json')
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(dados_antigos, f, indent=2, ensure_ascii=False)
            
            # Também fazer backup da configuração
            config_path = os.path.join(ROOT, 'data', 'config.json')
            if os.path.exists(config_path):
                backup_config = os.path.join(backup_dir, f'{timestamp}_config.json')
                with open(config_path, 'r', encoding='utf-8') as f_src:
                    with open(backup_config, 'w', encoding='utf-8') as f_dst:
                        json.dump(json.load(f_src), f_dst, indent=2, ensure_ascii=False)
            
            logger.info(f"Backup criado: {backup_path}")
        
        # Sempre limpar dados ao fazer setup
        # Use pelo menos um valor em 'dados_reais' (0) para satisfazer validação
        dados_base = {
            'peso_inicial': dados.get('peso_inicial', 0),
            'data_inicio': dados.get('data_inicio', ''),
            'data_fim': dados.get('data_fim', ''),
            'target_total': dados.get('target_total', 0),
            'dados_reais': [0],  # Começar do Q0 com 0kg registrado
            'quadrante_atual': 0,
            'historico_pesos': []  # Limpar histórico de pesos também
        }

        # Salvar dados limpos (fará validação). Também garante que
        # o arquivo final reflita o novo período iniciando em Q0.
        return salvar_dados_reais(dados_base)
    except Exception as e:
        logger.error(f"Erro ao limpar dados: {e}")
        return False

def registrar_peso_evolucao(peso: float):
    """Registra um novo valor de perda/variação para a lista 'dados_reais'.

    O arquivo `dados_reais.json` mantém a lista `dados_reais` com as perdas (ou variações)
    por quadrante. Esta função carrega o JSON, adiciona o valor e salva.
    """
    try:
        dados = carregar_dados_reais()
        if 'dados_reais' not in dados or not isinstance(dados['dados_reais'], list):
            dados['dados_reais'] = []

        # Armazenar valor numérico (float)
        dados['dados_reais'].append(float(peso))

        return salvar_dados_reais(dados)
    except Exception as e:
        logger.error(f"Erro ao registrar peso de evolução: {e}")
        return False