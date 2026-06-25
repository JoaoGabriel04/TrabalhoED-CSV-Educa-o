import csv
import os
import datetime

NOME_ARQUIVO = "student-mat.csv"
SEPARADOR = ";"

# =============================================================
# MÓDULO 1 e 2 — IMPORTAÇÃO E VALIDAÇÃO DE DADOS
# =============================================================

def importar_csv(caminho_arquivo=NOME_ARQUIVO, separador=SEPARADOR):
    cabecalho = []
    linhas = []

    try:
        with open(caminho_arquivo, mode="r", encoding="utf-8") as arquivo:
            leitor = csv.reader(arquivo, delimiter=separador)
            cabecalho = next(leitor)

            for linha in leitor:
                if linha:
                    linhas.append(linha)

    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{caminho_arquivo}' não foi encontrado.")
    except StopIteration:
        print(f"[ERRO] O arquivo '{caminho_arquivo}' está vazio.")
    except UnicodeDecodeError:
        print("[ERRO] Problema de codificação ao ler o arquivo.")
    except Exception as erro:
        print(f"[ERRO] Ocorreu um problema inesperado: {erro}")

    return cabecalho, linhas

def validar_importacao(cabecalho, linhas, total_colunas_esperado=33):
    if not cabecalho or not linhas:
        print("[AVISO] Nenhum dado foi importado.")
        return False

    if len(cabecalho) != total_colunas_esperado:
        print(
            f"[AVISO] Esperado {total_colunas_esperado} colunas, "
            f"mas o cabeçalho tem {len(cabecalho)}."
        )

    linhas_invalidas = [
        i for i, linha in enumerate(linhas, start=1)
        if len(linha) != len(cabecalho)
    ]

    if linhas_invalidas:
        print(
            f"[AVISO] {len(linhas_invalidas)} linha(s) com número de "
            f"colunas diferente do cabeçalho: {linhas_invalidas[:5]}"
        )
        return False

    return True


def listas_para_dicionarios(cabecalho, linhas):
    dados = []
    for linha in linhas:
        dicionario = {}
        for i, valor in enumerate(linha):
            try:
                dicionario[cabecalho[i]] = int(valor)
            except ValueError:
                dicionario[cabecalho[i]] = valor
        dados.append(dicionario)
    return dados


# =============================================================
# MÓDULO 3 — CONSULTAS
# =============================================================

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def buscar_por_campo(dados, campo, valor):
    resultado = []
    for registro in dados:
        v = registro.get(campo)
        if isinstance(v, int):
            try:
                if v == int(valor):
                    resultado.append(registro)
            except ValueError:
                pass
        else:
            if str(valor).lower() in str(v).lower():
                resultado.append(registro)
    return resultado


def filtrar_por_condicao(dados, campo, operador, valor):
    resultado = []
    for registro in dados:
        v = registro.get(campo)
        try:
            v_cmp = int(v) if isinstance(v, int) else v
            val_cmp = int(valor) if isinstance(v, int) else valor
        except (ValueError, TypeError):
            continue
        if operador == "=" and v_cmp == val_cmp:
            resultado.append(registro)
        elif operador == ">" and v_cmp > val_cmp:
            resultado.append(registro)
        elif operador == "<" and v_cmp < val_cmp:
            resultado.append(registro)
        elif operador == ">=" and v_cmp >= val_cmp:
            resultado.append(registro)
        elif operador == "<=" and v_cmp <= val_cmp:
            resultado.append(registro)
    return resultado


def ordenar_dados(dados, campo, crescente=True):
    lista = list(dados)
    for i in range(1, len(lista)):
        chave = lista[i]
        val_chave = chave.get(campo)
        j = i - 1
        if crescente:
            while j >= 0 and lista[j].get(campo) > val_chave:
                lista[j + 1] = lista[j]
                j -= 1
        else:
            while j >= 0 and lista[j].get(campo) < val_chave:
                lista[j + 1] = lista[j]
                j -= 1
        lista[j + 1] = chave
    return lista


