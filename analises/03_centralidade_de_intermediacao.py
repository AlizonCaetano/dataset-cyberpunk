from comum import *

rel = Relatorio("analise03", "ANÁLISE 3. Centralidade de intermediação")

# sem peso: aqui o peso é número de cenas (proximidade) e o algoritmo trataria peso como distância
intermediacao = pd.Series(nx.betweenness_centrality(G, normalized=True)).sort_values(ascending=False)
intermediacao.index = [nome(v) for v in intermediacao.index]
rel.tabela(intermediacao.round(3).head(12))
rel.salvar()

top = intermediacao.head(10).iloc[::-1]
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(top.index, top.values, color=COR_BARRA, height=0.6)
for y, v in enumerate(top.values):
    ax.text(v + 0.01, y, f"{v:.2f}", va="center", fontsize=8, color="#52514e")
ax.set_xlabel("intermediação normalizada (betweenness)")
ax.set_title("Os 10 personagens com maior intermediação")
ax.grid(axis="y", visible=False)
salvar(fig, "fig03_intermediacao")
