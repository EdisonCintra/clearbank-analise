# ClearBank — Análise Financeira com Python

Desafio final do módulo de fundamentos de Python aplicados à análise de dados. O projeto lê
o histórico mensal de transações de uma fintech fictícia (ClearBank), valida e limpa os
dados, calcula métricas financeiras por mês, sinaliza transações suspeitas e exporta o
resultado em JSON.

## Como executar

1. Abra `desafio-final.ipynb` no Google Colab ou no Jupyter Notebook local (Python 3.10+).
2. Garanta que `transacoes.csv` esteja na mesma pasta do notebook.
3. Execute todas as células em ordem (Run All). A célula de execução principal roda o
   pipeline completo: leitura → validação → processamento de datas → geração do relatório →
   exportação em JSON → exibição formatada no terminal.

Opcional (fora do notebook, via terminal):

```bash
pip install pandas matplotlib
python3 analise_pandas.py   # RO1 — versão alternativa com pandas
```

## O que o notebook gera

- **Saída no terminal**: resumo da limpeza dos dados (linhas lidas/válidas/inválidas),
  relatório mensal (transações, total de crédito/débito, saldo, média, maior e menor valor)
  e a lista de transações suspeitas (valor acima de R$ 10.000,00).
- **`relatorio.json`**: o mesmo relatório, estruturado em JSON.
- **`grafico.png`** *(opcional, RO2)*: gráfico de barras com o saldo mensal (crédito − débito).

## Estrutura

```
clearbank-analise/
├── desafio-final.ipynb    # notebook principal, com saídas executadas
├── transacoes.csv         # dados de entrada (18 válidos + 5 inválidos, para testar a validação)
├── relatorio.json          # gerado ao executar o notebook
├── analise_pandas.py       # RO1 — versão alternativa com pandas
├── grafico.png              # RO2 — saldo mensal
└── README.md
```

## Regras de validação aplicadas

Uma linha é descartada (sem interromper o programa) quando:

- `id` está vazio ou não é numérico;
- `cliente_id` está vazio;
- `data` não está no formato `AAAA-MM-DD`;
- `tipo` é diferente de `credito` ou `debito`;
- `valor` não é numérico ou é menor/igual a zero.

Transações com `valor` acima de `LIMITE_SUSPEITO = 10000.00` são marcadas como suspeitas.
