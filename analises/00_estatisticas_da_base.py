from comum import *

rel = Relatorio("estatisticas_da_base", "ESTATÍSTICAS DESCRITIVAS DA BASE")
participam = set(df["personagem1"]) | set(df["personagem2"])
rel.escrever(f"registros: {len(df)}")
rel.escrever(f"personagens no dicionário: {len(personagens)}; com ao menos um registro: {len(participam)}")
rel.escrever("\nregistros por sinal:")
rel.tabela(df["sinal"].value_counts())
rel.escrever("\nregistros por episódio e sinal:")
rel.tabela(df.groupby(["episodio", "sinal"]).size().unstack(fill_value=0))
rel.escrever("\nregistros por ambiente:")
rel.tabela(df["ambiente"].value_counts())
rel.salvar()
