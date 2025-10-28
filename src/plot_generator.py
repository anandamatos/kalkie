import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from datetime import timedelta
from src.utils import parse_date, format_date
from src.data_manager import carregar_dados_reais
from src.quadrant_config import get_quadrant_config

def plotar_evolucao_peso():
    """Função para plotar a evolução do peso."""
    # Obter configuração unificada
    config = get_quadrant_config()
    x_points = config['x_points']
    y_plan = config['y_plan']
    dias_por_quadrante = config['dias_por_quadrante']
    data_inicio_padrao = config['data_inicio_padrao']

    # Pontos Planejado
    last_x = x_points[-1]
    x_curve = np.linspace(0, last_x, 430)

    def f(x):
        # denom = last_x
        return 0.6 * (10 ** (x / max(1, last_x)))

    y_curve = f(x_curve)

    # Ajustar soma para target_total vindo da config
    target_total = config.get('target_total', 43)
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
    
    # Se não houver dados reais (Q0), inicializar com zero
    if not y_real:
        y_real = [0.0]  # Começa em Q0 com perda zero
        
    accum_real = np.cumsum(y_real)
    x_real = np.arange(len(y_real))

    # Data de início usando parse_date unificado
    data_inicio = parse_date(dados.get("data_inicio", data_inicio_padrao))

    # Usar format_date para rótulos consistentes
    dias_acumulados = [0]
    datas_formatadas = [format_date(data_inicio, 'short')]
    # construir acumulado a partir do dias_por_quadrante (compatível com total de quadrantes)
    for i in range(1, len(x_points)):
        dias_acumulados.append(dias_acumulados[-1] + (dias_por_quadrante[i] if i < len(dias_por_quadrante) else 0))
        nova_data = data_inicio + timedelta(days=dias_acumulados[-1])
        datas_formatadas.append(format_date(nova_data, 'short'))

    # Projeção Corrigida
    x_proj = []
    y_proj = []
    ponto_esperado = None
    
    # Se estiver em Q0 (apenas um valor e é zero), mostrar projeção do início
    if len(y_real) == 1 and y_real[0] == 0:
        # Projeção começa do zero
        mask = x_curve >= 0
        x_proj = x_curve[mask]
        y_proj = accum_curve[mask]
        ponto_esperado = (0, 0)  # Ponto inicial em Q0
    elif len(y_real) > 0:
        # Projeção normal para quadrantes após Q0
        last_real_value = accum_real[-1]
        f_interp = interp1d(accum_curve, x_curve, kind='linear', fill_value="extrapolate")
        x_esperado = f_interp(last_real_value)
        mask = x_curve <= x_esperado
        x_proj = x_curve[mask]
        y_proj = accum_curve[mask]
        ponto_esperado = (x_esperado, last_real_value)

    # (já construímos datas_formatadas acima usando dias_por_quadrante)

    # PLOTAGEM
    plt.figure(figsize=(16, 9))
    ax = plt.gca()

    # Fases coloridas no fundo
    # Fases coloridas no fundo - determinar spans com base em dias/quadrantes
    # tentar mapear 3 fases a partir de dias_por_quadrante se possível
    try:
        # detectar pontos de mudança de fase por valor distinto em dias_por_quadrante
        # fallback: dividir em três blocos proporcionais
        n = len(x_points)
        third = max(1, n // 3)
        ax.axvspan(-0.5, third - 0.5, color='green', alpha=0.2, lw=0)
        ax.axvspan(third - 0.5, 2 * third - 0.5, color='blue', alpha=0.2, lw=0)
        ax.axvspan(2 * third - 0.5, last_x + 0.5, color='purple', alpha=0.2, lw=0)
    except Exception:
        ax.axvspan(-0.5, last_x / 3, color='green', alpha=0.2, lw=0)
        ax.axvspan(last_x / 3, 2 * last_x / 3, color='blue', alpha=0.2, lw=0)
        ax.axvspan(2 * last_x / 3, last_x + 0.5, color='purple', alpha=0.2, lw=0)

    # No plot_generator.py - Ajustar coordenadas Y dos textos
    max_y = max(accum_plan.max(), accum_real.max() if len(y_real) > 0 else 0) + 3  # Reduzir margem

    # Ajustar posicionamento vertical
    text_y_position = max_y - 2  # 1 unidade abaixo do topo

    plt.text(1.5, text_y_position, '5 dias/quad', ha='center', va='bottom', 
            color='darkgreen', fontsize=9, bbox=dict(facecolor='white', alpha=0.8))
    plt.text(5, text_y_position, '7 dias/quad', ha='center', va='bottom',
            color='darkblue', fontsize=9, bbox=dict(facecolor='white', alpha=0.8))
    plt.text(10.5, text_y_position, '10 dias/quad', ha='center', va='bottom',
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

    # Eixo X com rótulos principais (usar acumulados de dias)
    x_tick_labels = []
    for i in range(len(accum_plan)):
        if i == 0:
            main_label = f'Q{i}\nP:0.0/{peso_inicial:.1f}\nD:0'
        else:
            peso_projetado = peso_inicial - accum_plan[i]
            dias_label = dias_acumulados[i] if i < len(dias_acumulados) else 0
            main_label = f'Q{i}\nP:{accum_plan[i]:.1f}/{peso_projetado:.1f}\nD:{dias_label}'
        x_tick_labels.append(main_label)

    ax.set_xticks(x_points)
    ax.set_xticklabels(x_tick_labels, fontsize=8)

    # Configurar posições Y para cada linha
    line1_y = -7.0    # Linha principal (já está nos ticklabels)
    line4_y = -6   # Datas na quarta linha

    # Adicionar rótulos de data na posição correta
    for i in range(1, len(x_points)):
        ax.text(x_points[i] - 0.2, line4_y, datas_formatadas[i], 
                rotation=30, ha='left', va='top', fontsize=8, color='black')

    # Ajustar limites do gráfico
    plt.ylim(-16, max_y)

    # Configurações finais
    plt.ylabel('Perda de Peso Acumulada (kg)')
    # Título mostra peso atual apenas se não estiver em Q0
    if len(y_real) > 1:  # Se tem mais que um registro
        plt.title(f'Evolução do Peso - Início: {peso_inicial}kg | Atual: {peso_inicial - accum_real[-1]:.1f}kg')
    else:
        plt.title(f'Evolução do Peso - Início: {peso_inicial}kg')
    
    plt.xlim(-0.5, last_x + 0.5)
    plt.ylim(-3, max_y)
    plt.grid(True, linestyle='--', alpha=0.6, color='gray')
    # Mover legenda para canto inferior direito
    plt.legend(loc='lower right', bbox_to_anchor=(0.99, 0.02), 
            fancybox=False, shadow=False, ncol=1)
    plt.tight_layout()
    plt.show()