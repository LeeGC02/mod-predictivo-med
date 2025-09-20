import pandas as pd
import numpy as np
import os
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error

# === RUTAS ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "DATASET_LIMPIO_FINAL_5.xlsx")
PARAMS_PATH = os.path.join(BASE_DIR, "resultados", "results_arima_model.xlsx")
RESULT_PATH = os.path.join(BASE_DIR, "resultados", "test_mae_rmse.xlsx")

# === CARGAR DATOS ===
df = pd.read_excel(DATA_PATH)
df_params = pd.read_excel(PARAMS_PATH)
df["Fecha"] = pd.to_datetime(df["Fecha"])

# === INICIALIZAR RESULTADOS ===
resultados = []

# === PROCESAR CADA MODELO ===
for _, row in df_params.iterrows():
    try:
        filtro = (
            (df["Medicamento e Insumo"].str.lower() == str(row["Medicamento"]).lower()) &
            (df["Concentración"].astype(str) == str(row["Concentración"])) &
            (df["Unidad de Medida"].str.lower() == str(row["Unidad de Medida"]).lower()) &
            (df["Forma Farmaceutica"].str.lower() == str(row["Forma Farmaceutica"]).lower())
        )

        df_med = df[filtro]
        serie = df_med.groupby("Fecha")["Salidas - Cantidad"].sum().asfreq("MS").fillna(0)

        if len(serie.dropna()) < 12:
            resultados.append({
                "Medicamento": row["Medicamento"],
                "Concentración": row["Concentración"],
                "Forma Farmaceutica": row["Forma Farmaceutica"],
                "Unidad de Medida": row["Unidad de Medida"],
                "RMSE": None,
                "MAE": None,
                "¿Predicción válida?": "No (pocos datos)"
            })
            continue

        train_size = int(len(serie) * 0.8)
        train, test = serie.iloc[:train_size], serie.iloc[train_size:]

        if len(test.dropna()) == 0:
            resultados.append({
                "Medicamento": row["Medicamento"],
                "Concentración": row["Concentración"],
                "Forma Farmaceutica": row["Forma Farmaceutica"],
                "Unidad de Medida": row["Unidad de Medida"],
                "RMSE": None,
                "MAE": None,
                "¿Predicción válida?": "No (test vacío)"
            })
            continue

        modelo = ARIMA(train, order=(int(row["p"]), int(row["d"]), int(row["q"])))
        modelo_fit = modelo.fit()
        pred = modelo_fit.predict(start=test.index[0], end=test.index[-1])

        rmse = np.sqrt(mean_squared_error(test, pred))
        mae = mean_absolute_error(test, pred)

        resultados.append({
            "Medicamento": row["Medicamento"],
            "Concentración": row["Concentración"],
            "Forma Farmaceutica": row["Forma Farmaceutica"],
            "Unidad de Medida": row["Unidad de Medida"],
            "RMSE": round(rmse, 2),
            "MAE": round(mae, 2),
            "¿Predicción válida?": "Sí"
        })

    except Exception as e:
        resultados.append({
            "Medicamento": row["Medicamento"],
            "Concentración": row["Concentración"],
            "Forma Farmaceutica": row["Forma Farmaceutica"],
            "Unidad de Medida": row["Unidad de Medida"],
            "RMSE": None,
            "MAE": None,
            "¿Predicción válida?": f"No (Error: {str(e)[:40]})"
        })

# === GUARDAR RESULTADOS ===
df_resultados = pd.DataFrame(resultados)
df_resultados.to_excel(RESULT_PATH, index=False)
print("✅ Evaluación completada. Archivo guardado en:", RESULT_PATH)
