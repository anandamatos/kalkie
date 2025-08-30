# NOVO src/diet_plan.py (versão corrigida)
from datetime import datetime, timedelta
from src.calculator import arredondar_500
from src.activity_planner import determinar_fase, calcular_atividades_base, ajustar_karate, calcular_meta_karate_diaria
from src.data_manager import carregar_dados_reais
from src.calculator import calcular_desvio_acumulado
from src.constants import KCAL_POR_KG, MAX_DEFICIT_ALIMENTAR, AGUA_Q10, KCAL_BIKE
from quadrant_config import get_quadrant_config

def calcular_data_inicio_quadrante(quadrante):
    """Calcula a data de início correta para cada quadrante."""
    dados = carregar_dados_reais()
    
    if isinstance(dados["data_inicio"], str):
        data_inicio = datetime.strptime(dados["data_inicio"], "%Y-%m-%d")
    else:
        data_inicio = datetime.strptime(data_inicio_padrao, "%Y-%m-%d")
    
    # Calcular dias acumulados até o início do quadrante
    dias_acumulados = sum(dias_por_quadrante[1:quadrante])
    return data_inicio + timedelta(days=dias_acumulados)

def calcular_plano(quadrante, meta_kg=None, dias=None, data_inicio_quad=None):
    """Calcula plano detalhado para o quadrante especificado."""
    # Obter configuração unificada
    config = get_quadrant_config()
    dias_por_quadrante = config['dias_por_quadrante']
    data_inicio_padrao = config['data_inicio_padrao']
    
    # Configurar data de início
    if quadrante == 0:
        fase = "EMERGÊNCIA"
        desvio_acumulado = 0
        if not all([meta_kg, dias, data_inicio_quad]):
            raise ValueError("Para emergência, informe meta_kg, dias e data_inicio_quad")
    else:
        if quadrante < 1 or quadrante > 14:
            raise ValueError("Quadrante deve estar entre 1-14")
            
        fase = determinar_fase(quadrante)
        dias = dias_por_quadrante[quadrante]
        data_inicio_quad = calcular_data_inicio_quadrante(quadrante)
        
        # Se não foi fornecida meta, calcular com base nos desvio
        if meta_kg is None:
            desvio_acumulado = calcular_desvio_acumulado(quadrante - 1)
            meta_kg = y_plan[quadrante] + desvio_acumulado
        else:
            desvio_acumulado = meta_kg - y_plan[quadrante]
    
    # ... restante do código permanece igual ...
    # Cálculos de déficit
    total_kcal = meta_kg * KCAL_POR_KG
    deficit_diario = arredondar_500(total_kcal / dias)
    
    # Déficit alimentar progressivo
    if quadrante == 0:
        deficit_alimentacao = MAX_DEFICIT_ALIMENTAR
    else:
        deficit_alimentacao = min(MAX_DEFICIT_ALIMENTAR, 
                                 (MAX_DEFICIT_ALIMENTAR / 14) * quadrante)
    
    queima_necessaria = max(0, deficit_diario - deficit_alimentacao)
    
    # Configurar datas e dias da semana
    datas = [data_inicio_quad + timedelta(days=i) for i in range(dias)]
    dias_semana = [data.strftime("%A") for data in datas]
    tradutor_dias = {
        "Monday": "segunda", "Tuesday": "terça", "Wednesday": "quarta",
        "Thursday": "quinta", "Friday": "sexta", "Saturday": "sábado",
        "Sunday": "domingo"
    }
    dias_semana = [tradutor_dias[dia] for dia in dias_semana]
    
    # Calcular plano diário
    planos = []
    for i, data in enumerate(datas):
        # 1. Atividades base
        plano_dia = calcular_atividades_base(quadrante if quadrante > 0 else 5)
        total_exerc = sum(kcal for _, _, kcal in plano_dia)
        deficit_restante = max(0, queima_necessaria - total_exerc)
        
        # 2. Ajustar karatê
        kcal_karate, plano_dia = ajustar_karate(
            dias_semana[i], 
            quadrante, 
            plano_dia,
            deficit_restante
        )
        total_exerc += kcal_karate
        deficit_restante = max(0, queima_necessaria - total_exerc)
        
        # 3. Calcular meta de karate para o dia
        meta_minutos, meta_kcal = calcular_meta_karate_diaria(dias_semana[i], quadrante)
        
        # 4. Verificar se o karate atingiu a meta antes de adicionar bike extra
        karate_atingiu_meta = kcal_karate >= meta_kcal * 0.8  # 80% da meta considera atingido
        
        # 5. Ajustar bike apenas se karate atingiu a meta
        atividades_complementares = []
        if deficit_restante > 0 and karate_atingiu_meta:
            # Encontra atividade de bike para atualizar
            for idx, (nome, det, kcal) in enumerate(plano_dia):
                if nome == "Bike":
                    km_extra = deficit_restante / KCAL_BIKE
                    km_total = float(det.split()[0]) + km_extra
                    kcal_extra = km_extra * KCAL_BIKE
                    plano_dia[idx] = ("Bike", f"{km_total:.1f} km", kcal + kcal_extra)
                    atividades_complementares.append(("Bike Extra", f"+{km_extra:.1f} km", kcal_extra))
                    total_exerc += kcal_extra
                    break
        
        # 6. Calcular déficit total
        total_deficit = total_exerc + deficit_alimentacao
        
        planos.append((
            data.strftime("%d/%m/%Y"),
            dias_semana[i],
            plano_dia,
            atividades_complementares,
            total_exerc,
            deficit_alimentacao,
            total_deficit,
            deficit_diario
        ))

    return {
        "quadrante": quadrante,
        "fase": fase,
        "dias": dias,
        "inicio": data_inicio_quad.strftime("%d/%m/%Y"),
        "meta_kg": round(meta_kg, 2),
        "desvio_kg": round(desvio_acumulado, 2) if quadrante > 0 else 0,
        "total_kcal": total_kcal,
        "deficit_diario": deficit_diario,
        "deficit_alimentacao": deficit_alimentacao,
        "queima_necessaria": queima_necessaria,
        "agua": min(int(500 * quadrante), AGUA_Q10) if quadrante > 0 else 6000,
        "planos": planos
    }