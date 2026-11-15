"""Código comum a todas as análises: leitura e validação da base, montagem das redes,
grupos dos personagens e estilo dos gráficos. Rode os scripts a partir da raiz do projeto."""
import os
import re
import sys
from collections import Counter

import matplotlib
if "ipykernel" not in sys.modules:      # fora do notebook, só grava as figuras em arquivo
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

BASE = "base_interacoes.txt"
os.makedirs("graficos", exist_ok=True)
os.makedirs("resultados", exist_ok=True)


# ---------- 1. leitura e validação da base ----------
def ler_base(caminho=BASE):
    """Devolve o dicionário de personagens e um DataFrame com um registro por linha."""
    personagens, linhas, erros = {}, [], []
    for n, linha in enumerate(open(caminho, encoding="utf-8").read().splitlines(), start=1):
        linha = linha.strip()
        if linha.startswith("# PERSONAGEM "):
            id_, nome_canonico, apelidos, primeira = [c.strip() for c in linha[13:].split("|")]
            personagens[id_] = {"nome_canonico": nome_canonico, "primeira_aparicao": primeira,
                                "apelidos": [a.strip() for a in apelidos.split(";") if a.strip()]}
            continue
        if not linha or linha.startswith("#"):
            continue
        campos = linha.split(" ")
        if len(campos) != 6:
            erros.append((n, f"esperados 6 campos, encontrados {len(campos)}"))
            continue
        p1, p2, sinal, ambiente, episodio, minuto = campos
        for p in (p1, p2):
            if p not in personagens:
                erros.append((n, f"ID fora do dicionário: {p}"))
        if p1 == p2:
            erros.append((n, "personagem1 e personagem2 são iguais"))
        if sinal not in ("+", "-", "0"):
            erros.append((n, f"sinal inválido: {sinal}"))
        if not re.fullmatch(r"[A-Za-z0-9]+", ambiente):
            erros.append((n, f"ambiente inválido: {ambiente}"))
        if not re.fullmatch(r"E\d{2}", episodio):
            erros.append((n, f"episódio inválido: {episodio}"))
        if not re.fullmatch(r"\d{2}:\d{2}", minuto):
            erros.append((n, f"minuto inválido: {minuto}"))
        linhas.append({"personagem1": p1, "personagem2": p2, "sinal": sinal, "ambiente": ambiente,
                       "episodio": episodio, "minuto": minuto})
    assert not erros, erros
    return personagens, pd.DataFrame(linhas)


personagens, df = ler_base()
EPISODIOS = sorted(df["episodio"].unique())


# ---------- 2. relatório de resultados ----------
class Relatorio:
    """Mostra o resultado na tela e grava o mesmo texto em resultados/."""

    def __init__(self, arquivo, titulo):
        self.caminho = f"resultados/{arquivo}.txt"
        self.linhas = []
        self.escrever(titulo)

    def escrever(self, texto=""):
        print(texto)
        self.linhas.append(str(texto))

    def tabela(self, tabela):
        self.escrever(tabela.to_string())

    def salvar(self):
        with open(self.caminho, "w", encoding="utf-8") as f:
            f.write("\n".join(self.linhas) + "\n")


# ---------- 3. redes ----------
def montar_grafo(registros):
    """Grafo não direcionado. O peso da aresta é o número de registros (cenas) do par."""
    g = nx.Graph()
    for a, b in zip(registros["personagem1"], registros["personagem2"]):
        if g.has_edge(a, b):
            g[a][b]["weight"] += 1
        else:
            g.add_edge(a, b, weight=1)
    return g


G = montar_grafo(df)                              # rede global
G_pos = montar_grafo(df[df["sinal"] == "+"])      # só interações positivas
G_neg = montar_grafo(df[df["sinal"] == "-"])      # só interações negativas
G_ep = {ep: montar_grafo(df[df["episodio"] == ep]) for ep in EPISODIOS}      # uma rede por episódio
G_acum = {ep: montar_grafo(df[df["episodio"] <= ep]) for ep in EPISODIOS}    # do episódio 1 até o N


def sinal_por_par(registros):
    """Sinal líquido de cada par: soma das cenas (+ vale 1, - vale -1, 0 vale 0).
    Soma positiva dá '+', negativa dá '-' e soma zero dá '0' (neutro)."""
    soma = Counter()
    for a, b, s in zip(registros["personagem1"], registros["personagem2"], registros["sinal"]):
        soma[tuple(sorted((a, b)))] += {"+": 1, "-": -1, "0": 0}[s]
    return {par: "+" if v > 0 else "-" if v < 0 else "0" for par, v in soma.items()}


