# src/plot_generator.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from datetime import datetime, timedelta
from src.data_manager import carregar_dados_reais
from quadrant_config import get_quadrant_config

def plotar_evolucao_peso():
    """Função para plotar a evolução do peso."""
    # Import local para y_plan se necessário
    from quadrant_config import get_quadrant_config

    # Ajustar soma para ~43kg
    target_total = 43
    scale_factor = target_total / np.sum(y_plan[1:])
    y_curve *= scale_factor
    y_plan_adjusted = y_plan.copy()

    # Quadrante 0 = ponto zero (0kg)
    y_plan_adjusted[0] = 0
    accum_plan = np.cumsum(y_plan_adjusted)

    # Criar função de interpolação para a curva suave
    accum_curve = np.cumsum(y_curve) * (accum_plan[-1] / np.sum(y_curve))

    # Dados Reais
    dados = carregar_dados_reais()
    peso_inicial = dados["peso_inicial"]
    y_real = dados["dados_reais"]
    accum_real = np.cumsum(y_real)
    x_real = np.arange(len(y_real))

    # Data de início
    if isinstance(dados["data_inicio"], str):
        data_inicio = datetime.strptime(dados["data_inicio"], "%Y-%m-%d")
    else:
        data_inicio = data_inicio_padrao

    # Projeção Corrigida
    x_proj = []
    y_proj = []
    ponto_esperado = None
    if len(y_real) > 0:
        last_real_value = accum_real[-1]
        
        f_interp = interp1d(accum_curve, x_curve, kind='linear', fill_value="extrapolate")
        x_esperado = f_interp(last_real_value)
        
        mask = x_curve <= x_esperado
        x_proj = x_curve[mask]
        y_proj = accum_curve[mask]
        
        ponto_esperado = (x_esperado, last_real_value)

    # Calcular dias acumulados por fase
    dias_acumulados = [0]
    datas_formatadas = [data_inicio.strftime('%d/%m/%y')]

    for i in range(1, 4):
        dias_acumulados.append(dias_acumulados[-1] + 5)
        nova_data = data_inicio + timedelta(days=dias_acumulados[-1])
        datas_formatadas.append(nova_data.strftime('%d/%m/%y'))

    for i in range(4, 8):
        dias_acumulados.append(dias_acumulados[-1] + 7)
        nova_data = data_inicio + timedelta(days=dias_acumulados[-1])
        datas_formatadas.append(nova_data.strftime('%d/%m/%y'))

    for i in range(8, 15):
        dias_acumulados.append(dias_acumulados[-1] + 10)
        nova_data = data_inicio + timedelta(days=dias_acumulados[-1])
        datas_formatadas.append(nova_data.strftime('%d/%m/%y'))

    # PLOTAGEM
    plt.figure(figsize=(16, 9))
    ax = plt.gca()

    # Fases coloridas no fundo
    ax.axvspan(-0.5, 3, color='green', alpha=0.2, lw=0)
    ax.axvspan(3, 7, color='blue', alpha=0.2, lw=0)
    ax.axvspan(7, 14.5, color='purple', alpha=0.2, lw=0)

    max_y = max(accum_plan.max(), accum_real.max() if len(y_real) > 0 else 0) + 5
    plt.text(1.5, max_y, '5 dias/quad', ha='center', va='bottom', 
             color='darkgreen', fontsize=9, bbox=dict(facecolor='white', alpha=0.8))
    plt.text(5, max_y, '7 dias/quad', ha='center', va='bottom',
             color='darkblue', fontsize=9, bbox=dict(facecolor='white', alpha=0.8))
    plt.text(10.5, max_y, '10 dias/quad', ha='center', va='bottom',
             color='purple', fontsize=9, bbox=dict(facecolor='white', alpha=0.8))

    # Projeção Corrigida
    if len(y_proj) > 0 and ponto_esperado is not None:
        plt.plot(x_proj, y_proj, color='blue', alpha=0.4, linewidth=8, zorder=1, label='Projeção')
        plt.plot(ponto_esperado[0], ponto_esperado[1], 'bo', markersize=10, zorder=4)
        
        quad_aprox = f'Q{ponto_esperado[0]:.1f}'
        plt.text(ponto_esperado[0], ponto_esperado[1] + 2, f'{quad_aprox}: {ponto_esperado[1]:.1f}kg',
                 color='blue', fontsize=10, ha='center', va='bottom', weight='bold', zorder=3)

    # Planejado
    plt.plot(x_points, accum_plan, color='blue', linestyle='--', linewidth=2, label='Planejado', zorder=2)

    # Rótulos na linha azul
    for i, val in enumerate(y_plan_adjusted):
        if i == 0:
            continue
        ha = 'left' if i == 1 else ('right' if i == 14 else 'center')
        plt.text(x_points[i], accum_plan[i] + 0.3, f'{val:.1f}',
                 color='blue', fontsize=8, ha=ha, va='bottom', weight='bold', zorder=3)

    # Real
    if len(y_real) > 0:
        plt.plot(x_real, accum_real, color='red', linewidth=2, marker='o', label='Real', zorder=3)
        for i, val in enumerate(accum_real):
            plt.text(x_real[i], val + 0.3, f'{val:.1f}', color='red', fontsize=8,
                     ha='center', va='bottom', weight='bold', zorder=3)

    # Eixo X com rótulos principais
    x_tick_labels = []
    for i in range(len(accum_plan)):
        if i == 0:
            main_label = f'Q{i}\\nP:0.0/{peso_inicial:.1f}\\nD:0'
        else:
            peso_projetado = peso_inicial - accum_plan[i]
            main_label = f'Q{i}\\nP:{accum_plan[i]:.1f}/{peso_projetado:.1f}\\nD:{dias_acumulados[i]}'
        x_tick_labels.append(main_label)

    ax.set_xticks(x_points)
    ax.set_xticklabels(x_tick_labels, fontsize=9)

    # Adicionar rótulos de data
    for i in range(1, len(x_points)):
        ax.text(x_points[i] - 0.2, -7.0, datas_formatadas[i], 
                rotation=30, ha='left', va='top', fontsize=10, color='black')

    # Configurações finais
    plt.ylabel('Perda de Peso Acumulada (kg)')
    plt.title(f'Evolução do Peso - Início: {peso_inicial}kg | Atual: {peso_inicial - accum_real[-1]:.1f}kg' if len(y_real) > 0 else f'Evolução do Peso - Início: {peso_inicial}kg')
    plt.xlim(-0.5, 14.5)
    plt.ylim(-3, max_y)
    plt.grid(True, linestyle='--', alpha=0.6, color='gray')
    plt.legend()
    plt.tight_layout()
    plt.show()