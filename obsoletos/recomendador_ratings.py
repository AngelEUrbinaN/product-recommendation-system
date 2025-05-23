# Recomendador colaborativo basado en calificaciones

import pandas as pd
import mysql.connector
from sklearn.metrics.pairwise import cosine_similarity

def recomendar_por_ratings(user_id, top_n=5):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='tienda_online'
    )
    ratings = pd.read_sql("SELECT user_id, product_id, rating FROM ratings", conn)
    productos = pd.read_sql("SELECT id, name FROM products", conn)
    conn.close()

    matrix = ratings.pivot_table(index='user_id', columns='product_id', values='rating').fillna(0)

    if user_id not in matrix.index:
        print(f"Usuario {user_id} no tiene calificaciones.")
        return []

    user_similarity = cosine_similarity(matrix)
    sim_df = pd.DataFrame(user_similarity, index=matrix.index, columns=matrix.index)

    similares = sim_df[user_id].drop(user_id).sort_values(ascending=False)

    predicciones = pd.Series(dtype=float)

    for other_user, sim in similares.items():
        otros_ratings = matrix.loc[other_user]
        predicciones = predicciones.add(otros_ratings * sim, fill_value=0)

    if similares.sum() == 0:
        return []

    predicciones = predicciones / similares.sum()

    ya_calificados = matrix.loc[user_id][matrix.loc[user_id] > 0].index
    predicciones = predicciones.drop(ya_calificados, errors='ignore')

    mejores = predicciones.sort_values(ascending=False).head(top_n)
    productos_nombres = productos.set_index('id')['name']
    
    print(f"\n🎯 Recomendaciones por ratings para el usuario {user_id}:")
    for pid, score in mejores.items():
        print(f"- {productos_nombres.get(pid)} (predicción: {round(score, 2)})")

    from utils_productos import obtener_detalles_productos
    return obtener_detalles_productos(mejores.index.tolist())
