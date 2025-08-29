## 🎯 Requisitos Funcionais (Atualizados)

| ID | Requisito | Descrição |
|----|-----------|-----------|
| RF01 | Gestão de Quadrantes | Sistema deve calcular automaticamente quadrantes com base na data de início |
| RF02 | Cálculo de Metas | Calcular meta de perda de peso para cada quadrante com base em função exponencial |
| RF03 | Ajuste por Desempenho | Ajustar metas futuras com base no desvio acumulado |
| RF04 | Planejamento de Atividades | Gerar plano de atividades diárias considerando regras de karatê e bike |
| RF05 | Modo Emergência | Permitir criação de planos personalizados para situações especiais |
| RF06 | Visualização de Dados | Gerar gráfico de evolução com planejado vs realizado |
| RF07 | Persistência de Dados | Carregar e salvar dados de progresso real |
| RF08 | Sistema de Alertas | Alertar quando houver desvio significativo (>25%) |
| RF09 | Calculadora de Calistenia | Oferecer calculadora para divisão de repetições em blocos usando Fibonacci |

## 📊 Requisitos Não Funcionais

| ID | Requisito | Descrição |
|----|-----------|-----------|
| RNF01 | Usabilidade | Interface clara com menu intuitivo e opções bem explicadas |
| RNF02 | Performance | Cálculos devem ser executados rapidamente (<1s) |
| RNF03 | Confiabilidade | Sistema deve lidar gracefulmente com dados missing ou inconsistentes |
| RNF04 | Maintainabilidade | Código bem estruturado e documentado para facilitar manutenção |
| RNF05 | Precisão | Cálculos calóricos e de peso devem ter precisão de pelo menos 1 casa decimal |