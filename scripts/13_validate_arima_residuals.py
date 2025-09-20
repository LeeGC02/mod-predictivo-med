import pandas as pd
import numpy as np
import os
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox

# rutas por la estructura
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "DATASET_LIMPIO_FINAL_5.xlsx")
PARAMS1_PATH = os.path.join(BASE_DIR, "resultados", "results_arima_parameters.xlsx")
PARAMS2_PATH = os.path.join(BASE_DIR, "resultados", "results_arima_nonstationary.xlsx")
RESULT_PATH = os.path.join(BASE_DIR, "resultados", "validation_arima_residuals.xlsx")

# cargar los datos
df = pd.read_excel(DATA_PATH)
df["Fecha"] = pd.to_datetime(df["Fecha"])

# unir parámetros de modelos
df_params1 = pd.read_excel(PARAMS1_PATH)
df_params2 = pd.read_excel(PARAMS2_PATH)
df_params = pd.concat([df_params1, df_params2], ignore_index=True)

# procesamiento de medicamentos
resultados = []

for _, row in df_params.iterrows():
    try:
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

        modelo = ARIMA(serie, order=(row["p"], row["d"], row["q"]))
        modelo_fit = modelo.fit()

        residuos = modelo_fit.resid.dropna()

        # prueba Ljung-Box
        ljung_result = acorr_ljungbox(residuos, lags=[10], return_df=True)
        p_valor = ljung_result['lb_pvalue'].values[0]
        pasa_prueba = p_valor > 0.05

        resultados.append({
            "Medicamento": row["Medicamento"],
            "Concentración": row["Concentración"],
            "Forma Farmaceutica": row["Forma Farmaceutica"],
            "Unidad de Medida": row["Unidad de Medida"],
            "p": row["p"],
            "d": row["d"],
            "q": row["q"],
            "AIC": modelo_fit.aic,
            "BIC": modelo_fit.bic,
            "p-valor Ljung-Box": round(p_valor, 4),
            "¿Residuos = Ruido Blanco?": "Sí" if pasa_prueba else "No"
        })

    except Exception as e:
        resultados.append({
            "Medicamento": row.get("Medicamento"),
            "Concentración": row.get("Concentración"),
            "Forma Farmaceutica": row.get("Forma Farmaceutica"),
            "Unidad de Medida": row.get("Unidad de Medida"),
            "p": row.get("p"),
            "d": row.get("d"),
            "q": row.get("q"),
            "AIC": None,
            "BIC": None,
            "p-valor Ljung-Box": None,
            "¿Residuos = Ruido Blanco?": "Error",
            "Error": str(e)
        })

# guardar resultados
df_resultados = pd.DataFrame(resultados)
df_resultados.to_excel(RESULT_PATH, index=False)
print(f"✅ Archivo guardado: {RESULT_PATH}")
