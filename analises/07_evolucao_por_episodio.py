from comum import *

rel = Relatorio("analise07", "ANÁLISE 7. Evolução por episódio")

linhas = []
for ep in EPISODIOS:
    g, acum = G_ep[ep], G_acum[ep]
    linhas.append({
        "episodio": ep,
        "registros": int((df["episodio"] == ep).sum()),
        "vertices_ep": g.number_of_nodes(),
        "arestas_ep": g.number_of_edges(),
        "densidade_ep": round(nx.density(g), 2),
        "grau_David_ep": g.degree("DavidMartinez") if "DavidMartinez" in g else 0,
        "vertices_acum": acum.number_of_nodes(),
        "densidade_acum": round(nx.density(acum), 2),
    })
evolucao = pd.DataFrame(linhas).set_index("episodio")
rel.tabela(evolucao)
rel.salvar()

rotulos = [f"E{int(e[1:])}" for e in EPISODIOS]
fig, ax = plt.subplots(figsize=(8, 3.8))
ax.plot(rotulos, evolucao["densidade_ep"], marker="o", color=COR_BARRA, lw=2, markersize=6)
for x, y in zip(rotulos, evolucao["densidade_ep"]):
    ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=8)
ax.set_ylim(0, 1)
ax.set_ylabel("densidade da rede do episódio")
ax.set_title("Densidade da rede de cada episódio")
salvar(fig, "fig07a_densidade_por_episodio")

fig, ax = plt.subplots(figsize=(8, 3.8))
ax.plot(rotulos, evolucao["vertices_acum"], marker="o", color=COR_BARRA, lw=2, markersize=6)
for x, y in zip(rotulos, evolucao["vertices_acum"]):
    ax.annotate(str(y), (x, y), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=8)
ax.set_ylim(0, evolucao["vertices_acum"].max() * 1.15)
ax.set_ylabel("personagens na rede acumulada")
ax.set_title("Personagens acumulados até cada episódio")
salvar(fig, "fig07b_personagens_acumulados")

# uma figura por episódio, com os personagens na mesma posição da rede global, para comparar
for ep in EPISODIOS:
    g = G_ep[ep]
    fig, ax = plt.subplots(figsize=(13, 10))
    desenhar_rede(ax, g, sinais=sinal_por_par(df[df["episodio"] == ep]))
    legenda_grupos(fig, g)
    legenda_sinais(fig)
    ax.set_title(f"Rede do episódio {int(ep[1:])}: {g.number_of_nodes()} personagens e {g.number_of_edges()} pares")
    salvar(fig, f"fig07c_rede_episodio_{ep[1:]}")
