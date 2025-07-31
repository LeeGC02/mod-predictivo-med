import pandas as pd
import matplotlib.pyplot as plt

# cargar el archivo ya limpio
df = pd.read_excel("../data/DATASET_LIMPIO_FINAL_5.xlsx")

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
plt.show()