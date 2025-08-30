# src/activity_planner.py
from src.constants import *

def determinar_fase(quadrante):
    """Classifica a fase do quadrante."""
    if quadrante <= 3:
        return "verde"
    elif quadrante <= 7:
        return "azul"
    return "roxo"

def calcular_atividades_base(quadrante):
    """Calcula atividades físicas base para o quadrante."""
    # Progressão em relação ao Q10
    fator_q10 = quadrante / 10.0
    
    reps = max(1, round(10 * fator_q10 * 10))
    km_corrida = max(1, round(1 * fator_q10 * 10, 1))
    km_bike = max(1, round(3 * fator_q10 * 10, 1))
    
    return [
        ("Calistenia", f"{reps} reps", (reps / 100) * KCAL_CALISTENIA),
        ("Corrida", f"{km_corrida} km", km_corrida * KCAL_CORRIDA),
        ("Bike", f"{km_bike} km", km_bike * KCAL_BIKE)
    ]

def calcular_meta_karate_diaria(dia_semana, quadrante):
    """Calcula a meta diária de karatê baseada no dia da semana e quadrante."""
    if dia_semana in ["segunda", "quarta"]:
        # Segunda e quarta: 100% do Q10 (120 minutos)
        return 120, KCAL_KARATE
    else:
        # Outros dias: proporcional ao quadrante vigente
        minutos_karate = (quadrante / 10.0) * 120
        kcal_karate = (minutos_karate / 120) * KCAL_KARATE
        return minutos_karate, kcal_karate

def ajustar_karate(dia_semana, quadrante, plano_atual, deficit_restante):
    """Adiciona sessões de karatê conforme necessário."""
    if quadrante < 3:
        return 0, plano_atual
    
    # Calcular meta de karatê para o dia
    meta_minutos, meta_kcal = calcular_meta_karate_diaria(dia_semana, quadrante)
    
    # Karatê obrigatório (seg/qua) - sempre adiciona 120min
    if dia_semana in ["segunda", "quarta"]:
        plano_atual.append(("Karate Obrigatório", "120 min", KCAL_KARATE))
        return KCAL_KARATE, plano_atual
    
    # Para outros dias, adiciona karatê proporcional se necessário para o déficit
    if deficit_restante > 250:
        # Calcula minutos proporcionais ao déficit restante, mas não excede a meta
        minutos_karate = min(meta_minutos, (deficit_restante / KCAL_KARATE) * 120)
        if minutos_karate >= 30:
            kcal_karate = (minutos_karate / 120) * KCAL_KARATE
            tipo_karate = "Karate Diário" if minutos_karate >= meta_minutos * 0.8 else "Karate Opcional"
            plano_atual.append((tipo_karate, f"{minutos_karate:.0f} min", kcal_karate))
            return kcal_karate, plano_atual
    
    return 0, plano_atual