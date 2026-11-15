from comum import *

rel = Relatorio("analise12", "ANÁLISE 12. A absorção do David pela equipe e a troca de liderança")

# que parte das interações do David, em cada episódio, é com a equipe de mercenários
linhas = []
for ep in EPISODIOS:
    do_ep = df[df["episodio"] == ep]
    do_david = do_ep[(do_ep["personagem1"] == "DavidMartinez") | (do_ep["personagem2"] == "DavidMartinez")]
    outro = do_david["personagem1"].where(do_david["personagem1"] != "DavidMartinez", do_david["personagem2"])
    linhas.append({"episodio": ep, "interacoes_David": len(do_david), "com_equipe": int(outro.isin(EQUIPE).sum())})
absorcao = pd.DataFrame(linhas).set_index("episodio")
absorcao["proporcao_equipe"] = (absorcao["com_equipe"] / absorcao["interacoes_David"]).round(2)
rel.tabela(absorcao)

# antes e depois da morte do Maine (episódio 6)
rel.escrever("")
for rotulo, parte in {"episódios 1 a 5": df[df["episodio"] <= "E05"], "episódios 6 a 10": df[df["episodio"] >= "E06"]}.items():
    h = montar_grafo(parte)
    inter = pd.Series(nx.betweenness_centrality(h)).sort_values(ascending=False).round(2)
    cenas = pd.Series(dict(h.degree(weight="weight"))).sort_values(ascending=False)
    rel.escrever(f"{rotulo}: {h.number_of_nodes()} personagens, David em {cenas['DavidMartinez']} de {len(parte)} registros")
    rel.escrever("  maiores graus ponderados: " + ", ".join(f"{nome(k)} {v}" for k, v in cenas.head(5).items()))
    rel.escrever("  maiores intermediações:   " + ", ".join(f"{nome(k)} {v}" for k, v in inter.head(5).items()))
rel.salvar()

rotulos = [f"E{int(e[1:])}" for e in absorcao.index]
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.bar(rotulos, absorcao["proporcao_equipe"] * 100, color=COR_BARRA, width=0.62)
for x, v in zip(rotulos, absorcao["proporcao_equipe"]):
    ax.text(x, v * 100 + 2, f"{v:.0%}", ha="center", fontsize=8, color="#52514e")
ax.axvline(5.42, color="#52514e", linestyle="--", lw=1)
ax.text(5.48, 104, "morte do Maine", fontsize=8, color="#52514e")
ax.set_ylim(0, 112)
ax.set_ylabel("% das interações do David com a equipe")
ax.set_title("Interações do David com a equipe de mercenários, por episódio")
ax.grid(axis="x", visible=False)
salvar(fig, "fig12_absorcao_do_david")
