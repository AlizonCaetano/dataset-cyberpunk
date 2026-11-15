from comum import *

rel = Relatorio("analise13", "ANÁLISE 13. O peso de cada perda na rede")

# personagem, episódio e minuto da cena da morte
MORTES = [("GloriaMartinez", "E01", "18:54"), ("Pilar", "E04", "15:52"), ("Dorio", "E06", "18:31"),
          ("Maine", "E06", "22:49"), ("Rebecca", "E10", "20:21"), ("DavidMartinez", "E10", "23:31")]


def rede_ate(ep, minuto):
    """Rede acumulada até a cena indicada."""
    return montar_grafo(df[(df["episodio"] < ep) | ((df["episodio"] == ep) & (df["minuto"] <= minuto))])


# para cada morte: tiro o personagem da rede daquele momento e vejo o que se quebra
linhas = []
for morto, ep, minuto in MORTES:
    antes = rede_ate(ep, minuto)
    depois = antes.copy()
    depois.remove_node(morto)
    comps_antes = list(nx.connected_components(antes))
    comps_depois = list(nx.connected_components(depois))
    principal_antes = max(comps_antes, key=len)
    principal_depois = max(comps_depois, key=len)
    perderam = sorted(nome(v) for v in principal_antes - principal_depois - {morto})
    linhas.append({
        "personagem": nome(morto), "cena": f"{ep} {minuto}",
        "intermediacao": round(nx.betweenness_centrality(antes)[morto], 2),
        "componentes": f"{len(comps_antes)} -> {len(comps_depois)}",
        "maior_componente": f"{len(principal_antes)} -> {len(principal_depois)}",
        "perdem a ligação": ", ".join(perderam) if perderam else "-",
    })
impacto = pd.DataFrame(linhas).set_index("personagem")
rel.tabela(impacto)

# interações só entre membros da equipe, por episódio e sinal
EQUIPE_COMPLETA = EQUIPE | {"DavidMartinez"}
da_equipe = df[df["personagem1"].isin(EQUIPE_COMPLETA) & df["personagem2"].isin(EQUIPE_COMPLETA)]
por_ep = da_equipe.groupby(["episodio", "sinal"]).size().unstack(fill_value=0).reindex(
    index=EPISODIOS, columns=["+", "-", "0"], fill_value=0)
rel.escrever("\ninterações dentro da equipe por episódio e sinal:")
rel.tabela(por_ep)
rel.salvar()

fig, ax = plt.subplots(figsize=(8, 4.2))
ax.bar(impacto.index, impacto["intermediacao"], color=COR_BARRA, width=0.6)
for x, v in enumerate(impacto["intermediacao"]):
    ax.text(x, v + 0.015, f"{v:.2f}", ha="center", fontsize=8, color="#52514e")
ax.set_ylabel("intermediação no momento da morte")
ax.set_title("Intermediação de cada personagem na cena da sua morte")
ax.grid(axis="x", visible=False)
salvar(fig, "fig13a_intermediacao_na_morte")

fig, ax = plt.subplots(figsize=(9, 4.4))
base = None
for s in ["+", "-", "0"]:
    ax.bar(range(len(EPISODIOS)), por_ep[s], bottom=base, color=COR_SINAL[s], label=NOME_SINAL[s], width=0.62,
           edgecolor="white", linewidth=1.5)
    base = por_ep[s] if base is None else base + por_ep[s]
topo = base.max()
for morto, ep, minuto in MORTES:
    x = EPISODIOS.index(ep) + int(minuto[:2]) / 25 - 0.5
    ax.axvline(x, color="#52514e", linestyle="--", lw=0.8)
    ax.text(x + 0.04, topo * 1.12, nome(morto), rotation=90, fontsize=7.5, va="top")
ax.set_ylim(0, topo * 1.18)
ax.set_xticks(range(len(EPISODIOS)))
ax.set_xticklabels([f"E{int(e[1:])}" for e in EPISODIOS])
ax.set_ylabel("interações entre membros da equipe")
ax.set_title("Interações dentro da equipe por episódio, com as mortes marcadas")
ax.legend(title="Sinal", loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=8, title_fontsize=8)
ax.grid(axis="x", visible=False)
salvar(fig, "fig13b_equipe_e_mortes")

# a rede no momento da morte do Maine, e a mesma rede sem ele
antes = rede_ate("E06", "22:49")
depois = antes.copy()
depois.remove_node("Maine")
principal = max(nx.connected_components(depois), key=len)
COR_ESTADO = {"Maine": "#f08c00", "continua ligado": "#2a78d6", "perde a ligação": "#d62f2f"}

fig, ax = plt.subplots(figsize=(13, 10))
desenhar_rede(ax, antes, cor_vertice={v: COR_ESTADO["Maine" if v == "Maine" else "continua ligado"] for v in antes})
fig.legend(handles=[Patch(color=COR_ESTADO[k], label=k) for k in ("Maine", "continua ligado")],
           loc="lower left", bbox_to_anchor=(0.06, 0.0), fontsize=9, ncol=2)
ax.set_title("Rede acumulada até a morte do Maine (episódio 6, 22:49)")
salvar(fig, "fig13c_rede_antes_da_morte_do_maine")

fig, ax = plt.subplots(figsize=(13, 10))
desenhar_rede(ax, depois, cor_vertice={v: COR_ESTADO["continua ligado" if v in principal else "perde a ligação"]
                                      for v in depois})
fig.legend(handles=[Patch(color=COR_ESTADO[k], label=k) for k in ("continua ligado", "perde a ligação")],
           loc="lower left", bbox_to_anchor=(0.06, 0.0), fontsize=9, ncol=2)
ax.set_title("A mesma rede sem o Maine: quem perde a ligação com o grupo principal")
salvar(fig, "fig13d_rede_depois_da_morte_do_maine")
