from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from core.db_utils.database_init import db
from core.service.identity_service import identify_route
import os

# Initialize the Flask application
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

db.init_app(app)

# Register blueprint for identity_service.py
app.register_blueprint(identify_route)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
