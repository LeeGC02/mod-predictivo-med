import pandas as pd
import os
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# rutas por la estructura
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXCEL_PATH = os.path.join(BASE_DIR, "data", "DATASET_LIMPIO_FINAL_5.xlsx")

EXCEL_PARAMS = os.path.join(BASE_DIR, "resultados", "results_arima_model.xlsx")

# === INPUT DEL USUARIO ===
medicamento = input("Medicamento: ").strip().lower()
concentracion = input("Concentración: ").strip()
unidad = input("Unidad de medida: ").strip().lower()
forma = input("Forma farmacéutica: ").strip().lower()

# === CARGAR DATOS ===
df = pd.read_excel(EXCEL_PATH)
df_params = pd.read_excel(EXCEL_PARAMS)
df["Fecha"] = pd.to_datetime(df["Fecha"])


# === FILTRO PARÁMETROS ===
filtro_params = (
    (df_params["Medicamento"].str.lower() == medicamento) &
    (df_params["Concentración"].astype(str) == concentracion) &
    (df_params["Unidad de Medida"].str.lower() == unidad) &
    (df_params["Forma Farmaceutica"].str.lower() == forma)
)

if not filtro_params.any():
    print("❌ No se encontraron parámetros para el medicamento ingresado.")
else:
    param = df_params[filtro_params].iloc[0]

    # === FILTRAR DATOS ===
    filtro_data = (
        (df["Medicamento e Insumo"].str.lower() == param["Medicamento"].lower()) &
        (df["Concentración"].astype(str) == str(param["Concentración"])) &
        (df["Unidad de Medida"].str.lower() == param["Unidad de Medida"].lower()) &
        (df["Forma Farmaceutica"].str.lower() == param["Forma Farmaceutica"].lower())
    )
    df_med = df[filtro_data]
    serie = df_med.groupby("Fecha")["Salidas - Cantidad"].sum().asfreq("MS")

    if serie.dropna().shape[0] < 12:
        print("⚠️ No hay suficientes datos para entrenar el modelo.")
    else:
        # === DIVIDIR EN TRAIN Y TEST ===
        train_size = int(len(serie) * 0.8)
        train, test = serie.iloc[:train_size], serie.iloc[train_size:]

        # === ENTRENAR Y PREDECIR ===
        modelo = ARIMA(train, order=(param["p"], param["d"], param["q"]))
        modelo_fit = modelo.fit()
        pred = modelo_fit.predict(start=test.index[0], end=test.index[-1])

        # === GRAFICAR ===
        plt.figure(figsize=(10, 5))
        plt.plot(train, label="Entrenamiento")
        plt.plot(test, label="Valores reales", color="green")
        plt.plot(pred, label="Predicción", color="red")
        plt.title(f"Predicción vs Real: {param['Medicamento']} {param['Concentración']} {param['Unidad de Medida']} {param['Forma Farmaceutica']}")
        plt.xlabel("Fecha")
        plt.ylabel("Cantidad salida")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()