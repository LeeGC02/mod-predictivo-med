import pandas as pd
import os
from statsmodels.tsa.stattools import acf, pacf

# === RUTAS ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ESTACIONARIOS_PATH = os.path.join(BASE_DIR, "resultados", "resultado_estacionariedad.xlsx")
DATA_PATH = os.path.join(BASE_DIR, "data", "DATASET_LIMPIO_FINAL_5.xlsx")
RESULT_PATH = os.path.join(BASE_DIR, "resultados", "results_arima_parameters.xlsx")

# === CARGAR DATOS ===
df_estacionarios = pd.read_excel(ESTACIONARIOS_PATH, sheet_name="Estacionarios")
df = pd.read_excel(DATA_PATH)
df["Fecha"] = pd.to_datetime(df["Fecha"])

# === FUNCION PARA DETERMINAR p y q ===
def obtener_p_q(serie):
    pacf_vals = pacf(serie.dropna(), nlags=10)
    acf_vals = acf(serie.dropna(), nlags=10)
    p = next((i for i, val in enumerate(pacf_vals[1:], 1) if abs(val) < 0.2), 1)
    q = next((i for i, val in enumerate(acf_vals[1:], 1) if abs(val) < 0.2), 1)
    return p, q

# === PROCESAR CADA MEDICAMENTO ===
resultados = []

for _, row in df_estacionarios.iterrows():
    filtro = (
        (df["Medicamento e Insumo"] == row["Medicamento"]) &
        (df["Concentración"] == row["Concentración"]) &
        (df["Forma Farmaceutica"] == row["Forma Farmaceutica"]) &
        (df["Unidad de Medida"] == row["Unidad de Medida"]) 
    )

    df_med = df[filtro]
    serie = df_med.groupby("Fecha")["Salidas - Cantidad"].sum().asfreq("MS")

    if serie.dropna().shape[0] < 12:
        continue

    try:
        p, q = obtener_p_q(serie)
        resultados.append({
            "Medicamento": row["Medicamento"],
            "Concentración": row["Concentración"],
            "Forma Farmaceutica": row["Forma Farmaceutica"],
            "Unidad de Medida": row["Unidad de Medida"],
            "p": p,
            "d": 0,
            "q": q
        })
    except Exception as e:
        continue

# === GUARDAR RESULTADOS ===
df_resultados = pd.DataFrame(resultados)
df_resultados.to_excel(RESULT_PATH, index=False)
print(f"✅ Archivo guardado: {RESULT_PATH}")
