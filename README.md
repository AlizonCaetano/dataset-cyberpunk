# Redes de personagens em Cyberpunk: Edgerunners (temporada 1)

Trabalho de recuperação da disciplina 45RPE (Resolução de Problemas com Estruturas de Dados), UDESC CEAVI Ibirama, prof. Marcelo de Souza.
Autor: Alison Natan Caetano.

Base de interações entre personagens dos 10 episódios da temporada 1, modelada como redes e analisada com Python e NetworkX.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `base_interacoes.txt` | Base de dados: esquema, critérios, dicionário de personagens e registros por episódio. |
| `trabalho_redes_edgerunners.ipynb` | Notebook de entrega, com as 10 seções pedidas. |
| `analises/comum.py` | Código comum: leitura e validação da base, redes, grupos e estilo dos gráficos. |
| `analises/NN_nome.py` | Um script por análise (00 é a estatística da base, 01 a 13 são as análises). |
| `analises/rodar_todas.py` | Roda todos os scripts em ordem. |
| `graficos/` | Figuras PNG geradas pelos scripts. |
| `resultados/` | Resultado em texto de cada análise. |

O notebook tem o mesmo código dos scripts, na mesma ordem.

## Como executar

Instale as dependências:

```
pip install networkx pandas matplotlib scipy ipykernel
```

Rode a partir da raiz do projeto. Todas as análises:

```
python3 analises/rodar_todas.py
```

Uma análise só:

```
python3 analises/01_caracterizacao_geral_da_rede.py
```

Para o notebook, abra no VS Code, escolha o kernel Python e rode as células em ordem. Ele só precisa do `base_interacoes.txt` na mesma pasta.

## Formato da base

Um registro por linha, 6 campos separados por espaço:

```
personagem1 personagem2 sinal ambiente episodio minuto
```

- Rede não direcionada: a ordem dos dois personagens não importa.
- Sinal, pelo resultado da interação para a equipe do David: `+` ganha, `-` perde ou sai prejudicada, `0` sem ganho nem perda clara.

Estado atual: 205 registros (122 `+`, 68 `-`, 15 `0`), 37 personagens, 84 pares, episódios 1 a 10.

## Redes

- `G`: rede global, peso da aresta = número de cenas do par.
- `G_pos` e `G_neg`: só interações positivas e só negativas.
- `G_ep`: uma rede por episódio. `G_acum`: rede acumulada até cada episódio.
- Sinal líquido do par: soma dos sinais das cenas. Soma zero é par neutro.

## Grupos (cor do vértice nos desenhos)

Mercenários, Arasaka, Militech, fixers (Faraday e Wakako), polícia (tiras e MAX-TAC) e outros. A divisão está em `GRUPOS`, no `analises/comum.py`.
