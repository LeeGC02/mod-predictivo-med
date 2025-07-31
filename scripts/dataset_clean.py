import pandas as pd

# Ruta del archivo Excel con las hojas por mes
file_path = "../data/INVENTARIO_SERIE_FINAL_2020_2024_DEFINITIVO.xlsx"

xls = pd.ExcelFile(file_path)
sheets = xls.sheet_names

# Lista para consolidar
df_consolidado = []

for sheet in sheets:
    df = xls.parse(sheet)

    # Saltar hojas vacías o sin columna "Código"
    if df.empty or 'Código' not in df.columns:
        continue

    # Convertir el nombre de la hoja a una fecha (ej: "2021-01")
    try:
        fecha = pd.to_datetime(sheet, format="%Y-%m")
        df["Fecha"] = fecha
    except:
        print(f"Error interpretando la hoja: {sheet}")
        continue

    # Eliminar filas con código vacío o código resumen tipo "99..."
    df = df[df["Código"].notna()]
    df = df[~df["Código"].astype(str).str.startswith("99")]

    # Reemplazos estándar para unidad de medida
    unidad_replace = {
        "g.": "gr",
        "g": "gr",
        "gr.": "gr",
        "gr": "gr",
        "ml.": "ml",
        "ml": "ml"
    }

    # Estandarizar textos en columnas clave
    for col in ["Medicamento e Insumo","Unidad de Medida", "Forma Farmaceutica", "Concentración"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.strip().str.replace(".", "", regex=False)

    # Reemplazo específico para Forma Farmaceutica
    if "Forma Farmaceutica" in df.columns:
        df["Forma Farmaceutica"] = df["Forma Farmaceutica"].replace(unidad_replace)


    # Agregar al total
    df_consolidado.append(df)

# Unir todas las hojas
df_final = pd.concat(df_consolidado, ignore_index=True)

# Exportar archivo limpio
df_final.to_excel("../data/DATASET_LIMPIO_FINAL_5.xlsx", index=False)

# Verificación rápida
print("Limpieza y consolidación completa.")
print("Número total de filas:", len(df_final))
print(df_final.head())
print(df_final["Concentración"].head(10))
