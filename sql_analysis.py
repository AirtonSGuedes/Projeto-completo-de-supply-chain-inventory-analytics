import sqlite3
from pathlib import Path
import kagglehub
import pandas as pd

# Configuração de exibição do Pandas
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

# 1. Carregar dataset limpo
path = Path(
    kagglehub.dataset_download(
        "anirudhchauhan/retail-store-inventory-forecasting-dataset"
    )
)
caminho_csv = path / "retail_store_inventory_cleaned.csv"
df = pd.read_csv(caminho_csv)

# 2. Conectar ao SQLite
conn = sqlite3.connect("supply_chain.db")
df.to_sql("tb_inventory", conn, if_exists="replace", index=False)

# 3. Criando VIEW 1: Resumo Executivo por Produto
query_create_vw_produto = """
CREATE VIEW IF NOT EXISTS vw_kpi_produto AS
SELECT 
    "Product ID" AS product_id,
    "Category" AS category,
    SUM("Units Sold") AS total_units_sold,
    ROUND(SUM("Revenue"), 2) AS total_revenue,
    ROUND(AVG("Days of Inventory"), 2) AS avg_days_inventory,
    SUM(CASE WHEN "Stock Status" = 'Crítico (Risco Ruptura)' THEN 1 ELSE 0 END) AS dias_criticos,
    ROUND(
        (SUM(CASE WHEN "Stock Status" = 'Crítico (Risco Ruptura)' THEN 1.0 ELSE 0.0 END) / COUNT(*)) * 100, 
        2
    ) AS pct_dias_criticos
FROM tb_inventory
GROUP BY "Product ID", "Category";
"""

# 4. Criando VIEW 2: Resumo Executivo por Loja
query_create_vw_loja = """
CREATE VIEW IF NOT EXISTS vw_kpi_loja AS
SELECT 
    "Store ID" AS store_id,
    "Region" AS region,
    SUM("Units Sold") AS total_units_sold,
    ROUND(SUM("Revenue"), 2) AS total_revenue,
    ROUND(AVG("Days of Inventory"), 2) AS avg_days_inventory,
    ROUND(
        (SUM(CASE WHEN "Stock Status" = 'Crítico (Risco Ruptura)' THEN 1.0 ELSE 0.0 END) / COUNT(*)) * 100, 
        2
    ) AS pct_dias_criticos
FROM tb_inventory
GROUP BY "Store ID", "Region";
"""

# Executar a criação das views
cursor = conn.cursor()
cursor.execute("DROP VIEW IF EXISTS vw_kpi_produto;")
cursor.execute("DROP VIEW IF EXISTS vw_kpi_loja;")
cursor.execute(query_create_vw_produto)
cursor.execute(query_create_vw_loja)
conn.commit()

print("--- VIEWS SQL CRIADAS COM SUCESSO! ---")

# 5. TESTE DE LEITURA DAS VIEWS
print("\n--- TESTE DE LEITURA DA VIEW: vw_kpi_loja ---")
df_loja_vw = pd.read_sql_query("SELECT * FROM vw_kpi_loja ORDER BY total_revenue DESC LIMIT 5;", conn)
df_loja_vw["total_revenue"] = df_loja_vw["total_revenue"].apply(lambda x: f"${x:,.2f}")
print(df_loja_vw.to_string(index=False))

# Fechar conexão
conn.close()