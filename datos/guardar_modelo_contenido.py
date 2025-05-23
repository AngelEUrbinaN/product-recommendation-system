import pandas as pd
import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin',
    database='tienda_online'
)
productos = pd.read_sql("""
    SELECT id, name, category, sub_category, price, rating, num_ratings, image
    FROM products
    WHERE name IS NOT NULL AND category IS NOT NULL
    AND sub_category IS NOT NULL AND price IS NOT NULL AND rating IS NOT NULL
""", conn)
conn.close()

productos['texto'] = productos['name'] + ' ' + productos['category'] + ' ' + productos['sub_category']

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(productos['texto'])
sim_texto = cosine_similarity(tfidf_matrix)

precios = (productos['price'] - productos['price'].min()) / (productos['price'].max() - productos['price'].min())
ratings = productos['rating'] / 5.0

sim_total = sim_texto.copy()
for i in range(len(productos)):
    for j in range(len(productos)):
        sim_total[i, j] = (
            0.6 * sim_texto[i, j] +
            0.2 * (1 - abs(precios[i] - precios[j])) +
            0.2 * (1 - abs(ratings[i] - ratings[j]))
        )

joblib.dump(productos, "C:\Users\aurbi\Github\Minería\modelos\modelo_productos.pkl")
joblib.dump(tfidf_matrix, "C:\Users\aurbi\Github\Minería\modelos\modelo_tfidf.pkl")
joblib.dump(sim_total, "C:\Users\aurbi\Github\Minería\modelos\modelo_sim_total.pkl")
print("✅ Archivos guardados exitosamente.")
