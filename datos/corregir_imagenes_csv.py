# Corregir URLs de imágenes en el archivo CSV

import pandas as pd
import re
import os

archivo = "C:\\Users\\aurbi\\Github\\Minería\\backend\\productos_limpios_balanceado.csv"

print(f"📁 Carpeta actual: {os.getcwd()}")

if not os.path.exists(archivo):
    print(f"❌ Archivo no encontrado: {archivo}")
    exit()

df = pd.read_csv(archivo)
print(f"📄 Productos cargados: {len(df)}")

correcciones = 0
def limpiar_url_imagen(url):
    global correcciones
    if isinstance(url, str):
        if re.search(r'W/IMAGERENDERING_[^/]+/images/', url):
            correcciones += 1
            return re.sub(r'W/IMAGERENDERING_[^/]+/images/', '', url)
    return url

df['image'] = df['image'].apply(limpiar_url_imagen)

print(f"🛠️ Imágenes corregidas: {correcciones}")

salida = "productos_imagenes_corregidas.csv"
df.to_csv(salida, index=False)

print(f"✅ Archivo generado: {os.path.abspath(salida)}")
