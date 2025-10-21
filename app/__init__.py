from flask import Flask
from app.database import db, init_db
from app.routes import bp as main_routes
from app.seed import seed_data

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@db:5432/athos_db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(main_routes)

    with app.app_context():
        init_db()
        seed_data()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
