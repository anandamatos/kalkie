## 🎨 Mockup de Interface

```
 DIET PLAN MANAGER
==========================================
📊 STATUS ATUAL:
Quadrante: 6 | Peso: 109.0kg | Desvio: 2.1kg

📅 PRÓXIMO QUADRANTE: 7 (01/09 - 07/09)
Meta: 2.8kg | Déficit diário: 2800kcal

------------------------------------------
🎯 OPÇÕES:
1. Avançar para Quadrante 7
2. Visualizar Gráfico de Evolução
3. Modo Emergência
99. Calculadora de Calistenia
0. Sair

Selecione uma opção: _
```

## 📝 Considerações de Implementação (Atualizadas)

1. **Estrutura de Dados**:
   - Dados reais armazenados em JSON
   - Estrutura de quadrantes pré-calculada
   - Histórico de atividades por dia
   - Nova funcionalidade de calculadora de calistenia integrada

2. **Fluxo de Cálculo**:
   ```
   Entrada → Carregar Dados → Calcular Desvio → 
   Definir Meta → Calcular Déficit → Gerar Atividades →
   Ajustar Karatê → Verificar Complementos → Saída
   ```

3. **Nova Funcionalidade**:
   ```
   Opção 99 → Calculadora Calistenia → 
   Selecionar Modo (Automático/Manual) → 
   Calcular Divisão Fibonacci → Exibir Resultados
   ```

4. **Tratamento de Erros**:
   - Valores padrão para dados missing
   - Verificação de consistência de datas
   - Limites para cálculos (valores mínimos/máximos)
   - Tratamento de entrada inválida na calculadora

5. **Interface**:
   - Menu interativo no console com nova opção 99
   - Formatação clara de resultados
   - Opções numeradas para fácil seleção
   - Interface dedicada para calculadora de calistenia

## 🚀 Funcionalidades Adicionadas

### Calculadora de Calistenia
- **Modo Automático**: Calcula automaticamente número de blocos e subblocos baseado no total de repetições
- **Modo Manual**: Permite personalizar número de blocos e subblocos
- **Algoritmo Fibonacci**: Usa sequência Fibonacci para distribuição inteligente de repetições
- **Redistribuição**: Combina valores pequenos (≤5) com blocos adjacentes para melhor experiência
- **Validação**: Garante valores mínimos em blocos principais (≥6 repetições)

### Integração com Sistema Principal
- Acessível através da opção 99 no menu principal
- Retorna ao menu principal após uso
- Mantém consistência com estilo e formatação do sistema
- Não interfere no fluxo principal de cálculo de quadrantes

## 📁 ESTRUTURA IDEAL ATUALIZADA:

```
diet_plan_project/
├── 📊 src/
│   ├── main.py               # Ponto de entrada principal
│   ├── diet_plan.py          # Lógica principal de quadrantes
│   ├── data_manager.py       # Gestão de dados JSON
│   ├── plot_generator.py     # Geração de gráficos
│   ├── calculator.py         # Cálculos de déficit e metas
│   ├── activity_planner.py   # Planejamento de atividades
│   ├── calisthenics_calc.py  # NOVO: Calculadora de calistenia
│   └── emergency_mode.py     # Modo emergência
│
├── 📚 docs/
│   ├── requirements.md       # Requisitos funcionais
│   ├── business_rules.md     # Regras de negócio atualizadas
│   ├── architecture.md       # Diagramas e arquitetura
│   ├── user_guide.md         # Manual do usuário
│   └── api_reference.md      # Referência de funções
│
├── 📂 data/
│   ├── dados_reais.json      # Dados de progresso
│   └── historical_data/      # Backup de dados
│
├── 📂 tests/
│   ├── test_calculator.py
│   ├── test_activities.py
│   └── test_calisthenics.py  # NOVO: Testes calculadora
│
└── 🚀 run.py                 # Script de execução
```

| **Constante (K)** | **Q1 (20%)** | **Q2 (30%)** | **Q3 (40%)** | **Q4 (60%)** | **Q5 (70%)** | **Q6 (80%)** | **Q7 (90%)** | **Q8 (100%)** | **Q9 (110%)** | **Q10 (120%)** | **Q11 (130%)** |
| --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |
| ⚖️ **7000 Kcal / Kg** (7000) | 1400 | 2100 | 2800 | 4200 | 4900 | 5600 | 6300 | 7000 | 7700 | 8400 | 9100 |
| --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |
| 💧 **AGUA por Dia** (5000) | 1000 | 1500 | 2000 | 3000 | 3500 | 4000 | 4500 | 5000 | 5500 | 6000 | 6500 |
| 🥋 **KARATE** (1000) | 200 | 300 | 400 | 600 | 700 | 800 | 900 | 1000 | 1100 | 1200 | 1300 |
| 💪 **CALISTENIA** (300) | 60 | 90 | 120 | 180 | 210 | 240 | 270 | 300 | 330 | 360 | 390 |
| 🏃 **CORRIDA** (100) | 20 | 30 | 40 | 60 | 70 | 80 | 90 | 100 | 110 | 120 | 130 |
| 🚴 **BIKE** (100) | 20 | 30 | 40 | 60 | 70 | 80 | 90 | 100 | 110 | 120 | 130 |
| 🧍 **BASAL** (2000) | 400 | 600 | 800 | 1200 | 1400 | 1600 | 1800 | 2000 | 2200 | 2400 | 2600 |
| 📉 **DEFICIT\_ALIMENTAR** (1000) | 200 | 300 | 400 | 600 | 700 | 800 | 900 | 1000 | 1100 | **1000** | **1000** |
| $\\sum$ **TOTAL (Karate até Déficit)** | **900** | **1320** | **1800** | **2700** | **3180** | **3640** | **4060** | **4500** | **4930** | **5180** | **5550** |