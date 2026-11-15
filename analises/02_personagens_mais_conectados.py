from comum import *

rel = Relatorio("analise02", "ANÁLISE 2. Personagens mais conectados")

# grau: com quantos personagens diferentes interage; grau ponderado: em quantas cenas aparece
graus = pd.DataFrame({
    "grau": dict(G.degree()),
    "grau_ponderado": dict(G.degree(weight="weight")),
}).sort_values("grau_ponderado", ascending=False)
graus.index = [nome(v) for v in graus.index]
rel.tabela(graus.head(12))
rel.salvar()

top = graus.head(12).iloc[::-1]
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(top.index, top["grau_ponderado"], color=COR_BARRA, height=0.6)
for y, v in enumerate(top["grau_ponderado"]):
    ax.text(v + 1, y, str(v), va="center", fontsize=8, color="#52514e")
ax.set_xlabel("grau ponderado (número de cenas de interação)")
ax.set_title("Os 12 personagens com maior grau ponderado")
ax.grid(axis="y", visible=False)
salvar(fig, "fig02_grau_ponderado")
