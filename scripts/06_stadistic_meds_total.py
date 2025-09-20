import pandas as pd
import os

# Cargar el archivo limpio
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXCEL_PATH = os.path.join(BASE_DIR, "data", "DATASET_LIMPIO_FINAL_5.xlsx")
GRAPHICS_PATH = os.path.join(BASE_DIR, "graficos")

# Leer el archivo
df = pd.read_excel(EXCEL_PATH)

# Agrupar todas las salidas mensuales de todos los medicamentos
serie_total = df.groupby("Fecha")["Salidas - Cantidad"].sum()

# Calcular estadísticas
estadisticas_total = {
    "Media": round(serie_total.mean(), 2),
    "Mediana": round(serie_total.median(), 2),
    "Desviación estándar": round(serie_total.std(), 2),
    "Máximo": int(serie_total.max()),
    "Mínimo": int(serie_total.min()),
    "Total de salidas": int(serie_total.sum()),
    "Total de registros (meses)": int(serie_total.count())
}

# Descripciones
descripciones_total = {
    "Media": "Promedio mensual de salidas considerando todos los medicamentos.",
    "Mediana": "Valor central de la suma mensual total de medicamentos.",
    "Desviación estándar": "Grado de variabilidad mensual de la demanda total.",
    "Máximo": "Mes con la mayor salida total registrada.",
    "Mínimo": "Mes con la menor salida total registrada.",
    "Total de salidas": "Suma total de todas las salidas mensuales agregadas.",
    "Total de registros (meses)": "Total de meses en los que se registraron datos agregados."
}

# Mostrar tabla
print("\nTABLA: Medidas Estadísticas Totales de Demanda de Medicamentos\n")
print(f"{'Indicador':<32}{'Valor':<20}{'Descripción'}")
print("-" * 100)
for indicador, valor in estadisticas_total.items():
    print(f"{indicador:<32}{str(valor):<20}{descripciones_total[indicador]}")
