import pandas as pd
import os

# Cargar el archivo limpio
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXCEL_PATH = os.path.join(BASE_DIR, "data", "DATASET_LIMPIO_FINAL_5.xlsx")
GRAPHICS_PATH = os.path.join(BASE_DIR, "graficos")

# Leer el archivo
df = pd.read_excel(EXCEL_PATH)

# Solicitar el nombre del medicamento
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

# Verificar si se encontraron datos
if df_med.empty:
    print(f"no se encuentra datos para: {medicamento} {concentracion} {forma} {unidad}")
else:
    # Agrupar por fecha y sumar salidas por mes
    serie = df_med.groupby("Fecha")["Salidas - Cantidad"].sum()

    # Calcular estadísticas
    estadisticas = {
        "Media": round(serie.mean(), 2),
        "Mediana": round(serie.median(), 2),
        "Desviación estándar": round(serie.std(), 2),
        "Máximo": int(serie.max()),
        "Mínimo": int(serie.min()),
        "Total de salidas": int(serie.sum()),
        "Número de meses registrados": int(serie.count())
    }

    # Diccionario de descripciones
    descripciones = {
        "Media": "Promedio mensual de salidas del medicamento durante todo el período.",
        "Mediana": "Valor central que divide la serie mensual en dos mitades iguales.",
        "Desviación estándar": "Grado de dispersión de las salidas respecto a la media.",
        "Máximo": "Cantidad más alta de salidas mensuales registradas.",
        "Mínimo": "Cantidad más baja de salidas mensuales registradas.",
        "Total de salidas": "Suma total de todas las salidas registradas.",
        "Número de meses registrados": "Cantidad total de meses con datos disponibles."
    }

    # Mostrar tabla
    print(f"\nTabla de Medidas Estadísticas del {medicamento.title()} {concentracion} {forma} {unidad}\n")
    print(f"{'Indicador':<28}{'Valor':<15}{'Descripción'}")
    print("-" * 90)
    for indicador, valor in estadisticas.items():
        print(f"{indicador:<28}{valor:<15}{descripciones[indicador]}")
