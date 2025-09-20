import pandas as pd
import os
import re
from unidecode import unidecode

# --- Rutas base ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXCEL_PATH = os.path.join(BASE_DIR, "data", "INVENTARIO_2021_2024.xlsx")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "DATASET_LIMPIO_FINAL_7.xlsx")
GRAPHICS_PATH = os.path.join(BASE_DIR, "graficos")

# Asegurar que las carpetas existen
os.makedirs(os.path.dirname(EXCEL_PATH), exist_ok=True)
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
os.makedirs(GRAPHICS_PATH, exist_ok=True)

# --- Carga de hojas ---
xls = pd.ExcelFile(EXCEL_PATH)
sheets = xls.sheet_names
df_consolidado = []

for sheet in sheets:
    df = xls.parse(sheet)

    # 🔥 eliminar columnas vacías "Unnamed"
    df = df.loc[:, ~df.columns.str.contains(r"^Unnamed", na=False)]

    # Saltar hojas vacías o sin columna "Código"
    if df.empty or "Código" not in df.columns:
        continue

    # Convertir el nombre de la hoja a fecha (e.g., "2021-01")
    try:
        fecha = pd.to_datetime(sheet, format="%Y-%m")
        df["Fecha"] = fecha
    except Exception:
        print(f"[WARN] No se pudo interpretar la hoja como fecha: {sheet}")
        continue

    # Filtrar códigos vacíos y códigos de resumen tipo "99..."
    df = df[df["Código"].notna()]
    df = df[~df["Código"].astype(str).str.startswith("99")]

    # Estandarizar textos (manteniendo tu lógica original)
    for col in ["Medicamento e Insumo", "Unidad de Medida", "Forma Farmaceutica", "Concentración"]:
        if col in df.columns and df[col].dtype == object:
            df[col] = (
                df[col]
                .astype(str)
                .str.lower()
                .str.strip()
                .str.replace(".", "", regex=False)
            )

    # --- Normalización estándar de unidades ---
    unidad_replace = {
        "g.": "gr",
        "g": "gr",
        "gr.": "gr",
        "gr": "gr",
        "ml.": "ml",
        "ml": "ml"
    }

    if "Forma Farmaceutica" in df.columns:
        df["Forma Farmaceutica"] = df["Forma Farmaceutica"].replace(unidad_replace)

        # Quitar espacios dentro de la cadena (ej. "mg + 100" -> "mg+100")
        df["Forma Farmaceutica"] = df["Forma Farmaceutica"].str.replace(" ", "", regex=False)

        # Corregir expresiones tipo "mg/ml(2)" -> "mg/2ml"
        df["Forma Farmaceutica"] = df["Forma Farmaceutica"].apply(
            lambda x: re.sub(r"(\w+)/(\w+)\(?(\d+)\)?", r"\1/\3\2", x)
        )

        # Reemplazar "g" por "gr" dentro de cadenas completas
        df["Forma Farmaceutica"] = df["Forma Farmaceutica"].apply(
            lambda x: re.sub(r"\bg\b", "gr", x)
        )

    if "Unidad de Medida" in df.columns:
        df["Unidad de Medida"] = df["Unidad de Medida"].replace(unidad_replace)
        # Quitar tildes
        df["Unidad de Medida"] = df["Unidad de Medida"].apply(lambda x: unidecode(x))
        # Cambiar g por gr en cadenas
        df["Unidad de Medida"] = df["Unidad de Medida"].apply(lambda x: re.sub(r"\bg\b", "gr", x))

    # Eliminar filas sin info en Concentración, Forma Farmaceutica y Unidad de Medida
    if all(col in df.columns for col in ["Concentración", "Forma Farmaceutica", "Unidad de Medida"]):
        df = df.dropna(subset=["Concentración", "Forma Farmaceutica", "Unidad de Medida"])
        df = df[(df["Concentración"] != "") & (df["Forma Farmaceutica"] != "") & (df["Unidad de Medida"] != "")]

    df_consolidado.append(df)

# Unir todas las hojas
if not df_consolidado:
    raise RuntimeError("No se consolidó ninguna hoja. Revisa nombres de hojas y columnas.")

df_final = pd.concat(df_consolidado, ignore_index=True)

# Exportar limpio (sin columnas unnamed)
df_final.to_excel(OUTPUT_PATH, index=False, engine="openpyxl")

print("Limpieza y consolidación completa ✅")
print("Archivo guardado en:", OUTPUT_PATH)
print("Número total de filas:", len(df_final))
print(df_final.head())
