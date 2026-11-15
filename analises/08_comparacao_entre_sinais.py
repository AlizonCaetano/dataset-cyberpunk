from comum import *

rel = Relatorio("analise08", "ANÁLISE 8. Comparação entre sinais")

rel.escrever("registros por sinal na temporada:")
rel.tabela(df["sinal"].value_counts())
sinais_ep = df.groupby(["episodio", "sinal"]).size().unstack(fill_value=0).reindex(columns=["+", "-", "0"], fill_value=0)
rel.escrever("\nregistros por episódio e sinal:")
rel.tabela(sinais_ep)

# grau ponderado de cada personagem na rede positiva e na negativa
por_personagem = pd.DataFrame({
    "positivas": dict(G_pos.degree(weight="weight")),
    "negativas": dict(G_neg.degree(weight="weight")),
}).fillna(0).astype(int).sort_values("negativas", ascending=False)
por_personagem.index = [nome(v) for v in por_personagem.index]
rel.escrever("\ninterações positivas e negativas por personagem (10 com mais negativas):")
rel.tabela(por_personagem.head(10))
rel.salvar()

rotulos = [f"E{int(e[1:])}" for e in sinais_ep.index]
fig, ax = plt.subplots(figsize=(8, 4.2))
base = None
for s in ["+", "-", "0"]:
    ax.bar(rotulos, sinais_ep[s], bottom=base, color=COR_SINAL[s], label=NOME_SINAL[s], width=0.62,
           edgecolor="white", linewidth=1.5)
    base = sinais_ep[s] if base is None else base + sinais_ep[s]
ax.set_ylabel("número de interações")
ax.set_title("Sinal das interações por episódio")
ax.legend(title="Sinal", fontsize=8, title_fontsize=8, loc="upper left")
ax.grid(axis="x", visible=False)
salvar(fig, "fig08_sinais_por_episodio")
