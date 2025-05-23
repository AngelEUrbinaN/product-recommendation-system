import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin',
    database='tienda_online'
)

productos = pd.read_sql("""
    SELECT id, name, category, sub_category, price, rating
    FROM products
    WHERE name IS NOT NULL AND category IS NOT NULL AND sub_category IS NOT NULL
""", conn)

compras = pd.read_sql("""
    SELECT user_id, product_id
    FROM purchases
""", conn)


productos['texto'] = productos['name'] + ' ' + productos['category'] + ' ' + productos['sub_category']
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(productos['texto'])
sim_texto = cosine_similarity(tfidf_matrix)

plt.figure(figsize=(10, 8))
sns.heatmap(sim_texto[:20, :20], cmap='viridis', xticklabels=False, yticklabels=False)
plt.title("Matriz de similitud (TF-IDF) entre primeros 20 productos")
plt.tight_layout()
plt.savefig("C:\Users\aurbi\Github\Minería\graficas\graficas\matriz_similitud_tfidf.png")

compras = compras.merge(productos[['id', 'category']], left_on='product_id', right_on='id', how='left')
conteo_categorias = compras['category'].value_counts().head(10)

plt.figure(figsize=(10, 5))
conteo_categorias.plot(kind='bar', color='skyblue')
plt.title("Top 10 Categorías más Compradas")
plt.ylabel("Número de compras")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("C:\Users\aurbi\Github\Minería\graficas\graficas\matriz_similitud_tfidf.png")

compras_por_usuario = compras['user_id'].value_counts()

plt.figure(figsize=(10, 5))
sns.histplot(compras_por_usuario, bins=20, kde=True, color='orange')
plt.title("Distribución de compras por usuario")
plt.xlabel("Cantidad de compras")
plt.ylabel("Número de usuarios")
plt.tight_layout()
plt.savefig("C:\Users\aurbi\Github\Minería\graficas\graficas\distribucion_compras_usuario.png")

similares_por_producto = (sim_texto > 0.5).sum(axis=1)
cobertura = (similares_por_producto > 1).sum() / len(productos)

with open("C:\Users\aurbi\Github\Minería\graficas\graficas\metricas_recomendacion.txt", "w") as f:
    f.write("--Métricas de evaluación--\n")
    f.write(f"Total de productos: {len(productos)}\n")
    f.write(f"Total de usuarios: {compras['user_id'].nunique()}\n")
    f.write(f"Total de compras: {len(compras)}\n")
    f.write(f"Cobertura de recomendación por contenido (>0.5): {cobertura:.2%}\n")
    f.write(f"Promedio de compras por usuario: {compras_por_usuario.mean():.2f}\n")
    f.write(f"Desviación estándar de compras por usuario: {compras_por_usuario.std():.2f}\n")

conn.close()