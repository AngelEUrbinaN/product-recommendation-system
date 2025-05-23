# Código para obtener gráficas (mapas de calor)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin',
    database='tienda_online'
)

purchases = pd.read_sql("SELECT user_id, product_id, quantity FROM purchases", conn)
products = pd.read_sql("SELECT * FROM products", conn)
conn.close()

matrix = purchases.pivot_table(index='user_id', columns='product_id', values='quantity', fill_value=0)

product_similarity = cosine_similarity(matrix.T)
sim_df = pd.DataFrame(product_similarity, index=matrix.columns, columns=matrix.columns)

plt.figure(figsize=(10, 8))
sns.heatmap(sim_df, cmap="coolwarm", xticklabels=False, yticklabels=False)
plt.title("Matriz de Similitud entre Productos")
plt.xlabel("Producto")
plt.ylabel("Producto")
plt.tight_layout()
plt.show()

recomendaciones = []
for user_id in matrix.index:
    user_vector = matrix.loc[user_id]
    comprados = user_vector[user_vector > 0].index.tolist()
    score = pd.Series(dtype=float)
    for pid in comprados:
        score = score.add(sim_df[pid], fill_value=0)
    score = score.drop(comprados, errors='ignore')
    top_recos = score.sort_values(ascending=False).head(5).index.tolist()
    recomendaciones.extend(top_recos)

conteo_recos = Counter(recomendaciones)
reco_df = pd.DataFrame.from_dict(conteo_recos, orient='index', columns=['Veces Recomendado']).sort_values(by='Veces Recomendado', ascending=False)
reco_df['Producto'] = reco_df.index.map(products.set_index('id')['name'])

plt.figure(figsize=(10, 5))
plt.barh(reco_df['Producto'].head(10), reco_df['Veces Recomendado'].head(10), color='skyblue')
plt.xlabel("Veces Recomendado")
plt.title("Top 10 Productos Más Recomendados")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

print("\n📋 Tabla de Productos Más Recomendados:")
print(reco_df.head(15))
