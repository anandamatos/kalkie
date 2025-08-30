"""
JUPYTER BRIDGE - Adaptador para execução no Jupyter Notebook
Permite migração gradual do código .ipynb para estrutura modular
"""

import warnings
from IPython.display import display, HTML
import pandas as pd

def run_jupyter_mode():
    """Executa o sistema em modo Jupyter"""
    print("🔗 Conectando estrutura modular com Jupyter...")
    
    try:
        # Importa módulos principais
        from src.data_manager import carregar_dados_reais
        from src.calculator import calcular_desvio_acumulado, calcular_meta_proximo_quadrante
        from src.activity_planner import calcular_plano
        from src.plot_generator import plotar_evolucao_peso
        from src.calisthenics_calc import calculadora_calistenia
        
        # Carrega dados atuais
        dados = carregar_dados_reais()
        quadrante_atual = 6  # Exemplo - deveria vir dos dados
        
        print(f"📊 Sistema carregado - Quadrante Atual: {quadrante_atual}")
        print("✅ Estrutura modular conectada com sucesso!")
        
        # Menu interativo para Jupyter
        exibir_menu_jupyter(dados, quadrante_atual)
        
    except ImportError as e:
        warnings.warn(f"Módulo não encontrado: {e}. Criando fallback...")
        fallback_jupyter_mode()

def exibir_menu_jupyter(dados, quadrante_atual):
    """Menu interativo adaptado para Jupyter"""
    display(HTML("<h2>🎯 Kalkie Diet Plan Manager</h2>"))
    
    while True:
        display(HTML("""
        <div style='border: 2px solid #4CAF50; padding: 15px; border-radius: 10px; margin: 10px;'>
        <h3>📋 MENU PRINCIPAL</h3>
        """))
        
        opcoes = [
            "1. Avançar para próximo quadrante",
            "2. Visualizar gráfico de evolução", 
            "3. Modo Emergência",
            "99. Calculadora de Calistenia",
            "0. Sair"
        ]
        
        for opcao in opcoes:
            display(HTML(f"<p>{opcao}</p>"))
        
        try:
            escolha = input("\n🎯 Escolha uma opção: ").strip()
            
            if escolha == "1":
                avancar_quadrante_jupyter(dados, quadrante_atual)
            elif escolha == "2":
                plotar_evolucao_jupyter()
            elif escolha == "3":
                modo_emergencia_jupyter()
            elif escolha == "99":
                calculadora_calistenia_jupyter()
            elif escolha == "0":
                print("👋 Saindo...")
                break
            else:
                display(HTML("<p style='color: red;'>❌ Opção inválida!</p>"))
                
        except KeyboardInterrupt:
            print("\n👋 Interrompido pelo usuário")
            break
        except Exception as e:
            display(HTML(f"<p style='color: red;'>💥 Erro: {e}</p>"))

def avancar_quadrante_jupyter(dados, quadrante_atual):
    """Lógica para avançar quadrante no Jupyter"""
    from src.calculator import calcular_meta_proximo_quadrante
    from src.activity_planner import calcular_plano
    
    proximo_quadrante = quadrante_atual + 1
    meta_kg = calcular_meta_proximo_quadrante(quadrante_atual)
    
    display(HTML(f"<h4>🔮 Planejamento para Quadrante {proximo_quadrante}</h4>"))
    display(HTML(f"<p>🎯 Meta de perda: {meta_kg:.1f}kg</p>"))
    
    plano = calcular_plano(proximo_quadrante, meta_kg=meta_kg)
    exibir_plano_jupyter(plano)

def exibir_plano_jupyter(plano):
    """Exibe plano formatado para Jupyter"""
    df = pd.DataFrame([{
        'Data': item[0],
        'Dia': item[1], 
        'Exercício': len(item[2]),
        'Complementos': len(item[3]),
        'Total kcal': item[6]
    } for item in plano['planos']])
    
    display(HTML("<h4>📅 RESUMO DO PLANO</h4>"))
    display(df)
    
    display(HTML(f"""
    <div style='background-color: #f0f8ff; padding: 10px; border-radius: 5px; margin: 10px;'>
    <strong>📊 Detalhes do Quadrante:</strong><br>
    Fase: {plano['fase']} | Dias: {plano['dias']} | Meta: {plano['meta_kg']}kg<br>
    Déficit diário: {plano['deficit_diario']}kcal | Água: {plano['agua']}ml
    </div>
    """))

def plotar_evolucao_jupyter():
    """Exibe gráfico no Jupyter"""
    from src.plot_generator import plotar_evolucao_peso
    plotar_evolucao_peso()

def calculadora_calistenia_jupyter():
    """Calculadora de calistenia para Jupyter"""
    from src.calisthenics_calc import calculadora_calistenia
    calculadora_calistenia()

def fallback_jupyter_mode():
    """Fallback se módulos não estiverem prontos"""
    print("⚠️  Módulos ainda não implementados. Executando fallback...")
    
    # Aqui você pode colocar o código atual do .ipynb temporariamente
    exec(open('seu_arquivo_atual.ipynb').read())