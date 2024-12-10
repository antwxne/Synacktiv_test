from flask import Flask
from vulnapp.routes import init_routes
from vulnapp.database import db
from vulnapp.data.data import add_data
from vulnapp.core.config import SECRET_KEY


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    db.init_table()
    add_data()
    init_routes(app)
    return app


app = create_app()
