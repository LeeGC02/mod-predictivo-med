import pandas as pd
import os

# Cargar el archivo limpio
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXCEL_PATH = os.path.join(BASE_DIR, "data", "DATASET_LIMPIO_FINAL_5.xlsx")
# EXCEL_PATH = os.path.join(BASE_DIR, "resultados", "resultado_estacionariedad.xlsx")
GRAPHICS_PATH = os.path.join(BASE_DIR, "graficos")

# Leer el archivo
df = pd.read_excel(EXCEL_PATH)
df["Fecha"] = pd.to_datetime(df["Fecha"])   

# ===== MÉTRICAS =====
total_registros = len(df)
num_columnas = len(df.columns)
periodo_inicio = df["Fecha"].min().strftime("%B %Y")
periodo_fin = df["Fecha"].max().strftime("%B %Y")
meses_representados = df["Fecha"].nunique()

medicamentos_unicos = df["Medicamento e Insumo"].nunique()
formas_farmaceuticas = df["Forma Farmaceutica"].nunique()
concentraciones_diferentes = df["Concentración"].nunique()

# ===== RESULTADOS =====
print("===== Características del Dataset =====")
print(f"Cantidad total de registros: {total_registros:,}")
print(f"Número de columnas: {num_columnas}")
print(f"Periodo cubierto: Desde {periodo_inicio} hasta {periodo_fin}")
print(f"Cantidad de meses representados: {meses_representados} meses")
print()
print(f"Medicamentos únicos registrados: {medicamentos_unicos}")
print(f"Formas farmacéuticas distintas: {formas_farmaceuticas}")
print(f"Concentraciones diferentes: {concentraciones_diferentes}")