# =============================================================
# MÓDULO 4 — ESTATÍSTICAS
# =============================================================

def calcular_media(dados, campo):
    valores = [r[campo] for r in dados if isinstance(r.get(campo), int)]
    if not valores:
        return 0.0
    return sum(valores) / len(valores)


def calcular_maximo(dados, campo):
    valores = [r[campo] for r in dados if isinstance(r.get(campo), int)]
    if not valores:
        return None
    maximo = valores[0]
    for v in valores[1:]:
        if v > maximo:
            maximo = v
    return maximo


def calcular_minimo(dados, campo):
    valores = [r[campo] for r in dados if isinstance(r.get(campo), int)]
    if not valores:
        return None
    minimo = valores[0]
    for v in valores[1:]:
        if v < minimo:
            minimo = v
    return minimo


def calcular_soma(dados, campo):
    return sum(r[campo] for r in dados if isinstance(r.get(campo), int))


def calcular_frequencia(dados, campo):
    freq = {}
    for r in dados:
        v = r.get(campo)
        if v is not None:
            freq[v] = freq.get(v, 0) + 1
    return freq


def calcular_percentual(dados, campo):
    freq = calcular_frequencia(dados, campo)
    total = sum(freq.values())
    if total == 0:
        return {}
    return {k: round(v / total * 100, 2) for k, v in freq.items()}


def gerar_ranking(dados, campo, top_n=10, crescente=False):
    ordenados = ordenar_dados(dados, campo, crescente)
    return ordenados[:top_n]


def gerar_eda(dados):
    linhas = []
    sep = "=" * 60
    linhas.append(sep)
    linhas.append("   ANÁLISE EXPLORATÓRIA DE DADOS (EDA)")
    linhas.append("   Dataset: Student Performance — Matemática")
    linhas.append(sep)
    linhas.append(f"\nTotal de registros: {len(dados)}")

    linhas.append("\n--- Distribuição de Notas ---")
    for campo in ["G1", "G2", "G3"]:
        media = calcular_media(dados, campo)
        maximo = calcular_maximo(dados, campo)
        minimo = calcular_minimo(dados, campo)
        linhas.append(f"  {campo}: média={media:.2f}  máx={maximo}  mín={minimo}")

    linhas.append("\n--- Distribuição por Escola ---")
    freq_escola = calcular_frequencia(dados, "school")
    pct_escola = calcular_percentual(dados, "school")
    for escola, qtd in freq_escola.items():
        linhas.append(f"  {escola}: {qtd} alunos ({pct_escola[escola]:.1f}%)")

    linhas.append("\n--- Distribuição por Sexo ---")
    freq_sexo = calcular_frequencia(dados, "sex")
    pct_sexo = calcular_percentual(dados, "sex")
    for sexo, qtd in freq_sexo.items():
        label = "Feminino" if sexo == "F" else "Masculino"
        linhas.append(f"  {label}: {qtd} alunos ({pct_sexo[sexo]:.1f}%)")

    linhas.append("\n--- Top 5 Alunos por Nota Final (G3) ---")
    top5 = gerar_ranking(dados, "G3", top_n=5, crescente=False)
    for i, aluno in enumerate(top5, 1):
        linhas.append(
            f"  {i}. Escola={aluno['school']}  Sexo={aluno['sex']}"
            f"  G1={aluno['G1']}  G2={aluno['G2']}  G3={aluno['G3']}"
        )

    linhas.append("\n--- Top 5 Alunos com Mais Faltas ---")
    top5_faltas = gerar_ranking(dados, "absences", top_n=5, crescente=False)
    for i, aluno in enumerate(top5_faltas, 1):
        linhas.append(
            f"  {i}. Escola={aluno['school']}  Sexo={aluno['sex']}"
            f"  Faltas={aluno['absences']}  G3={aluno['G3']}"
        )

    linhas.append("\n--- Média de G3 por Tempo de Estudo (studytime 1–4) ---")
    for nivel in [1, 2, 3, 4]:
        grupo = [r for r in dados if r.get("studytime") == nivel]
        if grupo:
            media_g3 = calcular_media(grupo, "G3")
            linhas.append(
                f"  Nível {nivel}: {len(grupo)} alunos  média G3={media_g3:.2f}"
            )

    linhas.append("\n" + sep)
    return "\n".join(linhas)


