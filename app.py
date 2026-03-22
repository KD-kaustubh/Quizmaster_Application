from flask import Flask
from backend.models import db, bcrypt, User
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os
from sqlalchemy import inspect
from datetime import datetime
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse, quote_plus

# Declare app globally
app = Flask(__name__)

# Initialize rate limiter for brute force protection
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


def build_database_uri():
    """Build a SQLAlchemy-compatible PostgreSQL URL for local or hosted Postgres."""
    raw_db_uri = os.getenv('DATABASE_URL') or os.getenv('SQLALCHEMY_DATABASE_URI')
    if not raw_db_uri:
        # Fallback for local PostgreSQL development.
        pg_user = quote_plus(os.getenv('POSTGRES_USER', 'postgres'))
        pg_password = quote_plus(os.getenv('POSTGRES_PASSWORD', 'postgres'))
        pg_host = os.getenv('POSTGRES_HOST', 'localhost')
        pg_port = os.getenv('POSTGRES_PORT', '5432')
        pg_db = os.getenv('POSTGRES_DB', 'quizmaster')
        raw_db_uri = f'postgresql+psycopg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}'

    # Normalize legacy postgres:// URLs to SQLAlchemy-compatible form.
    if raw_db_uri.startswith('postgres://'):
        raw_db_uri = raw_db_uri.replace('postgres://', 'postgresql://', 1)

    # Use psycopg driver for PostgreSQL URLs unless a driver is already specified.
    if raw_db_uri.startswith('postgresql://') and '+' not in raw_db_uri.split('://', 1)[0]:
        raw_db_uri = raw_db_uri.replace('postgresql://', 'postgresql+psycopg://', 1)

    parsed = urlparse(raw_db_uri)
    if parsed.scheme.startswith('postgresql'):
        query_params = dict(parse_qsl(parsed.query, keep_blank_values=True))
        hostname = (parsed.hostname or '').lower()
        is_local_host = hostname in {'localhost', '127.0.0.1'}
        query_params.setdefault('sslmode', 'disable' if is_local_host else 'require')
        raw_db_uri = urlunparse(parsed._replace(query=urlencode(query_params)))

    return raw_db_uri


def setup_app():
    # Load environment variables from .env file
    load_dotenv()

    # Set the configuration for SQLAlchemy and secret key from environment variables
    db_uri = build_database_uri()

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your_default_secret_key_change_this')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Connection pool settings for Neon PostgreSQL stability
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,   # Test connection before using it (fixes SSL drop)
        'pool_recycle': 300,     # Recycle connections every 5 minutes
        'pool_size': 5,          # Max 5 persistent connections
        'max_overflow': 2,       # Allow 2 extra connections under load
    }

    # Security configurations
    flask_env = os.getenv('FLASK_ENV', 'development').lower()
    app.config['SESSION_COOKIE_SECURE'] = flask_env == 'production'  # HTTPS only in production
    app.config['SESSION_COOKIE_HTTPONLY'] = True   # Prevent JavaScript access
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour session timeout
    app.config['WTF_CSRF_TIME_LIMIT'] = None  # No time limit on CSRF tokens

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)

    # Ensure tables exist in environments without a pre-populated database
    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table('user'):
            db.create_all()
            print("Database tables created on startup.")

        # Seed default admin and student if no users exist
        if User.query.count() == 0:
            admin = User(
                username='admin@gmail.com',
                full_name='Admin User',
                qualification='Administrator',
                dob=datetime(2000, 1, 1).date(),
                role=0
            )
            admin.set_password('Admin123')

            student = User(
                username='student@gmail.com',
                full_name='Student User',
                qualification='B.Tech',
                dob=datetime(2002, 5, 15).date(),
                role=1
            )
            student.set_password('Student123')

            db.session.add(admin)
            db.session.add(student)
            db.session.commit()
            print("Seeded default admin and student users.")

        # Optional full demo seed for hosted environments like Render.
        auto_seed = os.getenv('AUTO_SEED_DEMO_DATA', 'false').lower() in {'1', 'true', 'yes'}
        if auto_seed:
            try:
                from seed_demo_data import seed_demo_data

                seed_demo_data()
                print("Auto demo data seeding completed.")
            except Exception as exc:
                db.session.rollback()
                print(f"Auto demo data seeding skipped due to error: {exc}")

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Direct access to other models
    app.app_context().push()

    # Enable debug mode only for local development.
    app.debug = flask_env == 'development' and os.getenv('FLASK_DEBUG', '0').lower() in {'1', 'true', 'yes'}
    print("Quiz Master app is started...")


# Calling setup function
setup_app()

# Import controllers (routes) after app setup to avoid circular imports
from backend.controllers import *

if __name__ == '__main__':
    # Run the application
    app.run(debug=app.debug)