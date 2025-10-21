from flask import Blueprint, jsonify, request
from app.database import db
from app.models import Usuario, Produto

bp = Blueprint("main", __name__)

@bp.route("/usuarios", methods=["POST"])
def criar_usuario():
    data = request.get_json()
    if not data or "nome" not in data:
        return jsonify({"error": "nome é requerido"}), 400
    user = Usuario(nome=data["nome"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "nome": user.nome}), 201

@bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    users = Usuario.query.all()
    return jsonify([{"id": u.id, "nome": u.nome} for u in users])

@bp.route("/produtos", methods=["POST"])
def criar_produto():
    data = request.get_json()
    if not data or "nome" not in data or "preco" not in data:
        return jsonify({"error": "nome e preco são requeridos"}), 400
    prod = Produto(nome=data["nome"], preco=data["preco"])
    db.session.add(prod)
    db.session.commit()
    return jsonify({"id": prod.id, "nome": prod.nome, "preco": prod.preco}), 201

@bp.route("/produtos", methods=["GET"])
def listar_produtos():
    prods = Produto.query.all()
    return jsonify([{"id": p.id, "nome": p.nome, "preco": p.preco} for p in prods])
