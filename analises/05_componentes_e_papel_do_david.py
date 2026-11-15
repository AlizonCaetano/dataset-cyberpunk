from comum import *

rel = Relatorio("analise05", "ANÁLISE 5. Componentes conexos e o papel do David")


def componentes(grafo):
    return sorted((sorted(nome(v) for v in c) for c in nx.connected_components(grafo)), key=len, reverse=True)


rel.escrever(f"rede global: {nx.number_connected_components(G)} componente(s), o maior com "
             f"{len(componentes(G)[0])} personagens")

sem_david = G.copy()
sem_david.remove_node("DavidMartinez")
comps = componentes(sem_david)
rel.escrever(f"rede sem o David: {len(comps)} componentes, o maior com {len(comps[0])} personagens")
isolados = sorted(c[0] for c in comps if len(c) == 1)
rel.escrever(f"ficam isolados ({len(isolados)}): {', '.join(isolados)}")
rel.salvar()

# quem continua ligado ao grupo principal e quem fica isolado quando o David sai
principal = max(nx.connected_components(sem_david), key=len)
COR_ESTADO = {"continua ligado": "#2a78d6", "fica isolado": "#d62f2f"}
fig, ax = plt.subplots(figsize=(13, 10))
desenhar_rede(ax, sem_david, cor_vertice={v: COR_ESTADO["continua ligado" if v in principal else "fica isolado"]
                                         for v in sem_david})
fig.legend(handles=[Patch(color=c, label=k) for k, c in COR_ESTADO.items()], loc="lower left",
           bbox_to_anchor=(0.06, 0.0), fontsize=9, ncol=2)
ax.set_title("Rede global sem o David: quem continua ligado e quem fica isolado")
salvar(fig, "fig05_rede_sem_o_david")
