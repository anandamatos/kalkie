"""Setup interativo do KALKIE

Fornece um assistente em terminal para configurar:
- data de início
- peso inicial
- objetivo total (kg a perder)
- configuração de dias por quadrante (preset ou custom)

Também oferece opção de iniciar um dashboard Streamlit se instalado.
"""
import json
import os
from datetime import datetime

from src.data_manager import carregar_dados_reais, salvar_dados_reais


ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, 'data')
DEFAULT_DADOS_PATH = os.path.join(DATA_DIR, 'dados_reais.json')
CONFIG_PATH = os.path.join(DATA_DIR, 'config.json')


def _format_value_display(val):
    """Formata o valor para exibição, incluindo unidades quando apropriado."""
    if isinstance(val, float):
        return f"{val:.1f}kg"
    return str(val)

def _input_date(prompt, default=None, previous=None):
    if previous and not default:
        default = previous
    display_value = default or "não definido"
    while True:
        val = input(f"{prompt} [atual: {display_value}]: ") or default
        try:
            if isinstance(val, str):
                # aceitar YYYY-MM-DD ou DD/MM/YYYY
                try:
                    dt = datetime.strptime(val, "%Y-%m-%d")
                except Exception:
                    dt = datetime.strptime(val, "%d/%m/%Y")
            else:
                dt = val
            return dt.strftime("%Y-%m-%d")
        except Exception:
            print("Formato de data inválido. Use YYYY-MM-DD ou DD/MM/YYYY.")


def _input_float(prompt, default=None, previous=None, unit="kg"):
    if previous is not None and default is None:
        default = previous
    display_value = f"{default:.1f}{unit}" if default is not None else "não definido"
    while True:
        val = input(f"{prompt} [atual: {display_value}]: ") or str(default)
        try:
            return float(val)
        except Exception:
            print("Valor numérico inválido.")


def _input_int(prompt, default=None, previous=None):
    if previous is not None and default is None:
        default = previous
    display_value = str(default) if default is not None else "não definido"
    while True:
        val = input(f"{prompt} [atual: {display_value}]: ") or str(default)
        try:
            return int(val)
        except Exception:
            print("Valor inteiro inválido.")


