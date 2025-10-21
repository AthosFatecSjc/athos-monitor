from app.database import db
from app.models import Usuario, Produto

def seed_data():
    if Usuario.query.first() is not None:
        return
    users = [Usuario(nome="Ruth Mira"), Usuario(nome="João Silva"), Usuario(nome="Maria Costa")]
    prods = [
        Produto(nome="Notebook Dell", preco=4999.99),
        Produto(nome="Teclado Mecânico", preco=399.90),
        Produto(nome="Headset Gamer", preco=299.90)
    ]
    db.session.add_all(users + prods)
    db.session.commit()
