from comum import *

rel = Relatorio("analise09", "ANÁLISE 9. Viradas de sinal entre pares")

# para cada par, a sequência dos sinais em ordem de episódio e minuto
ordenado = df.sort_values(["episodio", "minuto"])
ordenado = ordenado.assign(par=[" e ".join(sorted([nome(a), nome(b)]))
                                for a, b in zip(ordenado["personagem1"], ordenado["personagem2"])])
sequencias = ordenado.groupby("par")["sinal"].apply(list)
viradas = sequencias[sequencias.apply(lambda s: "+" in s and "-" in s)]   # par com + e - tem virada
rel.escrever(f"pares com virada de sinal: {len(viradas)} de {len(sequencias)}\n")
for par, s in viradas.items():
    rel.escrever(f"{par:34s} {' '.join(s)}")
rel.salvar()

ordem_ep = {ep: i for i, ep in enumerate(EPISODIOS)}
MARCA = {"+": "o", "-": "s", "0": "D"}
fig, ax = plt.subplots(figsize=(10, 0.8 + 0.42 * len(viradas)))
for y, par in enumerate(viradas.index):
    sub = ordenado[ordenado["par"] == par]
    x = [ordem_ep[e] + int(m[:2]) / 25 for e, m in zip(sub["episodio"], sub["minuto"])]
    ax.plot(x, [y] * len(x), color="#d7d6d1", lw=1, zorder=1)
    for xi, s in zip(x, sub["sinal"]):
        ax.scatter(xi, y, color=COR_SINAL[s], marker=MARCA[s], s=34, zorder=2, edgecolors="white", linewidths=0.6)
ax.set_yticks(range(len(viradas)))
ax.set_yticklabels(viradas.index, fontsize=8)
ax.set_xticks(range(len(EPISODIOS)))
ax.set_xticklabels([f"E{int(e[1:])}" for e in EPISODIOS])
ax.set_xlabel("episódio (cada ponto é uma cena, na ordem do minuto)")
ax.grid(axis="y", visible=False)
ax.legend(handles=[Line2D([0], [0], marker=MARCA[s], color="w", markerfacecolor=COR_SINAL[s], markersize=7,
                          label=NOME_SINAL[s]) for s in ["+", "-", "0"]],
          title="Sinal", loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=8, title_fontsize=8)
ax.set_title("Pares que mudam de sinal ao longo da temporada")
salvar(fig, "fig09_viradas_de_sinal")
