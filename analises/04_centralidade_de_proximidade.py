from comum import *

rel = Relatorio("analise04", "ANÁLISE 4. Centralidade de proximidade")

# wf_improved=True é a correção de Wasserman e Faust, que reduz o valor de quem está em componente pequeno
proximidade = pd.Series(nx.closeness_centrality(G, wf_improved=True)).sort_values(ascending=False)
proximidade.index = [nome(v) for v in proximidade.index]
rel.tabela(proximidade.round(3))
rel.salvar()

top = pd.concat([proximidade.head(8), proximidade.tail(4)]).iloc[::-1]
fig, ax = plt.subplots(figsize=(8, 4.8))
ax.barh(top.index, top.values, color=COR_BARRA, height=0.6)
for y, v in enumerate(top.values):
    ax.text(v + 0.01, y, f"{v:.2f}", va="center", fontsize=8, color="#52514e")
ax.axhline(3.5, color="#52514e", linestyle="--", lw=0.8)
ax.set_xlabel("proximidade (closeness)")
ax.set_title("Proximidade: os 8 maiores valores e os 4 menores")
ax.grid(axis="y", visible=False)
salvar(fig, "fig04_proximidade")