# ---------- 4. grupos e nomes ----------
EQUIPE = {"Maine", "LucynaKushinada", "Kiwi", "Dorio", "Pilar", "Rebecca", "Falco", "Julio"}
GRUPOS = {
    "Mercenários": EQUIPE | {"DavidMartinez"},
    "Arasaka": {"DiretorAcademia", "SrTanaka", "Katsuo", "SegurancaArasaka", "AgentesArasaka",
                "OficialArasaka", "AdamSmasher", "Maxim"},
    "Militech": {"Militech"},
    "Fixers": {"Faraday", "Wakako"},
    "Polícia": {"Tiras", "MaxTac"},
}
COR_GRUPO = {"Mercenários": "#2a78d6", "Arasaka": "#222222", "Militech": "#f08c00",
             "Fixers": "#8e44ad", "Polícia": "#1baf7a", "Outros": "#c9c9c4"}


def grupo(v):
    for g, membros in GRUPOS.items():
        if v in membros:
            return g
    return "Outros"


NOME_CURTO = {"DavidMartinez": "David", "LucynaKushinada": "Lucy", "GloriaMartinez": "Glória",
              "CyberpsicopataEp1": "Cyberpsicopata (ep. 1)", "CyberpsicopataEp4": "Cyberpsicopata (ep. 4)",
              "MaxTac": "MAX-TAC", "SrTanaka": "Sr. Tanaka", "DiretorAcademia": "Diretor",
              "TraumaTeam": "Trauma Team", "MedicoHospital": "Médico", "JK": "JK",
              "SegurancaArasaka": "Segurança Arasaka", "InimigosAssalto": "Inimigos (assalto)",
              "InimigosGangue": "Inimigos (gangue)", "InimigosCampoAberto": "Inimigos (campo)",
              "AgentesArasaka": "Agentes Arasaka", "OficialArasaka": "Oficial Arasaka",
              "AdamSmasher": "Adam Smasher", "DronesArmados": "Drones", "ChefeGangue": "Chefe da gangue"}


def nome(v):
    return NOME_CURTO.get(v, re.sub(r"(?<!^)(?=[A-Z])", " ", v))


# ---------- 5. estilo dos gráficos ----------
plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 200, "font.size": 10, "axes.titlesize": 12,
    "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#52514e",
    "xtick.color": "#52514e", "ytick.color": "#52514e", "axes.grid": True, "grid.color": "#e6e6e3",
    "grid.linewidth": 0.6, "axes.axisbelow": True, "legend.frameon": False,
    "figure.facecolor": "white", "axes.facecolor": "white",
})
COR_SINAL = {"+": "#1a9850", "-": "#d62f2f", "0": "#7a7a7a"}
ESTILO_SINAL = {"+": "solid", "-": "dashed", "0": "dotted"}     # estilo repete a informação da cor
NOME_SINAL = {"+": "positiva", "-": "negativa", "0": "neutra"}
COR_BARRA = "#2a78d6"
COR_COMUNIDADE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#6250d6", "#52514e"]


def salvar(fig, arquivo):
    """Grava a figura em graficos/ e mostra no notebook."""
    fig.savefig(f"graficos/{arquivo}.png", bbox_inches="tight", pad_inches=0.15, facecolor="white")
    if "ipykernel" in sys.modules:
        plt.show()
    plt.close(fig)


# ---------- 6. posição dos personagens no desenho da rede ----------
# Cada grupo ocupa uma região fixa, a mesma em todas as figuras: mercenários no centro, com o David
# no meio, Arasaka à direita, polícia em cima, fixers e Militech embaixo, e os outros num arco à esquerda.
ORDEM_MERCENARIOS = ["Maine", "Dorio", "Kiwi", "LucynaKushinada", "Pilar", "Rebecca", "Julio", "Falco"]
CENTRO = {"Arasaka": (1.5, 0.0), "Militech": (1.9, -1.0), "Fixers": (1.05, -1.2), "Polícia": (0.2, 1.4)}
POSICAO_FIXA = {"CyberpsicopataEp1": (1.1, 1.4)}     # só se liga à polícia e à segurança da Arasaka


def _circulo(nos, centro, raio, inicio=90.0, abertura=360.0):
    passo = abertura / max(len(nos), 1)
    return {v: (centro[0] + raio * np.cos(np.radians(inicio + i * passo)),
                centro[1] + raio * np.sin(np.radians(inicio + i * passo))) for i, v in enumerate(nos)}


ORDEM_ANEL = {}


