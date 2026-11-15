from comum import *

rel = Relatorio("analise06", "ANÁLISE 6. Detecção de comunidades")

comunidades = sorted(nx.community.louvain_communities(G, weight="weight", seed=42), key=len, reverse=True)
modularidade = nx.community.modularity(G, comunidades, weight="weight")
rel.escrever(f"modularidade (Louvain, seed 42): {modularidade:.3f}")
for i, c in enumerate(comunidades, start=1):
    rel.escrever(f"comunidade {i} ({len(c)}): {', '.join(sorted(nome(v) for v in c))}")

# o Louvain tem parte aleatória: rodo 100 vezes e conto quantas vezes cada par cai na mesma comunidade
pares_teste = [("Faraday", "Kiwi"), ("Faraday", "AgentesArasaka"), ("Maine", "Dorio"),
               ("DavidMartinez", "LucynaKushinada"), ("Kiwi", "Rebecca"), ("DavidMartinez", "Maine")]
juntos, mods = Counter(), []
for semente in range(100):
    com = nx.community.louvain_communities(G, weight="weight", seed=semente)
    mods.append(nx.community.modularity(G, com, weight="weight"))
    rotulo = {v: i for i, c in enumerate(com) for v in c}
    for a, b in pares_teste:
        juntos[(a, b)] += rotulo[a] == rotulo[b]
rel.escrever(f"\nmodularidade em 100 execuções: de {min(mods):.3f} a {max(mods):.3f}")
rel.escrever("vezes em que o par caiu na mesma comunidade, em 100 execuções:")
for a, b in pares_teste:
    rel.escrever(f"  {nome(a)} e {nome(b)}: {juntos[(a, b)]}")

# comparação com um algoritmo sem sorteio (guloso de Clauset, Newman e Moore)
guloso = nx.community.greedy_modularity_communities(G, weight="weight")
do_faraday = [c for c in guloso if "Faraday" in c][0]
rel.escrever(f"\ncomunidade do Faraday no algoritmo guloso: {', '.join(sorted(nome(v) for v in do_faraday))}")
rel.salvar()

cor = {v: COR_COMUNIDADE[i] for i, c in enumerate(comunidades) for v in c}
fig, ax = plt.subplots(figsize=(13, 10))
desenhar_rede(ax, G, cor_vertice=cor)
fig.legend(handles=[Patch(color=COR_COMUNIDADE[i], label=f"Comunidade {i + 1} ({len(c)} personagens)")
                    for i, c in enumerate(comunidades)],
           title="Comunidades (Louvain, seed 42)", loc="lower left", bbox_to_anchor=(0.06, 0.0),
           fontsize=9, title_fontsize=9, ncol=3)
ax.set_title(f"Comunidades detectadas pelo Louvain, modularidade {modularidade:.2f}")
salvar(fig, "fig06_comunidades")
