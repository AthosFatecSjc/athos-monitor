from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def init_db():
    from app.models import Usuario, Produto
    db.create_all()
