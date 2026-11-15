from comum import *

rel = Relatorio("analise01", "ANÁLISE 1. Caracterização geral da rede")

# diâmetro e caminho médio só existem onde todos se alcançam, por isso uso o maior componente
maior = G.subgraph(max(nx.connected_components(G), key=len))
par = max(G.edges(data="weight"), key=lambda e: e[2])

rel.escrever(f"registros: {len(df)}")
rel.escrever(f"vértices: {G.number_of_nodes()}")
rel.escrever(f"arestas: {G.number_of_edges()}")
rel.escrever(f"par com mais cenas: {nome(par[0])} e {nome(par[1])} ({par[2]} cenas)")
rel.escrever(f"densidade: {nx.density(G):.3f}")
rel.escrever(f"grau médio: {2 * G.number_of_edges() / G.number_of_nodes():.2f}")
rel.escrever(f"agrupamento médio: {nx.average_clustering(G):.3f}")
rel.escrever(f"componentes conexos: {nx.number_connected_components(G)}")
rel.escrever(f"diâmetro: {nx.diameter(maior)}")
rel.escrever(f"caminho médio: {nx.average_shortest_path_length(maior):.2f}")
rel.salvar()

# rede global: cor do vértice pelo grupo, cor e estilo da aresta pelo sinal líquido do par
fig, ax = plt.subplots(figsize=(13, 10))
desenhar_rede(ax, G, sinais=sinal_por_par(df))
legenda_grupos(fig, G)
legenda_sinais(fig)
ax.set_title("Rede global de interações, temporada 1\n"
             "(tamanho do vértice pela raiz do número de cenas do personagem)")
salvar(fig, "fig01_rede_global")
