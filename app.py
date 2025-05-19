from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'API Flask funcionando'

@app.route('/actualizar', methods=['POST'])
def actualizar():
    try:
        data = request.json
        print("✅ /actualizar fue llamado")
        print(f"Datos recibidos: {data}")

        nombre = data.get('nombre')
        edad = data.get('edad')

        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )
        print("Conexión a la base de datos exitosa")

        cursor = conn.cursor()
        cursor.execute("REPLACE INTO personas (nombre, edad) VALUES (%s, %s)", (nombre, edad))
        conn.commit()
        print(f"Datos insertados o actualizados: nombre={nombre}, edad={edad}")

        cursor.close()
        conn.close()
        print("Conexión a la base de datos cerrada correctamente")

        return jsonify({'status': 'ok'})

    except Exception as e:
        print(f"❌ Error en /actualizar: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