def gerar_relatorio(dados, info):
    sep = "=" * 50
    linhas = []

    linhas.append(sep)
    linhas.append("   RELATÓRIO FINAL — DASHBOARD ESTATÍSTICO")
    linhas.append(sep)
    linhas.append(f"Disciplina  : {info['disciplina']}")
    linhas.append(f"Grupo/Alunos: {info['grupo']}")
    linhas.append(f"Data        : {info['data']}")
    linhas.append(f"Dataset     : student-mat.csv | {len(dados)} registros | {len(dados[0])} colunas")
    linhas.append(f"Gerado em   : {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    linhas.append(sep)

    linhas.append("\n--- 1. ESTATÍSTICAS GERAIS DAS NOTAS ---")
    for campo in ["G1", "G2", "G3"]:
        media = calcular_media(dados, campo)
        maximo = calcular_maximo(dados, campo)
        minimo = calcular_minimo(dados, campo)
        soma = calcular_soma(dados, campo)
        linhas.append(
            f"  {campo} | Média: {media:.2f}  Máx: {maximo}  Mín: {minimo}  Soma: {soma}"
        )

    linhas.append("\n--- 2. DISTRIBUIÇÕES CATEGÓRICAS ---")
    for campo in ["school", "sex", "address", "famsize", "Pstatus", "higher"]:
        freq = calcular_frequencia(dados, campo)
        pct = calcular_percentual(dados, campo)
        partes = "  ".join(
            f"{k}: {freq[k]} ({pct[k]:.1f}%)" for k in sorted(freq.keys(), key=str)
        )
        linhas.append(f"  [{campo}]  {partes}")

    linhas.append("\n--- 3. RANKINGS ---")
    linhas.append("  Top 10 por G3 (maior → menor):")
    for i, r in enumerate(gerar_ranking(dados, "G3", top_n=10, crescente=False), 1):
        linhas.append(
            f"    {i:>2}. Escola={r['school']}  Sexo={r['sex']}"
            f"  G1={r['G1']}  G2={r['G2']}  G3={r['G3']}"
        )

    linhas.append("\n  Top 10 por absences (maior → menor):")
    for i, r in enumerate(gerar_ranking(dados, "absences", top_n=10, crescente=False), 1):
        linhas.append(
            f"    {i:>2}. Escola={r['school']}  Sexo={r['sex']}"
            f"  Faltas={r['absences']}  G3={r['G3']}"
        )

    linhas.append("\n--- 4. ANÁLISE EXPLORATÓRIA COMPLETA (EDA) ---")
    linhas.append(gerar_eda(dados))

    linhas.append("\n" + sep)
    linhas.append("   FIM DO RELATÓRIO")
    linhas.append(sep)

    return "\n".join(linhas)


# =============================================================
# MENUS
# =============================================================#

LEGENDAS_CAMPOS = {
    "school":    "GP / MS",
    "sex":       "F / M",
    "address":   "U / R",
    "famsize":   "LE3 / GT3",
    "Pstatus":   "T / A",
    "Mjob":      "teacher / health / services / at_home / other",
    "Fjob":      "teacher / health / services / at_home / other",
    "reason":    "home / school / course / other",
    "guardian":  "mother / father / other",
    "schoolsup": "yes / no",
    "famsup":    "yes / no",
    "paid":      "yes / no",
    "activities":"yes / no",
    "nursery":   "yes / no",
    "higher":    "yes / no",
    "internet":  "yes / no",
    "romantic":  "yes / no",
}


def resolver_campo(dados, campo):
    for c in dados[0].keys():
        if c.lower() == campo.lower():
            return c
    return None


def exibir_registros(registros, limite=20):
    if not registros:
        print("\n[INFO] Nenhum registro encontrado.")
        return
    total = len(registros)
    print(f"\n{total} registro(s) encontrado(s). Exibindo até {limite}:\n")
    cabecalho = list(registros[0].keys())
    print("  ".join(f"{c:<10}" for c in cabecalho))
    print("-" * (12 * len(cabecalho)))
    for r in registros[:limite]:
        print("  ".join(f"{str(r[c]):<10}" for c in cabecalho))


def menu_consultas(dados):
    while True:
        limpar_tela()
        print("=" * 42)
        print("   CONSULTAS")
        print("=" * 42)
        print("[1] Buscar por campo")
        print("[2] Filtrar por condição")
        print("[3] Ordenar registros")
        print("[0] Voltar ao menu principal")
        opcao = input("\nEscolha: ").strip()

        if opcao == "1":
            limpar_tela()
            print("Campos disponíveis:")
            print(list(dados[0].keys()), "\n")
            campo = resolver_campo(dados, input("Campo: ").strip())
            if not campo:
                print("[ERRO] Campo não encontrado.")
                input("\nPressione Enter para continuar...")
                continue
            legenda = LEGENDAS_CAMPOS.get(campo, "")
            prompt_valor = f"Valor ({legenda}): " if legenda else "Valor: "
            valor = input(prompt_valor).strip()
            resultado = buscar_por_campo(dados, campo, valor)
            exibir_registros(resultado)
            input("\nPressione Enter para continuar...")

        elif opcao == "2":
            limpar_tela()
            print("Campos disponíveis:")
            print(list(dados[0].keys()), "\n")
            campo = resolver_campo(dados, input("Campo: ").strip())
            if not campo:
                print("[ERRO] Campo não encontrado.")
                input("\nPressione Enter para continuar...")
                continue
            print("Operadores disponíveis: =  >  <  >=  <=")
            operador = input("Operador: ").strip()
            if operador != "=" and not isinstance(dados[0].get(campo), int):
                print(f"\n[AVISO] O campo '{campo}' é texto — só aceita o operador '='.")
                print("        Use '=' para encontrar registros com valor exato.")
                input("\nPressione Enter para continuar...")
                continue
            legenda = LEGENDAS_CAMPOS.get(campo, "")
            prompt_valor = f"Valor ({legenda}): " if legenda else "Valor: "
            valor = input(prompt_valor).strip()
            resultado = filtrar_por_condicao(dados, campo, operador, valor)
            exibir_registros(resultado)
            input("\nPressione Enter para continuar...")

        elif opcao == "3":
            limpar_tela()
            print("Campos disponíveis:")
            print(list(dados[0].keys()), "\n")
            campo = resolver_campo(dados, input("Campo para ordenar: ").strip())
            if not campo:
                print("[ERRO] Campo não encontrado.")
                input("\nPressione Enter para continuar...")
                continue
            direcao = input("Direção [c = crescente  /  d = decrescente]: ").strip().lower()
            crescente = direcao != "d"
            resultado = ordenar_dados(dados, campo, crescente)
            exibir_registros(resultado)
            input("\nPressione Enter para continuar...")

        elif opcao == "0":
            break


def menu_estatisticas(dados):
    while True:
        limpar_tela()
        print("=" * 42)
        print("   ESTATÍSTICAS E EDA")
        print("=" * 42)
        print("[1] Estatísticas de campo numérico")
        print("[2] Frequência e percentual por categoria")
        print("[3] Ranking de registros")
        print("[4] Análise Exploratória (EDA)")
        print("[0] Voltar ao menu principal")
        opcao = input("\nEscolha: ").strip()

        if opcao == "1":
            limpar_tela()
            campos_num = [k for k, v in dados[0].items() if isinstance(v, int)]
            print("Campos numéricos disponíveis:")
            print(campos_num, "\n")
            campo = resolver_campo(dados, input("Campo: ").strip())
            if not campo:
                print("[ERRO] Campo não encontrado.")
                input("\nPressione Enter para continuar...")
                continue
            print(f"\n  Média : {calcular_media(dados, campo):.2f}")
            print(f"  Máximo: {calcular_maximo(dados, campo)}")
            print(f"  Mínimo: {calcular_minimo(dados, campo)}")
            print(f"  Soma  : {calcular_soma(dados, campo)}")
            input("\nPressione Enter para continuar...")

        elif opcao == "2":
            limpar_tela()
            print("Campos disponíveis:")
            print(list(dados[0].keys()), "\n")
            campo = resolver_campo(dados, input("Campo: ").strip())
            if not campo:
                print("[ERRO] Campo não encontrado.")
                input("\nPressione Enter para continuar...")
                continue
            freq = calcular_frequencia(dados, campo)
            pct = calcular_percentual(dados, campo)
            print(f"\n  {'Categoria':<20} {'Qtd':>6} {'%':>8}")
            print("  " + "-" * 36)
            for cat in sorted(freq.keys(), key=str):
                print(f"  {str(cat):<20} {freq[cat]:>6} {pct[cat]:>7.1f}%")
            input("\nPressione Enter para continuar...")

        elif opcao == "3":
            limpar_tela()
            campos_num = [k for k, v in dados[0].items() if isinstance(v, int)]
            print("Campos numéricos disponíveis:")
            print(campos_num, "\n")
            campo = resolver_campo(dados, input("Campo: ").strip())
            if not campo:
                print("[ERRO] Campo não encontrado.")
                input("\nPressione Enter para continuar...")
                continue
            try:
                top_n = int(input("Quantos registros no ranking? "))
            except ValueError:
                top_n = 10
            direcao = input("Direção [c = crescente  /  d = decrescente]: ").strip().lower()
            crescente = direcao != "d"
            resultado = gerar_ranking(dados, campo, top_n, crescente)
            exibir_registros(resultado, limite=top_n)
            input("\nPressione Enter para continuar...")

        elif opcao == "4":
            limpar_tela()
            print(gerar_eda(dados))
            input("\nPressione Enter para continuar...")

        elif opcao == "0":
            break


def menu_relatorio(dados):
    limpar_tela()
    print("=" * 50)
    print("   GERAR RELATÓRIO TXT")
    print("=" * 50)
    print()
    disciplina = input("Disciplina: ").strip()
    grupo = input("Grupo/Alunos: ").strip()
    data = input("Data (ex: 25/06/2026): ").strip()

    info = {"disciplina": disciplina, "grupo": grupo, "data": data}
    relatorio = gerar_relatorio(dados, info)

    limpar_tela()
    print("Prévia do relatório (primeiras 20 linhas):\n")
    for linha in relatorio.split("\n")[:20]:
        print(linha)
    print("\n[...]\n")

    nome = input("Nome do arquivo para salvar: ").strip() or "relatorio_final"
    if not nome.endswith(".txt"):
        nome += ".txt"

    with open(nome, "w", encoding="utf-8") as f:
        f.write(relatorio)

    print(f"\n[OK] Relatório salvo em '{nome}'.")
    input("\nPressione Enter para continuar...")


def menu_principal(dados):
    while True:
        limpar_tela()
        print("=" * 50)
        print("   DASHBOARD ESTATÍSTICO — STUDENT MAT")
        print("=" * 50)
        print(f"   Total de registros carregados: {len(dados)}")
        print()
        print("[1] Consultas")
        print("[2] Estatísticas e EDA")
        print("[3] Gerar Relatório TXT")
        print("[0] Sair")
        opcao = input("\nEscolha: ").strip()

        if opcao == "1":
            menu_consultas(dados)
        elif opcao == "2":
            menu_estatisticas(dados)
        elif opcao == "3":
            menu_relatorio(dados)
        elif opcao == "0":
            limpar_tela()
            print("Encerrando. Até logo!")
            break


if __name__ == "__main__":
    cabecalho, linhas = importar_csv()

    if validar_importacao(cabecalho, linhas):
        dados = listas_para_dicionarios(cabecalho, linhas)
        menu_principal(dados)
