"""
python app/app.py -> http://0.0.0.0:8080/

"""
from app.models.database import db, ma
from flask_session import Session
from flask_api import FlaskAPI, status
from flask_assets import Environment
from flask_cors import CORS
from flask import jsonify
import logging
import time
from routes.main_db import main_db_bp
from routes.secondary_db import secondary_db_bp


app = FlaskAPI(__name__)

app.logger.setLevel(logging.INFO)
CORS(app, resources=r'/api/*', supports_credentials=True)
app.config.from_object('config')
Environment(app)
db.init_app(app)
ma.init_app(app)
Session(app)

app.register_blueprint(main_db_bp)
app.register_blueprint(secondary_db_bp)


# Server status
@app.route("/")
def server_status():
    # Across config.py, app.py, ../setup.py
    return jsonify({'status': 'ONLINE', 'version': '0.1'}), status.HTTP_200_OK


# For timeout testing
@app.route("/timeout_test/<seconds>")
def timeout_test(seconds):
    time.sleep(int(seconds))
    return jsonify({'timeout_test': f'{seconds} seconds'}), status.HTTP_200_OK


# Error handling routes (Can't use blueprints)
@app.errorhandler(400)
def bad_request(_):
    return jsonify({'error': 'Bad request'}), status.HTTP_400_BAD_REQUEST


@app.errorhandler(404)
def not_found(_):
    return jsonify({'error': 'Not found'}), status.HTTP_404_NOT_FOUND


@app.errorhandler(405)
def not_allowed(_):
    return jsonify({'error': 'Method not allowed'}), status.HTTP_405_METHOD_NOT_ALLOWED


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8080)
