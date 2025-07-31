import pandas as pd
import matplotlib.pyplot as plt

# cargar el archivo ya limpio
df = pd.read_excel("../data/DATASET_LIMPIO_FINAL_5.xlsx")

# pedir nombre del medicamento
medicamento = input("Medicamento: ").strip()

# elegir las demanda del medicamento 
# paracetamol_df = df[df["Medicamento e Insumo"].str.contains("paracetamol", case=False, na=False)]

# agrupar por fecha sumando las salidas mensuales
# serie_paracetamol =  paracetamol_df.groupby("Fecha")["Salidas - Cantidad"].sum()

# filtrar registros que contienen el nombre del medicamento
med_df = df[df["Medicamento e Insumo"].str.contains(medicamento, case=False, na=False)]

# verificacion de registro del medicamento
if med_df.empty:
    print(f"no se encuentra datos para: {med_df}")
else:
    # agrupar por fecha y sumar las cantidades
    serie_medicamento = med_df.groupby("Fecha")["Salidas - Cantidad"].sum()

    # graficar
    plt.figure(figsize = (12,6))
    plt.plot(serie_medicamento.index, serie_medicamento.values, marker='o', color="#1f77b4")
    plt.title(f" Serie Temporal de la Demanda mensual del medicamento '{medicamento.title()}' (Salidas por mes)")
    plt.xlabel("Fecha")
    plt.ylabel("Cantidad de Salidas")
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()