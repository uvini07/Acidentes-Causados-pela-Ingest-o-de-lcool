# ==========================================================
# Análise de Acidentes de Trânsito (2017-2023)
# Autor: Marcelo Vinicius Jordão Almeida
# Descrição: Este script realiza análise exploratória, visualizações
# e estatísticas sobre acidentes de trânsito, com foco em causas, tipos
# de acidentes, horários e gravidade.
# ==========================================================

# -----------------------------
# 1. Importação das bibliotecas
# -----------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from tabulate import tabulate
from termcolor import colored

# Configurações globais para gráficos
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# -----------------------------
# 2. Leitura do dataset
# -----------------------------
df = pd.read_csv("accidents_2017_to_2023_portugues.csv")
df.head(50)  # visualização inicial dos dados

# -----------------------------
# 3. Percentual das causas de acidente
# -----------------------------
causas_pct = (
    df['causa_acidente']
    .value_counts(normalize=True) * 100
).round(2).reset_index()
causas_pct.columns = ["Causa do Acidente", "Percentual (%)"]
top_causas = causas_pct.head(15)

fig, ax = plt.subplots(figsize=(10, 6))
ax.axis("off")
tabela = ax.table(
    cellText=top_causas.values,
    colLabels=top_causas.columns,
    cellLoc="center",
    loc="center"
)
tabela.auto_set_font_size(False)
tabela.set_fontsize(10)
tabela.scale(1.2, 1.2)
for (row, col), cell in tabela.get_celld().items():
    if row == 0:
        cell.set_text_props(weight="bold", color="white")
        cell.set_facecolor("#2c3e50")
    elif row % 2 == 0:
        cell.set_facecolor("#ecf0f1")
    else:
        cell.set_facecolor("#ffffff")
plt.title("Top 15 Causas de Acidentes (%)", fontsize=14, weight="bold")
plt.show()

