import os
from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

from config import Config
from database.db import Database
from models.user_model import User
from utils.helper import format_currency, format_date, str_id

def create_app():
    """Application Factory Function."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure upload directory exists
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(os.path.join(Config.UPLOAD_FOLDER, 'id_proofs'), exist_ok=True)
    os.makedirs(os.path.join(Config.UPLOAD_FOLDER, 'rooms'), exist_ok=True)
    os.makedirs(os.path.join(Config.UPLOAD_FOLDER, 'staff_photos'), exist_ok=True)

    # Initialize Extensions
    Bcrypt(app)
    CSRFProtect(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.find_by_id(user_id)

    # Initialize MongoDB Connection
    Database.init_db(app)

    # Register Jinja2 Template Filters and Context Processors
    app.jinja_env.filters['currency'] = format_currency
    app.jinja_env.filters['date'] = format_date
    app.jinja_env.globals['str'] = str

    # Register Blueprints
    from routes import (
        auth_bp, 
        dashboard_bp, 
        customer_bp, 
        room_bp, 
        booking_bp, 
        billing_bp, 
        staff_bp
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(billing_bp)
    app.register_blueprint(staff_bp)

    # Custom Error Handlers
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

    return app

app = create_app()

if __name__ == '__main__':
    print("[*] Starting Hotel Management System on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
