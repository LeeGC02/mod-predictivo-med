import pandas as pd
import matplotlib.pyplot as plt
import os
# cargar el archivo ya limpio
# df = pd.read_excel("../data/DATASET_LIMPIO_FINAL_5.xlsx")
# Obtener ruta absoluta a la raíz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ruta absoluta al archivo Excel
EXCEL_PATH = os.path.join(BASE_DIR, "data", "DATASET_LIMPIO_FINAL_5.xlsx")

# Ruta a la carpeta de gráficos
GRAPHICS_PATH = os.path.join(BASE_DIR, "graficos")

# Leer el archivo
df = pd.read_excel(EXCEL_PATH)

# pedir nombre del medicamento
medicamento = input("Medicamento: ").strip()
concentracion = input("Concentración (ej. 500): ").strip()
forma = input("Forma Farmaceutica (ej. mg, gr): ").strip()
unidad = input("Unidad de Medida (ej. compr, inyec): ").strip()

# elegir las demanda del medicamento 
# paracetamol_df = df[df["Medicamento e Insumo"].str.contains("paracetamol", case=False, na=False)]

# agrupar por fecha sumando las salidas mensuales
# serie_paracetamol =  paracetamol_df.groupby("Fecha")["Salidas - Cantidad"].sum()

filtro = (
    df["Medicamento e Insumo"].str.contains(medicamento, case=False, na=False) &
    df["Concentración"].astype(str).str.contains(concentracion, case=False, na=False) &
    df["Forma Farmaceutica"].str.contains(forma, case=False, na=False) &
    df["Unidad de Medida"].str.contains(unidad, case=False, na=False) 
)

# filtrar registros que contienen el nombre del medicamento
med_df = df[filtro]

# verificacion de registro del medicamento
if med_df.empty:
    print(f"no se encuentra datos para: {medicamento} {concentracion} {forma} {unidad}")
else:
    # agrupar por fecha y sumar las cantidades
    serie_medicamento = med_df.groupby("Fecha")["Salidas - Cantidad"].sum()

    # graficar
    plt.figure(figsize = (12,6))
    plt.plot(serie_medicamento.index, serie_medicamento.values, marker='o', color="#1f77b4")
    plt.title(f" Serie Temporal de la Demanda mensual del medicamento '{medicamento.title()} {concentracion} {forma} {unidad}' (Salidas por mes)")
    plt.xlabel("Fecha")
    plt.ylabel("Cantidad de Salidas")
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)

    # Crear nombre del archivo con el nombre del medicamento
    nombre_archivo = f"{medicamento.lower().replace(' ', '_')}_{concentracion}{unidad.lower()}_{forma.lower().replace(' ', '_')}_demanda_mensual.png"

    # Ruta completa para guardar en la carpeta "graficos"
    ruta_guardado = os.path.join(GRAPHICS_PATH, nombre_archivo)

    # Guardar el gráfico como imagen
    plt.savefig(ruta_guardado)
    print(f"✅ Gráfico guardado en: {ruta_guardado}")

    plt.show()