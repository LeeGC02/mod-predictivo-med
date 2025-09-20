import pandas as pd
import os
from statsmodels.tsa.arima.model import ARIMA

# rutas por la estructura
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXCEL_PATH = os.path.join(BASE_DIR, "data", "DATASET_LIMPIO_FINAL_5.xlsx")

PARAMS_0_PATH = os.path.join(BASE_DIR, "resultados", "results_arima_parameters.xlsx")
PARAMS_1_PATH = os.path.join(BASE_DIR, "resultados", "results_arima_nonstationary.xlsx")

RESULT_PATH = os.path.join(BASE_DIR, "resultados", "results_arima_model.xlsx")

# cargar datos
df_0 = pd.read_excel(PARAMS_0_PATH)
df_1 = pd.read_excel(PARAMS_1_PATH)
df_params = pd.concat([df_0, df_1], ignore_index=True)
df = pd.read_excel(EXCEL_PATH)
df["Fecha"] = pd.to_datetime(df["Fecha"])

# entrenamiento de modelos ARIMA
resultados = []

for _, row in df_params.iterrows():
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
        modelo = ARIMA(serie, order=(row["p"], row["d"], row["q"]))
        modelo_entrenado = modelo.fit()

        resultados.append({
            "Medicamento": row["Medicamento"],
            "Concentración": row["Concentración"],
            "Unidad de Medida": row["Unidad de Medida"],
            "Forma Farmaceutica": row["Forma Farmaceutica"],
            "p": row["p"],
            "d": row["d"],
            "q": row["q"],
            "AIC": modelo_entrenado.aic,
            "BIC": modelo_entrenado.bic
        })

        print(f"✅ Entrenado: {row['Medicamento']}")

    except Exception as e:
        print(f"❌ Error al entrenar {row['Medicamento']}: {e}")
        continue

# guardar los resultados
df_resultados = pd.DataFrame(resultados)
df_resultados.to_excel(RESULT_PATH, index=False)
print(f"✅ Archivo guardado: {RESULT_PATH}")