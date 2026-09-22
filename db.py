from pathlib import Path
import kagglehub
import pandas as pd

# Configurações para exibir todas as colunas no terminal sem truncar
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

# 1. Baixar e identificar o dataset
path = Path(
    kagglehub.dataset_download(
        "anirudhchauhan/retail-store-inventory-forecasting-dataset"
    )
)

caminho_csv = next(path.glob("*.csv"))

# 2. Carregar o dataset
df = pd.read_csv(caminho_csv, parse_dates=["Date"])

# 3. Inspeção e diagnósticos
print(f"Arquivo: {caminho_csv.name} | Dimensões: {df.shape}")
print(f"Duplicados: {df.duplicated().sum()}")

print("\n--- Primeiras Linhas ---")
print(df.head())

print("\n--- Informações da Estrutura ---")
df.info()

print("\n--- Valores Nulos ---")
print(df.isnull().sum())

# 4. Visão geral do negócio
print("\n--- VISÃO GERAL DO DATASET ---")

print("Quantidade de lojas:", df["Store ID"].nunique())
print("Quantidade de produtos:", df["Product ID"].nunique())

print("\nCategorias:")
print(df["Category"].unique())

print("\nRegiões:")
print(df["Region"].unique())

print("\nPeríodo:")
print("Data inicial:", df["Date"].min())
print("Data final:", df["Date"].max())

# 5. Estatísticas das variáveis numéricas
print("\n--- ESTATÍSTICAS DAS VARIÁVEIS NUMÉRICAS ---")

print(
    df[
        [
            "Inventory Level",
            "Units Sold",
            "Units Ordered",
            "Demand Forecast",
            "Price",
            "Discount",
            "Competitor Pricing",
        ]
    ].describe()
)

# 6. Tratamento de inconsistências
# Ajustando demanda negativa para 0 em uma nova coluna tratada
df["Demand Forecast Adjusted"] = df["Demand Forecast"].apply(lambda x: max(0, x))

# 7. Criação de KPIs iniciais de Supply Chain
# Erro absoluto de previsão (Venda Real - Previsão Ajustada)
df["Forecast Error"] = df["Units Sold"] - df["Demand Forecast Adjusted"]

# Cobertura de estoque em dias (Tratando divisão por zero quando Units Sold for 0)
df["Days of Inventory"] = df.apply(
    lambda row: row["Inventory Level"] / row["Units Sold"] if row["Units Sold"] > 0 else row["Inventory Level"], 
    axis=1
)

# 8. Classificação de Status de Estoque
def categorizar_estoque(dias):
    if dias <= 2:
        return "Crítico (Risco Ruptura)"
    elif dias <= 5:
        return "Atenção (Estoque Baixo)"
    elif dias <= 15:
        return "Equilibrado"
    else:
        return "Excesso"

df["Stock Status"] = df["Days of Inventory"].apply(categorizar_estoque)

print("\n--- DISTRIBUIÇÃO DOS STATUS DE ESTOQUE ---")
print(df["Stock Status"].value_counts())

print("\n--- PERCENTUAL POR STATUS DE ESTOQUE ---")
print((df["Stock Status"].value_counts(normalize=True) * 100).round(2).astype(str) + "%")

print("\n--- KPI's DE SUPPLY CHAIN CRIADOS (AMOSTRA) ---")
print(
    df[
        [
            "Date",
            "Store ID",
            "Product ID",
            "Inventory Level",
            "Units Sold",
            "Demand Forecast Adjusted",
            "Forecast Error",
            "Days of Inventory",
        ]
    ].head(10)
)

print("\n--- ESTATÍSTICAS DOS NOVOS KPIS ---")
print(df[["Forecast Error", "Days of Inventory"]].describe())

# 9. Receita estimada e análise por Produto
df["Net Price"] = df["Price"] * (1 - (df["Discount"] / 100))
df["Revenue"] = df["Units Sold"] * df["Net Price"]

print("\n--- TOP 10 PRODUTOS POR FATURAMENTO E RISCO ---")

prod_summary = df.groupby(["Product ID", "Category"]).agg(
    Total_Units_Sold=("Units Sold", "sum"),
    Total_Revenue=("Revenue", "sum"),
    Avg_Days_of_Inventory=("Days of Inventory", "mean"),
    Pct_Critical=(
        "Stock Status",
        lambda x: (x == "Crítico (Risco Ruptura)").mean() * 100,
    ),
).reset_index()

# Ordenando pelos produtos de maior faturamento
prod_summary = prod_summary.sort_values(by="Total_Revenue", ascending=False)

# Formatação visual para impressão do Faturamento
prod_summary_print = prod_summary.copy()
prod_summary_print["Total_Revenue"] = prod_summary_print["Total_Revenue"].apply(lambda x: f"${x:,.2f}")

print(prod_summary_print.head(10).to_string(index=False))

 # 10. Análise agregada por Loja e Região
store_summary = df.groupby(["Store ID", "Region"]).agg(
    Total_Units_Sold=("Units Sold", "sum"),
    Total_Revenue=("Revenue", "sum"),
    Avg_Days_of_Inventory=("Days of Inventory", "mean"),
    Pct_Critical=(
        "Stock Status",
        lambda x: (x == "Crítico (Risco Ruptura)").mean() * 100,
    ),
).reset_index()

store_summary = store_summary.sort_values(by="Total_Revenue", ascending=False)
store_summary_print = store_summary.copy()
store_summary_print["Total_Revenue"] = store_summary_print["Total_Revenue"].apply(lambda x: f"${x:,.2f}")

print("\n--- PERFORMANCE E RISCO POR LOJA ---")
print(store_summary_print.head(5).to_string(index=False))

# 11. Análise do Impacto de Promoções e Descontos
print("\n--- IMPACTO DE PROMOÇÃO/FERIADO NAS VENDAS E ESTOQUE ---")

promo_summary = df.groupby("Holiday/Promotion").agg(
    Total_Registros=("Units Sold", "count"),
    Avg_Units_Sold=("Units Sold", "mean"),
    Avg_Discount=("Discount", "mean"),
    Avg_Days_of_Inventory=("Days of Inventory", "mean"),
    Pct_Critical=(
        "Stock Status",
        lambda x: (x == "Crítico (Risco Ruptura)").mean() * 100,
    ),
).reset_index()

print(promo_summary.to_string(index=False))

# 12. Exportação do dataset limpo e enriquecido para as próximas etapas
caminho_saida = path / "retail_store_inventory_cleaned.csv"
df.to_csv(caminho_saida, index=False)

print("\n--- ETAPA DO PYTHON CONCLUÍDA COM SUCESSO! ---")
print(f"Dataset limpo e enriquecido salvo em: {caminho_saida}")
print(f"Total de colunas finais: {df.shape[1]} | Total de linhas: {df.shape[0]}")