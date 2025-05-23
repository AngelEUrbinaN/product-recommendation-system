import json
import numpy as np
import mysql.connector
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

HIST_FILE = "C:\\Users\\aurbi\\Github\\Minería\\datos\\histogramas_por_subcategoria.json"

with open(HIST_FILE, "r") as f:
    histogramas = json.load(f)

def recomendar_por_histograma(product_id, top_n=9):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='tienda_online'
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, name, image, sub_category FROM products WHERE id = %s", (product_id,))
    base = cursor.fetchone()

    if not base or not base.get("image") or not base.get("sub_category"):
        conn.close()
        return []

    subcat = base["sub_category"]
    hist_base = histogramas.get(subcat, {}).get(str(product_id))
    if not hist_base:
        conn.close()
        return []

    hist_base = np.array(hist_base, dtype=np.float32)

    distancias = []
    for pid_str, hist in histogramas.get(subcat, {}).items():
        if int(pid_str) == product_id:
            continue
        h = np.array(hist, dtype=np.float32)
        score = cv2.compareHist(hist_base, h, cv2.HISTCMP_CORREL)
        distancias.append((int(pid_str), score))

    similares = sorted(distancias, key=lambda x: -x[1])[:top_n]
    ids_similares = [sid for sid, _ in similares]

    if not ids_similares:
        conn.close()
        return []

    format_strings = ','.join(['%s'] * len(ids_similares))
    cursor.execute(f"""
        SELECT id, name, image, price, rating, num_ratings
        FROM products
        WHERE id IN ({format_strings})
    """, tuple(ids_similares))
    resultados = cursor.fetchall()
    conn.close()

    resultados_ordenados = sorted(resultados, key=lambda p: ids_similares.index(p['id']))
    similitudes_ordenadas = [score for _, score in similares]
    ruta = generar_grafica_histograma(base['id'], base['name'], resultados_ordenados, similitudes_ordenadas)
    print(f"Gráfica generada: {ruta}")

    return resultados_ordenados

def generar_grafica_histograma(base_id, base_name, resultados, similitudes):
    nombres = [r['name'][:25] + "..." if len(r['name']) > 28 else r['name'] for r in resultados]
    scores = similitudes

    plt.figure(figsize=(10, 6))
    bars = plt.barh(nombres, scores, color='slateblue')
    plt.xlabel("Similitud (Histograma de color)")
    plt.title(f"Similitud visual por histograma - Producto base ID {base_id}")
    plt.gca().invert_yaxis()
    plt.tight_layout()

    os.makedirs("C:\\Users\\aurbi\\Github\\Minería\\graficas", exist_ok=True)
    ruta = f"C:\\Users\\aurbi\\Github\\Minería\\graficas\\histograma_product_{base_id}.png"
    plt.savefig(ruta)
    plt.close()
    return ruta


