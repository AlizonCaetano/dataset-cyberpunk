from comum import *

rel = Relatorio("analise10", "ANÁLISE 10. Distribuição dos graus")

contagem = Counter(d for _, d in G.degree())
rel.escrever("personagens por grau (grau: quantidade):")
rel.escrever(", ".join(f"{g}: {n}" for g, n in sorted(contagem.items())))
rel.escrever(f"assortatividade de grau: {nx.degree_assortativity_coefficient(G):.3f}")
rel.salvar()

grau_david = G.degree("DavidMartinez")
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(list(contagem.keys()), list(contagem.values()), color=COR_BARRA, width=0.7)
ax.set_xlabel("grau (número de personagens diferentes com quem interage)")
ax.set_ylabel("número de personagens")
ax.set_xticks(sorted(contagem))
ax.annotate("David", (grau_david, contagem[grau_david]), textcoords="offset points", xytext=(0, 6),
            ha="center", fontsize=8)
ax.set_title("Distribuição dos graus")
ax.grid(axis="x", visible=False)
salvar(fig, "fig10_distribuicao_dos_graus")
