import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import os

# Cargar el archivo limpio
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXCEL_PATH = os.path.join(BASE_DIR, "data", "DATASET_LIMPIO_FINAL_5.xlsx")
GRAPHICS_PATH = os.path.join(BASE_DIR, "graficos")

# Leer el archivo
df = pd.read_excel(EXCEL_PATH)

# Elegir el medicamento (puedes cambiar por input si quieres hacerlo interactivo)
medicamento = input("Medicamento: ").strip()
concentracion = input("Concentración (ej. 500): ").strip()
forma = input("Forma Farmaceutica (ej. mg, gr): ").strip()
unidad = input("Unidad de Medida (ej. compr, inyec): ").strip()

# Filtrar registros del medicamento
filtro = (
    df["Medicamento e Insumo"].str.contains(medicamento, case=False, na=False) &
    df["Concentración"].astype(str).str.contains(concentracion, case=False, na=False) &
    df["Forma Farmaceutica"].str.contains(forma, case=False, na=False) &
    df["Unidad de Medida"].str.contains(unidad, case=False, na=False) 
)
df_med = df[filtro]

# Agrupar por fecha y sumar la demanda mensual
serie = df_med.groupby("Fecha")["Salidas - Cantidad"].sum().asfreq("MS")  # frecuencia mensual fija

# Realizar prueba ADF
adf_result = adfuller(serie.dropna())


# Mostrar resultados ADF
print("\n📊 Resultado de la Prueba ADF (Dickey-Fuller):")
print(f"Estadístico ADF: {adf_result[0]:.4f}")
print(f"p-valor: {adf_result[1]:.4f}")
print(f"Número de rezagos usados: {adf_result[2]}")
print(f"Número de observaciones: {adf_result[3]}")
print("Valores críticos:")
for clave, valor in adf_result[4].items():
    print(f"  {clave}: {valor:.4f}")

# Determinar si es estacionaria
if adf_result[1] < 0.05:
    print("✅ La serie es **estacionaria** (p-valor < 0.05)")
    estacionariedad = "estacionaria"
else:
    print("❌ La serie **no es estacionaria** (p-valor >= 0.05)")
    estacionariedad = "no_estacionaria"

# Diferenciación
serie_diferenciada = serie.diff().dropna()

# Graficar
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(serie, marker='o')
plt.title("Serie Original")
plt.xlabel("Fecha")
plt.ylabel("Salidas Mensuales")
plt.xticks(rotation=45)
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(serie_diferenciada, color='green', marker='o')
plt.title("Serie Diferenciada")
plt.xlabel("Fecha")
plt.ylabel("Diferencia de Salidas")
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()

# Crear nombre del archivo
nombre_archivo = f"{medicamento.lower().replace(' ', '_')}_{concentracion}{forma.lower()}_{unidad.lower()}_{estacionariedad}.png"
ruta_guardado = os.path.join(GRAPHICS_PATH, nombre_archivo)

# Guardar la gráfica
plt.savefig(ruta_guardado)
print(f"\n📁 Gráfico guardado en: {ruta_guardado}")

plt.show()
