from flask import Flask
from backend.album_api.api_blueprint import construct_album_api_blueprint
from backend.qr_code_api.qr_code_blueprint import construct_qr_code_api_blueprint


def create_app(album_handler, static_folder_name, camera_module, qr_code_handler, force_album_name=None):
    app = Flask(__name__, static_folder=static_folder_name)

    app.register_blueprint(construct_album_api_blueprint(
        album_handler,
        camera_module
    ), url_prefix="/albums")

    app.register_blueprint(construct_qr_code_api_blueprint(
        qr_code_handler
    ), url_prefix="/qr_codes")

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')  # Make sure subpaths are routed to react
    def index(path):
        return app.send_static_file('react/index.html')

    return app
