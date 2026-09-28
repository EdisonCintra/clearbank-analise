"""
Requisito opcional (RO1) — versão alternativa da leitura e do agrupamento
usando pandas, para comparar com a solução nativa do desafio-final.ipynb.

Executar com: python3 analise_pandas.py
"""

import pandas as pd

LIMITE_SUSPEITO = 10000.00


def carregar_dados(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo, dtype=str)

    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")
    df["cliente_id"] = df["cliente_id"].str.strip()
    df["tipo"] = df["tipo"].str.strip().str.lower()

    total_lidas = len(df)

    validas = df[
        df["id"].str.isdigit()
        & df["cliente_id"].notna() & (df["cliente_id"] != "")
        & df["tipo"].isin(["credito", "debito"])
        & df["data"].notna()
        & df["valor"].notna() & (df["valor"] > 0)
    ].copy()

    total_invalidas = total_lidas - len(validas)
    validas["mes"] = validas["data"].dt.strftime("%Y-%m")
    validas["suspeita"] = validas["valor"] > LIMITE_SUSPEITO

    return validas, total_lidas, total_invalidas


def gerar_resumo_mensal(validas):
    creditos = validas[validas["tipo"] == "credito"].groupby("mes")["valor"].sum()
    debitos = validas[validas["tipo"] == "debito"].groupby("mes")["valor"].sum()

    resumo = validas.groupby("mes").agg(
        quantidade=("valor", "count"),
        maior_valor=("valor", "max"),
        menor_valor=("valor", "min"),
        media=("valor", "mean"),
    )
    resumo["total_credito"] = creditos.reindex(resumo.index).fillna(0.0)
    resumo["total_debito"] = debitos.reindex(resumo.index).fillna(0.0)
    resumo["saldo"] = resumo["total_credito"] - resumo["total_debito"]

    return resumo.round(2).sort_index()


if __name__ == "__main__":
    validas, total_lidas, total_invalidas = carregar_dados("transacoes.csv")

    print(f"Total de linhas lidas: {total_lidas}")
    print(f"Linhas válidas: {len(validas)}")
    print(f"Linhas inválidas: {total_invalidas}")
    print()

    resumo = gerar_resumo_mensal(validas)
    print("===== RESUMO MENSAL (pandas) =====")
    print(resumo[["quantidade", "total_credito", "total_debito", "saldo", "media",
                   "maior_valor", "menor_valor"]])

    suspeitas = validas[validas["suspeita"]].sort_values("data")
    print()
    print("===== TRANSAÇÕES SUSPEITAS (pandas) =====")
    if suspeitas.empty:
        print("Nenhuma transação suspeita encontrada.")
    else:
        for _, t in suspeitas.iterrows():
            print(f"ID: {t['id']} | Cliente: {t['cliente_id']} | "
                  f"Data: {t['data'].date()} | Valor: R$ {t['valor']:,.2f}")
