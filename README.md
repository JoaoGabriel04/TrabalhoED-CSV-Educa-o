# Dashboard Estatístico de Dados Públicos

## Proposta do Trabalho

Este projeto é o trabalho final da disciplina de **Estrutura de Dados**. O objetivo principal é fixar os conteúdos relacionados à estrutura de dados, implementando um sistema completo de análise de dados sem recorrer a bibliotecas prontas ou inteligência artificial.

Cada grupo deve escolher um conjunto de dados público no formato CSV (neste caso, utilizamos o dataset de desempenho escolar de estudantes do Ensino Médio português disponível no UCI Machine Learning Repository) e desenvolver os seguintes módulos:

| Módulo | Descrição |
|---|---|
| **1 — Importação** | Ler o arquivo CSV e carregar os dados |
| **2 — Armazenamento** | Armazenar os dados em uma **lista de dicionários** |
| **3 — Consultas** | Buscar, filtrar e ordenar registros |
| **4 — Estatísticas** | Calcular média, máximo, mínimo, soma, percentual, frequência por categoria e rankings |
| **5 — Relatório** | Gerar um arquivo TXT, DOCX ou PDF com cabeçalho e informações consolidadas |

Além disso, o módulo 4 inclui uma **Análise Exploratória de Dados (EDA)**, permitindo extrair *insights* sobre a base para enriquecer o relatório final.

---

## Dataset: Student Mat — Desempenho Escolar

Os dados foram extraídos do [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Student+Performance) e referem-se ao desempenho de estudantes de Matemática em duas escolas portuguesas. Abaixo, a descrição detalhada de cada coluna.

### Identificação da Escola e Dados Pessoais

| Coluna | Descrição |
|---|---|
| `school` | Escola do aluno: `GP` (Gabriel Pereira) ou `MS` (Mousinho da Silveira) |
| `sex` | Sexo do estudante: `F` (feminino) ou `M` (masculino) |
| `age` | Idade do estudante (numérica, 15 a 22 anos) |
| `address` | Tipo de endereço residencial: `U` (urbano) ou `R` (rural) |

### Estrutura Familiar

| Coluna | Descrição |
|---|---|
| `famsize` | Tamanho da família: `LE3` (≤ 3 pessoas) ou `GT3` (> 3 pessoas) |
| `Pstatus` | Situação de convivência dos pais: `T` (vivem juntos) ou `A` (vivem separados) |

### Escolaridade e Profissão dos Pais

| Coluna | Descrição |
|---|---|
| `Medu` | Escolaridade da mãe: 0 (nenhuma), 1 (ensino primário/4ª série), 2 (5ª a 9ª série), 3 (ensino secundário), 4 (ensino superior) |
| `Fedu` | Escolaridade do pai (mesma escala de Medu) |
| `Mjob` | Profissão da mãe: `teacher` (professor), `health` (saúde), `services` (serviços), `at_home` (do lar), `other` (outro) |
| `Fjob` | Profissão do pai (mesmas categorias de Mjob) |

### Contexto Escolar

| Coluna | Descrição |
|---|---|
| `reason` | Motivo da escolha da escola: `home` (proximidade de casa), `school` (reputação), `course` (preferência pelo curso), `other` (outro) |
| `guardian` | Responsável legal: `mother` (mãe), `father` (pai), `other` (outro) |
| `traveltime` | Tempo de deslocamento até a escola (escala de 1 a 4, sendo 1 o menor e 4 o maior) |
| `studytime` | Tempo semanal de estudo (escala de 1 a 4) |
| `failures` | Número de reprovações anteriores (0 a 3, sendo 3 usado para 4 ou mais) |

### Apoio e Atividades

| Coluna | Descrição |
|---|---|
| `schoolsup` | Apoio educacional extra da escola (`yes`/`no`) |
| `famsup` | Apoio educacional da família (`yes`/`no`) |
| `paid` | Aulas particulares pagas da disciplina (`yes`/`no`) |
| `activities` | Participação em atividades extracurriculares (`yes`/`no`) |
| `nursery` | Se frequentou a creche (`yes`/`no`) |
| `higher` | Se quer cursar o ensino superior (`yes`/`no`) |
| `internet` | Acesso à internet em casa (`yes`/`no`) |
| `romantic` | Se está em um relacionamento amoroso (`yes`/`no`) |

### Qualidade de Vida e Hábitos

| Coluna | Descrição |
|---|---|
| `famrel` | Qualidade do relacionamento familiar (1 — muito ruim a 5 — excelente) |
| `freetime` | Tempo livre após a escola (1 a 5) |
| `goout` | Frequência de saídas com amigos (1 a 5) |
| `Dalc` | Consumo de álcool em dias de semana (1 — muito baixo a 5 — muito alto) |
| `Walc` | Consumo de álcool em fins de semana (1 — muito baixo a 5 — muito alto) |
| `health` | Estado de saúde atual (1 — muito ruim a 5 — muito bom) |
| `absences` | Número de faltas escolares (0 a 93) |

### Notas (Alvo Principal da Análise)

| Coluna | Descrição |
|---|---|
| `G1` | Nota do primeiro período (0 a 20) |
| `G2` | Nota do segundo período (0 a 20) |
| `G3` | Nota final do ano (0 a 20) |

> **Observação:** Conforme mencionado no paper original, G3 tem forte correlação com G1 e G2, já que é a nota final emitida no terceiro período. Prever G3 sem considerar G1 e G2 é mais difícil, porém mais útil para cenários reais de predição precoce.

---

## Cronograma

| Data | Entrega |
|---|---|
| 18/06 | Módulos 1 e 2 |
| 25/06 | Módulos 3 e 4 |
| 30/06 | Módulo 5 (entrega final) |

---

## Estrutura do Projeto

```
/
├── main.py           # Código principal do projeto
├── student-mat.csv   # Base de dados utilizada
├── Escopo.pdf        # Documento de escopo do trabalho
└── README.md         # Este arquivo
```
