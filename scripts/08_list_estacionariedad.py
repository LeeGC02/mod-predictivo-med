import os
import pandas as pd
from statsmodels.tsa.stattools import adfuller

# Rutas
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXCEL_PATH = os.path.join(BASE_DIR, "data", "DATASET_LIMPIO_FINAL_5.xlsx")
RESULTADOS_PATH = os.path.join(BASE_DIR, "resultados", "resultado_estacionariedad.xlsx")

# Leer archivo
df = pd.read_excel(EXCEL_PATH)

# Limpiar fechas y columnas necesarias
df["Fecha"] = pd.to_datetime(df["Fecha"])

# Agrupar combinaciones únicas de medicamento
columnas_clave = ["Medicamento e Insumo", "Concentración", "Unidad de Medida", "Forma Farmaceutica"]
combinaciones = df[columnas_clave].drop_duplicates()

# Listas para almacenar resultados
resultados_estacionarios = []
resultados_no_estacionarios = []

# Evaluar cada combinación
for _, row in combinaciones.iterrows():
    med, conc, unidad, forma = row

    # Filtrar registros del medicamento específico
    filtro = (
        (df["Medicamento e Insumo"] == med) &
        (df["Concentración"] == conc) &
        (df["Unidad de Medida"] == unidad) &
        (df["Forma Farmaceutica"] == forma)
    )

    df_filtrado = df[filtro]

    # Agrupar por fecha
    serie = df_filtrado.groupby("Fecha")["Salidas - Cantidad"].sum().asfreq("MS")

    # Saltar si hay muy pocos datos
    if serie.dropna().shape[0] < 12:
        continue

    # Prueba ADF
    try:
        adf_result = adfuller(serie.dropna())
        adf_stat = adf_result[0]
        p_value = adf_result[1]

        resultado = {
            "Medicamento": med,
            "Concentración": conc,
            "Unidad de Medida": unidad,
            "Forma Farmaceutica": forma,
            "ADF Statistic": round(adf_stat, 4),
            "p-valor": round(p_value, 4)
        }

        if p_value < 0.05:
            resultados_estacionarios.append(resultado)
        else:
            resultados_no_estacionarios.append(resultado)

    except Exception as e:
        print(f"⚠️ Error con {med} {conc} {unidad} {forma}: {e}")
        continue

# Convertir a DataFrame
df_estacionarios = pd.DataFrame(resultados_estacionarios)
df_no_estacionarios = pd.DataFrame(resultados_no_estacionarios)

# Guardar en un mismo archivo Excel
with pd.ExcelWriter(RESULTADOS_PATH) as writer:
    df_estacionarios.to_excel(writer, sheet_name="Estacionarios", index=False)
    df_no_estacionarios.to_excel(writer, sheet_name="No_Estacionarios", index=False)

print(f"\n✅ Análisis finalizado. Archivo guardado en: {RESULTADOS_PATH}")
