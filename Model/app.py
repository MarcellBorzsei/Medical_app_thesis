from flask import Flask
from Model.Controllers.auth_controller import auth_bp
from Model.Controllers.register_controller import register_bp
from Model.Controllers.upload_controller import upload_bp
from Model.Controllers.profile_controller import profile_bp
from Model.Controllers.convert_controller import convert_bp
from Model.Database.conn import initialize_database
import os
from Model.config import HOST_NUM, PORT_NUM

def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(register_bp, url_prefix='/register')
    app.register_blueprint(upload_bp, url_prefix='/upload')
    app.register_blueprint(profile_bp,  url_prefix='/profile')
    app.register_blueprint(convert_bp, url_prefix='/convert')

    return app

if __name__ == "__main__":
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    initialize_database("prod")
    app = create_app()
    app.run(debug=True, use_reloader=False, host=HOST_NUM, port=PORT_NUM)

