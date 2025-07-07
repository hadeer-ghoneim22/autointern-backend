import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# DON\'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.internships import internships_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), \'static\'))

# Load configuration from environment variables
app.config[\'SECRET_KEY\'] = os.getenv(\'SECRET_KEY\', \'asdf#FGSgvasgf$5$WGT\')
app.config[\'SUPABASE_URL\'] = os.getenv(\'SUPABASE_URL\')
app.config[\'SUPABASE_ANON_KEY\'] = os.getenv(\'SUPABASE_ANON_KEY\')
app.config[\'SUPABASE_SERVICE_ROLE_KEY\'] = os.getenv(\'SUPABASE_SERVICE_ROLE_KEY\')
app.config[\'GOOGLE_CLIENT_ID\'] = os.getenv(\'GOOGLE_CLIENT_ID\')
app.config[\'GOOGLE_CLIENT_SECRET\'] = os.getenv(\'GOOGLE_CLIENT_SECRET\')

# احصل على عنوان URL للواجهة الأمامية من متغيرات البيئة
FRONTEND_URL = os.getenv(\'FRONTEND_URL\', \'http://localhost:3000\' ) # استخدم localhost للتطوير

# قم بتكوين CORS للسماح بالطلبات من الواجهة الأمامية
CORS(app, resources={r\"/*\": {\"origins\": FRONTEND_URL}})

# Register blueprints
app.register_blueprint(user_bp, url_prefix=\'/api\')
app.register_blueprint(auth_bp, url_prefix=\'/api/auth\')
app.register_blueprint(internships_bp, url_prefix=\'/api\')

# Database configuration
app.config[\"SQLALCHEMY_DATABASE_URI\"] = os.getenv(\"DATABASE_URL\")
app.config[\'SQLALCHEMY_TRACK_MODIFICATIONS\'] = False
db.init_app(app)

# Create tables and add sample data
with app.app_context():
    db.create_all()
    
    # Add sample internships if none exist
    from src.models.user import Internship
    if Internship.query.count() == 0:
        sample_internships = [
            Internship(
                title=\"Software Engineering Intern\",
                                company=\"Google\",
