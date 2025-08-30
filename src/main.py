# src/main.py
import numpy as np  # ← ADICIONAR ESTA LINHA
from src.data_manager import carregar_dados_reais
from src.calculator import calcular_desvio_acumulado, calcular_meta_proximo_quadrante
from src.diet_plan import calcular_plano
from src.plot_generator import plotar_evolucao_peso
from src.calisthenics_calc import calculadora_calistenia
from quadrant_config import get_quadrant_config
from datetime import datetime

def executar_programa_principal():
    """Executa o programa principal."""
    # Obter configuração unificada
    config = get_quadrant_config()
    y_plan = config['y_plan']
    try:
        # Carregar dados atuais
        dados = carregar_dados_reais()
        quadrante_atual = 6  # Forçando Q6 conforme solicitado
        dados_reais = dados["dados_reais"]
        perda_acumulada = sum(dados_reais)
        peso_atual = dados["peso_inicial"] - perda_acumulada
        
        # Calcular desvio atual (até Q5, já que Q6 está em andamento)
        desvio = calcular_desvio_acumulado(5)  # Até Q5
        
        # Calcular perda planejada acumulada até Q5
        perda_planejada_acum = np.sum(y_plan[1:6])
        
        # Calcular perda planejada para o Q6
        perda_planejada_quad = y_plan[6]
        
        # Calcular perda real no Q6
        perda_real_quad = dados_reais[6] if 6 < len(dados_reais) else 0
        
        print(f"\n📊 Status Atual: Quadrante 6 | Peso Atual: {peso_atual:.1f}kg")
        print(f"📅 Data atual: {datetime.now().strftime('%d/%m/%Y')}")
        print(f"⚠️ Desvio acumulado: {desvio:.1f}kg")
        
        # Verificar se o desvio é alto (≥25%)
        if perda_planejada_acum > 0 and abs(desvio) >= 0.25 * perda_planejada_acum:
            print("\n🚨 ALERTA: DESVIO SIGNIFICATIVO DETECTADO 🚨")
            print("="*50)
            print("ANÁLISE DETALHADA DO QUADRANTE ATUAL")
            print("="*50)
            print(f"Perda planejada acumulada: {perda_planejada_acum:.1f}kg")
            print(f"Perda real acumulada: {perda_acumulada:.1f}kg")
            print(f"Desvio acumulado: {desvio:.1f}kg ({desvio/perda_planejada_acum*100:.1f}%)")
            print("\nDETALHAMENTO DO QUADRANTE ATUAL:")
            print(f" - Planejado para este quadrante: {perda_planejada_quad:.1f}kg")
            print(f" - Realizado neste quadrante: {perda_real_quad:.1f}kg")
            if 6 < len(dados_reais):
                print(f" - Falta para meta do quadrante: {perda_planejada_quad - perda_real_quad:.1f}kg")
            print("="*50)
        
        print("\nOPÇÕES:")
        print("1. Avançar para próximo quadrante (Q7)")
        print("2. Visualizar gráfico de evolução")
        print("0. Entrar em modo emergência")
        print("99. Calculadora de Calistenia")
        
        opcao = int(input("\nEscolha uma opção: "))
        
        if opcao == 1:
            # Calcular automaticamente a meta para o Q7
            proximo_quadrante = 7
            meta_kg = calcular_meta_proximo_quadrante(6)  # Baseado no Q6
            
            # Calcular peso alvo
            peso_alvo = peso_atual - meta_kg
            
            res = calcular_plano(
                quadrante=proximo_quadrante,
                meta_kg=meta_kg
            )
            
            print(f"\n🔮 Planejamento para Quadrante {proximo_quadrante}")
            print(f"🎯 Meta de perda: {meta_kg:.1f}kg | Peso alvo: {peso_alvo:.1f}kg")
            
        elif opcao == 2:
            plotar_evolucao_peso()
            return
            
        elif opcao == 0:
            print("\n🚨 PROTOCOLO DE EMERGÊNCIA ATIVADO 🚨")
            hoje = datetime.now().strftime("%d/%m/%Y")
            print(f"📅 Data de início: {hoje} (hoje)")
            
            meta_kg_emergencia = float(input("Informe a meta de kg a perder: "))
            dias_emergencia = int(input("Informe o número de dias para atingir a meta: "))
            
            res = calcular_plano(
                quadrante=0,
                meta_kg=meta_kg_emergencia,
                dias=dias_emergencia,
                data_inicio_quad=datetime.now()
            )
            
        elif opcao == 99:
            calculadora_calistenia()
            return executar_programa_principal()  # Retorna ao menu principal
            
        else:
            raise ValueError("Opção inválida. Deve ser 0, 1, 2 ou 99.")
        
        # Exibir resultados
        print(f"\n{'='*70}")
        print(f"📊 QUADRANTE: {res['quadrante']} | FASE: {res['fase'].upper()}")
        
        if res['quadrante'] > 0:
            print(f"⚠️ Desvio acumulado: {res['desvio_kg']} kg")
        
        print(f"⏳ Dias: {res['dias']} (início: {res['inicio']})")
        print(f"🎯 Meta: {res['meta_kg']} kg | {res['total_kcal']:.0f} kcal")
        print(f"🔥 Déficit diário necessário: {res['deficit_diario']:.0f} kcal")
        print(f"🍎 Dieta Déficit base: {res['deficit_alimentacao']:.0f} kcal")
        print(f"💧 Água: {res['agua']}ml")
        
        print("\n📅 PLANO DIÁRIO:")
        for data, dia, plano, atividades_comp, exerc, aliment, total, meta in res['planos']:
            print(f"\n>>> {data} ({dia}):")
            for nome, det, kcal in plano:
                print(f" - {nome}: {det} = {kcal:.1f} kcal")
            
            # Mostrar atividades complementares se houver
            if atividades_comp:
                print("🔥🔥 Complementar")
                for nome, det, kcal in atividades_comp:
                    print(f" - {nome}: {det} = {kcal:.1f} kcal")
            
            status = "✅ ATINGIDO" if total >= meta else f"⚠️ FALTAM {meta - total:.1f} kcal"
            print(f"🍎 Dieta Déficit: {aliment:.1f} kcal")
            print(f"🔥 TOTAL: {total:.1f} kcal {status}")
            print(f"   (Exerc. {exerc:.1f} + Alim. {aliment:.1f} | Meta: {meta:.1f} kcal)")
        
    except ValueError as e:
        print(f"Erro: {e}")