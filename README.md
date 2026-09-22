
# 📦 Supply Chain & Inventory Analytics: Diagnóstico de Ruptura e Otimização de Abastecimento

![Power BI](https://img.shields.io/badge/Power_BI-F2C94C?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

## 📌 Resumo Executivo
Este projeto desenvolve uma solução ponta a ponta (*End-to-End*) de **Inteligência de Suprimentos e Gestão de Inventário** para uma rede varejista multicanal (5 lojas, 20 SKUs em 5 categorias e 4 regiões). 

A análise abrange **73.100 registros diários de operação (2022-2024)** e identifica um problema estrutural severo: **49,68% dos registros operam em nível crítico de estoque (<= 2 dias de cobertura)**. O diagnóstico comprovou que a causa raiz do risco de ruptura não é a volatilidade de demanda promocional ou sazonalidade, mas sim um **desalinhamento crônico na política de compras/reposição** (Units Ordered ~ 110 un. vs. Units Sold ~ 136 un.).

---

## 🎯 Contexto e Desafios de Negócio
A operação do varejo enfrentava riscos constantes de desabastecimento sem uma visão clara sobre a origem da falha. As principais perguntas que este projeto responde são:
1. **Qual é o nível real de risco de ruptura da operação e como ele se distribui na Curva ABC de produtos?**
2. **Existe impacto de volatilidade causada por campanhas promocionais, descontos ou fatores climáticos no esgotamento do estoque?**
3. **A falha é operacional/logística (reposição insuficiente) ou mercadológica (picos imprevisíveis de demanda)?**
4. **Qual é o impacto financeiro do risco de desabastecimento nos SKUs de maior faturamento?**

---

## 🔬 Metodologia e Pipeline de Dados

```
┌────────────────────────────────┐     ┌────────────────────────────────┐     ┌────────────────────────────────┐
│   1. ETL & EDA (Python)        │ ──► │   2. Data Modeling (SQL)       │ ──► │   3. Data Viz & DAX (Power BI) │
│ • Extração via Kaggle API      │     │ • Povoamento em SQLite         │     │ • Modelo Dimensional (Star)    │
│ • Limpeza de anomalias (0.92%) │     │ • Queries de Curva ABC         │     │ • Medidas DAX de Negócio       │
│ • Feature Engineering (KPIs)   │     │ • Agregações via Views         │     │ • Dashboard Executivo          │
└────────────────────────────────┘     └────────────────────────────────┘     └────────────────────────────────┘
``` 
## 1. Processamento e Sanitização de Dados (Python)
- Tratamento de Anomalias: Identificação e ajuste de 673 registros (0,92%) que apresentavam valores negativos no modelo original de Demand Forecast, corrigidos para 0 para evitar distorção no cálculo de erro.

- Engenharia de Métricas (Feature Engineering):

- Revenue (Faturamento): Units Sold * Price

- Days of Inventory (Dias de Cobertura): Inventory Level / Units Sold

- Forecast Error (Erro de Previsão): Units Sold - Demand Forecast

- Stock Status (Categorização Operacional):

- rítico (Risco Ruptura): <= 2 dias de estoque.

- tenção (Estoque Baixo): > 2 e <= 5 dias de estoque.

- Equilibrado: > 5 e <= 10 dias de estoque.

- Excesso: > 10 dias de estoque.

## 2. Engenharia de Dados & Consultas Estruturadas (SQL / SQLite)
- Povoamento da tabela tb_inventory no banco SQLite (supply_chain.db).

- Desenvolvimento de queries para validação da Curva A de Produtos usando funções condicionais (CASE WHEN) e agregações (SUM, AVG, ROUND).

- Criação de Views Executivas (vw_kpi_produto e vw_kpi_loja) para consumo otimizado de ferramentas de BI.

## 3. Modelagem e Visualização Executiva (Power BI & DAX)
- Estruturação de modelo relacional com tabela dCalendario conectada em 1:N.

- Criação de tabela dedicada de _Medidas com fórmulas DAX de performance (Faturamento Total, Média Dias Estoque, % Risco Ruptura, etc.).

## 📈 Principais Insights de Negócio e Conclusões
1. A Causa Raiz é Logística, não Promocional:

- A análise comparativa entre dias com e sem promoção (Holiday/Promotion) demonstrou que as vendas médias se mantêm praticamente idênticas (136,50 un. sem promoção vs. 136,42 un. com promoção), assim como a taxa de criticidade de estoque (49,75% vs. 49,61%).

- O problema reside na política de compras: os pedidos médios de reposição (Units Ordered = 110 un.) cobrem apenas 80,8% da demanda média diária.

2. Risco Crítico Concentrado na Curva A:

- Os 10 principais produtos em faturamento (representando mais de $53 Milhões no período) operam em estado crítico de estoque em mais de 50% dos dias.

- O SKU líder de receita (P0014 - Toys, faturamento de $5,51M) operou 406 dias em nível crítico (53,42% do tempo).

3. Performance homogênea e risco sistêmico por Loja:

- Todas as 5 unidades da rede exibem faturamento equilibrado (~$24M a $25.9M por combinação de região) e índice de risco crítico consistente entre 48% e 51%, comprovando que a falha na política de estoque é sistêmica em toda a cadeia de suprimentos.

## 🛠️ Recomendações Estratégicas de Supply Chain
Ajuste no Lote Mínimo de Compra (EOQ / Ponto de Pedido): Elevar a média de pedidos de reposição (Units Ordered) de 110 para no mínimo 145 unidades/dia, cobrindo a taxa de vendas reais e estabelecendo estoque de segurança (Safety Stock).

Priorização da Curva A: Implementar monitoramento diário focado nos TOP 10 SKUs de maior faturamento para evitar custo de oportunidade por falta de produto (Out-of-Stock).

Revisão do Algoritmo de Forecasting: Substituir o modelo atual de previsão de demanda devido às falhas de registros negativos e alto erro médio (Forecast Error ~ -5,06), adotando modelos de séries temporais mais precisos.

```
📂 Estrutura do Repositório
Plaintext
├── db.py                              # Script Python para ETL, sanitização, EDA e criação de KPIs
├── sql_analysis.py                    # Script de criação do banco SQLite e teste de Views
├── queries_supply_chain.sql           # Queries SQL puras e DDL de criação de Views
├── supply_chain.db                    # Banco de dados SQLite contendo a tabela tb_inventory e Views
├── retail_store_inventory_cleaned.csv # Dataset final tratado e enriquecido (21 colunas)
├── projeto analise.pbix               # Arquivo do relatório interativo no Power BI
└── README.md                          # Documentação técnica e executiva do projeto
```

## 🚀 Como Executar o Projeto
1.  Clonar este repositório
git clone https://github.com/AirtonSGuedes/Projeto-completo-de-supply-chain-inventory-analytics.git
cd Projeto-completo-de-supply-chain-inventory-analytics
2. Executar a esteira de tratamento em Python
py db.py
3. Gerar o banco de dados e as Views em SQL
py sql_analysis.py
4. Visualizar o Dashboard
- Abra o arquivo .pbix no Power BI Desktop ou consulte as visões resumidas na documentação.

## 📤 Publicando as Alterações no GitHub

Após executar:

- py gerar_readme.py

- Rode os seguintes comandos no terminal para subir a alteração ao GitHub:
```
git add README.md
git commit -m "docs: atualiza README executivo completo"
git push