from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'API Flask funcionando'

@app.route('/actualizar', methods=['POST'])
def actualizar():
    data = request.json
    nombre = data.get('nombre')
    edad = data.get('edad')

    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME')
    )

    cursor = conn.cursor()
    cursor.execute("REPLACE INTO personas (nombre, edad) VALUES (%s, %s)", (nombre, edad))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'status': 'ok'})
