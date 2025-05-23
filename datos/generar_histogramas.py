import mysql.connector
import requests
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
import json
from collections import defaultdict
from tqdm import tqdm

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin',
    database='tienda_online'
)
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT id, sub_category, image FROM products WHERE image IS NOT NULL")
productos = cursor.fetchall()
conn.close()

histogramas = defaultdict(dict)

def obtener_histograma(url):
    try:
        resp = requests.get(url, timeout=5)
        img = Image.open(BytesIO(resp.content)).convert('RGB')
        img_np = np.array(img.resize((100, 100)))
        hist = cv2.calcHist([img_np], [0, 1, 2], None, [8, 8, 8],
                            [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return hist.tolist()
    except Exception as e:
        print(f"Error con {url}: {e}")
        return None

for producto in tqdm(productos, desc="Procesando productos"):
    pid = producto["id"]
    subcat = producto["sub_category"]
    url = producto["image"]
    hist = obtener_histograma(url)
    if hist:
        histogramas[subcat][str(pid)] = hist

with open("C:\Users\aurbi\Github\Minería\datos\histogramas_por_subcategoria.json", "w") as f:
    json.dump(histogramas, f)

print("✅ Histogramas guardados en histogramas_por_subcategoria.json")
