import os
import networkx as nx

BASE = "base_interacoes.txt"
SAIDA = "resultados/analise01.txt"


def ler_registros(caminho=BASE):
    registros = []
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            p1, p2, sinal, ambiente, episodio, minuto = linha.split(" ")
            registros.append((p1, p2, sinal, ambiente, episodio, minuto))
    return registros


def montar_grafo(registros):
    G = nx.Graph()
    for p1, p2, sinal, ambiente, episodio, minuto in registros:
        if G.has_edge(p1, p2):
            G[p1][p2]["weight"] += 1
        else:
            G.add_edge(p1, p2, weight=1)
    return G


def calcular_metricas(G, n_registros):
    maior = G.subgraph(max(nx.connected_components(G), key=len))
    par = max(G.edges(data=True), key=lambda e: e[2]["weight"])
    return {
        "registros": n_registros,
        "vertices": G.number_of_nodes(),
        "arestas": G.number_of_edges(),
        "par_mais_cenas": (par[0], par[1], par[2]["weight"]),
        "densidade": round(nx.density(G), 3),
        "grau_medio": round(2 * G.number_of_edges() / G.number_of_nodes(), 2),
        "agrupamento_medio": round(nx.average_clustering(G), 3),
        "componentes": nx.number_connected_components(G),
        "diametro": nx.diameter(maior),
        "caminho_medio": round(nx.average_shortest_path_length(maior), 2),
    }


def montar_texto(m):
    a, b, w = m["par_mais_cenas"]
    return "\n".join([
        "ANALISE 1. Caracterizacao geral da rede",
        f"registros: {m['registros']}",
        f"vertices: {m['vertices']}",
        f"arestas: {m['arestas']}",
        f"par com mais cenas: {a} e {b} ({w} cenas)",
        f"densidade: {m['densidade']}",
        f"grau medio: {m['grau_medio']}",
        f"agrupamento medio: {m['agrupamento_medio']}",
        f"componentes conexos: {m['componentes']}",
        f"diametro: {m['diametro']}",
        f"caminho medio: {m['caminho_medio']}",
    ])


if __name__ == "__main__":
    registros = ler_registros()
    G = montar_grafo(registros)
    metricas = calcular_metricas(G, len(registros))
    texto = montar_texto(metricas)

    os.makedirs("resultados", exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(texto + "\n")

    print(texto)