## 📋 Regras de Negócio (Atualizadas)

### 1. Sistema de Quadrantes
- **15 quadrantes** (0-14) com durações progressivas:
  - Q0: Modo emergência (duraçao variável)
  - Q1-Q3: 5 dias cada (fase verde)
  - Q4-Q7: 7 dias cada (fase azul) 
  - Q8-Q14: 10 dias cada (fase roxa)

### 2. Progressão de Perda de Peso
- Função exponencial: `f(x) = 0.6 * (10^(x/14))`
- Meta total ajustada para ~43kg com fator de escala
- Q0 sempre tem perda 0kg (ponto de partida)

### 3. Cálculo de Déficit Calórico
- 7000kcal = 1kg de peso
- Déficit alimentar máximo: 1300kcal/dia
- Déficit total = meta_kg * 7000
- Déficit diário = déficit_total / dias (arredondado para múltiplos de 500)

### 4. Sistema de Atividades Físicas
- **Base** (proporcional ao quadrante):
  - Calistenia: 10 reps × (quadrante/10) × 10
  - Corrida: 1 km × (quadrante/10) × 10
  - Bike: 3 km × (quadrante/10) × 10 (3x a corrida)

- **Karate**:
  - Segunda/Quarta: 120 minutos (1000kcal) - obrigatório
  - Outros dias: proporcional ao quadrante vigente
  - Mínimo de 30 minutos para sessões opcionais

### 5. Regras de Complemento
- Bike extra só é adicionada se:
  - Karate atingiu a meta diária (80% do esperado)
  - Ainda há déficit restante após atividades base
- Atividades complementares são exibidas separadamente

### 6. Ajuste por Desempenho
- Desvio acumulado = perda planejada - perda real
- Meta do próximo quadrante = meta planejada + desvio acumulado
- Alertas para desvios > 25% da meta planejada

### 7. Sistema de Hidratação
- Progressão linear: 500ml × quadrante
- Teto de 5000ml (5L) a partir do Q10

### 8. Calculadora de Calistenia (NOVO)
- Divisão de repetições usando sequência Fibonacci
- Modo automático: define número de blocos e subblocos com base no total de repetições
- Modo manual: permite especificar número de blocos e subblocos
- Redistribui valores pequenos (<=5) combinando com blocos adjacentes
- Garante blocos principais com pelo menos 6 repetições