def calcular_posicoes(g):
    pos = {"DavidMartinez": (0.0, 0.0)}
    merc = [v for v in ORDEM_MERCENARIOS if v in g]
    pos.update(_circulo(merc, (0, 0), 0.42, inicio=100))
    # quem tem mais ligações fica do lado de dentro do grupo, virado para os mercenários
    for gr, centro in CENTRO.items():
        nos = sorted((v for v in g if grupo(v) == gr), key=lambda v: (v in ("SegurancaArasaka", "MaxTac"), -g.degree(v), v))
        if len(nos) <= 2:
            pos.update({v: (centro[0] + 0.28 * i, centro[1]) for i, v in enumerate(nos)})
        else:
            pos.update(_circulo(nos, centro, 0.36, inicio=180))
    # os outros ficam num arco à esquerda, ordenados pelo ângulo médio dos vizinhos mercenários
    pos.update({v: p for v, p in POSICAO_FIXA.items() if v in g})
    outros = [v for v in g if v not in pos]

    def angulo(v):
        viz = [pos[u] for u in g[v] if u in merc]
        if not viz:
            return 400.0
        a = np.degrees(np.arctan2(np.mean([p[1] for p in viz]), np.mean([p[0] for p in viz]))) % 360
        return a if a >= 60 else a + 360
    outros.sort(key=lambda v: (angulo(v), v))
    pos.update(_circulo(outros, (0, 0), 1.15, inicio=100, abertura=205))
    ORDEM_ANEL.update({v: i for i, v in enumerate(outros)})
    return {v: np.array(p) for v, p in pos.items()}


POS = calcular_posicoes(G)
_PESO_MAX = max(dict(G.degree(weight="weight")).values())


def tamanho(g, v):
    """Tamanho do vértice pela raiz do número de cenas do personagem, numa faixa estreita."""
    return 130 + 520 * (g.degree(v, weight="weight") / _PESO_MAX) ** 0.5


def _posicao_rotulo(v):
    """O nome fica do lado de fora do grupo do personagem, para não cair em cima das arestas."""
    x, y = POS[v]
    if v == "DavidMartinez":
        return x, y - 0.12, "center", "top"
    gr = grupo(v)
    cx, cy = (0.0, 0.0) if gr in ("Mercenários", "Outros") else CENTRO[gr]
    if gr in ("Militech", "Fixers", "Polícia") or v in POSICAO_FIXA:
        return x, y + 0.09, "center", "bottom"
    d = np.array([x - cx, y - cy])
    d = d / (np.linalg.norm(d) or 1)
    ha = "left" if d[0] > 0.3 else "right" if d[0] < -0.3 else "center"
    va = "bottom" if d[1] > 0.3 else "top" if d[1] < -0.3 else "center"
    # no arco, nomes vizinhos que ficam acima ou abaixo do vértice alternam a distância para não encostar
    dist = 0.17 if (ha == "center" and ORDEM_ANEL.get(v, 0) % 2) else 0.075
    return x + dist * d[0], y + dist * d[1], ha, va


def desenhar_rede(ax, g, cor_vertice=None, sinais=None, largura_peso=False):
    """Desenha a rede g. cor_vertice: dict vértice -> cor (padrão: cor do grupo).
    sinais: dict par -> '+', '-' ou '0', que define cor e estilo das arestas."""
    cor_vertice = cor_vertice or {v: COR_GRUPO[grupo(v)] for v in g}
    if sinais:
        for s in ["0", "+", "-"]:
            arestas = [e for e in g.edges() if sinais.get(tuple(sorted(e))) == s]
            nx.draw_networkx_edges(g, POS, edgelist=arestas, ax=ax, edge_color=COR_SINAL[s],
                                   style=ESTILO_SINAL[s], width=1.3, alpha=0.75)
    else:
        larguras = [0.6 + 0.3 * g[u][v]["weight"] for u, v in g.edges()] if largura_peso else 0.9
        nx.draw_networkx_edges(g, POS, ax=ax, edge_color="#a7a69f", width=larguras, alpha=0.6)
    nx.draw_networkx_nodes(g, POS, ax=ax, node_color=[cor_vertice[v] for v in g],
                           node_size=[tamanho(G, v) for v in g], edgecolors="white", linewidths=1.3)
    for v in g:
        x, y, ha, va = _posicao_rotulo(v)
        ax.text(x, y, nome(v), ha=ha, va=va, fontsize=8.5, color="#0b0b0b", zorder=5,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.8))
    ax.set_xlim(-1.75, 2.35)
    ax.set_ylim(-1.5, 1.65)
    ax.set_aspect("equal")
    ax.axis("off")


def legenda_grupos(fig, g):
    usados = [k for k in COR_GRUPO if any(grupo(v) == k for v in g)]
    fig.legend(handles=[Line2D([0], [0], marker="o", color="none", markerfacecolor=COR_GRUPO[k],
                               markeredgecolor="white", markersize=10, label=k) for k in usados],
               title="Grupo (cor do vértice)", loc="lower left", bbox_to_anchor=(0.06, 0.0),
               fontsize=9, title_fontsize=9, ncol=3)


def legenda_sinais(fig, sinais=("+", "-", "0")):
    fig.legend(handles=[Line2D([0], [0], color=COR_SINAL[s], linestyle=ESTILO_SINAL[s], lw=2,
                               label=NOME_SINAL[s]) for s in sinais],
               title="Sinal líquido do par (aresta)", loc="lower right", bbox_to_anchor=(0.94, 0.0),
               fontsize=9, title_fontsize=9, ncol=3)
