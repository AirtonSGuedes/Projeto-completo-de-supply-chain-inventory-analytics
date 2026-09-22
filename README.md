# 📦 Supply Chain & Inventory Analytics Dashboard

Este projeto apresenta um diagnóstico completo de inteligência de abastecimento, gestão de estoque e análise de risco financeiro de ruptura para uma operação de varejo multi-loja. 

A solução integra todo o pipeline de dados: **ETL & EDA em Python**, **Modelagem & Views em SQL (SQLite)** e **Dashboard Executivo no Power BI**.

---

## 🎯 Problema de Negócio & Principais Descobertas

* **Identificação de Causa Raiz:** O risco generalizado de ruptura de estoque (~49,68% dos dias em nível crítico, com $\le 2$ dias de cobertura) não decorre de volatilidade promocional ou sazonalidade, mas sim de um **desalinhamento estrutural no reabastecimento**: os pedidos médios de reposição (`Units Ordered` ~ 110 un.) são sistematicamente inferiores à demanda média real (`Units Sold` ~ 136 un.).
* **Impacto na Curva A:** Os produtos de maior faturamento (como os SKUs `P0014`, `P0016` e `P0015`, com vendas superiores a \$5,4M cada) operam em estado crítico de estoque em mais de **50% do tempo**.
* **Qualidade dos Dados:** Mapeamento e ajuste de anomalias no modelo de forecasting (0,92% de previsões negativas corrigidas para zero).

---

## 🛠️ Arquitetura e Tecnologias Utilizadas

[Kaggle Dataset] ➔ [Python / Pandas (ETL & EDA)] ➔ [SQLite (SQL Views & Queries)] ➔ [Power BI (DAX & Dashboard)]

* **Python 3.12 (Pandas, Pathlib, Kagglehub):**
  * Extração automatizada via API.
  * Sanitização de dados e tratamento de anomalias.
  * Engenharia de atributos: *Days of Inventory*, *Stock Status*, *Revenue* e *Forecast Error*.
  * Exportação do dataset limpo e enriquecido (`retail_store_inventory_cleaned.csv`).

* **SQL / SQLite:**
  * Modelagem da tabela `tb_inventory`.
  * Elaboração da consulta analítica de Curva ABC e matriz de risco financeiro.
  * Criação das Views executivas `vw_kpi_produto` e `vw_kpi_loja` utilizando funções agregadas (`SUM`, `AVG`, `CASE WHEN`).

* **Power BI Desktop:**
  * Criação da tabela dimensional `dCalendario` com relacionamento $1:N$.
  * Construção de medidas DAX estratégicas (*Faturamento Total*, *Total Unidades Vendidas*, *Média Dias Estoque*, *% Risco Ruptura*).
  * Design de painel interativo focado no tomador de decisão.

---

## 📊 Estrutura do Repositório

```text
├── db.py                       # Script Python para ETL, limpeza e engenharia de atributos
├── sql_analysis.py             # Script Python para integração com SQLite e execução de queries/views
├── queries_supply_chain.sql    # Consultas SQL puras e comandos CREATE VIEW
├── supply_chain.db             # Banco de dados SQLite contendo as tabelas e views
├── retail_store_inventory_cleaned.csv # Dataset final tratado
└── README.md                   # Documentação do projeto