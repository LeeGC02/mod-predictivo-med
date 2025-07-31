import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

# Cargar el archivo limpio
df = pd.read_excel("../data/DATASET_LIMPIO_FINAL_5.xlsx")

# Elegir el medicamento (puedes cambiar por input si quieres hacerlo interactivo)
medicamento = "paracetamol"

# Filtrar la serie
df_med = df[df["Medicamento e Insumo"].str.contains(medicamento, case=False, na=False)]

# Agrupar por fecha y sumar la demanda mensual
serie = df_med.groupby("Fecha")["Salidas - Cantidad"].sum().asfreq("MS")  # frecuencia mensual fija

# Realizar prueba ADF
adf_result = adfuller(serie.dropna())

# Mostrar resultados de la prueba ADF
print("\nResultado de la Prueba ADF (Dickey-Fuller):")
print(f"Estadístico ADF: {adf_result[0]:.4f}")
print(f"p-valor: {adf_result[1]:.4f}")
print(f"Número de rezagos usados: {adf_result[2]}")
print(f"Número de observaciones: {adf_result[3]}")
print("Valores críticos:")
for clave, valor in adf_result[4].items():
    print(f"  {clave}: {valor:.4f}")

# Transformar la serie (diferenciación)
serie_diferenciada = serie.diff().dropna()

# Graficar serie original y transformada
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
plt.title("Serie Diferenciada (Transformada)")
plt.xlabel("Fecha")
plt.ylabel("Diferencia de Salidas")
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()
