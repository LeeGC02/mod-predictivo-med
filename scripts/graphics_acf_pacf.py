import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# === RUTAS ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "DATASET_LIMPIO_FINAL_5.xlsx")
GRAPHICS_PATH = os.path.join(BASE_DIR, "graficos")

# === CARGAR DATA ===
df = pd.read_excel(DATA_PATH)
df["Fecha"] = pd.to_datetime(df["Fecha"])

# === PEDIR DATOS ===
medicamento = input("Medicamento: ").strip()
concentracion = input("Concentración (ej. 500): ").strip()
forma = input("Forma Farmaceutica (ej. mg, gr): ").strip()
unidad = input("Unidad de Medida (ej. compr, inyec): ").strip()

# === FILTRAR ===
filtro = (
    df["Medicamento e Insumo"].str.contains(medicamento, case=False, na=False) &
    df["Concentración"].astype(str).str.contains(concentracion, case=False, na=False) &
    df["Unidad de Medida"].str.contains(unidad, case=False, na=False) &
    df["Forma Farmaceutica"].str.contains(forma, case=False, na=False)
)
df_med = df[filtro]

if df_med.empty:
    print("❌ No se encontró ningún medicamento con esos datos.")
    exit()

# === AGRUPAR POR MES ===
serie = df_med.groupby("Fecha")["Salidas - Cantidad"].sum().asfreq("MS")

# === GRAFICAR ACF y PACF ===
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plot_acf(serie.dropna(), lags=20, ax=plt.gca())
plt.title("ACF")

plt.subplot(1, 2, 2)
plot_pacf(serie.dropna(), lags=20, ax=plt.gca(), method='ywm')
plt.title("PACF")

plt.tight_layout()

# === GUARDAR GRAFICO ===
nombre_archivo = f"{medicamento.lower().replace(' ', '_')}_{concentracion}{forma.lower()}_{unidad.lower()}_acf_pacf.png"
ruta_grafico = os.path.join(GRAPHICS_PATH, nombre_archivo)
plt.savefig(ruta_grafico)

# === MOSTRAR Y CONFIRMAR ===
print(f"\n✅ Gráfico ACF y PACF guardado en: {ruta_grafico}")
plt.show()
