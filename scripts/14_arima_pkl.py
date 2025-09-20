import pandas as pd
import os
import joblib
from statsmodels.tsa.arima.model import ARIMA

# === RUTAS ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "DATASET_LIMPIO_FINAL_5.xlsx")
PARAMS_PATH = os.path.join(BASE_DIR, "resultados", "results_arima_model.xlsx")
MODELS_DIR = os.path.join(BASE_DIR, "modelos")

# === CARGAR DATOS ===
df = pd.read_excel(DATA_PATH)
df_params = pd.read_excel(PARAMS_PATH)
df["Fecha"] = pd.to_datetime(df["Fecha"])

# === PROCESAR CADA MODELO ===
for _, row in df_params.iterrows():
    filtro = (
        (df["Medicamento e Insumo"].str.lower() == row["Medicamento"].lower()) &
        (df["Concentración"].astype(str) == str(row["Concentración"])) &
        (df["Forma Farmaceutica"].str.lower() == row["Forma Farmaceutica"].lower()) &
        (df["Unidad de Medida"].str.lower() == row["Unidad de Medida"].lower())
    )

    df_med = df[filtro]
    serie = df_med.groupby("Fecha")["Salidas - Cantidad"].sum().asfreq("MS")

    if serie.dropna().shape[0] < 12:
        print(f"⚠️ No hay datos suficientes para: {row['Medicamento']}")
        continue

    try:
        modelo = ARIMA(serie, order=(row["p"], row["d"], row["q"]))
        modelo_entrenado = modelo.fit()

        nombre_modelo = f"{row['Medicamento'].lower().replace(' ', '_')}_{row['Concentración']}_{row['Forma Farmaceutica'].lower()}_{row['Unidad de Medida'].lower()}.pkl"
        ruta_modelo = os.path.join(MODELS_DIR, nombre_modelo)

        joblib.dump(modelo_entrenado, ruta_modelo)
        print(f"✅ Modelo guardado: {nombre_modelo}")

    except Exception as e:
        print(f"❌ Error entrenando {row['Medicamento']}: {e}")
        continue
