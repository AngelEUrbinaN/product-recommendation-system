# Recomendador colaborativo mejorado con categoría + cantidad

from utils_productos import obtener_detalles_productos
import numpy as np
import matplotlib
matplotlib.use('Agg')


def recomendar_productos_mejorado(user_id, top_n=8, alpha=0.7, beta=0.3, verbose=True):
    import pandas as pd
    import mysql.connector
    from sklearn.metrics.pairwise import cosine_similarity

    # Conexión
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='tienda_online'
    )
    purchases = pd.read_sql("SELECT user_id, product_id, quantity FROM purchases", conn)
    products = pd.read_sql("SELECT id, name, category FROM products", conn)
    conn.close()

    # Matriz
    matrix = purchases.pivot_table(index='user_id', columns='product_id', values='quantity', fill_value=0)
    if user_id not in matrix.index:
        if verbose: print(f"Usuario {user_id} no tiene compras. Recomendando populares.")
        populares = products.copy()
        populares['score'] = purchases.groupby('product_id')['quantity'].sum()
        populares = populares.drop_duplicates('id').sort_values(by='score', ascending=False).head(top_n)
        return obtener_detalles_productos(populares['id'].tolist())


    # Similitud
    product_similarity = cosine_similarity(matrix.T)
    product_similarity_df = pd.DataFrame(product_similarity, index=matrix.columns, columns=matrix.columns)

    # Popularidad
    popularidad = purchases.groupby('product_id')['quantity'].sum()
    popularidad = popularidad / popularidad.max()

    # Categorías
    categorias = products.set_index('id')['category']
    nombres = products.set_index('id')['name']

    # Productos comprados
    user_vector = matrix.loc[user_id]
    comprados = user_vector[user_vector > 0].index.tolist()
    cat_usuario = categorias.loc[comprados].values
    cat_principal = pd.Series(cat_usuario).mode()[0]

    if verbose:
        print(f"\n Usuario {user_id}")
        print(f"Compró productos: {[nombres.get(pid) for pid in comprados]}")
        print(f"Categoría principal: {cat_principal}")

    # Scores por similitud
    scores = pd.Series(dtype=float)
    for pid in comprados:
        scores = scores.add(product_similarity_df[pid], fill_value=0)

    # Componente combinado
    scores = (scores * alpha) + (popularidad.reindex(scores.index).fillna(0) * beta)

    # Bonificación por categoría
    for pid in scores.index:
        if categorias.get(pid) == cat_principal:
            scores[pid] += 0.1

    scores = scores.drop(index=comprados, errors='ignore')

    resultados = scores.sort_values(ascending=False).head(top_n)

    if verbose:
        print("\n Puntajes de recomendación:")
        for pid, score in resultados.items():
            print(f"{nombres.get(pid)} - Score: {round(score, 3)}")

    if verbose:
        print(f"\n Puntajes de recomendación para el usuario {user_id}:\n")
        for pid, score in resultados.items():
            print(f"- {nombres.get(pid)} | Puntaje total: {round(score, 3)}")
            print(f"  Categoría: {categorias.get(pid)}")
            print(f"  Popularidad: {round(popularidad.get(pid, 0), 3)}")
            
            # Similitud promedio con productos del usuario
            similitudes = [product_similarity_df[pid][p] for p in comprados if pid in product_similarity_df.columns and p in product_similarity_df.columns]
            if similitudes:
                sim_prom = np.mean(similitudes)
                print(f"  Similitud promedio con compras previas: {sim_prom:.3f}")
            else:
                print("  Similitud promedio: N/A")

            # Coincidencia de categoría
            if categorias.get(pid) == cat_principal:
                print("  Coincide con la categoría principal del usuario")
            else:
                print("  No coincide con la categoría principal")

            # Usuarios que lo compraron
            if pid in matrix.columns:
                compraron = matrix[pid][matrix[pid] > 0].index.tolist()
                print(f"  Comprado por usuarios: {compraron}")
            print("")

    return obtener_detalles_productos(resultados.index.tolist())