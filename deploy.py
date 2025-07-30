#!/usr/bin/env python3
"""
Deployment script for Food Wastage Prediction System
This script helps set up the application for production deployment
"""

import os
import sys
import subprocess
import secrets

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def create_env_file():
    """Create .env file with production settings"""
    print("🔧 Creating environment file...")
    
    secret_key = secrets.token_hex(32)
    env_content = f"""# Production Environment Variables
SECRET_KEY={secret_key}
FLASK_ENV=production
DATABASE_URL=sqlite:///food_wastage.db
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Environment file created successfully")
    print("⚠️  Remember to update DATABASE_URL for production database")

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask', 'flask-sqlalchemy', 'flask-login', 'flask-wtf',
        'scikit-learn', 'pandas', 'numpy', 'geopy', 'gunicorn'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def initialize_database():
    """Initialize the database"""
    print("🗄️  Initializing database...")
    
    try:
        from app import app, db, initialize_database
        with app.app_context():
            db.create_all()
            initialize_database()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def test_application():
    """Test if the application runs correctly"""
    print("🧪 Testing application...")
    
    try:
        from app import app
        print("✅ Application imports successfully")
        return True
    except Exception as e:
        print(f"❌ Application test failed: {e}")
        return False

def create_deployment_files():
    """Create deployment-specific files"""
    print("📁 Creating deployment files...")
    
    # Create Procfile if it doesn't exist
    if not os.path.exists('Procfile'):
        with open('Procfile', 'w') as f:
            f.write('web: gunicorn app:app')
        print("✅ Procfile created")
    
    # Create runtime.txt if it doesn't exist
    if not os.path.exists('runtime.txt'):
        with open('runtime.txt', 'w') as f:
            f.write('python-3.9.18')
        print("✅ runtime.txt created")
    
    # Create wsgi.py if it doesn't exist
    if not os.path.exists('wsgi.py'):
        with open('wsgi.py', 'w') as f:
            f.write('from app import app\n\nif __name__ == "__main__":\n    app.run()')
        print("✅ wsgi.py created")

def main():
    """Main deployment function"""
    print("🚀 Food Wastage Prediction System - Deployment Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create deployment files
    create_deployment_files()
    
    # Create environment file
    create_env_file()
    
    # Test application
    if not test_application():
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        sys.exit(1)
    
    print("\n🎉 Deployment setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update .env file with your production settings")
    print("2. Set up your production database")
    print("3. Configure your web server (Nginx, Apache)")
    print("4. Set up SSL certificate")
    print("5. Deploy to your chosen platform")
    print("\n🚀 To run locally: python app.py")
    print("🌐 To run with gunicorn: gunicorn app:app")

if __name__ == "__main__":
    main() 