--> Sistema de Recomendación de Productos tipo Amazon <--
Este proyecto implementa un sistema de recomendación para una tienda en línea utilizando múltiples enfoques de minería de datos. Incluye una interfaz gráfica desarrollada con CustomTkinter y un backend con Flask que ofrece recomendaciones personalizadas basadas en usuarios, productos, ratings e imágenes.

--> Features <--
* Autenticación de usuario.
* Recomendaciones por:
    1. Filtrado colaborativo (similitud entre usuarios).
    2. Filtrado basado en contenido (similitud entre productos).
    3. Similitud visual (similitud en el análisis ed color en imágenes).
* Visualización de resultados mediante gráficas generadas por producto seleccionado.
* Sistema de historial de compras por usuario.
* Interfaz tipo aplicación móvil inspirada en el diseño de Amazon.

--> Instrucciones de ejecución <--
1. Clonar el respositorio: 
    https://github.com/AngelEUrbinaN/product-recommendation-system
2. Instalar las dependencias:
    pip install -r requirements.txt
3. Modificar todos los archivos que utilicen rutas locales para que coincidan con los directorios actuales.
4. Importar base de datos SQL recommendationSystem_DB.sql.
5. Iniciar el backend:
    python backend/app.py
6. Iniciar la interfaz gráfica:
    python frontend/amazon.py