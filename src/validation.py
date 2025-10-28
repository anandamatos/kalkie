# src/validation.py
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from src.utils import parse_date, format_date

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Schema completo para dados.json
DADOS_SCHEMA = {
    "peso_inicial": {
        "type": float,
        "required": True,
        "min": 50.0,
        "max": 200.0,
        "default": 112.4
    },
    "dados_reais": {
        "type": list,
        "required": True,
        "item_type": float,
        "min_length": 1,
        "max_length": 15,
        "default": [0, 1.7, -1.3, 2, -1.1, 2.8, -0.7]
    },
    "quadrante_atual": {
        "type": int,
        "required": True,
        "min": 0,
        "max": 14,
        "default": 6
    },
    "data_inicio": {
        "type": str,
        "required": True,
        "format": "date",  # YYYY-MM-DD
        "default": "2025-07-20"
    },
    "historico_pesos": {
        "type": list,
        "required": False,
        "item_type": dict,
        "default": []
    }
}

# Schema para itens do histórico de pesos
HISTORICO_PESO_SCHEMA = {
    "data": {"type": str, "required": True, "format": "date"},
    "peso": {"type": float, "required": True, "min": 50.0, "max": 200.0},
    "quadrante": {"type": int, "required": True, "min": 0, "max": 14}
}

def validar_tipo(valor, tipo_esperado, campo: str) -> bool:
    """Valida se o valor é do tipo esperado."""
    if tipo_esperado == float:
        # Aceita tanto float quanto int para campos numéricos
        if not isinstance(valor, (float, int)):
            logger.warning(f"Campo {campo}: Valor {valor} não é numérico")
            return False
    elif not isinstance(valor, tipo_esperado):
        logger.warning(f"Campo {campo}: Valor {valor} não é do tipo {tipo_esperado.__name__}")
        return False
    return True

def validar_numero(valor, campo: str, min_val: Optional[float] = None, max_val: Optional[float] = None) -> bool:
    """Validações para campos numéricos."""
    if min_val is not None and valor < min_val:
        logger.warning(f"Campo {campo}: Valor {valor} abaixo do mínimo permitido ({min_val})")
        return False
    if max_val is not None and valor > max_val:
        logger.warning(f"Campo {campo}: Valor {valor} acima do máximo permitido ({max_val})")
        return False
    return True

def validar_data_string(data_str: str, campo: str) -> bool:
    """Valida se a string está no formato de data correto."""
    try:
        parse_date(data_str)
        return True
    except ValueError:
        logger.warning(f"Campo {campo}: Data {data_str} em formato inválido")
        return False

def validar_lista(lista: List, campo: str, item_type: type, min_length: int = 0, max_length: Optional[int] = None) -> bool:
    """Validações para listas."""
    if not isinstance(lista, list):
        logger.warning(f"Campo {campo}: Não é uma lista")
        return False
    
    if len(lista) < min_length:
        logger.warning(f"Campo {campo}: Lista com apenas {len(lista)} itens (mínimo: {min_length})")
        return False
    
    if max_length is not None and len(lista) > max_length:
        logger.warning(f"Campo {campo}: Lista com {len(lista)} itens (máximo: {max_length})")
        return False
    
    for i, item in enumerate(lista):
        if not validar_tipo(item, item_type, f"{campo}[{i}]"):
            return False
    
    return True

def validar_objeto(objeto: Dict, schema: Dict, contexto: str = "") -> Dict:
    """
    Valida um objeto completo contra um schema.
    Retorna o objeto validado e corrigido.
    """
    resultado = {}
    erros = []
    
    for campo, config in schema.items():
        valor = objeto.get(campo)
        
        # Verificar se campo é obrigatório
        if config["required"] and valor is None:
            if "default" in config:
                resultado[campo] = config["default"]
                logger.info(f"Campo {contexto}{campo}: Usando valor padrão {config['default']}")
            else:
                erros.append(f"Campo obrigatório {contexto}{campo} faltando")
                continue
        elif valor is None:
            # Campo opcional não presente
            continue
        
        # Validar tipo
        if not validar_tipo(valor, config["type"], f"{contexto}{campo}"):
            if "default" in config:
                resultado[campo] = config["default"]
                logger.info(f"Campo {contexto}{campo}: Tipo inválido, usando padrão {config['default']}")
            else:
                erros.append(f"Tipo inválido para {contexto}{campo}")
            continue
        
        # Validações específicas por tipo
        if config["type"] in (int, float):
            if not validar_numero(valor, f"{contexto}{campo}", config.get("min"), config.get("max")):
                if "default" in config:
                    resultado[campo] = config["default"]
                    logger.info(f"Campo {contexto}{campo}: Valor inválido, usando padrão {config['default']}")
                else:
                    erros.append(f"Valor inválido para {contexto}{campo}")
                continue
        
        elif config["type"] == str and config.get("format") == "date":
            if not validar_data_string(valor, f"{contexto}{campo}"):
                if "default" in config:
                    resultado[campo] = config["default"]
                    logger.info(f"Campo {contexto}{campo}: Data inválida, usando padrão {config['default']}")
                else:
                    erros.append(f"Data inválida para {contexto}{campo}")
                continue
        
        elif config["type"] == list:
            item_type = config.get("item_type")
            if item_type == dict and "item_schema" in config:
                # Validar lista de objetos complexos
                lista_validada = []
                for i, item in enumerate(valor):
                    item_validado = validar_objeto(item, config["item_schema"], f"{contexto}{campo}[{i}].")
                    if item_validado:
                        lista_validada.append(item_validado)
                    else:
                        logger.warning(f"Item {i} da lista {contexto}{campo} inválido, ignorando")
                resultado[campo] = lista_validada
                continue
            else:
                if not validar_lista(valor, f"{contexto}{campo}", item_type, 
                                   config.get("min_length", 0), config.get("max_length")):
                    if "default" in config:
                        resultado[campo] = config["default"]
                        logger.info(f"Campo {contexto}{campo}: Lista inválida, usando padrão {config['default']}")
                    else:
                        erros.append(f"Lista inválida para {contexto}{campo}")
                    continue
        
        # Se passou todas as validações, usar o valor
        resultado[campo] = valor
    
    if erros:
        logger.error(f"Erros de validação em {contexto}: {', '.join(erros)}")
        # Para erros críticos, podemos levantar exceção ou usar fallback completo
        if contexto == "":  # Se for o objeto principal
            raise ValueError(f"Dados inválidos: {', '.join(erros)}")
    
    return resultado

def validar_dados_completos(dados: Dict) -> Dict:
    """Validação completa dos dados do sistema."""
    try:
        return validar_objeto(dados, DADOS_SCHEMA)
    except ValueError as e:
        logger.critical(f"Dados corrompidos: {e}. Usando fallback completo.")
        # Fallback completo com todos os valores padrão
        return {campo: config["default"] for campo, config in DADOS_SCHEMA.items() if "default" in config}

def validar_arquivo_json(caminho: str) -> Dict:
    """Carrega e valida um arquivo JSON."""
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        if not isinstance(dados, dict):
            logger.error(f"Arquivo {caminho} não contém objeto JSON válido")
            return None
        
        return validar_dados_completos(dados)
        
    except FileNotFoundError:
        logger.info(f"Arquivo {caminho} não encontrado, usando dados padrão")
        return validar_dados_completos({})
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON em {caminho}: {e}")
        return validar_dados_completos({})
    except Exception as e:
        logger.error(f"Erro inesperado ao carregar {caminho}: {e}")
        return validar_dados_completos({})