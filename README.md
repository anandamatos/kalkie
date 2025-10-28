# KALKIE

KALKIE é um sistema CLI (migrado de notebooks Jupyter) para planejamento e acompanhamento de perda de peso por "quadrantes". O projeto fornece cálculos de metas, geração de planos diários, armazenamento de dados reais e geração de gráficos de evolução.

Status atual
- Código organizado na pasta `src/`
- Assistente de setup interativo via terminal (`src/setup.py`) que grava `data/config.json` e `data/dados_reais.json` (com backups automáticos em `data/backups/`).
- Opções no menu principal (`run.py` → `src.main`): setup, registrar peso, visualizar gráfico, emergência e calculadora de calistenia.

Funcionalidades principais
- Definição de período (data de início e fim) e divisão em grupos/fases (p.ex. 3 grupos: 20%/30%/50%).
- Geração automática de `dias_por_quadrante` a partir das datas e dos grupos.
- Registro de evolução de perda/peso via terminal (salvo em `data/dados_reais.json`).
- Plot da evolução usando Matplotlib (consome `data/config.json` e `data/dados_reais.json`).
- Backups timestamped automáticos antes de sobrescrever os arquivos principais.

Instalação rápida
1. Crie/ative seu ambiente virtual (recomendado):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instale dependências:

```bash
pip install -r requirements.txt
```

Como executar
1. Inicie o programa principal:

```bash
python run.py
```

2. No menu principal, use as opções:
- 0 → Setup do programa (configurar datas, pesos, número de grupos e quadrantes)
- 1 → Avançar / Registrar novo peso (quando você avança o quadrante o sistema pergunta se deseja registrar um novo valor de evolução)
- 2 → Visualizar gráfico de evolução (gera o gráfico com as definições atuais)
- 4 → Modo emergência (criar um plano custom com início hoje)
- 99 → Calculadora de Calistenia

Arquivos importantes
- `run.py` — script de entrada (adiciona `src/` ao path e chama `src.main`).
- `src/main.py` — menu e fluxo principal.
- `src/setup.py` — assistente interativo que grava `data/config.json` e `data/dados_reais.json` e cria backups em `data/backups/`.
- `src/quadrant_config.py` — gera `x_points`, `y_plan` e lê `data/config.json` para overrides (`data_inicio_padrao`, `dias_por_quadrante`, `target_total`).
- `src/data_manager.py` — leitura/gravação de `dados_reais.json`, validação e novas funções para registrar evolução de peso.
- `src/plot_generator.py` — geração de gráficos com Matplotlib (usa `dias_por_quadrante` e `data_inicio` do `config.json`).
- `data/config.json` — arquivo de configuração gerado pelo setup (não comitado em geral).
- `data/dados_reais.json` — dados do usuário: `peso_inicial`, `data_inicio`, `dados_reais` (lista de variações por quadrante) e histórico.

Backups
- Antes de sobrescrever `data/dados_reais.json` ou `data/config.json` o assistente salva uma cópia em `data/backups/` com timestamp.

Boas práticas
- Prefira usar o assistente (`0` no menu) para configurar o projeto em vez de editar os JSONs manualmente.
- Faça commits frequentes ao evoluir a lógica; mantenha um ambiente virtual por projeto.

Desenvolvimento
- Código-fonte em `src/` (Python 3.9+ recomendado). Testes ainda não automatizados.

Próximos passos / Backlog (itens recomendados para adicionar ao seu backlog)

1) Computar `dias_por_quadrante` diretamente em `src/quadrant_config.py`
- Atualmente o assistente gera `dias_por_quadrante` e salva em `data/config.json`. Implementar a mesma lógica (calcular a partir de `data_inicio` e `data_fim` + `num_groups`) dentro de `quadrant_config` garante que qualquer consumidor (não só o wizard) obtenha a mesma divisão.

2) Restauração de backups via menu
- Adicionar opção no menu para listar backups em `data/backups/` e restaurar um deles (confirmar antes de sobrescrever). Útil para recuperação rápida.

3) Validações e UX no setup
- Melhoria das validações (ex.: garantir `data_fim > data_inicio`, `total_quadrants >= 2`, tipos corretos) e confirmação final antes de gravar.

4) Testes automatizados
- Adicionar testes unitários para: geração de dias por quadrante, leitura/escrita de `data/config.json`, salvar/backup, registro de peso e plot generation (mocking I/O onde necessário).

5) Dashboard interativo (Streamlit)
- Implementar um dashboard que permita editar config, ver gráficos e inserir/editar registros de peso via UI. O scaffold já está preparado e `streamlit` foi adicionado ao `requirements.txt`.

6) Histórico completo e análises comparativas
- Scripts que gerem relatórios comparando planejado vs realizado por períodos, exportáveis em CSV/PNG.

7) CI / Lint / Formatting
- Adicionar GitHub Actions para: lint (flake8/ruff), formatting (black/isort), testes, e verificação de segurança de dependências.

8) Packaging e distribuição
- Criar pyproject.toml e transformar o projeto em pacote instalável (`pip install .`) e comando CLI (`kalkie run`).

9) Persistência e Concurrency
- Para multiusuário ou acesso concorrente, usar um backend leve (SQLite) e locks para evitar corrupted writes.

10) Melhorias de logging e telemetria
- Centralizar logs, níveis configuráveis e arquivos rotativos. Possível integração com ferramentas de monitoramento.

11) Exportadores / Importadores
- Permitir importar dados históricos de outros trackers (CSV) e exportar planos e gráficos.

12) UI/UX refinements
- Se mais tarde migrar para web/UI, manter a camada de lógica desacoplada para facilitar a transição (service layer + API).

Se quiser, eu já posso:
- adicionar a opção de restauração de backups no menu (rápido), ou
- escrever o protótipo Streamlit para configurações e visualizações (maior esforço), ou
- implementar os testes automáticos básicos.

---
README gerado automaticamente por assistente. Se quiser que eu adicione informações específicas (licença, autor, badge de CI), diga quais e eu atualizo.
