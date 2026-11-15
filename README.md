# Redes de personagens em Cyberpunk: Edgerunners (temporada 1)

Trabalho de recuperação da disciplina 45RPE (Resolução de Problemas com Estruturas de Dados), UDESC CEAVI Ibirama, prof. Marcelo de Souza.
Autor: Alison Natan Caetano.

## O que é

Uma base de interações entre personagens dos 10 episódios da temporada 1, modelada como redes e analisada com Python e NetworkX.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `base_interacoes.txt` | Base de dados. Cabeçalho com esquema, critérios e dicionário de personagens, depois os registros por episódio. |
| `trabalho_redes_edgerunners.ipynb` | Notebook com as 10 seções pedidas, código, resultados, figuras e interpretações. |
| `graficos/` | Figuras PNG, criadas ao executar o notebook. |

## Formato da base

Um registro por linha, 6 campos separados por espaço:

```
personagem1 personagem2 sinal ambiente episodio minuto
```

- Rede não direcionada: a ordem dos dois personagens não importa.
- Sinal, pelo resultado da interação para a equipe do David: `+` ganha, `-` perde ou sai prejudicada, `0` sem ganho nem perda clara.
- Uma linha de comentário logo abaixo do registro traz a descrição curta da cena.

Estado atual: 203 registros (121 `+`, 67 `-`, 15 `0`), 40 personagens, episódios 1 a 10.

## Como executar

1. Deixe `base_interacoes.txt` e o notebook na mesma pasta.
2. Instale as dependências:
   ```
   pip install networkx pandas matplotlib ipykernel
   ```
3. Abra o notebook no VS Code, escolha o kernel Python e rode as células em ordem.
4. As figuras são salvas em `graficos/`.

## Redes montadas

- `G`: rede global, peso da aresta = número de cenas do par.
- `G_pos` e `G_neg`: redes só com interações positivas e só com negativas.
- `G_ep`: uma rede por episódio.
- `G_acum`: rede acumulada até cada episódio.
