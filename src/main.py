import numpy as np
from datetime import datetime  # ← ADICIONAR ESTA LINHA
from src.data_manager import carregar_dados_reais
from src.calculator import calcular_desvio_acumulado, calcular_meta_proximo_quadrante
from src.diet_plan import calcular_plano
from src.plot_generator import plotar_evolucao_peso
from src.calisthenics_calc import calculadora_calistenia
from src.quadrant_config import get_quadrant_config

def executar_programa_principal():
    """Executa o programa principal."""
    try:
        # Carregar dados atuais
        dados = carregar_dados_reais()
        dados_reais = dados["dados_reais"]
        peso_inicial = dados["peso_inicial"]
        target_total = dados.get('target_total', 0)
        
        # No Q0 não há perdas acumuladas
        perda_acumulada = 0 if not dados_reais else sum(dados_reais)
        peso_atual = peso_inicial - perda_acumulada
        
        # Começar sempre no Q0 se não houver dados
        quadrante_atual = 0 if not dados_reais else max(0, len(dados_reais) - 1)

        # Carregar configuração atual de quadrantes
        config_q = get_quadrant_config()
        y_plan = config_q['y_plan']

        # Em Q0, não há perdas ou desvios para mostrar
        perda_planejada_acum = 0
        perda_planejada_quad = y_plan[0] if y_plan is not None and len(y_plan) > 0 else 0  # Q0 sempre é zero
        perda_real_quad = 0        # Status atual e data
        print(f"\n📊 Status Atual: Quadrante {quadrante_atual} | Peso Atual: {peso_atual:.1f}kg")
        print(f"📅 Data atual: {datetime.now().strftime('%d/%m/%Y')}")
        
        # Em Q0, mostrar objetivo total. Em outros quadrantes, mostrar desvio
        if quadrante_atual == 0:
            print(f"⚠️ Faltam {target_total}kg para atingir o objetivo desejado")
        else:
            # Calcular desvio atual
            desvio = calcular_desvio_acumulado(quadrante_atual - 1)
            print(f"⚠️ Desvio acumulado: {desvio:.1f}kg")
        
            # Verificar se o desvio é alto (≥25%) - apenas após Q0
            if perda_planejada_acum > 0 and abs(desvio) >= 0.25 * perda_planejada_acum:
                print("\n🚨 ALERTA: DESVIO SIGNIFICATIVO DETECTADO 🚨")
                print("="*50)
                print(f"Perda planejada acumulada: {perda_planejada_acum:.1f}kg")
                print(f"Perda real acumulada: {perda_acumulada:.1f}kg")
                print(f"Desvio acumulado: {desvio:.1f}kg ({desvio/perda_planejada_acum*100:.1f}%)")
                print("="*50)
        
        print("\nOPÇÕES:")
        print("0. Setup do programa")
        print(f"1. Avançar para Quadrante {quadrante_atual + 1}")
        print("2. Visualizar gráfico de evolução")
        print("3. Entrar em modo emergencia")
        print("4. Plano de Treinamento")
        print("5. Calculadora de Calistenia")

        opcao = int(input("\nEscolha uma opção: "))

        if opcao == 1:
            # Menu de interações para avançar/editar quadrantes
            print("\nOpções para avançar/editar quadrantes:")
            print("a) Registrar um novo valor para o próximo quadrante")
            print("b) Inserir vários valores de uma vez (vírgula-separados)")
            print("c) Editar um quadrante anterior (formato: QX: valor, ex: Q1: -1.7)")
            print("d) Remover um dado (digite Q1 para remover Q1, ou apenas Q para remover todos)")
            escolha_q = input("Escolha (a/b/c/d) ou ENTER para cancelar: ") or ''
            from src.data_manager import registrar_peso_evolucao, salvar_dados_reais
            dados = carregar_dados_reais()
            if escolha_q.lower() == 'a':
                try:
                    novo_peso = float(input("Informe a perda/variação (kg) para registrar (ex: -0.7): "))
                    ok = registrar_peso_evolucao(novo_peso)
                    if ok:
                        print("✅ Peso registrado com sucesso.")
                    else:
                        print("⚠️ Falha ao registrar peso.")
                except Exception as e:
                    print(f"Entrada de peso inválida: {e}")

            elif escolha_q.lower() == 'b':
                entrada = input("Digite valores separados por vírgula (ex: 0.5, -0.2, 1.0): ")
                try:
                    vals = [float(x.strip()) for x in entrada.split(',') if x.strip()]
                    for v in vals:
                        registrar_peso_evolucao(v)
                    print(f"✅ {len(vals)} valores registrados.")
                except Exception as e:
                    print(f"Erro ao registrar valores múltiplos: {e}")

            elif escolha_q.lower() == 'c':
                ed = input("Digite edição (ex: Q1: -1.7): ")
                try:
                    if ':' in ed:
                        left, right = ed.split(':', 1)
                        q = left.strip().upper()
                        if q.startswith('Q'):
                            idx = int(q[1:])
                            val = float(right.strip())
                            # carregar, atualizar e salvar
                            dados = carregar_dados_reais()
                            if 'dados_reais' not in dados or not isinstance(dados['dados_reais'], list):
                                dados['dados_reais'] = []
                            # expand list if needed
                            while len(dados['dados_reais']) <= idx:
                                dados['dados_reais'].append(0.0)
                            dados['dados_reais'][idx] = val
                            salvar_dados_reais(dados)
                            print(f"✅ Quadrante Q{idx} atualizado para {val}kg")
                        else:
                            print("Formato inválido. Use Q<number>:")
                    else:
                        print("Formato inválido. Use Q1: -1.7")
                except Exception as e:
                    print(f"Erro ao editar quadrante: {e}")

            elif escolha_q.lower() == 'd':
                rem = input("Digite Qn para remover um quadrante (ex: Q1) ou Q para remover todos: ") or ''
                rem = rem.strip().upper()
                try:
                    dados = carregar_dados_reais()
                    if rem == 'Q':
                        # remover todos os dados (reset ao Q0)
                        dados['dados_reais'] = [0]
                        dados['quadrante_atual'] = 0
                        salvar_dados_reais(dados)
                        print("✅ Todos os dados removidos. Sistema resetado para Q0.")
                    elif rem.startswith('Q') and rem[1:].isdigit():
                        idx = int(rem[1:])
                        if 'dados_reais' not in dados or not isinstance(dados['dados_reais'], list):
                            print("Nenhum dado para remover.")
                        elif idx < 0 or idx >= len(dados['dados_reais']):
                            print(f"Quadrante Q{idx} não existe nos dados atuais.")
                        else:
                            # set the value to 0 and trim trailing zeros at the end if any
                            dados['dados_reais'][idx] = 0.0
                            # trim trailing zeros beyond the last non-zero (but keep at least one)
                            while len(dados['dados_reais']) > 1 and dados['dados_reais'][-1] == 0.0:
                                dados['dados_reais'].pop()
                            # ensure at least [0]
                            if not dados['dados_reais']:
                                dados['dados_reais'] = [0]
                            salvar_dados_reais(dados)
                            print(f"✅ Q{idx} removido (valor zerado).")
                    else:
                        print("Entrada inválida para remoção.")
                except Exception as e:
                    print(f"Erro ao remover dados: {e}")
            else:
                print("Operação cancelada.")

            # Após as operações, recalcular e mostrar planejamento para o próximo quadrante
            proximo_quadrante = len(carregar_dados_reais().get('dados_reais', []))
            meta_kg = calcular_meta_proximo_quadrante(proximo_quadrante - 1 if proximo_quadrante>0 else 0)
            dados = carregar_dados_reais()
            dados_reais = dados.get('dados_reais', [])
            perda_acumulada = sum(dados_reais)
            peso_atual = dados.get('peso_inicial', 0) - perda_acumulada
            peso_alvo = peso_atual - meta_kg

            res = calcular_plano(
                quadrante=proximo_quadrante,
                meta_kg=meta_kg
            )

            print(f"\n🔮 Planejamento para Quadrante {proximo_quadrante}")
            print(f"🎯 Meta de perda: {meta_kg:.1f}kg | Peso alvo: {peso_alvo:.1f}kg")

        elif opcao == 2:
            plotar_evolucao_peso()
            # Após fechar a janela do matplotlib, voltar ao menu principal
            input("\nPressione ENTER para voltar ao menu principal...")
            return executar_programa_principal()

        elif opcao == 0:
            # Opção de setup/configuração do programa
            try:
                from src import setup as setup_module
                result = setup_module.run_setup()
                # Se o setup retornou (saved, periodo_alterado), apenas limpar se periodo_alterado
                from src.data_manager import limpar_dados_reais
                try:
                    saved, periodo_alterado = result
                except Exception:
                    # compat fallback: boolean
                    saved = bool(result)
                    periodo_alterado = True
                if saved and periodo_alterado:
                    limpar_dados_reais()
            except Exception as e:
                print(f"❌ Falha ao executar setup: {e}")
            return executar_programa_principal()

        elif opcao == 3:  # Avançar ao próximo quadrante (protocolo rápido)
            # Calcular automaticamente a meta necessária para avançar ao próximo quadrante
            try:
                proximo_quadrante = quadrante_atual + 1
                meta_kg_auto = calcular_meta_proximo_quadrante(quadrante_atual)
                hoje = datetime.now().strftime("%d/%m/%Y")
                print(f"\n➡️ Para avançar de Q{quadrante_atual} para Q{proximo_quadrante} você precisa perder ~{meta_kg_auto:.2f} kg")
                print(f"📅 Data de início: {hoje} (hoje)")
                dias_emergencia = int(input("Informe o número de dias para atingir essa meta: "))

                res = calcular_plano(
                    quadrante=proximo_quadrante,
                    meta_kg=meta_kg_auto,
                    dias=dias_emergencia,
                    data_inicio_quad=datetime.now()
                )
            except Exception as e:
                print(f"Erro ao calcular plano rápido: {e}")
                # fallback: pedir entrada manual como antes
                try:
                    meta_kg_emergencia = float(input("Informe a meta de kg a perder: "))
                    dias_emergencia = int(input("Informe o número de dias para atingir a meta: "))
                    res = calcular_plano(
                        quadrante=0,
                        meta_kg=meta_kg_emergencia,
                        dias=dias_emergencia,
                        data_inicio_quad=datetime.now()
                    )
                except Exception as e2:
                    print(f"Operação cancelada: {e2}")
                    return executar_programa_principal()

        elif opcao == 4:
            # Plano de Treinamento: listar atividades físicas necessárias para avançar
            try:
                from src import activity_planner
                dados = carregar_dados_reais()
                proximo_quadrante = len(dados.get('dados_reais', []))
                atividades = activity_planner.calcular_atividades_base(proximo_quadrante)
                fase = activity_planner.determinar_fase(proximo_quadrante)
                print(f"\n🏋️ Plano de Treinamento para avançar ao Quadrante {proximo_quadrante} (fase: {fase})")
                total_kcal = 0
                for nome, desc, kcal in atividades:
                    print(f" - {nome}: {desc} = {kcal:.0f} kcal")
                    try:
                        total_kcal += float(kcal)
                    except Exception:
                        pass
                print(f"\nTotal estimado calorias (atividades base): {total_kcal:.0f} kcal")
            except Exception as e:
                print(f"Erro ao gerar plano de treinamento: {e}")
            return executar_programa_principal()

        elif opcao == 5:  # Calculadora de Calistenia
            calculadora_calistenia()
            return executar_programa_principal()  # Retorna ao menu principal

        else:
            raise ValueError("Opção inválida. Deve ser 0, 1, 2, 3, 4, 5 ou 99.")

        # Exibir resultados resumidos e perguntar se usuário quer ver cálculos calóricos detalhados
        print(f"\n{'='*70}")
        print(f"📊 QUADRANTE: {res['quadrante']} | FASE: {res['fase'].upper()}")

        if res['quadrante'] > 0:
            print(f"⚠️ Desvio acumulado: {res['desvio_kg']} kg")

        print(f"⏳ Dias: {res['dias']} (início: {res['inicio']})")
        print(f"🎯 Meta: {res['meta_kg']} kg")
        print(f"💧 Água: {res['agua']}ml")

        show_cal = input("\nDeseja ver o cálculo calórico e o plano diário detalhado? (s/N): ") or 'n'
        if show_cal.lower().startswith('s'):
            print(f"🎯 Meta: {res['meta_kg']} kg | {res['total_kcal']:.0f} kcal")
            print(f"🔥 Déficit diário necessário: {res['deficit_diario']:.0f} kcal")
            print(f"🍎 Dieta Déficit base: {res['deficit_alimentacao']:.0f} kcal")

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
        else:
            print("(Resumo exibido. Escolha opção 2 no menu para ver gráfico ou 0 para setup.)")
        # Depois de mostrar o resumo, voltar ao menu principal
        return executar_programa_principal()
        
    except Exception as e:
        print(f"❌ Erro não esperado: {e}")
        import traceback
        traceback.print_exc()