# -----------------------------
# 4. Criação de coluna de hora e faixa de hora
# -----------------------------
df["hora"] = pd.to_datetime(df["horario"], errors="coerce").dt.hour
df["faixa_hora"] = (df["hora"] // 2) * 2  # Agrupamento de 2 em 2 horas

# -----------------------------
# 5. Comparação dias úteis x finais de semana
# -----------------------------
# Criar coluna de dia da semana
df['dia_semana'] = pd.to_datetime(df['data'], errors='coerce').dt.dayofweek

# Categorizar dias
df['tipo_dia'] = df['dia_semana'].apply(lambda x: 'Final de Semana' if x >= 5 else 'Dia Útil')

# Agrupar número de acidentes por tipo de dia
acidentes_dia = df.groupby('tipo_dia').size()

# Plotar gráfico de barras
plt.figure(figsize=(8,5))
sns.barplot(x=acidentes_dia.index, y=acidentes_dia.values, palette="Set1")
plt.title("Comparação de Acidentes: Dias Úteis x Finais de Semana")
plt.ylabel("Número de Acidentes")
plt.xlabel("Tipo de Dia")
plt.show()

# -----------------------------
# 6. H4: Colisão traseira vs. Falta de atenção ao longo do dia
# -----------------------------
colisao_traseira = df[df["tipo_acidente"] == "Colisão traseira"].groupby("faixa_hora").size()
alcool = df[df["causa_acidente"].str.contains("Falta de Atenção à Condução", case=False, na=False)].groupby("faixa_hora").size()
plt.figure(figsize=(10,5))
plt.plot(colisao_traseira.index, colisao_traseira.values, marker="o", label="Colisão Traseira (manhã)")
plt.plot(alcool.index, alcool.values, marker="s", label="Falta de Atenção")
plt.xticks(range(0, 24, 2))
plt.xlabel("Hora do dia (agrupado de 2 em 2)")
plt.ylabel("Número de acidentes")
plt.title("H4 - Colisão traseira x Falta de Atenção ao longo do dia")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()

# -----------------------------
# 7. Falta de atenção à condução em RETAS
# -----------------------------
df_falta_atencao_reta = df[
    (df["causa_acidente"] == "Falta de Atenção à Condução") &
    (df["tracado_via"] == "Reta")
].copy()
df_falta_atencao_reta["pista_tracado"] = (
    df_falta_atencao_reta["tipo_pista"].astype(str) + " | " + df_falta_atencao_reta["tracado_via"].astype(str)
)
pista_tracado_acidente = pd.crosstab(
    df_falta_atencao_reta["pista_tracado"],
    df_falta_atencao_reta["tipo_acidente"]
)
plt.figure(figsize=(16,8))
sns.heatmap(pista_tracado_acidente, annot=True, fmt="d", cmap="OrRd")
plt.title("Falta de Atenção à Condução em RETAS - Distribuição de Tipo de Acidente por Tipo de Pista")
plt.xlabel("Tipo de Acidente")
plt.ylabel("Tipo de Pista + Traçado (Reta)")
plt.xticks(rotation=45, ha="right")
plt.show()

# -----------------------------
# 8. Análise específica de colisões traseiras
# -----------------------------
colisao_traseira = df[df["tipo_acidente"] == "Colisão traseira"]

# 8.1 Top 10 causas
causas = colisao_traseira["causa_acidente"].value_counts().head(10)
plt.figure(figsize=(10,5))
sns.barplot(x=causas.values, y=causas.index, palette="viridis")
plt.title("Top 10 causas de Colisão Traseira")
plt.xlabel("Quantidade de Acidentes")
plt.ylabel("Causa do Acidente")
plt.show()

# 8.2 Proporção de "Falta de Atenção"
causa_counts = colisao_traseira["causa_acidente"].value_counts(normalize=True) * 100
plt.figure(figsize=(6,6))
plt.pie(
    [causa_counts.get("Falta de Atenção à Condução", 0), 100 - causa_counts.get("Falta de Atenção à Condução", 0)],
    labels=["Falta de Atenção", "Outras Causas"],
    autopct="%.1f%%",
    colors=["#e63946", "#a8dadc"]
)
plt.title("Proporção da Falta de Atenção nas Colisões Traseiras")
plt.show()

# 8.3 Evolução temporal da Falta de Atenção
if "ano" in df.columns:
    evolucao = colisao_traseira.groupby("ano")["causa_acidente"].apply(
        lambda x: (x == "Falta de Atenção à Condução").sum()
    )
    plt.figure(figsize=(10,5))
    sns.lineplot(x=evolucao.index, y=evolucao.values, marker="o", color="crimson")
    plt.title("Evolução da Falta de Atenção em Colisões Traseiras")
    plt.xlabel("Ano")
    plt.ylabel("Número de Acidentes")
    plt.show()

# 8.4 Gravidade dos acidentes por causa (Top 5)
top5_causas = colisao_traseira["causa_acidente"].value_counts().head(5).index
gravidade = colisao_traseira[colisao_traseira["causa_acidente"].isin(top5_causas)].copy()
gravidade["vitimas"] = gravidade["mortos"] + gravidade["feridos_graves"] + gravidade["feridos_leves"]
plt.figure(figsize=(10,5))
sns.boxplot(x="causa_acidente", y="vitimas", data=gravidade, palette="Set2")
plt.title("Distribuição de Vítimas por Causa (Top 5)")
plt.xlabel("Causa do Acidente")
plt.ylabel("Total de Vítimas")
plt.xticks(rotation=30)
plt.show()

# -----------------------------
# 9. Gravidade dos acidentes por falta de atenção
# -----------------------------
mask = df['causa_acidente'].str.upper().str.contains("FALTA DE ATENÇÃO", na=False)
df_falta = df[mask]
grav_counts = df_falta['classificacao_acidente'].value_counts(normalize=True) * 100
colors = plt.cm.Blues_r(np.linspace(0.3, 1, len(grav_counts)))
plt.figure(figsize=(7,7))
plt.pie(
    grav_counts,
    labels=grav_counts.index,
    autopct="%.1f%%",
    startangle=140,
    colors=colors
)
plt.title("Gravidade dos Acidentes por Falta de Atenção (2017-2023)", fontsize=14, weight="bold")
plt.show()
