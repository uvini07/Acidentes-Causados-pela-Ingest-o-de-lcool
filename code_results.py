import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
from termcolor import colored


df = pd.read_csv("accidents_2017_to_2023_portugues.csv")
df.head(50)


# Calcular percentual das causas de acidente
causas_pct = (
    df['causa_acidente']
    .value_counts(normalize=True) * 100
).round(2).reset_index()

# Renomear colunas
causas_pct.columns = ["Causa do Acidente", "Percentual (%)"]

# Selecionar top 15
top_causas = causas_pct.head(15)

# Criar figura
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis("off")  # Remove os eixos

# Criar tabela formatada
tabela = ax.table(
    cellText=top_causas.values,
    colLabels=top_causas.columns,
    cellLoc="center",
    loc="center"
)

# Estilizar tabela
tabela.auto_set_font_size(False)
tabela.set_fontsize(10)
tabela.scale(1.2, 1.2)

# Cor do cabeçalho
for (row, col), cell in tabela.get_celld().items():
    if row == 0:  # cabeçalho
        cell.set_text_props(weight="bold", color="white")
        cell.set_facecolor("#2c3e50")
    elif row % 2 == 0:  # linhas pares
        cell.set_facecolor("#ecf0f1")
    else:  # linhas ímpares
        cell.set_facecolor("#ffffff")

plt.title("Top 15 Causas de Acidentes (%)", fontsize=14, weight="bold")
plt.show()



# Criar coluna de hora e agrupar de 2 em 2 horas
df["hora"] = pd.to_datetime(df["horario"], errors="coerce").dt.hour
df["faixa_hora"] = (df["hora"] // 2) * 2  # arredonda para baixo de 2 em 2

# -----------------
# H4: Colisão traseira (manhã) vs. Álcool (noite)
# -----------------
colisao_traseira = df[df["tipo_acidente"] == "Colisão traseira"].groupby("faixa_hora").size()
alcool = df[df["causa_acidente"].str.contains("Falta de Atenção à Condução", case=False, na=False)].groupby("faixa_hora").size()

plt.figure(figsize=(10,5))
plt.plot(colisao_traseira.index, colisao_traseira.values, marker="o", label="Colisão Traseira (manhã)")
plt.plot(alcool.index, alcool.values, marker="s", label="Falta de atenção")
plt.xticks(range(0, 24, 2))
plt.xlabel("Hora do dia (agrupado de 2 em 2)")
plt.ylabel("Número de acidentes")
plt.title("H4 - Colisão traseira x Álcool ao longo do dia")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()

# Filtrar apenas "Falta de Atenção à Condução" em RETAS
df_falta_atencao_reta = df[
    (df["causa_acidente"] == "Falta de Atenção à Condução") &
    (df["tracado_via"] == "Reta")
].copy()

# Criar coluna combinando tipo_pista + tracado_via (aqui sempre será '... | Reta')
df_falta_atencao_reta["pista_tracado"] = (
    df_falta_atencao_reta["tipo_pista"].astype(str) + " | " + df_falta_atencao_reta["tracado_via"].astype(str)
)

# Tabela de frequência: pista+traçado x tipo de acidente
pista_tracado_acidente = pd.crosstab(
    df_falta_atencao_reta["pista_tracado"],
    df_falta_atencao_reta["tipo_acidente"]
)

# Plotar heatmap (sem filtro de >=5000, mas pode colocar de novo se quiser)
plt.figure(figsize=(16,8))
sns.heatmap(pista_tracado_acidente, annot=True, fmt="d", cmap="OrRd")
plt.title("Falta de Atenção à Condução em RETAS - Distribuição de Tipo de Acidente por Tipo de Pista")
plt.xlabel("Tipo de Acidente")
plt.ylabel("Tipo de Pista + Traçado (Reta)")
plt.xticks(rotation=45, ha="right")
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Filtrar apenas colisões traseiras
colisao_traseira = df[df["tipo_acidente"] == "Colisão traseira"]

# ------------------------------
# 1. Top 10 causas de colisão traseira
# ------------------------------
causas = colisao_traseira["causa_acidente"].value_counts().head(10)
    
plt.figure(figsize=(10,5))
sns.barplot(x=causas.values, y=causas.index, palette="viridis")
plt.title("Top 10 causas de Colisão Traseira")
plt.xlabel("Quantidade de Acidentes")
plt.ylabel("Causa do Acidente")
plt.show()


# ------------------------------
# 2. Proporção da 'Falta de Atenção' nas colisões traseiras
# ------------------------------
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


# ------------------------------
# 3. Evolução temporal da Falta de Atenção em colisões traseiras
# ------------------------------
# (ajuste a coluna de ano conforme seu dataset, ex: 'ano', 'data', etc.)
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


# ------------------------------
# 4. Gravidade dos acidentes por causa (top 5 causas)
# ------------------------------
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


# Filtrar acidentes por falta de atenção
mask = df['causa_acidente'].str.upper().str.contains("FALTA DE ATENÇÃO", na=False)
df_falta = df[mask]

# Usar a coluna de classificação (leve, grave, fatal, etc.)
grav_counts = df_falta['classificacao_acidente'].value_counts(normalize=True) * 100

# Gerar paleta variando de tons claros até escuros de azul
colors = plt.cm.Blues_r(np.linspace(0.3, 1, len(grav_counts)))

# Gráfico de pizza
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
