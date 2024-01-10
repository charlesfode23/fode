from flask import Flask, request, jsonify, render_template
from redis import Redis
app = Flask(__name__)
redis = Redis(host="redis", db=0, socket_timeout=5, charset="utf-8", decode_responses=True)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
       
        # Accéder au fichier téléversé
        uploaded_file = request.files['file']
        if uploaded_file:
            # Sauvegarder le fichier ou effectuer d'autres opérations nécessaires
            uploaded_file.save(f'uploads/{uploaded_file.filename}')

        redis.rpush('students', name)
        return jsonify({'name': name})

    if request.method == 'GET':
        students = redis.lrange('students', 0, -1)
        return render_template('index.html', students=students)
