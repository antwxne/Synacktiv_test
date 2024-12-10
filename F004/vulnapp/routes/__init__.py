from .api import api
from .gallery import gallery
from .home import home
from .search import search
from .blog import blog
from .admin_panel import admin_panel


def init_routes(app):
    app.register_blueprint(api)
    app.register_blueprint(gallery)
    app.register_blueprint(home)
    app.register_blueprint(search)
    app.register_blueprint(blog)
    app.register_blueprint(admin_panel)
