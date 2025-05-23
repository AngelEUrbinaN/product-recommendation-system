# Función para obtener información completa de productos por ID

import mysql.connector

def obtener_detalles_productos(product_ids):
    """Devuelve una lista de diccionarios con información extendida de productos."""
    if not product_ids:
        return []

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='tienda_online'
    )
    cursor = conn.cursor(dictionary=True)
    formato = ",".join(["%s"] * len(product_ids))
    query = f"SELECT * FROM products WHERE id IN ({formato})"
    cursor.execute(query, tuple(product_ids))
    resultados = cursor.fetchall()
    conn.close()
    return resultados
