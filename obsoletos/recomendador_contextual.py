# Recomendador por producto actual (filtrado colaborativo por ítem)

import pandas as pd
import mysql.connector
from sklearn.metrics.pairwise import cosine_similarity

def recomendar_similares(product_id, top_n=5, bonus_categoria=0.1):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='tienda_online'
    )
    compras = pd.read_sql("SELECT user_id, product_id FROM purchases", conn)
    productos = pd.read_sql("SELECT id, name, category FROM products", conn)
    conn.close()

    matriz = compras.assign(comprado=1).pivot_table(index='product_id', columns='user_id', values='comprado', fill_value=0)

    if product_id not in matriz.index:
        print(f"Producto {product_id} no encontrado.")
        return []

    similitud = cosine_similarity(matriz)
    sim_df = pd.DataFrame(similitud, index=matriz.index, columns=matriz.index)

    categoria_actual = productos.set_index('id').loc[product_id, 'category']
    nombres = productos.set_index('id')['name']
    categorias = productos.set_index('id')['category']

    scores = sim_df.loc[product_id].copy()

    for pid in scores.index:
        if categorias.get(pid) == categoria_actual and pid != product_id:
            scores[pid] += bonus_categoria

    scores = scores.drop(index=product_id, errors='ignore')

    similares = scores.sort_values(ascending=False).head(top_n)
    print("\n📦 Recomendaciones similares a:", nombres.get(product_id))
    for pid, score in similares.items():
        print(f"- {nombres.get(pid)} | Score: {round(score, 3)}")

    from utils_productos import obtener_detalles_productos
    return obtener_detalles_productos(similares.index.tolist())