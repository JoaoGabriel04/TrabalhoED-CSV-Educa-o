import csv
import os

NOME_ARQUIVO = "student-mat.csv"
SEPARADOR = ";"

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


# =============================================================
# MENUS
# =============================================================

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
            valor = input("Valor: ").strip()
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
            valor = input("Valor: ").strip()
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
            print("[a] Exibir no terminal")
            print("[b] Salvar em arquivo TXT")
            print("[c] Ambos")
            sub = input("\nEscolha: ").strip().lower()
            relatorio = gerar_eda(dados)
            if sub in ("a", "c"):
                limpar_tela()
                print(relatorio)
            if sub in ("b", "c"):
                with open("eda_relatorio.txt", "w", encoding="utf-8") as f:
                    f.write(relatorio)
                print("\n[OK] Relatório salvo em 'eda_relatorio.txt'.")
            input("\nPressione Enter para continuar...")

        elif opcao == "0":
            break


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
        print("[0] Sair")
        opcao = input("\nEscolha: ").strip()

        if opcao == "1":
            menu_consultas(dados)
        elif opcao == "2":
            menu_estatisticas(dados)
        elif opcao == "0":
            limpar_tela()
            print("Encerrando. Até logo!")
            break


if __name__ == "__main__":
    cabecalho, linhas = importar_csv()

    if validar_importacao(cabecalho, linhas):
        dados = listas_para_dicionarios(cabecalho, linhas)
        menu_principal(dados)
