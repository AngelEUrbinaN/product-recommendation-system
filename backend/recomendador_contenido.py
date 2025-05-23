#	Recomendador basado en contenido (TF-IDF + precio + rating)

from sklearn.metrics.pairwise import cosine_similarity
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from math import pi
import os
from joblib import load

productos = None
sim_total = None

def inicializar_modelo():
    global productos, tfidf_matrix, sim_total

    ruta_productos = "C:\\Users\\aurbi\\Github\\Minería\\modelos\\modelo_productos.pkl"
    ruta_tfidf = "C:\\Users\\aurbi\\Github\\Minería\\modelos\\modelo_tfidf.pkl"
    ruta_sim_total = "C:\\Users\\aurbi\\Github\\Minería\\modelos\\modelo_sim_total.pkl"

    if os.path.exists(ruta_productos) and os.path.exists(ruta_tfidf) and os.path.exists(ruta_sim_total):
        productos = load(ruta_productos)
        tfidf_matrix = load(ruta_tfidf)
        sim_total = load(ruta_sim_total)
        print("Modelo cargado desde archivo.")
    else:
        print("No se encontraron los archivos del modelo.")
        print("   Ejecuta 'guardar_modelo_contenido.py' para generarlos.")
        productos = None
        tfidf_matrix = None
        sim_total = None

def recomendar_por_contenido(product_id, top_n=8, verbose=True):
    global productos, sim_total

    if productos is None or sim_total is None:
        inicializar_modelo()

    if product_id not in productos['id'].values:
        print(f"Producto con ID {product_id} no encontrado.")
        return []

    idx = productos[productos['id'] == product_id].index[0]
    scores = list(enumerate(sim_total[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    indices = [i[0] for i in scores[1:top_n + 1]]
    recomendados = productos.iloc[indices]

    if verbose:
        base = productos.iloc[idx]
        print(f"\n Recomendaciones por contenido para producto ID {product_id}: {base['name']}")
        print(f"Categoría: {base['category']} | Subcategoría: {base['sub_category']}")
        print(f"Precio: ${base['price']:.2f} | Rating: {base['rating']:.1f}\n")

        for i in indices:
            recomendado = productos.iloc[i]
            sim_tfidf = cosine_similarity(tfidf_matrix[idx], tfidf_matrix[i]).flatten()[0] if 'texto' in productos.columns else 0.0

            precio_dif = abs(base['price'] - recomendado['price']) / max(productos['price'].max(), 1)
            rating_dif = abs(base['rating'] - recomendado['rating']) / 5.0
            sim_total_score = sim_total[idx][i]

            print(f"- {recomendado['name']} (ID: {recomendado['id']})")
            print(f"  Subcategoría: {recomendado['sub_category']}")
            print(f"  Similitud TF-IDF: {sim_tfidf:.3f}")
            print(f"  Diferencia normalizada de precio: {precio_dif:.3f}")
            print(f"  Diferencia normalizada de rating: {rating_dif:.3f}")
            print(f"  Similitud total combinada: {sim_total_score:.3f}\n")

    generar_graficas_contenido(base, recomendados, tfidf_matrix, sim_total, idx, recomendados.index.tolist())

    return recomendados[['id', 'name', 'category', 'sub_category',
                         'price', 'rating', 'num_ratings', 'image']].to_dict(orient='records')

def generar_graficas_contenido(producto_base, recomendados, tfidf_matrix, sim_total, idx, indices):
    nombres = recomendados['name'].tolist()
    tfidf_scores = []
    precio_difs = []
    rating_difs = []
    sim_totales = []

    for i in indices:
        recomendado = recomendados.loc[i]
        sim_tfidf = cosine_similarity(tfidf_matrix[idx], tfidf_matrix[i]).flatten()[0]
        precio_dif = abs(producto_base['price'] - recomendado['price']) / max(recomendados['price'].max(), 1)
        rating_dif = abs(producto_base['rating'] - recomendado['rating']) / 5.0
        sim_total_score = sim_total[idx][i]

        tfidf_scores.append(sim_tfidf)
        precio_difs.append(precio_dif)
        rating_difs.append(rating_dif)
        sim_totales.append(sim_total_score)

    nombres_cortos = [n[:18] + "..." if len(n) > 21 else n for n in nombres]

    fig, ax = plt.subplots(figsize=(10, 6))
    bar1 = [0.6 * s for s in tfidf_scores]
    bar2 = [0.2 * (1 - p) for p in precio_difs]
    bar3 = [0.2 * (1 - r) for r in rating_difs]
    x = np.arange(len(nombres))

    ax.barh(x, bar1, label='TF-IDF (60%)', color='cornflowerblue')
    ax.barh(x, bar2, left=bar1, label='Precio (20%)', color='lightgreen')
    ax.barh(x, bar3, left=np.add(bar1, bar2), label='Rating (20%)', color='orange')

    ax.set_yticks(x)
    ax.set_yticklabels(nombres_cortos)
    ax.invert_yaxis()
    ax.set_xlabel('Puntaje total')
    ax.set_title(f'Score detallado - Producto base: {producto_base["name"][:40]}...')
    ax.legend()
    plt.tight_layout()

    os.makedirs("C:\\Users\\aurbi\\Github\\Minería\\graficas", exist_ok=True)
    plt.savefig(f"C:\\Users\\aurbi\\Github\\Minería\\graficas\\barras_product_{producto_base['id']}.png")
    plt.close()

    labels = ['TF-IDF', '1-Precio', '1-Rating', 'Total']
    num_vars = len(labels)
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    for i in range(len(nombres)):
        values = [tfidf_scores[i], 1 - precio_difs[i], 1 - rating_difs[i], sim_totales[i]]
        values += values[:1]
        ax.plot(angles, values, label=nombres_cortos[i])
        ax.fill(angles, values, alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title("Radar de recomendaciones")
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.05))
    plt.tight_layout()
    plt.savefig(f"C:\\Users\\aurbi\\Github\\Minería\\graficas\\radar_product_{producto_base['id']}.png")
    plt.close()