def run_setup():
    """Executa o assistente interativo de configuração."""
    print("\n=== KALKIE: Novo Objetivo ===\n")
    print("💡 Configure as datas primeiro para ver o total de dias disponíveis.\n")

    # Carregar dados existentes e configuração
    dados = carregar_dados_reais()
    cfg = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
        except Exception:
            cfg = {}

    # Valores existentes ou padrões
    peso_inicial = dados.get('peso_inicial', 80.0)
    target_total = dados.get('target_total', cfg.get('target_total', 43))
    data_inicio_anterior = dados.get('data_inicio')
    # data_fim may be stored in dados or in config; prefer explicit config value if present
    data_fim_anterior = dados.get('data_fim') or cfg.get('data_fim')
    fqd_anterior = cfg.get('fqd_string', '')  # Formato F/Q/D salvo
    
    print("\n📊 Valores atuais:")
    print("-" * 40)
    if data_inicio_anterior:
        print(f"Data início  : {data_inicio_anterior}")
    if data_fim_anterior:
        print(f"Data fim     : {data_fim_anterior}")
    if peso_inicial:
        print(f"Peso inicial : {peso_inicial:.1f}kg")
    if target_total:
        print(f"Meta total   : {target_total:.1f}kg")
    if fqd_anterior:
        print(f"Distribuição : {fqd_anterior}")
    print("-" * 40)
    
    # Perguntar se quer manter tudo igual
    if all([data_inicio_anterior, data_fim_anterior, peso_inicial, target_total, fqd_anterior]):
        manter = input("\nDeseja manter todos os valores atuais? (S/n): ").lower() or 's'
        if manter == 's':
            print("\n✅ Configuração mantida!")
            return (False, False)  # Indica que não houve mudanças

    novo_data_inicio = _input_date("Data de início (YYYY-MM-DD)", 
                                 default=datetime.now().strftime("%Y-%m-%d"), 
                                 previous=data_inicio_anterior)
    novo_data_fim = _input_date("Data de fim (YYYY-MM-DD)", 
                               default=data_fim_anterior or datetime.now().strftime("%Y-%m-%d"), 
                               previous=data_fim_anterior)
    
    # Mostrar total de dias e sugestões de distribuição
    total_days = 0
    try:
        from src.utils import diferenca_dias
        total_days = diferenca_dias(novo_data_inicio, novo_data_fim)
        print(f"\n📅 Você tem {total_days} dias para distribuir")
        if total_days >= 60 and total_days <= 120:
            print("💡 Sugestões de distribuição F/Q/D:")
            print("   90 dias → 3F=[3Q(10D),3Q(8D),4Q(7D)]")
            print("   60 dias → 3F=[2Q(8D),3Q(6D),4Q(5D)]")
    except Exception:
        pass

    novo_peso_inicial = _input_float("Peso inicial", previous=peso_inicial)
    novo_target_total = _input_float("Objetivo total de perda", previous=target_total)

    print("\nComo deseja definir a distribuição dos quadrantes?")
    print("1) Direto: 3F=[2Q(10D),3Q(7D),5Q(5D)]")
    print("2) Passo a passo")
    modo = _input_int("Escolha (1 ou 2)", default=1)
    
    # Inicializar variáveis necessárias
    num_groups = cfg.get('num_groups', 3)  # default 3 fases
    total_quadrants = cfg.get('total_quadrants', 15)  # default 15 quadrantes (Q0..Q14)
    
    # Forçar modo manual para permitir entrada do formato F/Q/D
    manual_fqd = True
    if modo == 1:
        # Usar F/Q/D anterior como default se existir
        fqd_anterior = cfg.get('fqd_string', '')
        one_line = input(f"Digite a distribuição F/Q/D [{fqd_anterior}]: ") or fqd_anterior
        
        # Extrair num_groups, quadrants e dias da entrada
        try:
            import re
            # Example: "3F=[2Q(10D),3Q(7D),5Q(5D)]"
            match = re.match(r'(\d+)F=\[(.*)\]', one_line)
            if match:
                num_groups = int(match.group(1))
                quadrants = re.findall(r'(\d+)Q\((\d+)D\)', match.group(2))
                total_quadrants = sum(int(q[0]) for q in quadrants) + 1  # +1 for Q0
                total_days_planned = sum(int(q[0]) * int(q[1]) for q in quadrants)
                print(f"\n📊 Dias planejados: {total_days_planned}")
                if total_days_planned > total_days:
                    print(f"⚠️  Aviso: Você planejou {total_days_planned} dias, mas tem apenas {total_days} dias disponíveis!")
                    print("    Considere reduzir o número de dias por quadrante.")
                else:
                    print(f"✅ Distribuição aceita: {total_days_planned} dias")
                # Salvar string F/Q/D na configuração para uso futuro
                cfg['fqd_string'] = one_line
                # Salvar configuração atualizada
                with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                    json.dump(cfg, f, indent=2)
                # Parse os dias por quadrante
                novo_dias = []
                for q in quadrants:
                    novo_dias.extend([int(q[1])] * int(q[0]))
                return novo_data_inicio, novo_data_fim, novo_peso_inicial, novo_target_total, num_groups, total_quadrants, novo_dias, manual_fqd, one_line
        except Exception as e:
            print("⚠️  Erro ao interpretar o formato F/Q/D. Usando valores padrão.")
            pass  # manter os valores padrão se falhar o parsing

    # Presets para dias por quadrante (apenas como fallback se o usuário não quer calcular por datas)
    print("\nEscolha preset de dias por quadrante:")
    print("1) Preset padrão: 0,5,5,5,7,7,7,7,10,10,10,10,10,10,10")
    print("2) Preset curto (todos 5 dias)")
    print("3) Preset longo (todos 10 dias)")
    print("4) Customizar manualmente os 15 valores")

    escolha = _input_int("Escolha (1-4) — se deseja calcular automaticamente com base nas datas, escolha 1", default=1)

    if manual_fqd:
        # permitir entrada em uma linha no formato: 3F=[2Q(10D),3Q(7D),5Q(5D)]
        one_line = input("Deseja inserir F/Q/D em uma linha? Ex: 3F=[2Q(10D),3Q(7D),5Q(5D)] (Enter para pular): ") or ''

        def _parse_fqd(s: str):
            """Parseia string como '3F=[2Q(10D),3Q(7D),5Q(5D)]' e retorna (num_phases, [(q,d),...])."""
            import re
            s = s.strip()
            if not s:
                return None
            try:
                # extrair número de fases (opcional)
                m = re.match(r"\s*(\d+)\s*F\s*=\s*\[(.*)\]\s*", s, re.IGNORECASE)
                inner = s
                num_phases = None
                if m:
                    num_phases = int(m.group(1))
                    inner = m.group(2)

                parts = [p.strip() for p in inner.split(',') if p.strip()]
                tuples = []
                for part in parts:
                    # aceitar formatos como '2Q(10D)' ou '2Q (10D)'
                    mm = re.match(r"\s*(\d+)\s*Q\s*\(?\s*(\d+)\s*D\s*\)?\s*", part, re.IGNORECASE)
                    if not mm:
                        return None
                    q = int(mm.group(1))
                    d = int(mm.group(2))
                    tuples.append((q, d))
                if num_phases and num_phases != len(tuples):
                    # não fatal, apenas ajustar num_phases
                    num_phases = len(tuples)
                return num_phases or len(tuples), tuples
            except Exception:
                return None

        parsed = _parse_fqd(one_line)
        if parsed:
            num_phases, phase_list = parsed
            phase_quads = [q for q, d in phase_list]
            phase_days = [d for q, d in phase_list]
        else:
            # Solicitar número de fases (pode sobrescrever num_groups)
            num_phases = _input_int("Número de fases (F)", default=num_groups)
            phase_quads = []
            phase_days = []
            remaining_quads = max(0, total_quadrants - 1)
            for p in range(num_phases):
                q_default = max(1, remaining_quads // (num_phases - p) if (num_phases - p) > 0 else 1)
                q_in_phase = _input_int(f"Quadrantes na fase {p+1} (exclui Q0)", default=q_default)
                d_in_phase = _input_int(f"Dias totais para a fase {p+1}", default= q_in_phase * 5)
                phase_quads.append(max(1, q_in_phase))
                phase_days.append(max(1, d_in_phase))
                remaining_quads = max(0, remaining_quads - q_in_phase)

        # Construir novo_dias a partir das fases (cada Q tem D dias)
        novo_dias = [0]  # Q0 tem 0 dias
        for qcnt, dias_por_q in zip(phase_quads, phase_days):
            # cada quadrante na fase tem dias_por_q dias
            for _ in range(qcnt):
                novo_dias.append(dias_por_q)

        # ajustar se não bate com total_quadrants
        if len(novo_dias) < total_quadrants:
            novo_dias += [1] * (total_quadrants - len(novo_dias))
        elif len(novo_dias) > total_quadrants:
            novo_dias = novo_dias[:total_quadrants]

    elif escolha == 1:
        novo_dias = [0] + [5,5,5] + [7,7,7,7] + [10]*7
    elif escolha == 2:
        novo_dias = [0] + [5]*14
    elif escolha == 3:
        novo_dias = [0] + [10]*14
    else:
        novo_dias = []
        print("Informe os 15 valores (Q0..Q14). Comece por Q0 (normalmente 0). Exemplo: 0 5 5 5 7 7 7 7 10 10 10 10 10 10 10")
        while len(novo_dias) != 15:
            linha = input("Digite 15 números separados por espaço: ")
            try:
                vals = [int(x) for x in linha.strip().split()]
                if len(vals) != 15:
                    print("É necessário fornecer exatamente 15 valores.")
                    continue
                novo_dias = vals
            except Exception:
                print("Entrada inválida. Tente novamente.")

    # Se o usuário escolheu calcular automaticamente (escolha 1), vamos gerar dias por quadrante
    if escolha == 1:
        # Total de dias entre inicio e fim
        from src.utils import parse_date, diferenca_dias
        try:
            total_days = diferenca_dias(novo_data_inicio, novo_data_fim)
            if total_days <= 0:
                print("Aviso: data de fim menor ou igual à data de início. Mantendo preset de dias por quadrante.")
            else:
                # Definir percentuais para grupos
                if num_groups == 3:
                    percents = [0.2, 0.3, 0.5]
                else:
                    # gerar sequência de Fibonacci como pesos
                    def fib(n):
                        a, b = 1, 1
                        seq = [a]
                        for _ in range(n-1):
                            a, b = b, a + b
                            seq.append(a)
                        return seq

                    weights = fib(num_groups)
                    s = sum(weights)
                    percents = [w / s for w in weights]

                # distribuir dias por grupo
                group_days = [max(1, round(p * total_days)) for p in percents]
                # ajustar soma
                diff = total_days - sum(group_days)
                group_days[-1] += diff

                # distribuir quadrantes (exclui Q0)
                nonzero_quads = max(1, total_quadrants - 1)
                group_quads = [max(1, round(gd / total_days * nonzero_quads)) for gd in group_days]
                # ajustar soma dos quadrantes
                diffq = nonzero_quads - sum(group_quads)
                group_quads[-1] += diffq

                # calcular dias por quadrante
                novo_dias = [0]
                for gd, gq in zip(group_days, group_quads):
                    # distribuir gd dias entre gq quadrantes
                    base = gd // gq
                    extras = gd % gq
                    for i in range(gq):
                        d = base + (1 if i < extras else 0)
                        novo_dias.append(d)

                # se sobrar (caso total_quadrants mismatch), ajustar
                if len(novo_dias) < total_quadrants:
                    # append 1 dia para completar
                    novo_dias += [1] * (total_quadrants - len(novo_dias))
                elif len(novo_dias) > total_quadrants:
                    novo_dias = novo_dias[:total_quadrants]

                print(f"Gerado dias por quadrante com base em {total_days} dias e {num_groups} grupos.")
        except Exception:
            print("Erro ao calcular dias entre datas — preservando preset/custom fornecido.")

    # Atualizar arquivos
    # 1) Atualizar dados reais (peso_inicial e data_inicio)
    dados['peso_inicial'] = novo_peso_inicial
    dados['data_inicio'] = novo_data_inicio
    # Salvar também data_fim no arquivo de dados para facilitar histórico/consulta
    dados['data_fim'] = novo_data_fim
    # manter 'dados_reais' se existir, senão inicializar
    dados.setdefault('dados_reais', [])

    # Fazer backup do arquivo de dados atual antes de salvar
    def _backup_file(path):
        try:
            if os.path.exists(path):
                os.makedirs(os.path.join(DATA_DIR, 'backups'), exist_ok=True)
                ts = datetime.now().strftime('%Y%m%d_%H%M%S')
                base = os.path.basename(path)
                dest = os.path.join(DATA_DIR, 'backups', f"{ts}_{base}")
                with open(path, 'rb') as fr, open(dest, 'wb') as fw:
                    fw.write(fr.read())
                print(f"⤓ Backup criado: {dest}")
        except Exception as e:
            print(f"⚠️ Falha ao criar backup de {path}: {e}")

    _backup_file(DEFAULT_DADOS_PATH)

    saved = salvar_dados_reais(dados)
    if saved:
        print(f"\n✅ Dados salvos em '{DEFAULT_DADOS_PATH}'.")
    else:
        print(f"⚠️ Falha ao salvar dados em '{DEFAULT_DADOS_PATH}'.")

    # 2) Atualizar config.json com target_total e dias_por_quadrante
    new_cfg = {
        'data_inicio_padrao': novo_data_inicio,
        'data_fim': novo_data_fim,
        'target_total': novo_target_total,
        'num_groups': num_groups,
        'total_quadrants': total_quadrants,
        'dias_por_quadrante': novo_dias
    }
    # preservar a string F/Q/D se houver
    new_cfg['fqd_string'] = cfg.get('fqd_string', '')

    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        # backup config.json se existir
        _backup_file(CONFIG_PATH)
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(new_cfg, f, indent=2, ensure_ascii=False)
        print(f"✅ Configuração salva em '{CONFIG_PATH}'.")
    except Exception as e:
        print(f"⚠️ Falha ao salvar configuração: {e}")

    # Oferecer iniciar dashboard Streamlit se instalado
    try:
        import streamlit as st  # noqa: F401
        usar_streamlit = input("Deseja iniciar o dashboard Streamlit agora? (s/N): ") or 'n'
        if usar_streamlit.lower().startswith('s'):
            print("Iniciando Streamlit... (use Ctrl+C para voltar)")
            # iniciar via comando externo não é ideal aqui; orientar o usuário
            print("Execute no terminal: streamlit run src/setup.py -- --dashboard")
    except Exception:
        # Streamlit não instalado; apenas informar
        print("(Dica) Para dashboard interativo, instale 'streamlit' e execute:\n  streamlit run src/setup.py -- --dashboard")

    # Determinar se o período (datas) mudou comparado ao anterior
    periodo_alterado = False
    try:
        periodo_alterado = (data_inicio_anterior != novo_data_inicio) or (data_fim_anterior != novo_data_fim)
    except Exception:
        periodo_alterado = False

    print("\nSetup concluído. Retornando ao menu principal.")
    return (True, periodo_alterado)


if __name__ == '__main__':
    # Suporte a execução via streamlit quando passado --dashboard
    import sys
    if '--dashboard' in sys.argv:
        try:
            import streamlit as st
        except Exception:
            print("Streamlit não está instalado. Instale com 'pip install streamlit' e tente novamente.")
            raise SystemExit(1)

        st.title('KALKIE - Dashboard de Configuração')
        st.write('Use o assistente de terminal para gravar as configurações ou execute a versão Streamlit completa.')
    else:
        run_setup()
