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
