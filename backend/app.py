from flask import Flask
from album_api.api_blueprint import construct_album_api_blueprint


def create_app(album_handler, static_folder_name, camera_module):
    app = Flask(__name__, static_folder=static_folder_name)

    app.register_blueprint(construct_album_api_blueprint(
        album_handler,
        camera_module
    ), url_prefix='/albums')

    return app
