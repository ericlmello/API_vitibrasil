from flask import jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

# Usuários cadastrados (nome de usuário e senha hash)
users = {
    'user1': generate_password_hash('password1'),
    'user2': generate_password_hash('password2')
}

def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Nome de usuário e senha são obrigatórios"}), 400

    user_password_hash = users.get(username)
    if not user_password_hash or not check_password_hash(user_password_hash, password):
        return jsonify({"msg": "Credenciais inválidas"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
