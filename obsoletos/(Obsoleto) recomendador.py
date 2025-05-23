# Código antiguo; en desuso

import pandas as pd
import mysql.connector
from sklearn.metrics.pairwise import cosine_similarity

def obtener_matriz():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='tienda_online'
    )
    purchases = pd.read_sql("SELECT user_id, product_id FROM purchases", conn)
    conn.close()
    matrix = purchases.assign(purchased=1).pivot_table(index='user_id', columns='product_id', values='purchased', fill_value=0)
    return matrix

def calcular_similitud(matrix):
    sim = cosine_similarity(matrix.T)
    return pd.DataFrame(sim, index=matrix.columns, columns=matrix.columns)

def recomendar_productos(user_id, top_n=5):
    matrix = obtener_matriz()
    if user_id not in matrix.index:
        return []

    sim_df = calcular_similitud(matrix)
    user_vector = matrix.loc[user_id]
    comprados = user_vector[user_vector > 0].index.tolist()

    scores = pd.Series(dtype=float)
    for p in comprados:
        similares = sim_df[p]
        scores = scores.add(similares, fill_value=0)

    scores = scores.drop(comprados, errors='ignore')
    return scores.sort_values(ascending=False).head(top_n).index.tolist()
