# Inserta productos desde CSV limpio en MySQL

import pandas as pd
import mysql.connector

archivo_csv = "C:\Users\aurbi\Github\Minería\datos\productos_imagenes_corregidas.csv"
df = pd.read_csv(archivo_csv)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="tienda_online"
)
cursor = conn.cursor()

insertados = 0

for _, row in df.iterrows():
    try:
        sql = """
            INSERT INTO products (
                name, category, sub_category, image, link,
                rating, num_ratings, price, actual_price
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            row.get("name"),
            row.get("main_category"),
            row.get("sub_category"),
            row.get("image"),
            row.get("link"),
            float(row["ratings"]) if pd.notnull(row.get("ratings")) else None,
            int(row["no_of_ratings"]) if pd.notnull(row.get("no_of_ratings")) else None,
            float(row["discount_price"]),
            float(row["actual_price"]) if pd.notnull(row.get("actual_price")) else None
        )
        cursor.execute(sql, values)
        insertados += 1
    except Exception as e:
        print(f"Error al insertar producto: {row.get('name')}\n{e}")

conn.commit()
cursor.close()
conn.close()

print(f"Inserción completada: {insertados} productos insertados correctamente.")
