# Servidor Flask con endpoints para obtener recomendaciones

from flask import Flask, request, jsonify
import mysql.connector
from recomendador_mejorado import recomendar_productos_mejorado
from recomendador_contenido import recomendar_por_contenido, inicializar_modelo
from recomendador_histograma import recomendar_por_histograma
inicializar_modelo()

app = Flask(__name__)

# Endpoint para obtener recomendaciones basado en usuario
@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': 'Falta el parámetro user_id'}), 400

    productos = recomendar_productos_mejorado(user_id)  # productos ya enriquecidos
    return jsonify(productos)

# Endpoint para obtener recomendaciones basado en producto actual    
@app.route('/recommendations_content', methods=['GET'])
def get_recommendations_content():
    
    product_id = request.args.get('product_id', type=int)
    if not product_id:
        return jsonify({'error': 'Falta el parámetro product_id'}), 400

    recomendaciones = recomendar_por_contenido(product_id)
    return jsonify(recomendaciones)

# Endpoint para obtener recomendaciones basado en imagen del producto
@app.route('/recommendations_image', methods=['GET'])
def endpoint_recomendacion_imagen():
    product_id = request.args.get('product_id', type=int)
    if not product_id:
        return jsonify({'error': 'Falta product_id'}), 400

    try:
        recomendaciones = recomendar_por_histograma(product_id)
        return jsonify(recomendaciones)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para buscar productos
@app.route('/search', methods=['GET'])
def buscar_productos():
    query = request.args.get('query', default="", type=str)

    if not query:
        return jsonify({'error': 'Falta el parámetro query'}), 400

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin',
            database='tienda_online'
        )
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT * FROM products
            WHERE name LIKE %s OR sub_category LIKE %s OR category LIKE %s
            ORDER BY rating DESC, price ASC
            LIMIT 20
        """
        like_pattern = f"%{query}%"
        cursor.execute(sql, (like_pattern, like_pattern, like_pattern))
        productos = cursor.fetchall()

        conn.close()
        return jsonify(productos)

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Endpoint para obtener historial de compras
@app.route('/history', methods=['GET'])
def historial_usuario():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': 'Falta user_id'}), 400

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin',
            database='tienda_online'
        )
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT p.id, p.name, p.image, p.price, p.rating, p.num_ratings
            FROM purchases pu
            JOIN products p ON pu.product_id = p.id
            WHERE pu.user_id = %s
            GROUP BY p.id
            ORDER BY MAX(pu.timestamp) DESC
            LIMIT 50
        """, (user_id,))
        historial = cursor.fetchall()
        conn.close()

        return jsonify(historial)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para registrar compra
@app.route('/compra', methods=['POST'])
def registrar_compra():
    data = request.get_json()
    user_id = data.get("user_id")
    product_id = data.get("product_id")

    if not user_id or not product_id:
        return jsonify({"error": "Faltan parámetros"}), 400

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin',
            database='tienda_online'
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO purchases (user_id, product_id) VALUES (%s, %s)", (user_id, product_id))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Compra registrada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para registrar usuario
@app.route('/registro', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin',
            database='tienda_online'
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Usuario registrado"}), 200
    except mysql.connector.IntegrityError:
        return jsonify({"error": "El correo ya está registrado"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Endpoint para iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Faltan credenciales'}), 400

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin',
            database='tienda_online'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email FROM users WHERE email = %s AND password = %s", (email, password))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            return jsonify(usuario)
        else:
            return jsonify({'error': 'Credenciales inválidas'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)

''' FUNCIONES OBSOLETAS

# from recomendador_contextual import recomendar_similares
# from recomendador_ratings import recomendar_por_ratings

# Recomendaciones por ratings - Matriz usuarios vs productos basada en ratings. - Obsoleta por sufrir de cold start.
@app.route('/recommendations_ratings', methods=['GET'])
def get_recommendations_ratings():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': 'Falta el parámetro user_id'}), 400

    productos = recomendar_por_ratings(user_id)
    return jsonify(productos)

# Recomendaciones similares - Matriz productos vs productos. - El uso combinado de recomendador por usuario y recomendador por contenido es más efectivo.
@app.route('/similar-products', methods=['GET'])
def productos_similares():
    product_id = request.args.get('product_id', type=int)
    if not product_id:
        return jsonify({'error': 'Falta el parámetro product_id'}), 400

    productos = recomendar_similares(product_id)
    return jsonify(productos)
'''