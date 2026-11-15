from comum import *

rel = Relatorio("analise11", "ANÁLISE 11. Equilíbrio estrutural da rede com sinal")

# rede só com os pares de sinal líquido definido; par neutro (soma zero) fica fora
liquido = sinal_por_par(df)
G_sinal = nx.Graph()
for (a, b), s in liquido.items():
    if s != "0":
        G_sinal.add_edge(a, b, sinal=1 if s == "+" else -1)
n_pos = sum(1 for *_, s in G_sinal.edges(data="sinal") if s > 0)
rel.escrever(f"pares com sinal líquido definido: {G_sinal.number_of_edges()} "
             f"({n_pos} positivos, {G_sinal.number_of_edges() - n_pos} negativos)")
rel.escrever(f"pares neutros, fora da análise: {sum(1 for s in liquido.values() if s == '0')}")

# triângulo equilibrado: produto dos três sinais positivo (Heider; Cartwright e Harary)
triangulos = [c for c in nx.enumerate_all_cliques(G_sinal) if len(c) == 3]


def produto(t):
    a, b, c = t
    return G_sinal[a][b]["sinal"] * G_sinal[b][c]["sinal"] * G_sinal[a][c]["sinal"]


equilibrados = [t for t in triangulos if produto(t) > 0]
rel.escrever(f"triângulos: {len(triangulos)}, equilibrados: {len(equilibrados)} "
             f"({len(equilibrados) / len(triangulos):.0%})")
rel.escrever("\ntriângulos desequilibrados:")
for t in triangulos:
    if produto(t) < 0:
        rel.escrever("  " + ", ".join(nome(v) for v in t))
rel.salvar()

fig, ax = plt.subplots(figsize=(13, 10))
desenhar_rede(ax, G_sinal, sinais={k: s for k, s in liquido.items() if s != "0"})
legenda_grupos(fig, G_sinal)
legenda_sinais(fig, sinais=("+", "-"))
ax.set_title("Rede com o sinal líquido de cada par (pares neutros fora)")
salvar(fig, "fig11_rede_sinal_liquido")
