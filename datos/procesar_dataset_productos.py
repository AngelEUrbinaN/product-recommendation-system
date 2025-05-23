import os
import pandas as pd

CARPETA_CSV = "C:\\Users\\aurbi\\Downloads\\archive"

COLUMNAS_VALIDAS = [
    "name", "main_category", "sub_category", "image", "link",
    "ratings", "no_of_ratings", "discount_price", "actual_price"
]

MAX_TOTAL = 5000

def limpiar_precio(valor):
    try:
        return float(str(valor).replace(",", "").replace("₹", "").replace(" ", "").strip())
    except:
        return None

productos_validos_por_archivo = []
archivos = [f for f in os.listdir(CARPETA_CSV) if f.endswith(".csv")]
print(f"Archivos detectados: {len(archivos)}")

for archivo in archivos:
    ruta = os.path.join(CARPETA_CSV, archivo)
    try:
        df = pd.read_csv(ruta)
        if df.empty:
            continue
        df = df[[c for c in COLUMNAS_VALIDAS if c in df.columns]]
        df["discount_price"] = df["discount_price"].apply(limpiar_precio)
        df["actual_price"] = df["actual_price"].apply(limpiar_precio)
        df["ratings"] = pd.to_numeric(df["ratings"], errors='coerce')
        df["no_of_ratings"] = pd.to_numeric(df["no_of_ratings"].astype(str).str.replace(",", ""), errors='coerce')
        df = df.dropna(subset=["name", "main_category", "discount_price"])
        if not df.empty:
            productos_validos_por_archivo.append((archivo, df, len(df)))
            print(f"{archivo} → {len(df)} productos válidos")
    except Exception as e:
        print(f"❌ {archivo}: {e}")
        continue

total_disponible = sum(n for _, _, n in productos_validos_por_archivo)
print(f"\n Total de productos disponibles: {total_disponible}")

df_final = pd.DataFrame()
for archivo, df, cantidad in productos_validos_por_archivo:
    proporcion = cantidad / total_disponible
    cantidad_a_tomar = max(1, int(proporcion * MAX_TOTAL))
    df_final = pd.concat([df_final, df.sample(n=cantidad_a_tomar)], ignore_index=True)
    print(f"Seleccionando {cantidad_a_tomar} productos de {archivo}")

if len(df_final) > MAX_TOTAL:
    df_final = df_final.sample(n=MAX_TOTAL).reset_index(drop=True)
else:
    df_final = df_final.reset_index(drop=True)
    print(f"Solo se encontraron {len(df_final)} productos. El archivo final tendrá menos de {MAX_TOTAL}.")
ruta_salida = os.path.join("C:\\Users\\aurbi\\Downloads", "productos_limpios_balanceado.csv")
df_final.to_csv(ruta_salida, index=False)
print(f"\n Archivo generado: {ruta_salida}")
