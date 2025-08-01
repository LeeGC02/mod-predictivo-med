import pandas as pd
import matplotlib.pyplot as plt
import os

# cargar el archivo ya limpio
#df = pd.read_excel("../data/DATASET_LIMPIO_FINAL_5.xlsx")
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXCEL_PATH = os.path.join(BASE_DIR, "data", "DATASET_LIMPIO_FINAL_5.xlsx")
GRAPHICS_PATH = os.path.join(BASE_DIR, "graficos")

# Leer el archivo
df = pd.read_excel(EXCEL_PATH)

# Agrupar la demanda total por mes sumando todas las salidas
serie_total = df.groupby("Fecha")["Salidas - Cantidad"].sum()

# Graficar la serie temporal de demanda total
plt.figure(figsize=(12, 6))
plt.plot(serie_total.index, serie_total.values, marker='o', color='#ffbb33')
plt.title("Serie Temporal de la Demanda Total de Medicamentos (2021–2024)")
plt.xlabel("Fecha")
plt.ylabel("Cantidad Total de Salidas")
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)

# Guardar la gráfica
ruta_guardado = os.path.join(GRAPHICS_PATH, "demanda_total_medicamentos.png")
plt.savefig(ruta_guardado)
print(f"✅ Gráfico guardado en: {ruta_guardado}")

plt.show()